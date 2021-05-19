"""Read and write RIS and WOK files."""

__version__ = "0.6.0"

from .config import LIST_TYPE_TAGS, TAG_KEY_MAPPING, TYPE_OF_REFERENCE_MAPPING
from .parser import load, loads, BaseParser, RisParser, WokParser
from .writer import dump, dumps, BaseWriter, RisWriter

__all__ = [
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
