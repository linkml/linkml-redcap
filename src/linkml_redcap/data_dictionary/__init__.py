"""LinkML meta-schema for REDCap data dictionaries."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from linkml_redcap._resources import resolve_schema

if TYPE_CHECKING:
    from linkml_runtime.utils.schemaview import SchemaView

SCHEMA_FILENAME = "redcap_data_dictionary.yaml"


def schema_path() -> Path:
    """Return the filesystem path to the bundled meta-schema YAML."""
    return resolve_schema(__name__, SCHEMA_FILENAME)


def schema_view() -> SchemaView:
    """Return a SchemaView instance ready for introspection."""
    from linkml_runtime.utils.schemaview import SchemaView

    return SchemaView(str(schema_path()))
