"""LinkML meta-schema for REDCap data dictionaries."""

from __future__ import annotations

from importlib.resources import as_file, files
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from linkml_runtime.utils.schemaview import SchemaView

SCHEMA_FILENAME = "redcap_data_dictionary.yaml"


def schema_path() -> Path:
    """Return the filesystem path to the bundled meta-schema YAML."""
    resource = files(__name__).joinpath("schema").joinpath(SCHEMA_FILENAME)
    with as_file(resource) as p:
        return Path(p)


def schema_view() -> SchemaView:
    """Return a SchemaView instance ready for introspection."""
    from linkml_runtime.utils.schemaview import SchemaView

    return SchemaView(str(schema_path()))
