try:
    from linkml_redcap._version import __version__, __version_tuple__
except ImportError:  # pragma: no cover
    __version__ = "0.0.1"
    __version_tuple__ = (0, 0, 1)
