"""Read and write WOK and Refman's RIS files"""

__version__ = "0.4.3-next"

from .config import LIST_TYPE_TAGS, TAG_KEY_MAPPING  # noqa
from .parser import load, loads  # noqa
from .writer import dump, dumps  # noqa
