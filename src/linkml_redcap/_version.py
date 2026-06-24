"""Resolved package version (falls back when running from a source tree)."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("linkml-redcap")
except PackageNotFoundError:  # not installed (e.g. running from a checkout)
    __version__ = "0.1.0"
