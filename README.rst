Python RIS files parser and reader
==================================

A Python 3.6+ reader/writer of RIS reference files.

Usage
-----

Parsing:

.. code:: python

   >>> import os
   >>> from pprint import pprint
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

Writing:

.. code:: python

   >>> import os
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


Some RIS files contain additional metadata that by default will raise an exception in the parsing. To ignore metadata which is not officially part of the RIS spec, you can use the optional `strict` flag:

.. code:: python

   >>> from pathlib import Path
   >>> import rispy
   >>> p = Path('tests/data/example_extraneous_data.ris')   
   >>> print("\n".join(p.read_text().splitlines()[:10]))
   Record #1 of 2
   Provider: Provider
   Content: text/plain; charset="UTF-8"
   1.
   TY  - JOUR
   ID  - 12345
   T1  - Title of reference
   A1  - Marx, Karl
   A1  - Lindgren, Astrid
   A2  - Glattauer, Daniel
   >>> entries = rispy.load(p, strict=False)
   >>> print(entries[0]['id'])
   12345
   

Example RIS entry
-----------------

.. code:: text

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


TAG_KEY_MAPPING
---------------

The most fields contain string values, but some like first_authors (A1) are parsed into lists. The default mapping were created from specifications scattered around the web, but to our knowledge there is not one single source of RIS truth, so these may need to be modified for specific export systems:

- Wikipedia_
- ResearcherId_
- Refman_
- `Refman (RIS format)`_
- Zotero_

.. _Wikipedia: https://en.wikipedia.org/wiki/RIS_(file_format)
.. _ResearcherId: https://web.archive.org/web/20170707033254/http://www.researcherid.com/resources/html/help_upload.htm
.. _Refman: https://web.archive.org/web/20110930172154/http://www.refman.com/support/risformat_intro.asp
.. _`Refman (RIS format)`: https://web.archive.org/web/20120526103719/http://refman.com/support/risformat_intro.asp
.. _Zotero: https://github.com/zotero/translators/blob/master/RIS.js

Complete list of ListType tags
******************************

.. code:: python

    >>> from rispy.config import LIST_TYPE_TAGS
    >>> pprint(LIST_TYPE_TAGS)
    ['A1', 'A2', 'A3', 'A4', 'AU', 'KW', 'N1']


Complete default mapping
************************

.. code:: python

    >>> from rispy.config import TAG_KEY_MAPPING
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
     'UR': 'url',
     'VL': 'volume',
     'Y1': 'publication_year',
     'Y2': 'access_date'}

Override key mapping
********************

The parser use a ``TAG_KEY_MAPPING``, which one can override by calling ``rispy.load()`` with a custom mapping.

.. code:: python

   >>> import os
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
    'url',
    'volume']

Software for other RIS-like formats
-----------------------------------
Some RIS-like formats contain rich citation data, for example lists and nested attributes, that :code:`rispy` does not
support. Software specializing on these formats include:

* `nbib <https://pypi.org/project/nbib/>`_ parses the "PubMed" or "MEDLINE" format


Developer instructions
----------------------

Common developer commands are in the provided `Makefile`; if you don't have `make` installed, you can view the make commands and run the commands from the command-line manually:

.. code:: bash

   # setup environment
   python -m venv venv
   source venv/bin/activate
   pip install -e .[dev,test]

   # check if code format changes are required
   make lint
   
   # reformat code
   make format

   # run tests
   make test 

Github Actions are currently enabled to run `lint` and `test` when submitting a pull-request.
