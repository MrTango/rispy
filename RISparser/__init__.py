__author__ = 'maik'


# Copyright (C) 2013 Angel Yanguas-Gil
# This program is free software, licensed under GPLv2 or later.
# A copy of the GPLv2 license is provided in the root directory of
# the source code.

"""Parse WOK and Refman's RIS files"""

import re
import types

from config import LIST_TYPE_KEYS, TYPE_OF_REFERENCE_MAPPING, TAG_KEY_MAPPING

woktag = "^[A-Z][A-Z0-9] |^ER$|^EF$"
ristag = "^[A-Z][A-Z0-9]  - "
riscounter = "^[0-9]+."

wokpat = re.compile(woktag)
rispat = re.compile(ristag)
riscounterpat = re.compile(riscounter)

ris_boundtags = ('TY', 'ER')
wok_boundtags = ('PT', 'ER')

wok_ignoretags = ['FN', 'VR', 'EF']
ris_ignoretags = []


def readris(bibliography_file, mapping=None, wok=False):
    """Parse a ris file and return a list of entries.

    Entries are codified as dictionaries whose keys are the
    different tags. For single line and singly ocurring tags,
    the content is codified as a string. In the case of multiline
    or multiple key ocurrences, the content is returned as a list
    of strings.

    Keyword arguments:
    bibliography_file -- ris filehandle
    mapping -- custom RIS tags mapping
    wok -- flag, Web of Knowledge format is used if True, otherwise
           Refman's RIS specifications are used.

    """
    ignored_lines = []

    if not mapping:
        mapping = TAG_KEY_MAPPING

    if wok:
        gettag = lambda line: line[0:2]
        getcontent = lambda line: line[2:].strip()
        istag = lambda line: (wokpat.match(line) is not None)
        starttag, endtag = wok_boundtags
        ignoretags = wok_ignoretags
    else:
        gettag = lambda line: line[0:2]
        getcontent = lambda line: line[6:].strip()
        istag = lambda line: (rispat.match(line) is not None)
        iscounter = lambda line: (riscounterpat.match(line) is not None)
        starttag, endtag = ris_boundtags
        ignoretags = ris_ignoretags

    filelines = bibliography_file.readlines()
    # Corrects for BOM in utf-8 encodings while keeping an 8-bit
    # string representation
    st = filelines[0]
    if (st[0], st[1], st[2]) == ('\xef', '\xbb', '\xbf'):
        filelines[0] = st[3:]

    inref = False
    tag = None
    current = {}
    ln = 0

    for line in filelines:
        ln += 1
        if istag(line):
            tag = gettag(line)
            if tag in ignoretags:
                continue
            elif tag == endtag:
                # Close the active entry and yield it
                yield current
                current = {}
                inref = False
            elif tag == starttag:
                # New entry
                if inref:
                    text = "Missing end of record tag in line %d:\n %s" % (
                        ln, line)
                    raise IOError(text)
                current[mapping[tag]] = getcontent(line)
                inref = True
            else:
                if not inref:
                    text = "Invalid start tag in line %d:\n %s" % (ln, line)
                    raise IOError(text)
                if tag in LIST_TYPE_KEYS:
                    if mapping[tag] not in current:
                        current[mapping[tag]] = []
                    current[mapping[tag]].append(getcontent(line))
                elif mapping[tag] not in current:
                    current[mapping[tag]] = getcontent(line)
                else:
                    ignored_lines.append(line)

        else:
            if not line.strip():
                continue
            if inref:
                # Active reference
                if tag is None:
                    text = "Expected tag in line %d:\n %s" % (ln, line)
                    raise IOError(text)
                else:
                    # Active tag
                    if hasattr(current[mapping[tag]], '__iter__'):
                        current[mapping[tag]].append(line.strip())
                    else:
                        current[mapping[tag]] = [
                            current[mapping[tag]], line.strip()]
            else:
                if iscounter(line):
                    continue
                text = "Expected start tag in line %d:\n %s" % (ln, line)
                raise IOError(text)
