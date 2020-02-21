"""RIS Writer"""

import logging

from .config import LIST_TYPE_TAGS
from .config import TAG_KEY_MAPPING

__all__ = ["dump", "dumps"]


def _inverse_mapping(mapping):
    remap = {v: k for k, v in mapping.items()}
    if len(remap) != len(mapping):
        raise ValueError("Mapping cannot be inverted; some values were not unique")
    return remap


class BaseWriter(object):
    START_TAG = None
    END_TAG = "ER"
    IGNORE = []
    PATTERN = None

    def __init__(self, references, mapping, type_of_reference):
        self.references = references
        self.mapping = mapping
        self._rev_mapping = _inverse_mapping(mapping)
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
                logging.warning("label {} not exported".format(label))
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


def dump(references, file, mapping=None):
    """Dump a ris lines to file.

    Entries are codified as dictionaries whose keys are the
    different tags. For single line and singly occurring tags,
    the content is codified as a string. In the case of multiline
    or multiple key occurrences, the content is returned as a list
    of strings.

    Args:
        references (list): List of references.
        file (object): File handle to store ris formatted data.
        mapping (dict): Custom RIS tags mapping.

    """
    if not mapping:
        mapping = TAG_KEY_MAPPING

    for line in RISWriter(references, mapping, type_of_reference="JOUR").format():
        file.write(line + "\n")


def dumps(references, mapping=None):

    if not mapping:
        mapping = TAG_KEY_MAPPING

    lines = RISWriter(references, mapping, type_of_reference="JOUR").format()
    return "\n".join(lines) + "\n"
