"""Tests for the record submodule: loader API and structural grouping."""

from pathlib import Path

from linkml_redcap.record import (
    SCHEMA_FILENAME,
    group_flat_records,
    schema_path,
    schema_view,
    ungroup_records,
)


def test_schema_path_exists():
    p = schema_path()
    assert isinstance(p, Path)
    assert p.exists()
    assert p.name == SCHEMA_FILENAME


def test_schema_view_loads():
    sv = schema_view()
    assert "FlatRecord" in sv.all_classes()
    assert "StructuredRecord" in sv.all_classes()
    assert "RepeatedElement" in sv.all_classes()
    assert "FormCompleteStatus" in sv.all_enums()
    assert "redcap_date" in sv.all_types()
    assert "redcap_integer" in sv.all_types()


# --- grouping ---------------------------------------------------------------

FLAT = [
    # record 1: one non-repeating base row + two repeats of one instrument
    {
        "record_id": "1",
        "redcap_repeat_instrument": "",
        "redcap_repeat_instance": "",
        "snomedct_184099003": "2015-01-12",
        "loinc_76689_9": "snomedct_248153007",
        "disease_coding": "",
    },
    {
        "record_id": "1",
        "redcap_repeat_instrument": "rarelink_5_disease",
        "redcap_repeat_instance": "1",
        "snomedct_184099003": "",
        "loinc_76689_9": "",
        "disease_coding": "mondo",
    },
    {
        "record_id": "1",
        "redcap_repeat_instrument": "rarelink_5_disease",
        "redcap_repeat_instance": "2",
        "snomedct_184099003": "",
        "loinc_76689_9": "",
        "disease_coding": "ordo",
    },
]


def test_group_flat_records_basic():
    grouped = group_flat_records(FLAT)
    assert len(grouped) == 1
    rec = grouped[0]
    assert rec["record_id"] == "1"
    # non-repeating fields merged onto the root
    assert rec["snomedct_184099003"] == "2015-01-12"
    # two repeats captured, instance coerced to int
    assert len(rec["repeated_elements"]) == 2
    first = rec["repeated_elements"][0]
    assert first["redcap_repeat_instrument"] == "rarelink_5_disease"
    assert first["redcap_repeat_instance"] == 1
    assert first["disease_coding"] == "mondo"


def test_group_flat_records_drop_empty():
    grouped = group_flat_records(FLAT, drop_empty=True)
    rec = grouped[0]
    # empty strings removed from the merged root
    assert "disease_coding" not in rec
    # but present where populated in a repeat
    assert rec["repeated_elements"][0]["disease_coding"] == "mondo"


def test_round_trip_group_then_ungroup():
    grouped = group_flat_records(FLAT)
    rows = ungroup_records(grouped)
    # one base row + two repeat rows
    assert len(rows) == 3
    base = rows[0]
    assert base["redcap_repeat_instrument"] == ""
    assert base["snomedct_184099003"] == "2015-01-12"
    repeats = rows[1:]
    assert {r["redcap_repeat_instance"] for r in repeats} == {1, 2}
    assert all(r["redcap_repeat_instrument"] == "rarelink_5_disease" for r in repeats)


def test_event_aware_grouping():
    rows = [
        {
            "record_id": "1",
            "redcap_event_name": "baseline",
            "redcap_repeat_instrument": "",
            "redcap_repeat_instance": "",
            "x": "a",
        },
        {
            "record_id": "1",
            "redcap_event_name": "followup",
            "redcap_repeat_instrument": "",
            "redcap_repeat_instance": "",
            "x": "b",
        },
    ]
    grouped = group_flat_records(rows, event_aware=True)
    assert len(grouped) == 2
    assert {g["redcap_event_name"] for g in grouped} == {"baseline", "followup"}
