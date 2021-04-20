"""RIS Parser."""

from enum import Enum
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, TextIO, Union
import re

from .config import (LIST_TYPE_TAGS, TAG_KEY_MAPPING,
                     WOK_TAG_KEY_MAPPING, WOK_LIST_TYPE_TAGS)


__all__ = ["load", "loads"]


class RisImplementation(Enum):
    BASE = "base"
    WOK = "wok"


class NextLine(Exception):
    pass


class Base:
    START_TAG: str = None
    END_TAG: str = "ER"
    IGNORE: List[str] = []
    PATTERN: str = None

    def __init__(self, lines, mapping, list_tags, strict=True):
        self.lines = lines
        self.pattern = re.compile(self.PATTERN)
        self._mapping = mapping
        self._list_tags = list_tags
        self.strict = strict

    @property
    def mapping(self):
        if self._mapping is not None:
            return self._mapping
        else:
            return self.default_mapping

    @property
    def list_tags(self):
        if self._list_tags is not None:
            return self._list_tags
        else:
            return self.default_list_tags

    def parse(self):
        self.in_ref = False
        self.current = {}
        self.last_tag = None

        for line_number, line in enumerate(self.lines):
            if not line.strip():
                continue

            if self.is_tag(line):
                try:
                    yield self.parse_tag(line, line_number)
                    self.current = {}
                    self.in_ref = False
                    self.last_tag = None
                except NextLine:
                    continue
            else:
                try:
                    yield self.parse_other(line, line_number)
                except NextLine:
                    continue

    def parse_tag(self, line, line_number):
        tag = self.get_tag(line)
        if tag in self.IGNORE:
            raise NextLine

        if tag == self.END_TAG:
            return self.current

        if tag == self.START_TAG:
            # New entry
            if self.in_ref:
                raise IOError(
                    "Missing end of record tag in line "
                    f"{line_number}:\n {line}"
                    )
            self.add_tag(tag, line)
            self.in_ref = True
            raise NextLine

        if not self.in_ref:
            raise IOError(f"Invalid start tag in line {line_number}:\n {line}")

        if tag in self.mapping:
            self.add_tag(tag, line)
            raise NextLine
        else:
            self.add_unknown_tag(tag, line)
            raise NextLine

        raise NextLine

    def parse_other(self, line, line_number):
        if not self.strict:
            raise NextLine
        if self.in_ref:
            # Active reference
            if self.last_tag is None:
                raise IOError(f"Expected tag in line {line_number}:\n {line}")
            # Active tag
            self.add_tag(self.last_tag, line, all_line=True)
            raise NextLine

        if self.is_counter(line):
            raise NextLine
        raise IOError(f"Expected start tag in line {line_number}:\n {line}")

    def add_single_value(self, name, value, is_multi=False):
        if not is_multi:
            ignore_this_if_has_one = value
            self.current.setdefault(name, ignore_this_if_has_one)
            return

        value_must_exist_or_is_bug = self.current[name]
        self.current[name] = " ".join((value_must_exist_or_is_bug, value))

    def add_list_value(self, name, value):
        try:
            self.current[name].append(value)
        except KeyError:
            self.current[name] = [value]

    def add_tag(self, tag, line, all_line=False):
        self.last_tag = tag
        name = self.mapping[tag]
        if all_line:
            new_value = line.strip()
        else:
            new_value = self.get_content(line)

        if tag not in self.list_tags:
            self.add_single_value(name, new_value, is_multi=all_line)
            return

        self.add_list_value(name, new_value)

    def add_unknown_tag(self, tag, line):
        name = self.mapping["UK"]
        tag = self.get_tag(line)
        value = self.get_content(line)
        # check if unknown_tag dict exists
        if name not in self.current:
            self.current[name] = defaultdict(list)

        self.current[name][tag].append(value)

    def get_tag(self, line):
        return line[0:2]

    def is_tag(self, line):
        return bool(self.pattern.match(line))

    def get_content(self, line):
        raise NotImplementedError


class Wok(Base):
    START_TAG = "PT"
    IGNORE = ["FN", "VR", "EF"]
    PATTERN = r"^[A-Z][A-Z0-9] |^ER\s?|^EF\s?"
    default_mapping = WOK_TAG_KEY_MAPPING
    default_list_tags = WOK_LIST_TYPE_TAGS

    def get_content(self, line):
        return line[2:].strip()

    def is_counter(self, line):
        return True


class Ris(Base):
    START_TAG = "TY"
    PATTERN = r"^[A-Z][A-Z0-9]  - |^ER  -\s*$"
    default_mapping = TAG_KEY_MAPPING
    default_list_tags = LIST_TYPE_TAGS

    counter_re = re.compile("^[0-9]+.")

    def get_content(self, line):
        return line[6:].strip()

    def is_counter(self, line):
        none_or_match = self.counter_re.match(line)
        return bool(none_or_match)


def load(
    file: Union[TextIO, Path],
    mapping: Optional[Dict] = None,
    list_tags: Optional[List] = None,
    implementation: RisImplementation = RisImplementation.BASE,
    strict: bool = True,
) -> List[Dict]:
    """Load a RIS file and return a list of entries.

    Entries are codified as dictionaries whose keys are the
    different tags. For single line and singly occurring tags,
    the content is codified as a string. In the case of multiline
    or multiple key occurrences, the content is returned as a list
    of strings.

    Args:
        file (Union[TextIO, Path]): File handle to read ris formatted data.
        mapping (Dict, optional): a tag mapping dictionary.
        list_tags (List, optional): Custom list tags.
        implementation (RisImplementation): RIS implementation; base by
                                            default.
        strict (bool): Boolean to allow non-tag data between records to
                       be ignored.

    Returns:
        list: Returns list of RIS entries.
    """
    text = file.read_text() if isinstance(file, Path) else file.read()
    return list(loads(text, mapping, list_tags, implementation, strict))


def loads(
    obj: str,
    mapping: Optional[Dict] = None,
    list_tags: Optional[List] = None,
    implementation: RisImplementation = RisImplementation.BASE,
    strict: bool = True,
) -> List[Dict]:
    """Load a RIS file and return a list of entries.

    Entries are codified as dictionaries whose keys are the
    different tags. For single line and singly occurring tags,
    the content is codified as a string. In the case of multiline
    or multiple key occurrences, the content is returned as a list
    of strings.

    Args:
        obj (str): A string version of an RIS file.
        mapping (Dict, optional): a tag mapping dictionary.
        list_tags (List, optional): Custom list tags.
        implementation (RisImplementation): RIS implementation; base by
                                            default.
        strict (bool): Boolean to allow non-tag data between records to
                       be ignored.

    Returns:
        list: Returns list of RIS entries.
    """
    # remove BOM if present
    obj = obj.lstrip("\ufeff")

    filelines = obj.split("\n")

    implementation = RisImplementation(implementation)

    if implementation == RisImplementation.WOK:
        return Wok(filelines, mapping, list_tags).parse()
    elif implementation == RisImplementation.BASE:
        return list(Ris(filelines, mapping, list_tags, strict).parse())
    else:
        raise ValueError(f"Unknown implementation: {implementation}")
