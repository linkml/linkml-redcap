"""Resolve bundled schema files to stable filesystem paths.

``importlib.resources.as_file`` only guarantees a real path *within* its context
manager: for a zip-imported package it extracts the resource to a temporary file
that is removed as soon as the context exits. Returning such a path from a public
``schema_path()`` would hand callers (and ``SchemaView``) a path that may already
be gone.

We therefore enter the ``as_file`` context under a single process-lifetime
``ExitStack`` that is closed at interpreter shutdown, so the path stays valid for
the whole session. For a normally installed (unzipped) wheel this is a no-op that
simply returns the real file on disk.
"""

from __future__ import annotations

import atexit
from contextlib import ExitStack
from importlib.resources import as_file, files
from pathlib import Path

_file_manager = ExitStack()
atexit.register(_file_manager.close)


def resolve_schema(package: str, filename: str) -> Path:
    """Return a stable filesystem path to ``<package>/schema/<filename>``."""
    resource = files(package).joinpath("schema").joinpath(filename)
    return Path(_file_manager.enter_context(as_file(resource)))
