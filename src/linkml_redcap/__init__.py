"""linkml-redcap: LinkML schemas for REDCap structures.

Two submodules are available:

* :mod:`linkml_redcap.data_dictionary` — the meta-schema describing a valid
  REDCap *data dictionary* (the 18-column CSV).
* :mod:`linkml_redcap.record` — the reusable envelope for REDCap *record data*,
  in both its flat-export and structured/nested shapes, plus structural
  grouping helpers for flat ⇄ structured conversion.

:func:`importmap` lets a downstream schema use the documented bare import
(``imports: - redcap_record``) and resolve it from the installed package instead
of copying the YAML into the consuming project.
"""

from linkml_redcap import data_dictionary, record
from linkml_redcap._importmap import importmap, write_importmap
from linkml_redcap._version import __version__
from linkml_redcap.data_dictionary import schema_path, schema_view

__all__ = [
    "data_dictionary",
    "record",
    "schema_path",
    "schema_view",
    "importmap",
    "write_importmap",
    "__version__",
]
