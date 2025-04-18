"""A Python reader/writer of RIS reference files"""

from .config import LIST_TYPE_TAGS, TAG_KEY_MAPPING, TYPE_OF_REFERENCE_MAPPING
from .parser import BaseParser, RisParser, WokParser, load, loads
from .writer import BaseWriter, RisWriter, dump, dumps

__version__ = "0.9.0"

__all__ = [
    "LIST_TYPE_TAGS",
    "TAG_KEY_MAPPING",
    "TYPE_OF_REFERENCE_MAPPING",
    "BaseParser",
    "BaseWriter",
    "RisParser",
    "RisWriter",
    "WokParser",
    "__version__",
    "dump",
    "dumps",
    "load",
    "loads",
]
