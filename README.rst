Python RIS files parser
=======================

It reads RIS files and provides Python dictionaries via a generator.
This works also for very larg RIS files.


Usage
-----
::

   >>> import os
   >>> from RISparser import readris
   >>> from pprint import pprint

   >>> filepath = 'tests/example_full.ris'
   >>> entries = readris(filepath)
   >>> for entry in entries:
   ...     pprint(entry)
   {'abstract': 'BACKGROUND: Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.  RESULTS: Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. CONCLUSIONS: Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium.',
    'alternate_title2': 'lorem',
    'alternate_title3': 'Lorem',
    'file_attachments2': 'http://example.com',
    'first_authors': ['Marx, Karl', 'Lindgren, Astrid'],
    'id': '12345',
    'issn': '1932-6208',
    'keywords': ['Pippi', 'Nordwind', 'Piraten'],
    'note': '1008150341',
    'number': '3',
    'place_published': 'United States',
    'primary_title': 'Title of reference',
    'publication_year': '2014//',
    'publisher': 'Fun Factory',
    'secondary_authors': ['Glattauer, Daniel'],
    'start_page': 'e0815',
    'type_of_reference': 'JOUR',
    'url': 'http://example_url.com',
    'volume': '9'}
   {'abstract': 'BACKGROUND: Lorem dammed ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.  RESULTS: Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. CONCLUSIONS: Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium.',
    'alternate_title2': 'lorem',
    'alternate_title3': 'Lorem',
    'file_attachments2': 'http://example2.com',
    'first_authors': ['Marxus, Karlus', 'Lindgren, Astrid'],
    'id': '12345',
    'issn': '1732-4208',
    'keywords': ['Pippi Langstrumpf', 'Nordwind', 'Piraten'],
    'note': '1228150341',
    'number': '3',
    'place_published': 'Germany',
    'primary_title': 'The title of the reference',
    'publication_year': '2006//',
    'publisher': 'Dark Factory',
    'secondary_authors': ['Glattauer, Daniel'],
    'start_page': 'e0815341',
    'type_of_reference': 'JOUR',
    'url': 'http://example_url.com',
    'volume': '6'}

   >>> entries = readris(filepath)
   >>> entries_list = list(entries)
   >>> print(len(entries_list))
   2


Example RIS entry
-----------------
::

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

Complete default mapping
************************
::

    >>> from RISparser.config import TAG_KEY_MAPPING
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
     'KW': 'keywords',
     'L1': 'file_attachments1',
     'L2': 'file_attachments2',
     'L4': 'figure',
     'LA': 'language',
     'LB': 'label',
     'M1': 'note',
     'M3': 'type_of_work',
     'N1': 'notes',
     'N2': 'abstract',
     'NV': 'number_of_Volumes',
     'OP': 'original_publication',
     'PB': 'publisher',
     'PY': 'year',
     'RI': 'reviewed_item',
     'RN': 'research_notes',
     'RP': 'reprint_edition',
     'SE': 'version',
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
     'UR': 'url',
     'VL': 'volume',
     'Y1': 'publication_year',
     'Y2': 'access_date'}

Override key mapping
********************

The parser use a TAG_KEY_MAPPING, witch one can override by calling readris() with a custom mapping.

::

   >>> import os
   >>> from RISparser import readris, TAG_KEY_MAPPING
   >>> from pprint import pprint

   >>> filepath = 'tests/example_full.ris'
   >>> mapping = TAG_KEY_MAPPING
   >>> mapping["SP"] = "pages"
   >>> entries = list(readris(filepath, mapping=mapping))
   >>> pprint(entries[0])
   {'abstract': 'BACKGROUND: Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.  RESULTS: Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. CONCLUSIONS: Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium.',
    'alternate_title2': 'lorem',
    'alternate_title3': 'Lorem',
    'file_attachments2': 'http://example.com',
    'first_authors': ['Marx, Karl', 'Lindgren, Astrid'],
    'id': '12345',
    'issn': '1932-6208',
    'keywords': ['Pippi', 'Nordwind', 'Piraten'],
    'note': '1008150341',
    'number': '3',
    'pages': 'e0815',
    'place_published': 'United States',
    'primary_title': 'Title of reference',
    'publication_year': '2014//',
    'publisher': 'Fun Factory',
    'secondary_authors': ['Glattauer, Daniel'],
    'type_of_reference': 'JOUR',
    'url': 'http://example_url.com',
    'volume': '9'}

