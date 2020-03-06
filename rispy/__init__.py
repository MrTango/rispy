"""Read and write RIS and WOK files"""

__version__ = "0.5.0"

from .config import LIST_TYPE_TAGS, TAG_KEY_MAPPING  # noqa
from .parser import RisImplementation, load, loads  # noqa
from .writer import dump, dumps  # noqa
