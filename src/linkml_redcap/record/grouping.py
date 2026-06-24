"""Structural grouping between REDCap's flat and structured record shapes.

These helpers perform the *only* part of a flat <-> structured REDCap
transformation that ``linkml-map`` cannot express declaratively: the
record-level **grouping** (many flat rows -> one nested record) and the
repeat-instance **fan-in/out**. Everything else — renaming variables into
instrument blocks, casting types, mapping coded values onto enums — is
field-level and class-level work that belongs in a ``linkml-map``
``TransformationSpecification`` instead of hand-written Python.

The intended pipeline is therefore::

    flat REDCap export (list[dict])
        --> group_flat_records(...)        # this module (generic, project-agnostic)
        --> grouped records (list[dict])   # record_id + flat fields + per-instrument repeats
        --> linkml-map TransformationSpecification  # declarative, per project/rarelink
        --> typed structured records       # StructuredRecord (here) + project instrument classes

and the reverse for round-tripping back to a REDCap import file::

    typed structured records
        --> linkml-map (inverse spec)
        --> grouped records (list[dict])
        --> ungroup_records(...)           # this module
        --> flat REDCap import rows (list[dict])

The grouped intermediate is a plain, *untyped* ``dict`` shape that matches the
generic ``StructuredRecord`` / ``RepeatedElement`` envelope this package defines
(``record_id`` + ``repeated_elements``). The *typed instrument classes* that give
those fields meaning are the consuming project's, layered on top via
``linkml-map``. These helpers live here because the grouping depends on
REDCap-native structural fields alone and is identical for every project.
Neither function imports ``linkml-runtime``.
"""

from __future__ import annotations

import contextlib
from collections import defaultdict
from collections.abc import Iterable
from typing import Any

# Structural keys that REDCap adds to every flat row. They are handled
# explicitly by the grouping logic and never treated as instrument fields.
STRUCTURAL_KEYS = (
    "record_id",
    "redcap_event_name",
    "redcap_repeat_instrument",
    "redcap_repeat_instance",
    "redcap_data_access_group",
    "redcap_survey_identifier",
)

__all__ = [
    "STRUCTURAL_KEYS",
    "group_flat_records",
    "ungroup_records",
]


def _is_empty(value: Any) -> bool:
    return value is None or value == ""


def group_flat_records(
    rows: Iterable[dict[str, Any]],
    *,
    record_id_key: str = "record_id",
    event_aware: bool = False,
    drop_empty: bool = False,
    cast_instance: bool = True,
) -> list[dict[str, Any]]:
    """Group a flat REDCap export into per-record structured stubs.

    Each output record has the shape::

        {
          "record_id": "<id>",
          # ...non-repeating fields merged from the record's base row(s)...
          "repeated_elements": [
            {
              "redcap_repeat_instrument": "<form>",
              "redcap_repeat_instance": <int>,
              # ...the instrument's fields for that instance...
            },
            ...
          ],
        }

    This is deliberately *project-agnostic*: it does not know which field
    belongs to which instrument, and it does not bucket fields into named
    instrument blocks — that is the job of the downstream ``linkml-map``
    specification. It only separates non-repeating rows from repeating ones
    and preserves the (instrument, instance) identity of each repeat.

    Args:
        rows: The flat export — an iterable of row dicts (REDCap API/JSON/CSV).
        record_id_key: Name of the record-identifier column.
        event_aware: If True, longitudinal events are kept distinct by
            grouping on ``(record_id, redcap_event_name)`` and emitting one
            structured record per event (the event name is retained on the
            output). If False (default, classic projects), rows are grouped on
            ``record_id`` only.
        drop_empty: If True, empty-string / None field values are omitted from
            the output (useful to keep grouped JSON compact before mapping).
        cast_instance: If True, ``redcap_repeat_instance`` is coerced to ``int``
            (REDCap exports it as a string).

    Returns:
        A list of grouped record dicts, ordered by first appearance.
    """
    groups: dict[Any, list[dict[str, Any]]] = defaultdict(list)
    order: list[Any] = []
    for row in rows:
        record_id = row.get(record_id_key, "")
        key = (record_id, row.get("redcap_event_name", "")) if event_aware else record_id
        if key not in groups:
            order.append(key)
        groups[key].append(row)

    out: list[dict[str, Any]] = []
    for key in order:
        entries = groups[key]
        record_id = key[0] if event_aware else key
        record: dict[str, Any] = {record_id_key: record_id}
        if event_aware:
            record["redcap_event_name"] = key[1]

        repeated: list[dict[str, Any]] = []
        for entry in entries:
            instrument = entry.get("redcap_repeat_instrument", "")
            if _is_empty(instrument):
                # Non-repeating row: merge its (non-structural) fields onto the root.
                for field, value in entry.items():
                    if field in STRUCTURAL_KEYS or field == record_id_key:
                        continue
                    if drop_empty and _is_empty(value):
                        continue
                    record[field] = value
            else:
                instance = entry.get("redcap_repeat_instance", "")
                if cast_instance and not _is_empty(instance):
                    with contextlib.suppress(TypeError, ValueError):
                        instance = int(instance)
                element: dict[str, Any] = {
                    "redcap_repeat_instrument": instrument,
                    "redcap_repeat_instance": instance,
                }
                for field, value in entry.items():
                    if field in STRUCTURAL_KEYS or field == record_id_key:
                        continue
                    if drop_empty and _is_empty(value):
                        continue
                    element[field] = value
                repeated.append(element)

        record["repeated_elements"] = repeated
        out.append(record)
    return out


