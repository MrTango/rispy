"""RIS Parser."""

from collections import defaultdict
from pathlib import Path
from typing import ClassVar, Optional, TextIO, Union

from .config import (
    DELIMITED_TAG_MAPPING,
    LIST_TYPE_TAGS,
    PUBMED_LIST_TYPE_TAGS,
    PUBMED_TAG_KEY_MAPPING,
    TAG_KEY_MAPPING,
    WOK_LIST_TYPE_TAGS,
    WOK_TAG_KEY_MAPPING,
)

__all__ = ["RisParser", "WokParser", "load", "loads"]


class NextLine(Exception):
    pass


class ParseError(Exception):
    pass


class RisParser:
    """RIS parser class

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

    """

    START_TAG: str = "TY"
    END_TAG: str = "ER"
    PATTERN: str
    DEFAULT_IGNORE: ClassVar[list[str]] = []
    DEFAULT_MAPPING: dict = TAG_KEY_MAPPING
    DEFAULT_LIST_TAGS: list[str] = LIST_TYPE_TAGS
    DEFAULT_DELIMITER_MAPPING: dict = DELIMITED_TAG_MAPPING
    DEFAULT_NEWLINE: ClassVar[str] = "\n"

    def __init__(
        self,
        *,
        mapping: Optional[dict] = None,
        list_tags: Optional[list[str]] = None,
        delimiter_tags_mapping: Optional[dict] = None,
        ignore: Optional[list[str]] = None,
        skip_unknown_tags: bool = False,
        enforce_list_tags: bool = True,
        newline: Optional[str] = None,
        undo_wrapping: bool = False,
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
        self.undo_wrapping = undo_wrapping

    def _iter_till_start(self, lines) -> dict:
        while True:
            line = next(lines)
            if line.startswith(self.START_TAG):
                return {self.mapping[self.START_TAG]: self.parse_line(line)[1]}

    def parse(self, text: str) -> list[dict]:
        """Parse RIS string."""
        line_gen = (line for line in text.split(self.newline))
        return self.parse_lines(line_gen)

    def parse_lines(self, lines: Union[TextIO, list[str]]) -> list[dict]:
        """Parse RIS file line by line."""

        result = []
        last_tag = None

        try:
            record = self._iter_till_start(lines)

            while True:
                tag, content = self.parse_line(next(lines))

                if tag in self.ignore:
                    continue

                if self.END_TAG and tag == self.END_TAG:
                    result.append(record)
                    last_tag = tag
                    record = self._iter_till_start(lines)
                    continue

                if self.END_TAG is None and tag == self.START_TAG:
                    result.append(record)
                    record = {self.mapping[self.START_TAG]: content}
                    last_tag = tag
                    continue

                if tag is None and not self.undo_wrapping and last_tag in self.list_tags:
                    self._add_tag(record, last_tag, content)
                elif tag is None:
                    self._extend_tag(record, last_tag, content)
                else:
                    self._add_tag(record, tag, content)
                    last_tag = tag

        except StopIteration:
            pass

        if self.END_TAG is not None and last_tag != self.END_TAG:
            raise ParseError(f"Missing end tag: {self.END_TAG}")

        if self.END_TAG is None:
            result.append(record)

        return result

    def parse_line(self, line: str) -> Union[tuple[str, str], tuple[None, str]]:
        """Parse line of RIS file.

        This method parses a line between the start and end tag.
        It returns the tag and the content of the line. Typically,
        the first 2 characters are the tag, followed by a seperator,
        and the rest of the line is the content.

        Custom parsers can override this method to change the way
        lines are parsed. For example, a very basic RIS parser would
        return the first 2 characters as the tag and the rest of the
        line as the content of the tag. `(line[0:2], line[6:].strip())`

        Parameters
        ----------
        line : str
            Line of RIS file between start and end tag.

        Returns
        -------
        tuple
            Tuple containing the tag and the content of the tag.
        """
        if line[2:5] == "  -" and line[:2].isupper() and line[0:1].isalpha():
            return (line[0:2], line[6:].strip())
        else:
            return (None, line.strip())

    def _add_single_value(
        self, record: dict, name: str, value: Union[str, list[str]], is_multi: bool = False
    ) -> None:
        """Process a single line.

        This method is only run on tags where repeated tags are not expected.
        The output for a tag can be a list when a delimiter is specified,
        even if it is not a list tag.
        """
        if self.enforce_list_tags or name not in record:
            ignore_this_if_has_one = value
            record.setdefault(name, ignore_this_if_has_one)
        else:
            self._add_list_value(record, name, value)

    def _add_list_value(self, record: dict, name: str, value: Union[str, list[str]]) -> None:
        """Process tags with multiple values."""
        value_list = value if isinstance(value, list) else [value]
        try:
            record[name].extend(value_list)
        except KeyError:
            record[name] = value_list
        except AttributeError:
            must_exist = record[name]
            record[name] = [must_exist, *value_list]

    def _extend_tag(self, record: dict, tag: str, content: Union[str, list[str]]) -> None:
        """Extend tags with multiline values."""

        sep = " " if self.undo_wrapping else "\n"

        name = self.mapping[tag]
        if isinstance(record[name], list):
            record[name][-1] = sep.join((record[name][-1], content))
        else:
            record[name] = sep.join((record[name], content))

    def _add_tag(self, record: dict, tag: str, content: str) -> None:
        try:
            name = self.mapping[tag]
        except KeyError:
            if self.skip_unknown_tags:
                return

            record.setdefault("unknown_tag", defaultdict(list))[tag].append(content)
            return
        else:
            if delimiter := self.delimiter_map.get(tag):
                content = [i.strip() for i in content.split(delimiter)]

            if tag in self.list_tags:
                self._add_list_value(record, name, content)
            else:
                self._add_single_value(record, name, content)


class WokParser(RisParser):
    """Subclass of Base for reading Wok RIS files."""

    START_TAG = "PT"
    DEFAULT_IGNORE: ClassVar[list[str]] = ["FN", "VR", "EF"]
    DEFAULT_MAPPING = WOK_TAG_KEY_MAPPING
    DEFAULT_LIST_TAGS = WOK_LIST_TYPE_TAGS
    DEFAULT_DELIMITER_MAPPING: ClassVar[dict] = {}

    def __init__(self, undo_wrapping: bool = True, **kw):
        super().__init__(undo_wrapping=undo_wrapping, **kw)

    def parse_line(self, line: str) -> Union[tuple[str, str], tuple[None, str]]:
        """Parse line of RIS file.

        This method parses a line between the start and end tag.
        It returns the tag and the content of the line. Typically,
        the first 2 characters are the tag, and the rest of the line
        is the content.

        Parameters
        ----------
        line : str
            Line of RIS file between start and end tag.

        Returns
        -------
        tuple
            Tuple containing the tag and the content of the tag.
        """
        if line[0:2] == "  ":
            return (None, line[3:].strip())
        else:
            return (line[0:2], line[3:].strip())


class PubMedParser(RisParser):
    """Subclass of Base for reading PubMed RIS files."""

    START_TAG: str = "PMID"
    END_TAG: None = None
    DEFAULT_MAPPING: dict = PUBMED_TAG_KEY_MAPPING
    DEFAULT_LIST_TAGS: list[str] = PUBMED_LIST_TYPE_TAGS
    DEFAULT_DELIMITER_MAPPING: ClassVar[dict] = {}

    def __init__(self, undo_wrapping: bool = True, **kw):
        super().__init__(undo_wrapping=undo_wrapping, **kw)

    def parse_line(self, line: str) -> Union[tuple[str, str], tuple[None, str]]:
        """Parse line of PubMed file.

        Parameters
        ----------
        line : str
            Line of RIS file between start and end tag.

        Returns
        -------
        tuple
            Tuple containing the tag and the content of the tag.
        """

        if line[4:5] == "-":
            return (line[0:4].rstrip(), line[6:].rstrip())
        else:
            return (None, line[6:].rstrip())


def load(
    file: Union[TextIO, Path],
    *,
    encoding: Optional[str] = None,
    newline: Optional[str] = None,
    implementation: type[RisParser] = RisParser,
    **kw,
) -> list[dict]:
    """Load a RIS file and return a list of entries.

    Entries are codified as dictionaries whose keys are the
    different tags. For single line and singly occurring tags,
    the content is codified as a string. In the case of multiline
    or multiple key occurrences, the content is returned as a list
    of strings.

    Args:
        file (Union[TextIO, Path]): File handle of RIS data.
        encoding(str, optional): File encoding, only used when a Path is supplied.
                                 Consistent with the python standard library,
                                 if `None` is supplied, the default system
                                 encoding is used.
        newline(str, optional): File line separator.
        implementation (RisParser): RIS implementation; RisParser by default.

    Returns:
        list: Returns list of RIS entries.
    """
    if isinstance(file, Path):
        with file.open(mode="r", newline=newline, encoding=encoding) as f:
            return implementation(**kw).parse_lines(f)
    if hasattr(file, "readline"):
        return implementation(newline=newline, **kw).parse_lines(file)
    elif hasattr(file, "read"):
        return loads(file.read(), implementation=implementation, newline=newline, **kw)
    raise ValueError("File must be a file-like object or a Path object")


def loads(text: str, *, implementation: type[RisParser] = RisParser, **kw) -> list[dict]:
    """Load a RIS file and return a list of entries.

    Entries are codified as dictionaries whose keys are the
    different tags. For single line and singly occurring tags,
    the content is codified as a string. In the case of multiline
    or multiple key occurrences, the content is returned as a list
    of strings.

    Args:
        text (str): A string version of RIS data
        implementation (RisParser): RIS implementation; RisParser by default.

    Returns:
        list: Returns list of RIS entries.
    """
    return implementation(**kw).parse(text)
