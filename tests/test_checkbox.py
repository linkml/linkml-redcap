"""Tests for linkml_redcap.record.checkbox — flat ⇄ multivalued checkbox shapes."""

from __future__ import annotations

import pytest

from linkml_redcap.record.checkbox import (
    checkbox_column,
    checkbox_map_from_data_dictionary,
    collapse_checkboxes,
    expand_checkboxes,
    infer_checkbox_map,
)
from linkml_redcap.record.grouping import group_flat_records, ungroup_records

CMAP = {"index_manifest": ["1", "2", "3", "10", "9"], "ab_wirkstoffe": ["1", "7"]}


def flat_row(**over):
    row = {
        "record_id": "4",
        "redcap_repeat_instrument": "",
        "redcap_repeat_instance": "",
        "zentrum": "Berlin",
        "index_manifest___1": "0",
        "index_manifest___2": "1",
        "index_manifest___3": "0",
        "index_manifest___10": "1",
        "index_manifest___9": "0",
        "ab_wirkstoffe___1": "1",
        "ab_wirkstoffe___7": "0",
    }
    row.update(over)
    return row


def test_checkbox_column_sanitises_like_redcap():
    assert checkbox_column("f", "1") == "f___1"
    assert checkbox_column("f", "-2") == "f____2"
    assert checkbox_column("f", "A+") == "f___a_"


def test_infer_checkbox_map_recovers_fields_and_signed_codes():
    m = infer_checkbox_map(flat_row().keys())
    assert m["index_manifest"] == ["1", "2", "3", "10", "9"]
    assert m["ab_wirkstoffe"] == ["1", "7"]
    assert infer_checkbox_map(["meds____2", "meds___1"]) == {"meds": ["_2", "1"]}


def test_collapse_flat_row_with_map():
    out = collapse_checkboxes(flat_row(), CMAP)
    assert out["index_manifest"] == ["2", "10"]
    assert out["ab_wirkstoffe"] == ["1"]
    assert "index_manifest___1" not in out
    assert out["zentrum"] == "Berlin"


def test_collapse_without_map_infers_per_record():
    out = collapse_checkboxes(flat_row())
    assert out["index_manifest"] == ["2", "10"]


def test_collapse_orders_by_map_declaration():
    row = flat_row(index_manifest___9="1", index_manifest___2="1")
    out = collapse_checkboxes(row, CMAP)
    assert out["index_manifest"] == ["2", "10", "9"]


def test_collapse_uniform_empty_list_and_padding():
    row = {k: ("" if "___" in k else v) for k, v in flat_row().items()}
    out = collapse_checkboxes(row, CMAP)
    assert out["index_manifest"] == []
    assert out["ab_wirkstoffe"] == []


def test_collapse_skips_absent_fields_with_explicit_map():
    out = collapse_checkboxes({"record_id": "1", "zentrum": "B"}, CMAP)
    assert "index_manifest" not in out


def test_collapse_strict_raises_on_junk():
    with pytest.raises(ValueError, match="index_manifest___2"):
        collapse_checkboxes(flat_row(index_manifest___2="yes"), CMAP, strict=True)
    # non-strict treats junk as unchecked
    out = collapse_checkboxes(flat_row(index_manifest___2="yes"), CMAP)
    assert out["index_manifest"] == ["10"]


def test_collapse_descends_into_repeated_elements():
    grouped = group_flat_records(
        [
            flat_row(),
            {
                "record_id": "4",
                "redcap_repeat_instrument": "chronologie_infektionen",
                "redcap_repeat_instance": "1",
                "inf_manifest___1": "1",
                "inf_manifest___2": "0",
            },
        ]
    )
    out = [collapse_checkboxes(r, {**CMAP, "inf_manifest": ["1", "2"]}) for r in grouped]
    el = out[0]["repeated_elements"][0]
    assert el["inf_manifest"] == ["1"]
    assert out[0]["index_manifest"] == ["2", "10"]
    # the explicit map must not inject inf_manifest onto the record root
    assert "inf_manifest" not in {k: v for k, v in out[0].items() if k != "repeated_elements"}


def test_expand_round_trip_full_width():
    collapsed = collapse_checkboxes(flat_row(), CMAP)
    expanded = expand_checkboxes(collapsed, CMAP)
    original = flat_row()
    for field, codes in CMAP.items():
        for code in codes:
            col = checkbox_column(field, code)
            assert expanded[col] == original[col]
    assert expanded["zentrum"] == "Berlin"


def test_expand_rejects_undeclared_code():
    with pytest.raises(ValueError, match="not declared"):
        expand_checkboxes({"index_manifest": ["2", "42"]}, CMAP)


def test_expand_then_ungroup_produces_importable_rows():
    grouped = group_flat_records([flat_row()])
    collapsed = [collapse_checkboxes(r, CMAP) for r in grouped]
    # ungroup_records rejects list values by design ...
    with pytest.raises(ValueError, match="checkbox"):
        ungroup_records(collapsed)
    # ... and accepts the expanded form
    rows = ungroup_records([expand_checkboxes(r, CMAP) for r in collapsed])
    assert rows[0]["index_manifest___2"] == "1"
    assert rows[0]["index_manifest___1"] == "0"


def test_map_from_data_dictionary_headers_and_snake_case():
    dd = [
        {
            "Variable / Field Name": "index_manifest",
            "Field Type": "checkbox",
            "Choices, Calculations, OR Slider Labels": "1, Meningitis | 2, Sepsis | 10, Andere | 9, Unbekannt",
        },
        {
            "Variable / Field Name": "zentrum",
            "Field Type": "text",
            "Choices, Calculations, OR Slider Labels": "",
        },
        {
            "variable_field_name": "familie_typ",
            "field_type": "checkbox",
            "choices_calculations_slider_labels": "1, Geschwister | -2, Sonder",
        },
    ]
    m = checkbox_map_from_data_dictionary(dd)
    assert m == {"index_manifest": ["1", "2", "10", "9"], "familie_typ": ["1", "-2"]}
    assert checkbox_column("familie_typ", "-2") == "familie_typ____2"
