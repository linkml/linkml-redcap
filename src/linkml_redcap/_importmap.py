"""Resolve bare ``imports:`` names to the bundled schema files.

A downstream schema declares the import by canonical URI::

    imports:
      - linkml:types
      - https://w3id.org/linkml/redcap-record

Use the URI form, not the bare name ``redcap_record``. linkml-runtime's
``imports_closure()`` rewrites a bare import to be relative to the *importing*
file's directory (``if "/" in sn and ":" not in i``), so a bare name inside a
subdirectory such as ``schema/instruments/`` resolves to
``schema/instruments/redcap_record.yaml`` and never reaches the importmap.
Imports containing ``":"`` are exempt from that rewrite, so the URI resolves from
any depth. Both spellings are mapped below, but only the URI is depth-safe.

LinkML resolves a bare import name relative to the importing file's directory, so
without help the only way to satisfy that import is to *copy* ``redcap_record.yaml``
into the consuming project — which defeats the point of shipping the schema as a
package and lets the copy drift.

``importmap()`` returns the mapping LinkML needs, so a consumer can keep the
documented import and resolve it from the installed package::

    from linkml_runtime import SchemaView
    from linkml_redcap import importmap
    sv = SchemaView("my_schema.yaml", importmap=importmap())

For the LinkML command-line generators, which take a JSON file, write one::

    linkml-redcap-importmap importmap.json
    gen-project --importmap importmap.json my_schema.yaml

Both the bare names and the canonical ``w3id.org`` URIs are mapped, so either
import style resolves.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

__all__ = ["importmap", "write_importmap", "main"]

_CANONICAL = {
    "redcap_record": "https://w3id.org/linkml/redcap-record",
    "redcap_data_dictionary": "https://w3id.org/linkml/redcap-data-dictionary",
}


def importmap() -> dict[str, str]:
    """Map every supported import spelling to a bundled schema path.

    Returns:
        Mapping suitable for ``SchemaView(..., importmap=...)`` or for
        serialising to a LinkML CLI ``--importmap`` JSON file.
    """
    from linkml_redcap import data_dictionary, record

    paths = {
        "redcap_record": record.schema_path(),
        "redcap_data_dictionary": data_dictionary.schema_path(),
    }
    mapping: dict[str, str] = {}
    for name, path in paths.items():
        # LinkML appends the ``.yaml`` extension to whatever an importmap resolves
        # to, so the target must be the extension-less path.
        target = str(path.with_suffix(""))
        mapping[name] = target
        mapping[_CANONICAL[name]] = target
        # LinkML also probes the extension-less sibling of a relative import
        mapping[f"./{name}"] = target
    return mapping


def write_importmap(path: str | Path) -> Path:
    """Write :func:`importmap` to ``path`` as JSON and return the path."""
    destination = Path(path)
    destination.write_text(json.dumps(importmap(), indent=2, sort_keys=True) + "\n")
    return destination


def main(argv: list[str] | None = None) -> int:
    """Console entry point: ``linkml-redcap-importmap [OUTPUT]``.

    Writes to ``OUTPUT`` when given, otherwise to stdout.
    """
    args = sys.argv[1:] if argv is None else argv
    if args and args[0] in ("-h", "--help"):
        print(main.__doc__)
        return 0
    if args:
        print(write_importmap(args[0]))
    else:
        json.dump(importmap(), sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
