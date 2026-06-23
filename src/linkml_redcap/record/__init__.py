"""Reusable LinkML envelope for REDCap record data (flat and structured)."""

from __future__ import annotations

from importlib.resources import as_file, files
from pathlib import Path
from typing import TYPE_CHECKING

from linkml_redcap.record.grouping import (
    STRUCTURAL_KEYS,
    group_flat_records,
    ungroup_records,
)

if TYPE_CHECKING:
    from linkml_runtime.utils.schemaview import SchemaView

SCHEMA_FILENAME = "redcap_record.yaml"

__all__ = [
    "SCHEMA_FILENAME",
    "STRUCTURAL_KEYS",
    "schema_path",
    "schema_view",
    "group_flat_records",
    "ungroup_records",
]


def schema_path() -> Path:
    """Return the filesystem path to the bundled record-envelope schema YAML."""
    resource = files(__name__).joinpath("schema").joinpath(SCHEMA_FILENAME)
    with as_file(resource) as p:
        return Path(p)


def schema_view() -> SchemaView:
    """Return a SchemaView over the record-envelope schema, ready for introspection."""
    from linkml_runtime.utils.schemaview import SchemaView

    return SchemaView(str(schema_path()))
