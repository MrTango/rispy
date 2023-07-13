"""A Python reader/writer of RIS reference files"""

from .config import LIST_TYPE_TAGS, TAG_KEY_MAPPING, TYPE_OF_REFERENCE_MAPPING
from .parser import BaseParser, RisParser, WokParser, load, loads
from .writer import BaseWriter, RisWriter, dump, dumps

__version__ = "0.8.0"

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
