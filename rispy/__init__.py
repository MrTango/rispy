"""Read and write RIS and WOK files."""

from .config import LIST_TYPE_TAGS, TAG_KEY_MAPPING, TYPE_OF_REFERENCE_MAPPING
from .parser import load, loads, BaseParser, RisParser, WokParser
from .version import __version__
from .writer import dump, dumps, BaseWriter, RisWriter

__all__ = [
    "__version__",
    "LIST_TYPE_TAGS",
    "TAG_KEY_MAPPING",
    "TYPE_OF_REFERENCE_MAPPING",
    "load",
    "loads",
    "dump",
    "dumps",
    "BaseParser",
    "WokParser",
    "RisParser",
    "BaseWriter",
    "RisWriter",
]
