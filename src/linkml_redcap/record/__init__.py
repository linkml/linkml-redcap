"""Reusable LinkML envelope for REDCap record data (flat and structured)."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from linkml_redcap._resources import resolve_schema
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
    return resolve_schema(__name__, SCHEMA_FILENAME)


def schema_view() -> SchemaView:
    """Return a SchemaView over the record-envelope schema, ready for introspection."""
    from linkml_runtime.utils.schemaview import SchemaView

    return SchemaView(str(schema_path()))
