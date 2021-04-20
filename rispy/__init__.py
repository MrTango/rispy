"""Read and write RIS and WOK files."""

__version__ = "0.6.0"

from .config import LIST_TYPE_TAGS, TAG_KEY_MAPPING, TYPE_OF_REFERENCE_MAPPING
from .parser import RisImplementation, load, loads
from .writer import dump, dumps

__all__ = [
    "LIST_TYPE_TAGS",
    "TAG_KEY_MAPPING",
    "TYPE_OF_REFERENCE_MAPPING",
    "RisImplementation",
    "load",
    "loads",
    "dump",
    "dumps",
]
