"""RIS Writer."""

import warnings
from abc import ABC, abstractmethod
from pathlib import Path
from typing import ClassVar, Optional, TextIO, Union

from .config import DELIMITED_TAG_MAPPING, LIST_TYPE_TAGS, TAG_KEY_MAPPING
from .utils import invert_dictionary

__all__ = ["BaseWriter", "RisWriter", "dump", "dumps"]


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
    UNKNOWN_TAG: str = "UK"
    PATTERN: str
    DEFAULT_IGNORE: ClassVar[list[str]] = []
    DEFAULT_MAPPING: dict
    DEFAULT_LIST_TAGS: list[str]
    DEFAULT_DELIMITER_MAPPING: dict
    DEFAULT_REFERENCE_TYPE: str = "JOUR"
    REFERENCE_TYPE_KEY: str = "type_of_reference"
    SEPARATOR: Optional[str] = ""
    NEWLINE: str = "\n"

    def __init__(
        self,
        *,
        mapping: Optional[dict] = None,
        list_tags: Optional[list[str]] = None,
        delimiter_tags_mapping: Optional[dict] = None,
        ignore: Optional[list[str]] = None,
        skip_unknown_tags: bool = False,
        enforce_list_tags: bool = True,
    ):
        """Override default tag map and list tags in instance.

        Args:
            mapping (dict, optional): Map tags to tag names.
            list_tags (list, optional): List of list-type tags.
            delimiter_tags_mapping (dict, optional): Map of delimiters to tags.
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
        self.delimiter_map = (
            delimiter_tags_mapping
            if delimiter_tags_mapping is not None
            else self.DEFAULT_DELIMITER_MAPPING
        )
        self.ignore = ignore if ignore is not None else self.DEFAULT_IGNORE
        self._rev_mapping = invert_dictionary(self.mapping)
        self.skip_unknown_tags = skip_unknown_tags
        self.enforce_list_tags = enforce_list_tags

    def _get_reference_type(self, ref):
        if self.REFERENCE_TYPE_KEY in ref:
            return ref[self.REFERENCE_TYPE_KEY]
        return self.DEFAULT_REFERENCE_TYPE

    def _format_line(self, tag, value=""):
        """Format a RIS line."""
        return self.PATTERN.format(tag=tag, value=value)

    def _format_reference(self, ref, count, n):
        if header := self.set_header(count):
            yield header
        yield self._format_line(self.START_TAG, self._get_reference_type(ref))

        tags_to_skip = [self.START_TAG, *self.ignore]
        if self.skip_unknown_tags:
            tags_to_skip.append(self.UNKNOWN_TAG)

        for label, value in ref.items():
            # not available
            try:
                tag = self._rev_mapping[label.lower()]
            except KeyError:
                if label.lower() == "unknown_tag":
                    tag = self.UNKNOWN_TAG
                else:
                    warnings.warn(UserWarning(f"label `{label}` not exported"), stacklevel=2)
                    continue

            # ignore
            if tag in tags_to_skip:
                continue

            # list tag
            if tag in self.list_tags or (not self.enforce_list_tags and isinstance(value, list)):
                for val_i in value:
                    yield self._format_line(tag, val_i)

            # unknown tag(s), which are lists held in a defaultdict
            elif tag == self.UNKNOWN_TAG:
                for unknown_tag in value.keys():
                    for val_i in value[unknown_tag]:
                        yield self._format_line(unknown_tag, val_i)

            # write delimited tags
            elif tag in self.delimiter_map:
                combined_val = self.delimiter_map[tag].join(value)
                yield self._format_line(tag, combined_val)

            # all non-list tags
            else:
                yield self._format_line(tag, value)

        yield self._format_line(self.END_TAG)

        if self.SEPARATOR is not None and count < n:
            yield self.SEPARATOR

    def _yield_lines(self, references, extra_line=False):
        n = len(references)
        for i, ref in enumerate(references):
            yield from self._format_reference(ref, count=i + 1, n=n)
        if extra_line:
            yield ""

    def format_lines(self, file, references):
        """Write references to a file."""
        for line in self._yield_lines(references):
            file.write(f"{line}{self.NEWLINE}")

    def formats(self, references: list[dict]) -> str:
        """Format a list of references into an RIS string."""
        lines = self._yield_lines(references, extra_line=True)
        return self.NEWLINE.join(lines)

    @abstractmethod
    def set_header(self, count: int) -> str:
        """Create the header for each reference; if empty string, unused."""
        ...


class RisWriter(BaseWriter):
    """Subclass of BaseWriter for writing RIS files."""

    START_TAG = "TY"
    PATTERN = "{tag}  - {value}"
    DEFAULT_MAPPING = TAG_KEY_MAPPING
    DEFAULT_LIST_TAGS = LIST_TYPE_TAGS
    DEFAULT_DELIMITER_MAPPING = DELIMITED_TAG_MAPPING

    def set_header(self, count):
        return f"{count}."


def dump(
    references: list[dict],
    file: Union[TextIO, Path],
    *,
    encoding: Optional[str] = None,
    implementation: type[BaseWriter] = RisWriter,
    **kw,
):
    """Write an RIS file to file or file-like object.

    Entries are codified as dictionaries whose keys are the
    different tags. For single line and singly occurring tags,
    the content is codified as a string. In the case of multiline
    or multiple key occurrences, the content is returned as a list
    of strings.

    Args:
        references (list[dict]): List of references.
        file (TextIO): File handle to store ris formatted data.
        encoding (str, optional): Encoding to use when opening file.
        implementation (BaseWriter): RIS implementation; base by default.
    """
    if isinstance(file, Path):
        with file.open(mode="w", encoding=encoding) as f:
            implementation(**kw).format_lines(f, references)
    elif hasattr(file, "write"):
        implementation(**kw).format_lines(file, references)
    else:
        raise ValueError("File must be a file-like object or a Path object")


def dumps(references: list[dict], *, implementation: type[BaseWriter] = RisWriter, **kw) -> str:
    """Return an RIS formatted string.

    Entries are codified as dictionaries whose keys are the
    different tags. For single line and singly occurring tags,
    the content is codified as a string. In the case of multiline
    or multiple key occurrences, the content is returned as a list
    of strings.

    Args:
        references (list[dict]): List of references.
        implementation (BaseWriter): RIS implementation; RisWriter by default.
    """
    return implementation(**kw).formats(references)
