"""Round-trip and integrity tests for the flat <-> structured grouping.

The committed fixture is a small, synthetic, vendor-neutral REDCap flat export.
To additionally run the round-trip against a REAL export (e.g. the RareLink
evaluation cohort or a CIEINR export), point an env var at a flat JSON file --
the test is skipped when unset, so no registry data ever enters the repo or CI:

    LINKML_REDCAP_FLAT_FIXTURE=/abs/path/evaluation_cohort_redcap.json \
        poetry run pytest tests/test_grouping_roundtrip.py -k local -q
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from linkml_redcap.record import group_flat_records, ungroup_records

FIXTURE = Path(__file__).parent / "fixtures" / "redcap_flat_sample.json"
GROUPED_DROPEMPTY = Path(__file__).parent / "fixtures" / "redcap_grouped_dropempty_sample.json"


def _load(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def _columns(rows: list[dict]) -> list[str]:
    cols: dict[str, None] = {}
    for row in rows:
        for key in row:
            cols.setdefault(key, None)
    return list(cols)


def _normalize(rows: list[dict], columns: list[str]) -> list[dict]:
    """Full-width, all-string, order-independent view for comparison."""
    norm = [{c: str(row.get(c, "")) for c in columns} for row in rows]
    norm.sort(
        key=lambda r: (
            r.get("record_id", ""),
            r.get("redcap_repeat_instrument", ""),
            r.get("redcap_repeat_instance", ""),
        )
    )
    return norm


def _assert_lossless_roundtrip(rows: list[dict]) -> None:
    columns = _columns(rows)
    grouped = group_flat_records(rows)
    restored = ungroup_records(grouped, template=dict.fromkeys(columns, ""))
    assert _normalize(restored, columns) == _normalize(rows, columns)


def _assert_dropempty_roundtrip(rows: list[dict]) -> None:
    """drop_empty grouping is still lossless once re-padded via the template.

    This is the import path the plain round-trip does not cover: dropping empties
    discards which columns existed, so reconstruction relies on the full-width
    template. Verified here so the documented template contract has teeth.
    """
    columns = _columns(rows)
    grouped = group_flat_records(rows, drop_empty=True)
    restored = ungroup_records(grouped, template=dict.fromkeys(columns, ""))
    assert _normalize(restored, columns) == _normalize(rows, columns)


# --- committed synthetic fixture -------------------------------------------


def test_sample_roundtrip_is_lossless():
    _assert_lossless_roundtrip(_load(FIXTURE))


def test_sample_dropempty_roundtrip_is_lossless():
    # drop_empty + template must round-trip exactly like the full-width path
    _assert_dropempty_roundtrip(_load(FIXTURE))


def test_dropempty_grouping_matches_committed_fixture():
    # The compact (empties-dropped) grouped shape is pinned as a fixture so the
    # documented output is verified, not just described.
    grouped = group_flat_records(_load(FIXTURE), drop_empty=True)
    assert grouped == _load(GROUPED_DROPEMPTY)


def test_dropempty_omits_only_empty_values():
    # Every key dropped by drop_empty must have been empty; no real datum is lost.
    rows = _load(FIXTURE)
    full = group_flat_records(rows)
    drop = group_flat_records(rows, drop_empty=True)
    for rf, rd in zip(full, drop, strict=True):
        # root-level fields
        for key, val in rf.items():
            if key == "repeated_elements":
                continue
            if key not in rd:
                assert val in ("", None), f"dropped non-empty root field {key!r}={val!r}"
        # repeated elements (same order, paired by index)
        for ef, ed in zip(rf["repeated_elements"], rd["repeated_elements"], strict=True):
            for key, val in ef.items():
                if key not in ed:
                    assert val in ("", None), f"dropped non-empty repeat field {key!r}={val!r}"
    # and the structural keys always survive in every repeated element
    for rd in drop:
        for el in rd["repeated_elements"]:
            assert "redcap_repeat_instrument" in el
            assert "redcap_repeat_instance" in el


def test_sample_grouping_structure():
    grouped = group_flat_records(_load(FIXTURE))
    assert [r["record_id"] for r in grouped] == ["1", "2"]
    rec1 = next(r for r in grouped if r["record_id"] == "1")
    assert rec1["demographics_name"] == "Ada"
    assert [e["redcap_repeat_instance"] for e in rec1["repeated_elements"]] == [1, 2]


# --- regression tests for the review fixes ---------------------------------


def test_empty_row_does_not_clobber_captured_value():
    rows = [
        {"record_id": "1", "redcap_repeat_instrument": "", "x": "A"},
        {"record_id": "1", "redcap_repeat_instrument": "", "x": ""},
    ]
    (record,) = group_flat_records(rows)
    assert record["x"] == "A"


def test_ungroup_rejects_list_valued_field():
    records = [{"record_id": "1", "hpo_terms": ["HP:1", "HP:2"], "repeated_elements": []}]
    with pytest.raises(ValueError, match="list-valued"):
        ungroup_records(records)


def test_custom_record_id_key_not_leaked_into_repeats():
    rows = [
        {"patient_id": "1", "redcap_repeat_instrument": "", "name": "Ada"},
        {
            "patient_id": "1",
            "redcap_repeat_instrument": "visit",
            "redcap_repeat_instance": "1",
            "weight": "60",
        },
    ]
    (record,) = group_flat_records(rows, record_id_key="patient_id")
    assert "patient_id" not in record["repeated_elements"][0]


# --- optional: real export via env var (skipped in CI) ---------------------

_LOCAL = os.environ.get("LINKML_REDCAP_FLAT_FIXTURE")


@pytest.mark.skipif(not _LOCAL, reason="set LINKML_REDCAP_FLAT_FIXTURE to a flat REDCap export")
def test_local_real_export_roundtrip():
    rows = _load(Path(_LOCAL))
    assert isinstance(rows, list) and rows
    _assert_lossless_roundtrip(rows)
    _assert_dropempty_roundtrip(rows)
