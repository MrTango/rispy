"""RIS Writer."""

import warnings
from typing import Dict, List, TextIO, Optional

from .config import LIST_TYPE_TAGS
from .config import TAG_KEY_MAPPING


__all__ = ["dump", "dumps", "BaseWriter", "RisWriter"]


def invert_dictionary(mapping):
    remap = {v: k for k, v in mapping.items()}
    if len(remap) != len(mapping):
        raise ValueError("Dictionary cannot be inverted; some values were not unique")
    return remap


class BaseWriter:
    """Base writer class. Create a subclass to use."""

    START_TAG: str
    END_TAG: str = "ER"
    IGNORE: List[str] = []
    PATTERN: str
    SKIP_UNKNOWN_TAGS: bool = False
    ENFORCE_LIST_TAGS: bool = True
    DEFAULT_MAPPING: Dict
    DEFAULT_LIST_TAGS: List[str]
    DEFAULT_REFERENCE_TYPE: str = "JOUR"
    SEPARATOR: Optional[str] = "\n"

    def __init__(self, mapping: Optional[Dict] = None, list_tags: Optional[List] = None):
        """Override default tag map and list tags in instance."""
        self.mapping = mapping or self.DEFAULT_MAPPING
        self._rev_mapping = invert_dictionary(self.mapping)
        self.list_tags = list_tags or self.DEFAULT_LIST_TAGS

        if self.SKIP_UNKNOWN_TAGS:
            self.IGNORE.append("UK")

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
            if tag in [self.START_TAG] + self.IGNORE:
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


class RisWriter(BaseWriter):
    """Subclass of BaseWriter for writing RIS files."""

    START_TAG = "TY"
    PATTERN = "{tag}  - {value}"
    DEFAULT_MAPPING = TAG_KEY_MAPPING
    DEFAULT_LIST_TAGS = LIST_TYPE_TAGS

    def set_header(self, count):
        return "{i}.".format(i=count)


def dump(
    references: List[Dict], file: TextIO, implementation: Optional[BaseWriter] = None,
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


def dumps(references: List[Dict], implementation: Optional[BaseWriter] = None,) -> str:
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
    if implementation is None:
        writer = RisWriter()
    else:
        writer = implementation

    return writer.formats(references)
