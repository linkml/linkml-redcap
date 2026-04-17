"""Tests for the public loader API."""

from pathlib import Path

from linkml_redcap.data_dictionary import schema_path, schema_view


def test_schema_path_exists():
    p = schema_path()
    assert isinstance(p, Path)
    assert p.exists()
    assert p.name == SCHEMA_FILENAME


def test_schema_view_loads():
    sv = schema_view()
    # Sanity: core classes from the meta-schema are reachable
    assert "DataDictionary" in sv.all_classes()
    assert "Field" in sv.all_classes()
    assert "FieldType" in sv.all_enums()


def test_version_importable():
    import linkml_redcap_data_dictionary
    assert linkml_redcap_data_dictionary.__version__
