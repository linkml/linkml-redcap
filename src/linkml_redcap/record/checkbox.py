"""Checkbox collapse/expand between REDCap's flat columns and multivalued slots.

REDCap has no native multi-select value: a ``checkbox`` field is exported as one
binary column **per option** (``<field>___<code>`` holding ``"1"``/``"0"``), so
the flat export of

    index_manifest = {Meningitis, Sepsis}   (options 1..10)

is ``index_manifest___1 = "1"``, ``index_manifest___2 = "1"``,
``index_manifest___3 = "0"``, ... — one column per option, all padded with
``"0"``/``""`` for the unchecked rest.

A LinkML project schema wants the *semantic* shape instead: **one multivalued
slot** whose range is the option enum (each permissible value ideally carrying a
``meaning:`` ontology binding), i.e. ``index_manifest: ["1", "2"]``. This module
is the lossless, vendor-neutral bridge between the two shapes — the checkbox
counterpart of :mod:`linkml_redcap.record.grouping`:

    flat export row(s)
        --> group_flat_records(...)                      # grouping (repeats)
        --> collapse_checkboxes(record, checkbox_map)    # THIS MODULE
        --> structured record with multivalued checkbox slots
        --> ... project mapping / rarelink ...
    and back:
        --> expand_checkboxes(record, checkbox_map)      # THIS MODULE
        --> ungroup_records(...)                         # flat import rows

Like the grouping helpers, everything here is *structural* and project-agnostic:
it depends only on REDCap's ``___`` export convention, never on what a field
means. It imports neither ``linkml-runtime`` nor anything project-specific.

Losslessness: the collapsed form keeps only the **checked** option codes.  Given
the field's full option-code list (the ``checkbox_map``), the unchecked columns
are reconstructable (absent = ``"0"``), so collapse→expand round-trips to the
full-width flat form. Without a map, :func:`infer_checkbox_map` recovers the
option lists from the columns present in the data — sufficient whenever the data
carries the full column set (REDCap exports always do).

Column-name caveat (handled): REDCap sanitises the option code when building the
export column name — the code is lower-cased and every character that is not
``[a-z0-9_]`` becomes ``_`` (e.g. option code ``-2`` → column ``field____2``,
i.e. FOUR underscores). :func:`checkbox_column` reproduces that, and both
directions use it, so signed/alphanumeric option codes survive the round-trip
as long as the sanitised forms do not collide (REDCap itself has the same
constraint).
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from typing import Any

#: Separator between a checkbox field name and the (sanitised) option code in
#: the flat export column name.
CHECKBOX_SEP = "___"

#: Export values a checkbox column may hold: checked, unchecked, or the empty
#: padding REDCap uses for rows outside the field's instrument.
CHECKED = "1"
UNCHECKED = "0"

__all__ = [
    "CHECKBOX_SEP",
    "CHECKED",
    "UNCHECKED",
    "checkbox_column",
    "infer_checkbox_map",
    "checkbox_map_from_data_dictionary",
    "collapse_checkboxes",
    "expand_checkboxes",
]

_SANITISE_RE = re.compile(r"[^a-z0-9_]")


def _sanitise_code(code: str) -> str:
    """Sanitise an option code the way REDCap does for export column names."""
    return _SANITISE_RE.sub("_", str(code).lower())


def checkbox_column(field: str, code: str, *, sep: str = CHECKBOX_SEP) -> str:
    """Return the flat export column name for one checkbox option.

    >>> checkbox_column("index_manifest", "1")
    'index_manifest___1'
    >>> checkbox_column("meds", "-2")     # negative codes: '-' becomes '_'
    'meds____2'
    """
    return f"{field}{sep}{_sanitise_code(code)}"


def infer_checkbox_map(columns: Iterable[str], *, sep: str = CHECKBOX_SEP) -> dict[str, list[str]]:
    """Infer ``{field: [option codes...]}`` from flat export column names.

    Codes come back in column order, in their **sanitised** form (the only form
    the flat file itself knows). When the original option codes matter (signed
    or mixed-case codes), pass an explicit map from the data dictionary via
    :func:`checkbox_map_from_data_dictionary` instead.
    """
    out: dict[str, list[str]] = {}
    for col in columns:
        if sep not in col:
            continue
        field, code = col.rsplit(sep, 1)
        # A signed code like -2 sanitises to _2 and rsplit() eats its leading
        # underscore into the separator; re-attach it to the code.
        while field.endswith("_"):
            field = field[:-1]
            code = "_" + code
        if not field or not code:
            continue
        out.setdefault(field, [])
        if code not in out[field]:
            out[field].append(code)
    return out


def checkbox_map_from_data_dictionary(
    rows: Iterable[Mapping[str, Any]],
) -> dict[str, list[str]]:
    """Build ``{field: [option codes...]}`` from REDCap data dictionary rows.

    Accepts rows as dicts keyed by the standard 18 data dictionary column
    headers (``csv.DictReader`` output of the DD export) or by their
    snake_case aliases as used in the ``redcap_data_dictionary`` schema
    (``field_type``, ``variable_field_name``,
    ``choices_calculations_slider_labels``). Only ``checkbox`` rows contribute.
    Codes are returned **unsanitised**, exactly as declared in the choices
    string ``"code1, Label 1 | code2, Label 2"``.
    """
    out: dict[str, list[str]] = {}
    for row in rows:
        ftype = row.get("Field Type") or row.get("field_type") or ""
        if str(ftype).strip() != "checkbox":
            continue
        name = row.get("Variable / Field Name") or row.get("variable_field_name") or ""
        choices = (
            row.get("Choices, Calculations, OR Slider Labels")
            or row.get("choices_calculations_slider_labels")
            or ""
        )
        codes = []
        for part in str(choices).split("|"):
            code = part.split(",", 1)[0].strip()
            if code:
                codes.append(code)
        if name and codes:
            out[str(name).strip()] = codes
    return out


def _is_repeat_list(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(v, dict) for v in value)


def collapse_checkboxes(
    record: Mapping[str, Any],
    checkbox_map: Mapping[str, Iterable[str]] | None = None,
    *,
    sep: str = CHECKBOX_SEP,
    strict: bool = False,
) -> dict[str, Any]:
    """Collapse ``field___code`` columns into multivalued ``field`` lists.

    Works on a flat export row, a grouped record from
    :func:`~linkml_redcap.record.grouping.group_flat_records` (the
    ``repeated_elements`` list is descended into), or any nested dict shape —
    the transformation is applied at every dict level.

    Args:
        record: The row / record to collapse. Not mutated.
        checkbox_map: ``{field: [option codes...]}``. When given, only these
            fields collapse and every field in the map collapses **even when
            all its columns are unchecked or absent** (yielding ``[]``), so the
            collapsed shape is uniform across records. When ``None``, checkbox
            columns are auto-detected per record via :func:`infer_checkbox_map`.
        sep: Column-name separator (default ``"___"``).
        strict: If True, raise :class:`ValueError` on a checkbox column whose
            value is not ``"1"``, ``"0"``, ``""``, ``0``, ``1`` or ``None``;
            otherwise such values are treated as unchecked.

    Returns:
        A new dict in which each checkbox field appears once, as the list of
        its **checked** option codes (declaration order of ``checkbox_map``,
        column order otherwise), and its ``field___code`` columns are removed.
    """

    def _collapse(node: Mapping[str, Any]) -> dict[str, Any]:
        cmap = (
            {f: list(codes) for f, codes in checkbox_map.items()}
            if checkbox_map is not None
            else infer_checkbox_map(node.keys(), sep=sep)
        )
        column_of = {
            field: {checkbox_column(field, c, sep=sep): c for c in codes}
            for field, codes in cmap.items()
        }
        checkbox_cols = {
            col: (f, code) for f, cols in column_of.items() for col, code in cols.items()
        }

        out: dict[str, Any] = {}
        checked: dict[str, list[str]] = {}
        seen_fields: set[str] = set()
        for key, value in node.items():
            if key in checkbox_cols:
                field, code = checkbox_cols[key]
                seen_fields.add(field)
                if value in (CHECKED, 1):
                    checked.setdefault(field, []).append(code)
                elif value in (UNCHECKED, "", 0, None):
                    checked.setdefault(field, [])
                elif strict:
                    raise ValueError(
                        f"Checkbox column {key!r} holds {value!r}; expected '1', '0' or ''."
                    )
                else:
                    checked.setdefault(field, [])
                continue
            if _is_repeat_list(value):
                out[key] = [_collapse(el) for el in value]
            elif isinstance(value, dict):
                out[key] = _collapse(value)
            else:
                out[key] = value

        for field, codes in cmap.items():
            if checkbox_map is not None and field not in seen_fields:
                # Explicit map, but none of this field's columns exist on this
                # node (e.g. a repeated element of another instrument): skip.
                continue
            ordered = (
                [c for c in codes if c in checked.get(field, [])]
                if checkbox_map is not None
                else checked.get(field, [])
            )
            out[field] = ordered
        return out

    return _collapse(record)


def expand_checkboxes(
    record: Mapping[str, Any],
    checkbox_map: Mapping[str, Iterable[str]],
    *,
    sep: str = CHECKBOX_SEP,
) -> dict[str, Any]:
    """Expand multivalued checkbox lists back into ``field___code`` columns.

    The inverse of :func:`collapse_checkboxes`. Requires an explicit
    ``checkbox_map`` — the full option-code list per field is what makes the
    expansion full-width (every option column emitted, ``"1"`` for checked,
    ``"0"`` otherwise), which is the shape a REDCap import expects and the
    shape :func:`~linkml_redcap.record.grouping.ungroup_records` can flatten
    (it rejects any remaining list value on purpose).

    Raises:
        ValueError: If a field's list contains a code not present in
            ``checkbox_map`` — dropping it silently would corrupt the import.
    """
    cmap = {f: list(codes) for f, codes in checkbox_map.items()}

    def _expand(node: Mapping[str, Any]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in node.items():
            if key in cmap and isinstance(value, list):
                codes = cmap[key]
                unknown = [c for c in value if c not in codes]
                if unknown:
                    raise ValueError(
                        f"Checkbox field {key!r} holds code(s) {unknown!r} not "
                        f"declared in checkbox_map {codes!r}."
                    )
                for code in codes:
                    out[checkbox_column(key, code, sep=sep)] = (
                        CHECKED if code in value else UNCHECKED
                    )
            elif _is_repeat_list(value):
                out[key] = [_expand(el) for el in value]
            elif isinstance(value, dict):
                out[key] = _expand(value)
            else:
                out[key] = value
        return out

    return _expand(record)
