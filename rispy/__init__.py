"""Read and write RIS and WOK files."""

__version__ = "0.6.0"

from .config import LIST_TYPE_TAGS, TAG_KEY_MAPPING, TYPE_OF_REFERENCE_MAPPING
from .parser import RisImplementation, load, loads, Base, Ris, Wok
from .writer import dump, dumps, WriterImplementation, BaseWriter, RISWriter

__all__ = [
    "LIST_TYPE_TAGS",
    "TAG_KEY_MAPPING",
    "TYPE_OF_REFERENCE_MAPPING",
    "RisImplementation",
    "load",
    "loads",
    "dump",
    "dumps",
    "Base",
    "Ris",
    "Wok",
    "WriterImplementation",
    "BaseWriter",
    "RISWriter",
]
