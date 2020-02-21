from collections import defaultdict
import re

from .config import LIST_TYPE_TAGS, TAG_KEY_MAPPING, WOK_TAG_KEY_MAPPING, WOK_LIST_TYPE_TAGS


__all__ = ["load", "loads"]


class NextLine(Exception):
    pass


class Base(object):
    START_TAG = None
    END_TAG = "ER"
    IGNORE = []
    PATTERN = None

    def __init__(self, lines, mapping):
        self.lines = lines
        self.pattern = re.compile(self.PATTERN)
        self._mapping = mapping

    @property
    def mapping(self):
        if self._mapping is not None:
            return self._mapping
        else:
            return self.default_mapping

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
                    "Missing end of record tag in line " "%d:\n %s" % (line_number, line)
                )
            self.add_tag(tag, line)
            self.in_ref = True
            raise NextLine

        if not self.in_ref:
            text = "Invalid start tag in line %d:\n %s" % (line_number, line)
            raise IOError(text)

        if tag in self.mapping:
            self.add_tag(tag, line)
            raise NextLine
        else:
            self.add_unknown_tag(tag, line)
            raise NextLine

        raise NextLine

    def parse_other(self, line, line_number):
        if self.in_ref:
            # Active reference
            if self.last_tag is None:
                text = "Expected tag in line %d:\n %s" % (line_number, line)
                raise IOError(text)
            # Active tag
            self.add_tag(self.last_tag, line, all_line=True)
            raise NextLine

        if self.is_counter(line):
            raise NextLine
        text = "Expected start tag in line %d:\n %s" % (line_number, line)
        raise IOError(text)

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

        if tag not in LIST_TYPE_TAGS:
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
    LIST_TYPE_TAGS = WOK_LIST_TYPE_TAGS
    default_mapping = WOK_TAG_KEY_MAPPING

    def get_content(self, line):
        return line[2:].strip()

    def is_counter(self, line):
        return True


class Ris(Base):
    START_TAG = "TY"
    PATTERN = "^[A-Z][A-Z0-9]  - "
    default_mapping = TAG_KEY_MAPPING

    counter_re = re.compile("^[0-9]+.")

    def get_content(self, line):
        return line[6:].strip()

    def is_counter(self, line):
        none_or_match = self.counter_re.match(line)
        return bool(none_or_match)


def load(file, mapping=None, wok=False):
    """Load a RIS file and return a list of entries.

    Entries are codified as dictionaries whose keys are the
    different tags. For single line and singly occurring tags,
    the content is codified as a string. In the case of multiline
    or multiple key occurrences, the content is returned as a list
    of strings.

    Args:
        file (object): File handle to read ris formatted data.
        mapping (dict): Custom RIS tags mapping.
        wok (bool): Use WOK format. Default False.

    Returns:
        list: Returns list of RIS entries.
    """
    c = file.read()
    # Corrects for BOM in utf-8 encodings while keeping an 8-bit
    # string representation
    if (c[0], c[1], c[2]) == ("\xef", "\xbb", "\xbf"):
        c = c[3:]

    return loads(c, mapping, wok)


def loads(obj, mapping=None, wok=False):

    filelines = obj.split("\n")

    if wok:
        return Wok(filelines, mapping).parse()

    return Ris(filelines, mapping).parse()
