"""RIS Parser."""

import re
from abc import ABC, abstractmethod
from collections import defaultdict
from pathlib import Path
from typing import ClassVar, Dict, List, Optional, TextIO, Type, Union

from .config import (
    DELIMITED_TAG_MAPPING,
    LIST_TYPE_TAGS,
    TAG_KEY_MAPPING,
    WOK_LIST_TYPE_TAGS,
    WOK_TAG_KEY_MAPPING,
)

__all__ = ["load", "loads", "BaseParser", "WokParser", "RisParser"]


class NextLine(Exception):
    pass


class ParseError(Exception):
    pass


class BaseParser(ABC):
    """Base parser class. Create a subclass to use.

    When creating a new implementation class, some variables and classes need
    to be overridden. This docstring documents how to override these
    parameters when creating a subclass.

    Class variables:
        START_TAG (str): Start tag, required.
        END_TAG (str): End tag. Defaults to 'ER'.
        PATTERN (str): String containing a regex pattern. This pattern
                       determines if a line has a valid tag. Required.
        DEFAULT_IGNORE (list, optional): Default list of tags to ignore.
        DEFAULT_MAPPING (dict): A default mapping for the custom parser.
                                Required.
        DEFAULT_LIST_TAGS (list): A list of tags that should be read as lists.
                                  Required.

    Class methods:
        get_content: Returns the non-tag part of a line. Required.
        get_tag: Returns the tag part of a line. Default is to return the
                 first two characters.
        clean_text: Clean each line before it's parsed.

    """

    START_TAG: str
    END_TAG: str = "ER"
    UNKNOWN_TAG: str = "UK"
    PATTERN: str
    DEFAULT_IGNORE: ClassVar[List[str]] = []
    DEFAULT_MAPPING: Dict
    DEFAULT_LIST_TAGS: List[str]
    DEFAULT_DELIMITER_MAPPING: Dict
    DEFAULT_NEWLINE: ClassVar[str] = "\n"

    def __init__(
        self,
        *,
        mapping: Optional[Dict] = None,
        list_tags: Optional[List[str]] = None,
        delimiter_tags_mapping: Optional[Dict] = None,
        ignore: Optional[List[str]] = None,
        skip_unknown_tags: bool = False,
        enforce_list_tags: bool = True,
        newline: Optional[str] = None,
    ):
        """Initialize the parser function.

        Args:
            mapping (dict, optional): Map tags to tag names.
            list_tags (list, optional): List of list-type tags.
            delimiter_tags_mapping (dict, optional): Map of delimiters to tags.
            ignore (list, optional): List of tags to ignore.
            skip_unknown_tags (bool, optional): Bool to skip tags that are not in
                                                `TAG_KEY_MAPPING`. If unknown tags
                                                are not skipped, they will be added
                                                to the `unknown_tag` key.
                                                Defaults to `False`.
            enforce_list_tags (bool, optional): Bool for choosing whether to
                                                strictly enforce list type tags.
                                                If this is `False`, tags that
                                                occur multiple times in a reference
                                                will be converted to a list instead
                                                of being overridden. Values set to
                                                be list tags will still be read as
                                                list tags. Defaults to `True`.
            newline (str, optional): Line separator.

        """
        self.pattern = re.compile(self.PATTERN)
        self.mapping = mapping if mapping is not None else self.DEFAULT_MAPPING
        self.list_tags = list_tags if list_tags is not None else self.DEFAULT_LIST_TAGS
        self.delimiter_map = (
            delimiter_tags_mapping
            if delimiter_tags_mapping is not None
            else self.DEFAULT_DELIMITER_MAPPING
        )
        self.ignore = ignore if ignore is not None else self.DEFAULT_IGNORE
        self.skip_unknown_tags = skip_unknown_tags
        self.enforce_list_tags = enforce_list_tags
        self.newline = newline if newline is not None else self.DEFAULT_NEWLINE

    def parse(self, text: str) -> List[Dict]:
        """Parse RIS string."""
        return self.parse_lines((l for l in text.split(self.newline)))

    def parse_lines(self, lines: Union[TextIO, List[str]]):
        """Parse RIS file line by line."""
        return list(self._yield_lines(lines))

    def _parse_tag(self, line):

        return (self.get_tag(line), self.get_content(line))

    def _iter_till_start(self, lines):

        while True:
            line = next(lines)
            if line.startswith(self.START_TAG):
                return {self.mapping[self.START_TAG]: self.get_content(line)}

    def _yield_lines(self, lines):

        last_tag = None

        try:

            record = self._iter_till_start(lines)

            while True:

                tag, content = self._parse_tag(next(lines))

                if tag == "  ":
                    self._add_tag(record, last_tag, content, extend_multiline=True)
                    continue

                if tag in self.ignore:
                    continue

                if tag == self.END_TAG:

                    yield record

                    # iterate lines to get the next start tag
                    record = self._iter_till_start(lines)

                    continue

                self._add_tag(record, tag, content)
                last_tag = tag

        except StopIteration:
            pass

    def _add_single_value(self, record, name, value, is_multi=False):
        """Process a single line.

        This method is only run on tags where repeated tags are not expected.
        The output for a tag can be a list when a delimiter is specified,
        even if it is not a list tag.
        """
        if not is_multi:
            if self.enforce_list_tags or name not in record:
                ignore_this_if_has_one = value
                record.setdefault(name, ignore_this_if_has_one)
            else:
                self._add_list_value(record, name, value)
        else:
            value_must_exist_or_is_bug = record[name]
            if isinstance(value, list):
                record[name].extend(value)
            else:
                record[name] = " ".join((value_must_exist_or_is_bug, value))

    def _add_list_value(self, record, name, value):
        """Process tags with multiple values."""
        value_list = value if isinstance(value, list) else [value]
        try:
            record[name].extend(value_list)
        except KeyError:
            record[name] = value_list
        except AttributeError:
            if not isinstance(record[name], str):
                raise
            must_exist = record[name]
            record[name] = [must_exist, *value_list]

    def _add_tag(self, record, tag, content, extend_multiline=False):

        try:
            name = self.mapping[tag]
        except KeyError:
            if self.skip_unknown_tags:
                return

            # handle unknown tag
            name = self.mapping[self.UNKNOWN_TAG]
            if name not in record:
                record[name] = defaultdict(list)
            record[name][tag].append(content)

        else:

            if delimiter := self.delimiter_map.get(tag):
                content = [i.strip() for i in content.split(delimiter)]

            if tag in self.list_tags:
                self._add_list_value(record, name, content)
            else:
                self._add_single_value(record, name, content, is_multi=extend_multiline)

    def clean_text(self, text: str) -> str:
        """Clean each line."""
        return text

    def get_tag(self, line: str) -> str:
        """Get the tag from a line in the RIS file."""
        return line[0:2]

    @abstractmethod
    def get_content(self, line: str) -> str:
        """Get the content (non-tag part) of a line."""

    def get_content(self, line):
        return line[6:].strip()


