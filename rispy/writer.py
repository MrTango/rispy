"""RIS Writer."""

from enum import Enum
import warnings
from typing import Dict, List, TextIO, Union, Optional

from .config import LIST_TYPE_TAGS
from .config import TAG_KEY_MAPPING

__all__ = ["dump", "dumps", "WriterImplementation", "BaseWriter", "RISWriter"]


def invert_dictionary(mapping):
    remap = {v: k for k, v in mapping.items()}
    if len(remap) != len(mapping):
        raise ValueError("Dictionary cannot be inverted; some values were not unique")
    return remap


class WriterImplementation(str, Enum):
    """List default RIS writer implementations."""

    BASE = "base"


class BaseWriter:
    """Base writer class. Create a subclass to use."""

    START_TAG: str = ""
    END_TAG: str = "ER"
    IGNORE: List[str] = []
    PATTERN: str = ""
    SKIP_UNKNOWN_TAGS: bool = False
    ENFORCE_LIST_TAGS: bool = True
    DEFAULT_MAPPING: Optional[Dict] = None
    DEFAULT_LIST_TAGS: Optional[List[str]] = None
    DEFAULT_REFERENCE_TYPE: str = "JOUR"
    SEPARATOR: Optional[str] = "\n"

    def __init__(self, mapping: Optional[Dict] = None, list_tags: Optional[List] = None):
        """Override default tag map and list tags in instance."""
        self._mapping = mapping
        self._rev_mapping = invert_dictionary(self.mapping)
        self._list_tags = list_tags
        self._skip_unknown = ["UK"] if self.SKIP_UNKNOWN_TAGS else []

    @property
    def mapping(self):
        """Check if a tag map can be found."""
        if self._mapping is not None:
            return self._mapping
        elif self.DEFAULT_MAPPING is not None:
            return self.DEFAULT_MAPPING
        else:
            raise IOError("Default mapping not set.")

    @property
    def list_tags(self):
        """Check if a set of list tags can be found."""
        if self._list_tags is not None:
            return self._list_tags
        elif self.DEFAULT_LIST_TAGS is not None:
            return self.DEFAULT_LIST_TAGS
        else:
            raise IOError("Default list tags not set.")

    def _get_reference_type(self, ref):

        if "type_of_reference" in ref.keys():
            # TODO add check
            return ref["type_of_reference"]

        if self.DEFAULT_REFERENCE_TYPE is not None:
            return self.DEFAULT_REFERENCE_TYPE
        else:
            raise ValueError("Unknown type of reference")

    def _format_line(self, tag, value=""):
        """Format a RIS line."""
        return self.PATTERN.format(tag=tag, value=value)

    def _format_reference(self, ref, count):

        lines = []

        header = self.set_header(count)
        if header is not None:
            lines.append(header)
        lines.append(self._format_line(self.START_TAG, self._get_reference_type(ref)))

        for label, value in ref.items():

            # not available
            try:
                tag = self._rev_mapping[label.lower()]
            except KeyError:
                warnings.warn(UserWarning(f"label `{label}` not exported"))
                continue

            # ignore
            if tag in [self.START_TAG] + self.IGNORE + self._skip_unknown:
                continue

            # list tag
            if tag in self.list_tags or (not self.ENFORCE_LIST_TAGS and isinstance(value, list)):
                for val_i in value:
                    lines.append(self._format_line(tag, val_i))
            else:
                lines.append(self._format_line(tag, value))

        lines.append(self._format_line("ER"))

        if self.SEPARATOR is not None:
            lines.append(self.SEPARATOR.replace("\n", "", 1))

        return lines

    def _format_all_references(self, references):

        for i, ref in enumerate(references):
            lines_ref = self._format_reference(ref, count=i + 1)
            for line in lines_ref:
                yield line

    def formats(self, references: List[Dict]) -> str:
        """Format a list of references into an RIS string."""
        lines = self._format_all_references(references)
        return "\n".join(lines)

    def set_header(self, count: int) -> Optional[str]:
        """Create the header for each reference."""
        return None


class RISWriter(BaseWriter):
    """Subclass of BaseWriter for writing RIS files."""

    START_TAG = "TY"
    PATTERN = "{tag}  - {value}"
    DEFAULT_MAPPING = TAG_KEY_MAPPING
    DEFAULT_LIST_TAGS = LIST_TYPE_TAGS

    def set_header(self, count):
        return "{i}.".format(i=count)


def dump(
    references: List[Dict],
    file: TextIO,
    implementation: Union[WriterImplementation, BaseWriter] = WriterImplementation.BASE,
):
    """Write an RIS file to file or file-like object.

    Entries are codified as dictionaries whose keys are the
    different tags. For single line and singly occurring tags,
    the content is codified as a string. In the case of multiline
    or multiple key occurrences, the content is returned as a list
    of strings.

    Args:
        references (List[Dict]): List of references.
        file (TextIO): File handle to store ris formatted data.
        implementation (RisImplementation): RIS implementation; base by
                                            default.
    """
    text = dumps(references, implementation)
    file.writelines(text)


def dumps(
    references: List[Dict],
    implementation: Union[WriterImplementation, BaseWriter] = WriterImplementation.BASE,
) -> str:
    """Return an RIS formatted string.

    Entries are codified as dictionaries whose keys are the
    different tags. For single line and singly occurring tags,
    the content is codified as a string. In the case of multiline
    or multiple key occurrences, the content is returned as a list
    of strings.

    Args:
        references (List[Dict]): List of references.
        implementation (RisImplementation): RIS implementation; base by
                                            default.
    """
    if implementation == WriterImplementation.BASE:
        writer = RISWriter()
    elif isinstance(implementation, str):
        raise ValueError(f"Unknown implementation: {implementation}")
    else:
        writer = implementation

    return writer.formats(references)
