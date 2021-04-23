"""RIS Parser."""

from enum import Enum
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, TextIO, Union, Optional
import re

from .config import LIST_TYPE_TAGS, TAG_KEY_MAPPING, WOK_TAG_KEY_MAPPING, WOK_LIST_TYPE_TAGS


__all__ = ["load", "loads", "RisImplementation", "Base", "Wok", "Ris"]


class RisImplementation(str, Enum):
    """List default RIS parser implementations."""

    BASE = "base"
    WOK = "wok"


class NextLine(Exception):
    pass


class Base:
    """Base parser class. Create a subclass to use."""

    START_TAG: Optional[str] = None
    END_TAG: str = "ER"
    IGNORE: List[str] = []
    PATTERN: str = ""
    SKIP_MISSING_TAGS: bool = False
    SKIP_UNKNOWN_TAGS: bool = False
    ENFORCE_LIST_TAGS: bool = True
    DEFAULT_MAPPING: Optional[Dict] = None
    DEFAULT_LIST_TAGS: Optional[List[str]] = None

    def __init__(self, mapping: Optional[Dict] = None, list_tags: Optional[List] = None):
        """Override default tag map and list tags in instance."""
        self.pattern = re.compile(self.PATTERN)
        self._mapping = mapping
        self._list_tags = list_tags

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

    def parse(self, obj: str) -> List[Dict]:
        """Parse RIS string."""
        clean_obj = self.clean(obj)
        lines = clean_obj.split("\n")
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
        if tag in self.IGNORE:
            raise NextLine

        if tag == self.END_TAG:
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
        elif not self.SKIP_UNKNOWN_TAGS:
            self._add_unknown_tag(tag, line)
            raise NextLine

        raise NextLine

    def _parse_other(self, line, line_number):
        if self.SKIP_MISSING_TAGS:
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
            if self.ENFORCE_LIST_TAGS or name not in self.current:
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
        tag = self.get_tag(line)
        value = self.get_content(line)
        # check if unknown_tag dict exists
        if name not in self.current:
            self.current[name] = defaultdict(list)

        self.current[name][tag].append(value)

    def clean(self, obj: str) -> str:
        """Clean string before parsing."""
        # remove BOM if present
        obj = obj.lstrip("\ufeff")
        return obj

    def get_tag(self, line: str) -> str:
        """Get the tag from a line in the RIS file."""
        return line[0:2]

    def is_tag(self, line: str) -> bool:
        """Determine if the line has a tag using regex."""
        return bool(self.pattern.match(line))

    def get_content(self, line: str) -> str:
        """Get the content (non-tag part) of a line."""
        raise NotImplementedError

    def is_header(self, line: str) -> bool:
        """Determine if a line outside of the reference can be skipped."""
        return False


class Wok(Base):
    """Subclass of Base for reading Wok RIS files."""

    START_TAG = "PT"
    IGNORE = ["FN", "VR", "EF"]
    PATTERN = r"^[A-Z][A-Z0-9] |^ER\s?|^EF\s?"
    DEFAULT_MAPPING = WOK_TAG_KEY_MAPPING
    DEFAULT_LIST_TAGS = WOK_LIST_TYPE_TAGS

    def get_content(self, line):
        return line[2:].strip()

    def is_header(self, line):
        return True


class Ris(Base):
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
    implementation: Union[RisImplementation, Base] = RisImplementation.BASE,
) -> List[Dict]:
    """Load a RIS file and return a list of entries.

    Entries are codified as dictionaries whose keys are the
    different tags. For single line and singly occurring tags,
    the content is codified as a string. In the case of multiline
    or multiple key occurrences, the content is returned as a list
    of strings.

    Args:
        file (Union[TextIO, Path]): File handle to read ris formatted data.
        implementation (RisImplementation): RIS implementation; base by
                                            default.

    Returns:
        list: Returns list of RIS entries.
    """
    text = file.read_text() if isinstance(file, Path) else file.read()
    return loads(text, implementation)


def loads(
    obj: str, implementation: Union[RisImplementation, Base] = RisImplementation.BASE,
) -> List[Dict]:
    """Load a RIS file and return a list of entries.

    Entries are codified as dictionaries whose keys are the
    different tags. For single line and singly occurring tags,
    the content is codified as a string. In the case of multiline
    or multiple key occurrences, the content is returned as a list
    of strings.

    Args:
        obj (str): A string version of an RIS file.
        implementation (RisImplementation): RIS implementation; base by
                                            default.

    Returns:
        list: Returns list of RIS entries.
    """
    if implementation == RisImplementation.WOK:
        parser = Wok()
    elif implementation == RisImplementation.BASE:
        parser = Ris()
    elif isinstance(implementation, str):
        raise ValueError(f"Unknown implementation: {implementation}")
    else:
        parser = implementation

    return parser.parse(obj)