class WokParser(BaseParser):
    """Subclass of Base for reading Wok RIS files."""

    START_TAG = "PT"
    PATTERN = r"^[A-Z][A-Z0-9] |^ER\s?|^EF\s?"
    DEFAULT_IGNORE: ClassVar[List[str]] = ["FN", "VR", "EF"]
    DEFAULT_MAPPING = WOK_TAG_KEY_MAPPING
    DEFAULT_LIST_TAGS = WOK_LIST_TYPE_TAGS
    DEFAULT_DELIMITER_MAPPING: ClassVar[Dict] = {}

    def get_content(self, line):
        return line[2:].strip()


class RisParser(BaseParser):
    """Subclass of Base for reading base RIS files."""

    START_TAG = "TY"
    PATTERN = r"^[A-Z][A-Z0-9]  - |^ER  -\s*$"
    DEFAULT_MAPPING = TAG_KEY_MAPPING
    DEFAULT_LIST_TAGS = LIST_TYPE_TAGS
    DEFAULT_DELIMITER_MAPPING = DELIMITED_TAG_MAPPING

    counter_re = re.compile("^[0-9]+.")


def load(
    file: Union[TextIO, Path],
    *,
    encoding: Optional[str] = None,
    newline: Optional[str] = None,
    implementation: Optional[BaseParser] = None,
    **kw,
) -> List[Dict]:
    """Load a RIS file and return a list of entries.

    Entries are codified as dictionaries whose keys are the
    different tags. For single line and singly occurring tags,
    the content is codified as a string. In the case of multiline
    or multiple key occurrences, the content is returned as a list
    of strings.

    Args:
        file (Union[TextIO, Path]): File handle to read ris formatted data.
        encoding(str, optional): File encoding, only used when a Path is supplied.
                                 Consistent with the python standard library,
                                 if `None` is supplied, the default system
                                 encoding is used.
        newline(str, optional): File line separator.
        implementation (RisImplementation): RIS implementation; base by
                                            default.

    Returns:
        list: Returns list of RIS entries.
    """
    if implementation is None:
        parser = RisParser
    else:
        parser = implementation

    if hasattr(file, "readline"):
        return parser(newline=newline, **kw).parse_lines(file)
    elif hasattr(file, "open"):
        with file.open(mode="r", newline=newline, encoding=encoding) as f:
            return parser(**kw).parse_lines(f)
    elif hasattr(file, "read"):
        return loads(file.read(), implementation=implementation, newline=newline, **kw)
    else:
        raise ValueError("File must be a file-like object or a Path object")


def loads(text: str, *, implementation: Optional[Type[BaseParser]] = None, **kw) -> List[Dict]:
    """Load a RIS file and return a list of entries.

    Entries are codified as dictionaries whose keys are the
    different tags. For single line and singly occurring tags,
    the content is codified as a string. In the case of multiline
    or multiple key occurrences, the content is returned as a list
    of strings.

    Args:
        text (str): A string version of an RIS file.
        implementation (RisImplementation): RIS implementation; base by
                                            default.

    Returns:
        list: Returns list of RIS entries.
    """
    if implementation is None:
        parser = RisParser
    else:
        parser = implementation

    return parser(**kw).parse(text)
