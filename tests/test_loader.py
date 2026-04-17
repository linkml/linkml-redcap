"""Tests for the public loader API."""

from pathlib import Path

from linkml_redcap import __version__
from linkml_redcap.data_dictionary import SCHEMA_FILENAME, schema_path, schema_view


def test_schema_path_exists():
    p = schema_path()
    assert isinstance(p, Path)
    assert p.exists()
    assert p.name == SCHEMA_FILENAME


def test_schema_view_loads():
    sv = schema_view()
    assert "DataDictionary" in sv.all_classes()
    assert "Field" in sv.all_classes()
    assert "FieldType" in sv.all_enums()


def test_version_importable():
    assert __version__