def ungroup_records(
    records: Iterable[dict[str, Any]],
    *,
    template: dict[str, Any] | None = None,
    record_id_key: str = "record_id",
    repeated_key: str = "repeated_elements",
) -> list[dict[str, Any]]:
    """Flatten grouped/structured records back into REDCap flat import rows.

    The inverse of :func:`group_flat_records`. Each non-repeating record yields
    one base row; each entry in ``repeated_elements`` yields one further row
    carrying its ``redcap_repeat_instrument`` / ``redcap_repeat_instance``.

    Args:
        records: Grouped records (record_id + flat fields + repeated_elements).
            Nested instrument blocks (one level of ``dict`` values) are flattened
            so this also accepts the structured output of a ``linkml-map`` run.
        template: Optional full-width row template (all variables -> "") so every
            emitted row carries the complete column set REDCap expects on import.
            When omitted, rows contain only the fields present in the input.
        record_id_key: Name of the record-identifier column.
        repeated_key: Name of the repeating-elements list slot.

    Returns:
        A flat list of row dicts suitable for serialising to a REDCap import.
    """

    def _flatten_block(target: dict[str, Any], block: Any) -> None:
        """Merge a field block (possibly nested one level) onto a row."""
        if not isinstance(block, dict):
            return
        for field, value in block.items():
            if isinstance(value, dict):
                _flatten_block(target, value)
            elif not isinstance(value, list):
                target[field] = value

    rows: list[dict[str, Any]] = []
    for record in records:
        base: dict[str, Any] = dict(template) if template else {}
        base[record_id_key] = record.get(record_id_key, "")
        base.setdefault("redcap_repeat_instrument", "")
        base.setdefault("redcap_repeat_instance", "")
        if "redcap_event_name" in record:
            base["redcap_event_name"] = record["redcap_event_name"]

        for key, value in record.items():
            if key in (record_id_key, repeated_key, "redcap_event_name"):
                continue
            if isinstance(value, dict):
                _flatten_block(base, value)
            elif not isinstance(value, list):
                base[key] = value
        rows.append(base)

        for element in record.get(repeated_key, []) or []:
            row: dict[str, Any] = dict(template) if template else {}
            row[record_id_key] = record.get(record_id_key, "")
            row["redcap_repeat_instrument"] = element.get("redcap_repeat_instrument", "")
            row["redcap_repeat_instance"] = element.get("redcap_repeat_instance", "")
            if "redcap_event_name" in record:
                row["redcap_event_name"] = record["redcap_event_name"]
            for key, value in element.items():
                if key in ("redcap_repeat_instrument", "redcap_repeat_instance"):
                    continue
                if isinstance(value, dict):
                    _flatten_block(row, value)
                elif not isinstance(value, list):
                    row[key] = value
            rows.append(row)
    return rows
