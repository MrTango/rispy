# rispy - an RIS file parser/writer for Python

[![PyPI version](https://badge.fury.io/py/rispy.svg)](https://badge.fury.io/py/rispy)

A Python reader/writer of [RIS](https://en.wikipedia.org/wiki/RIS_(file_format)) reference files.

*Pronunciation* - `rispee` - like "crispy", but without the c.

## Usage

Parsing:

```python
>>> import rispy
>>> filepath = 'tests/data/example_full.ris'
>>> with open(filepath, 'r') as bibliography_file:
...     entries = rispy.load(bibliography_file)
...     for entry in entries:
...         print(entry['id'])
...         print(entry['first_authors'])
12345
['Marx, Karl', 'Lindgren, Astrid']
12345
['Marxus, Karlus', 'Lindgren, Astrid']

```

A file path can also be used to read RIS files. If an encoding is not specified in ``load``, the default system encoding
will be used.

```python
>>> from pathlib import Path
>>> import rispy
>>> p = Path('tests', 'data', 'example_utf_chars.ris')
>>> entries = rispy.load(p, encoding='utf-8-sig')
>>> for entry in entries:
...     print(entry['authors'][0])
Dobrokhotova, Yu E.

```

Writing:

```python
>>> import rispy
>>> entries = [
... {'type_of_reference': 'JOUR',
...  'id': '42',
...  'primary_title': 'The title of the reference',
...  'first_authors': ['Marxus, Karlus', 'Lindgren, Astrid']
...  },{
... 'type_of_reference': 'JOUR',
...  'id': '43',
...  'primary_title': 'Reference 43',
...  'abstract': 'Lorem ipsum'
...  }]
>>> filepath = 'export.ris'
>>> with open(filepath, 'w') as bibliography_file:
...     rispy.dump(entries, bibliography_file)

```

## Example RIS entry

```text
   1.
   TY  - JOUR
   ID  - 12345
   T1  - Title of reference
   A1  - Marx, Karl
   A1  - Lindgren, Astrid
   A2  - Glattauer, Daniel
   Y1  - 2014//
   N2  - BACKGROUND: Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.  RESULTS: Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. CONCLUSIONS: Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium.
   KW  - Pippi
   KW  - Nordwind
   KW  - Piraten
   JF  - Lorem
   JA  - lorem
   VL  - 9
   IS  - 3
   SP  - e0815
   CY  - United States
   PB  - Fun Factory
   PB  - Fun Factory USA
   SN  - 1932-6208
   M1  - 1008150341
   L2  - http://example.com
   ER  -
```

## TAG_KEY_MAPPING

Most fields contain string values, but some like first_authors (A1) are parsed into lists. The default mapping is
created from specifications scattered around the web, but to our knowledge there is not one single source of RIS truth,
so these may need to be modified for specific export systems:

- [Wikipedia](https://en.wikipedia.org/wiki/RIS_(file_format))
- [ResearcherId](https://web.archive.org/web/20170707033254/http://www.researcherid.com/resources/html/help_upload.htm)
- [Refman](https://web.archive.org/web/20110930172154/http://www.refman.com/support/risformat_intro.asp)
- [Refman (RIS format)](https://web.archive.org/web/20110930172154/http://www.refman.com/support/risformat_intro.asp)
- [Zotero](https://github.com/zotero/translators/blob/master/RIS.js)

### Complete list of ListType tags

```python
>>> from rispy import LIST_TYPE_TAGS
>>> print(LIST_TYPE_TAGS)
['A1', 'A2', 'A3', 'A4', 'AU', 'KW', 'N1', 'UR']

```

### Complete default mapping

```python
>>> from rispy import TAG_KEY_MAPPING
>>> from pprint import pprint
>>> pprint(TAG_KEY_MAPPING)
{'A1': 'first_authors',
 'A2': 'secondary_authors',
 'A3': 'tertiary_authors',
 'A4': 'subsidiary_authors',
 'AB': 'abstract',
 'AD': 'author_address',
 'AN': 'accession_number',
 'AU': 'authors',
 'C1': 'custom1',
 'C2': 'custom2',
 'C3': 'custom3',
 'C4': 'custom4',
 'C5': 'custom5',
 'C6': 'custom6',
 'C7': 'custom7',
 'C8': 'custom8',
 'CA': 'caption',
 'CN': 'call_number',
 'CY': 'place_published',
 'DA': 'date',
 'DB': 'name_of_database',
 'DO': 'doi',
 'DP': 'database_provider',
 'EP': 'end_page',
 'ER': 'end_of_reference',
 'ET': 'edition',
 'ID': 'id',
 'IS': 'number',
 'J2': 'alternate_title1',
 'JA': 'alternate_title2',
 'JF': 'alternate_title3',
 'JO': 'journal_name',
 'KW': 'keywords',
 'L1': 'file_attachments1',
 'L2': 'file_attachments2',
 'L4': 'figure',
 'LA': 'language',
 'LB': 'label',
 'M1': 'note',
 'M3': 'type_of_work',
 'N1': 'notes',
 'N2': 'notes_abstract',
 'NV': 'number_of_volumes',
 'OP': 'original_publication',
 'PB': 'publisher',
 'PY': 'year',
 'RI': 'reviewed_item',
 'RN': 'research_notes',
 'RP': 'reprint_edition',
 'SE': 'section',
 'SN': 'issn',
 'SP': 'start_page',
 'ST': 'short_title',
 'T1': 'primary_title',
 'T2': 'secondary_title',
 'T3': 'tertiary_title',
 'TA': 'translated_author',
 'TI': 'title',
 'TT': 'translated_title',
 'TY': 'type_of_reference',
 'UK': 'unknown_tag',
 'UR': 'urls',
 'VL': 'volume',
 'Y1': 'publication_year',
 'Y2': 'access_date'}

```

### Override key mapping

The parser uses a `TAG_KEY_MAPPING`, which one can override by calling `rispy.load()` with the `mapping` parameter.

```python
>>> from copy import deepcopy
>>> import rispy
>>> from pprint import pprint

>>> filepath = 'tests/data/example_full.ris'
>>> mapping = deepcopy(rispy.TAG_KEY_MAPPING)
>>> mapping["SP"] = "pages_this_is_my_fun"
>>> with open(filepath, 'r') as bibliography_file:
...     entries = rispy.load(bibliography_file, mapping=mapping)
...     pprint(sorted(entries[0].keys()))
['alternate_title2',
 'alternate_title3',
 'file_attachments2',
 'first_authors',
 'id',
 'issn',
 'keywords',
 'note',
 'notes_abstract',
 'number',
 'pages_this_is_my_fun',
 'place_published',
 'primary_title',
 'publication_year',
 'publisher',
 'secondary_authors',
 'type_of_reference',
 'urls',
 'volume']

```

List tags can be customized in the same way, by passing a list to the `list_tags` parameter.

### Changing rispy behavior

There are a few flags that can be passed to `rispy.load()` and `rispy.dump()` that change how `rispy` deals with tags.
For example, setting `skip_unknown_tags` to `True` will cause `rispy` do not read or write tags not in the tag map. More
can be found in the docstrings for each class. If more customization is necessary, a custom implementation can be
created (see next section).

## Using custom implementations

Not all RIS files follow the same formatting guidelines. There is an interface for creating custom implementations for
reading and writing such files. An implementation contains the methods and parameters used to work with RIS files, and
should be passed to `rispy.load()` or `rispy.dump()`.

### Customizing implementations

Creating a custom implementation involves creating a class that inherits a base class, and overriding the necessary
variables and methods. One of the existing parsers can also be inherited. Inheriting an existing class is advantageous
if only minor changes need to be made. The sections below document what is available to be overridden, along with a few
examples.

#### Parsing

Custom parsers can inherit `RisParser` (the default parser). Various parameters and methods can be overridden when creating a new parser.

Examples:

```python
class WokParser(RisParser):
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

```

### Writing

Writing is very similar to parsing. A custom writer class can inherit `BaseWriter` or one if its subclasses, such as
`RisWriter`.

Examples:

```python
class RisWriter(BaseWriter):
      """Subclass of BaseWriter for writing RIS files."""

      START_TAG = "TY"
      PATTERN = "{tag}  - {value}"
      DEFAULT_MAPPING = TAG_KEY_MAPPING
      DEFAULT_LIST_TAGS = LIST_TYPE_TAGS

      def set_header(self, count):
         return "{i}.".format(i=count)

```

## Other functionality

Other various utilities included in `rispy` are documented below.

### Reference type conversion

A method is available to convert common RIS reference types into more readable terms. It takes a list of references and
returns a copy of that list with modified reference types. The map for this conversion is located in ``config.py``.

```python
>>> from rispy.utils import convert_reference_types
>>> refs = [{"type_of_reference": "JOUR"}]
>>> print(convert_reference_types(refs))
[{'type_of_reference': 'Journal'}]

```

## Software for other RIS-like formats

Some RIS-like formats contain rich citation data, for example lists and nested attributes, that `rispy` does not
support. Software specializing in these formats includes:

* [nbib](https://pypi.org/project/nbib/) - parses the "PubMed" or "MEDLINE" format

## Developer instructions

Install [uv](https://docs.astral.sh/uv/) and make it available and on your path. Then:

```bash
# setup environment
uv venv --python=3.13
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"

# list available tasks
poe

# check if code format changes are required
poe lint

# reformat code
poe format

# run tests
poe test

# run benchmark tests
poe bench
```

If you'd prefer not to use `uv`, that's fine too; this is a standard Python package so feel free to use your
preferred workflow.

Github Actions are currently enabled to run `lint` and `test` when submitting a pull-request.
