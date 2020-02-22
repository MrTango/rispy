"""RIS Writer"""

import logging
from typing import Dict, List, Optional, TextIO

from .config import LIST_TYPE_TAGS
from .config import TAG_KEY_MAPPING

__all__ = ["dump", "dumps"]


def invert_dictionary(mapping):
    remap = {v: k for k, v in mapping.items()}
    if len(remap) != len(mapping):
        raise ValueError("Dictionary cannot be inverted; some values were not unique")
    return remap


class BaseWriter:
    START_TAG: str = None
    END_TAG: str = "ER"
    IGNORE: List[str] = []
    PATTERN: str = None

    def __init__(self, references, mapping, type_of_reference):
        self.references = references
        self.mapping = mapping
        self._rev_mapping = invert_dictionary(mapping)
        self.type_of_reference = type_of_reference

    def _get_reference_type(self, ref):

        if "type_of_reference" in ref.keys():
            # TODO add check
            return ref["type_of_reference"]

        if self.type_of_reference is not None:
            return self.type_of_reference
        else:
            raise ValueError("Unknown type of reference")

    def _format_line(self, tag, value=""):
        """Format a RIS line."""
        return self.PATTERN.format(tag=tag, value=value)

    def _format_reference(self, ref, count):

        lines = []

        lines.append("{i}.".format(i=count))
        lines.append(self._format_line(self.START_TAG, self._get_reference_type(ref)))

        for label, value in ref.items():

            # not available
            try:
                tag = self._rev_mapping[label.lower()]
            except KeyError:
                logging.warning(f"label {label} not exported")
                continue

            # ignore
            if tag in [self.START_TAG] + self.IGNORE:
                continue

            # list tag
            if tag in LIST_TYPE_TAGS:
                for val_i in value:
                    lines.append(self._format_line(tag, val_i))
            else:
                lines.append(self._format_line(tag, value))

        lines.append(self._format_line("ER"))
        lines.append("")
        lines.append("")

        return lines

    def format(self):

        for i, ref in enumerate(self.references):
            lines_ref = self._format_reference(ref, count=i + 1)
            for line in lines_ref:
                yield line


class RISWriter(BaseWriter):

    START_TAG = "TY"
    PATTERN = "{tag}  - {value}"


def dump(references: List[Dict], file: TextIO, mapping: Optional[Dict] = None):
    """
    Write an RIS file to file or file-like object.

    Entries are codified as dictionaries whose keys are the
    different tags. For single line and singly occurring tags,
    the content is codified as a string. In the case of multiline
    or multiple key occurrences, the content is returned as a list
    of strings.

    Args:
        references (List[Dict]): List of references.
        file (TextIO): File handle to store ris formatted data.
        mapping (Dict, optional): Custom RIS tags mapping.
    """
    text = dumps(references, mapping)
    file.writelines(text)


def dumps(references: List[Dict], mapping: Optional[Dict] = None) -> str:
    """
    Return an RIS formatted string.

    Entries are codified as dictionaries whose keys are the
    different tags. For single line and singly occurring tags,
    the content is codified as a string. In the case of multiline
    or multiple key occurrences, the content is returned as a list
    of strings.

    Args:
        references (List[Dict]): List of references.
        file (TextIO): File handle to store ris formatted data.
        mapping (Dict, optional): Custom RIS tags mapping.
    """
    if not mapping:
        mapping = TAG_KEY_MAPPING

    lines = RISWriter(references, mapping, type_of_reference="JOUR").format()
    return "\n".join(lines) + "\n"
