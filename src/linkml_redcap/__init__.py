"""linkml-redcap: LinkML schemas for REDCap structures.

Two submodules are available:

* :mod:`linkml_redcap.data_dictionary` — the meta-schema describing a valid
  REDCap *data dictionary* (the 18-column CSV).
* :mod:`linkml_redcap.record` — the reusable envelope for REDCap *record data*,
  in both its flat-export and structured/nested shapes, plus structural
  grouping helpers for flat ⇄ structured conversion.
"""

from linkml_redcap import data_dictionary, record
from linkml_redcap.data_dictionary import schema_path, schema_view

__all__ = [
    "data_dictionary",
    "record",
    "schema_path",
    "schema_view",
    "__version__",
]

__version__ = "0.1.0"
