"""RIS Writer."""

import warnings
from typing import Dict, List, TextIO, Optional
from abc import ABC

from .config import LIST_TYPE_TAGS, TAG_KEY_MAPPING
from .utils import invert_dictionary


__all__ = ["dump", "dumps", "BaseWriter", "RisWriter"]


class BaseWriter(ABC):
    """Base writer class. Create a subclass to use.

    When creating a new implementation class, some variables and classes need
    to be overridden. This docstring documents how to override these
    parameters when creating a subclass.

    Class variables:
        START_TAG (str): Start tag, required.
        END_TAG (str): End tag. Defaults to 'ER'.
        IGNORE (list, optional): List of tags to ignore. Defaults to [].
        PATTERN (str): String containing a format for a line
                       (e.g. ``"{tag}  - {value}"``). Should contain `tag` and
                       `value` in curly brackets. Required.
        DEFAULT_MAPPING (list): Default mapping for this class. Required.
        DEFAULT_LIST_TAGS (list): Default list tags for this class. Required.
        DEFAULT_REFERENCE_TYPE (str): Default reference type, used if a
                                      reference does not have a type.
        SEPARATOR (str, optional): String to separate the references in the
                                  file. Defaults to newline.

    Class methods:
        set_header: Create a header for each reference. Has the reference
                    number as a parameter.

    """

    START_TAG: str
    END_TAG: str = "ER"
    PATTERN: str
    DEFAULT_IGNORE: List[str] = []
    DEFAULT_MAPPING: Dict
    DEFAULT_LIST_TAGS: List[str]
    DEFAULT_REFERENCE_TYPE: str = "JOUR"
    SEPARATOR: Optional[str] = "\n"

    def __init__(
        self,
        *,
        mapping: Optional[Dict] = None,
        list_tags: Optional[List[str]] = None,
        ignore: Optional[List[str]] = None,
        skip_unknown_tags: bool = False,
        enforce_list_tags: bool = True,
    ):
        """Override default tag map and list tags in instance.

        Args:
            mapping (dict, optional): Map tags to tag names.
            list_tags (list, optional): List of list-type tags.
            ignore (list, optional): List of tags to ignore.
            skip_unknown_tags (bool, optional): Bool for whether to write unknown
                                                tags to the file. Defaults to
                                                `False`.
            enforce_list_tags (bool, optional): If `True` tags that are not set as
                                                list tags will be written into one
                                                line. Defaults to `True`.

        """
        self.mapping = mapping if mapping is not None else self.DEFAULT_MAPPING
        self.list_tags = list_tags if list_tags is not None else self.DEFAULT_LIST_TAGS
        self.ignore = ignore if ignore is not None else self.DEFAULT_IGNORE
        self._rev_mapping = invert_dictionary(self.mapping)
        self.skip_unknown_tags = skip_unknown_tags
        self.enforce_list_tags = enforce_list_tags

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

        tags_to_skip = [self.START_TAG] + self.ignore
        if self.skip_unknown_tags:
            tags_to_skip.append("UK")

        for label, value in ref.items():

            # not available
            try:
                tag = self._rev_mapping[label.lower()]
            except KeyError:
                warnings.warn(UserWarning(f"label `{label}` not exported"))
                continue

            # ignore
            if tag in tags_to_skip:
                continue

            # list tag
            if tag in self.list_tags or (not self.enforce_list_tags and isinstance(value, list)):
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
    references: List[Dict], file: TextIO, *, implementation: Optional[BaseWriter] = None, **kw,
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
    text = dumps(references, implementation=implementation, **kw)
    file.writelines(text)


def dumps(references: List[Dict], *, implementation: Optional[BaseWriter] = None, **kw) -> str:
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
        writer = RisWriter
    else:
        writer = implementation

    return writer(**kw).formats(references)
