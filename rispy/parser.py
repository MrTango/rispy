"""RIS Parser."""

from collections import defaultdict
from itertools import chain
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, TextIO, Union, Optional
import re

from .config import LIST_TYPE_TAGS, TAG_KEY_MAPPING, WOK_TAG_KEY_MAPPING, WOK_LIST_TYPE_TAGS


__all__ = ["load", "loads", "BaseParser", "WokParser", "RisParser"]


class NextLine(Exception):
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
        is_header: Returns a bool for whether a line is a header and should be
                   skipped. This method only operates on lines outside of a
                   reference. Defaults to `False` for all lines.
        get_tag: Returns the tag part of a line. Default is to return the
                 first two characters.
        is_tag: Determines whether a line has a tag, returning a bool. Uses
                regex in `PATTERN` by default.
        clean_text: Clean the text body before parsing begins. By default,
                    it removes UTF-BOM characters.

    """

    START_TAG: str
    END_TAG: str = "ER"
    PATTERN: str
    DEFAULT_IGNORE: List[str] = []
    DEFAULT_MAPPING: Dict
    DEFAULT_LIST_TAGS: List[str]

    def __init__(
        self,
        *,
        mapping: Optional[Dict] = None,
        list_tags: Optional[List[str]] = None,
        ignore: Optional[List[str]] = None,
        skip_missing_tags: bool = False,
        skip_unknown_tags: bool = False,
        enforce_list_tags: bool = True,
    ):
        """Initialize the parser function.

        Args:
            mapping (dict, optional): Map tags to tag names.
            list_tags (list, optional): List of list-type tags.
            ignore (list, optional): List of tags to ignore.
            skip_missing_tags (bool, optional): Bool to skip lines that don't have
                                                valid tags, regardless of whether
                                                of where they are in a reference.
                                                This is the inverse of the former
                                                `strict` parameter. If the goal is
                                                to skip reference headers, see the
                                                `is_header` method. Defaults to
                                                `False`.
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

        """
        self.pattern = re.compile(self.PATTERN)
        self.mapping = mapping if mapping is not None else self.DEFAULT_MAPPING
        self.list_tags = list_tags if list_tags is not None else self.DEFAULT_LIST_TAGS
        self.ignore = ignore if ignore is not None else self.DEFAULT_IGNORE
        self.skip_missing_tags = skip_missing_tags
        self.skip_unknown_tags = skip_unknown_tags
        self.enforce_list_tags = enforce_list_tags

    def parse(self, text: str) -> List[Dict]:
        """Parse RIS string."""
        clean_body = self.clean_text(text)
        lines = clean_body.split("\n")
        return list(self._parse_lines(lines))

    def _parse_lines(self, lines):
        self.in_ref = False
        self.current = {}
        self.last_tag = None

        for line_number, line in enumerate(lines):
            if not line.strip():
                continue

            if self.is_tag(line):
                try:
                    yield self._parse_tag(line, line_number)
                    self.current = {}
                    self.in_ref = False
                    self.last_tag = None
                except NextLine:
                    continue
            else:
                try:
                    yield self._parse_other(line, line_number)
                except NextLine:
                    continue

    def _parse_tag(self, line, line_number):
        tag = self.get_tag(line)
        if tag in self.ignore:
            raise NextLine

        if tag == self.END_TAG:
            self._finalize_record(self.current)
            return self.current

        if tag == self.START_TAG:
            # New entry
            if self.in_ref:
                raise IOError(f"Missing end of record tag in line {line_number}:\n {line}")
            self._add_tag(tag, line)
            self.in_ref = True
            raise NextLine

        if not self.in_ref:
            raise IOError(f"Invalid start tag in line {line_number}:\n {line}")

        if tag in self.mapping:
            self._add_tag(tag, line)
            raise NextLine
        elif not self.skip_unknown_tags:
            self._add_unknown_tag(tag, line)
            raise NextLine

        raise NextLine

    def _parse_other(self, line, line_number):
        if self.skip_missing_tags:
            raise NextLine
        if self.in_ref:
            # Active reference
            if self.last_tag is None:
                raise IOError(f"Expected tag in line {line_number}:\n {line}")
            # Active tag
            self._add_tag(self.last_tag, line, all_line=True)
            raise NextLine

        if self.is_header(line):
            raise NextLine
        raise IOError(f"Expected start tag in line {line_number}:\n {line}")

    def _add_single_value(self, name, value, is_multi=False):
        if not is_multi:
            if self.enforce_list_tags or name not in self.current:
                ignore_this_if_has_one = value
                self.current.setdefault(name, ignore_this_if_has_one)
            else:
                self._add_list_value(name, value)
            return

        value_must_exist_or_is_bug = self.current[name]
        self.current[name] = " ".join((value_must_exist_or_is_bug, value))

    def _add_list_value(self, name, value):
        try:
            self.current[name].append(value)
        except KeyError:
            self.current[name] = [value]
        except AttributeError:
            if not isinstance(self.current[name], str):
                raise
            must_exist = self.current[name]
            self.current[name] = [must_exist] + [value]

    def _add_tag(self, tag, line, all_line=False):
        self.last_tag = tag
        name = self.mapping[tag]
        if all_line:
            new_value = line.strip()
        else:
            new_value = self.get_content(line)

        if tag not in self.list_tags:
            self._add_single_value(name, new_value, is_multi=all_line)
            return

        self._add_list_value(name, new_value)

    def _add_unknown_tag(self, tag, line):
        name = self.mapping["UK"]
        value = self.get_content(line)
        # check if unknown_tag dict exists
        if name not in self.current:
            self.current[name] = defaultdict(list)

        self.current[name][tag].append(value)

    def _finalize_record(self, record: dict):
        """Make final updates to record inplace prior to completion."""

        # split/strip multiple URLs on a single line; consistent with the the UR
        # specification: "multiple addresses can be entered on one line using a
        # semi-colon as a separator"
        if "urls" in record:
            record["urls"] = [
                url.strip() for url in chain(*[url.split(";") for url in record["urls"]])
            ]

    def clean_text(self, text: str) -> str:
        """Clean string before parsing."""
        # remove BOM if present
        text = text.lstrip("\ufeff")
        return text

    def get_tag(self, line: str) -> str:
        """Get the tag from a line in the RIS file."""
        return line[0:2]

    def is_tag(self, line: str) -> bool:
        """Determine if the line has a tag using regex."""
        return bool(self.pattern.match(line))

    @abstractmethod
    def get_content(self, line: str) -> str:
        """Get the content (non-tag part) of a line."""
        raise NotImplementedError

    def is_header(self, line: str) -> bool:
        """Determine whether a line is a header and should be skipped.

        Only operates on lines outside of the reference.
        """
        return False


class WokParser(BaseParser):
    """Subclass of Base for reading Wok RIS files."""

    START_TAG = "PT"
    PATTERN = r"^[A-Z][A-Z0-9] |^ER\s?|^EF\s?"
    DEFAULT_IGNORE = ["FN", "VR", "EF"]
    DEFAULT_MAPPING = WOK_TAG_KEY_MAPPING
    DEFAULT_LIST_TAGS = WOK_LIST_TYPE_TAGS

    def get_content(self, line):
        return line[2:].strip()

    def is_header(self, line):
        return True


class RisParser(BaseParser):
    """Subclass of Base for reading base RIS files."""

    START_TAG = "TY"
    PATTERN = r"^[A-Z][A-Z0-9]  - |^ER  -\s*$"
    DEFAULT_MAPPING = TAG_KEY_MAPPING
    DEFAULT_LIST_TAGS = LIST_TYPE_TAGS

    counter_re = re.compile("^[0-9]+.")

    def get_content(self, line):
        return line[6:].strip()

    def is_header(self, line):
        none_or_match = self.counter_re.match(line)
        return bool(none_or_match)


def load(
    file: Union[TextIO, Path],
    *,
    encoding: Optional[str] = None,
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
        implementation (RisImplementation): RIS implementation; base by
                                            default.

    Returns:
        list: Returns list of RIS entries.
    """
    text = file.read_text(encoding=encoding) if isinstance(file, Path) else file.read()
    return loads(text, implementation=implementation, **kw)


def loads(text: str, *, implementation: Optional[BaseParser] = None, **kw) -> List[Dict]:
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
