Python RIS files parser
=======================

It reads RIS files and provides Python dictionaries via a generator.
This works also for very larg ris files.

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
    'authors': ['Marx, Karl', 'Lindgren, Astrid'],
    'file_attachments2': 'http://example.com',
    'id': '12345',
    'issn': '1932-6208',
    'keywords': ['Pippi', 'Nordwind', 'Piraten'],
    'note': '1008150341',
    'number': '3',
    'place_published': 'United States',
    'primary_title': 'Title of reference',
    'publication_year': '2014//',
    'publisher': ['Fun Factory', 'Fun Factory USA'],
    'secondary_authors': 'Glattauer, Daniel',
    'start_page': 'e0815',
    'type': 'JOUR',
    'url': 'http://example_url.com',
    'volume': '9'}
   {'abstract': 'BACKGROUND: Lorem dammed ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.  RESULTS: Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. CONCLUSIONS: Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium.',
    'alternate_title2': 'lorem',
    'alternate_title3': 'Lorem',
    'authors': ['Marxus, Karlus', 'Lindgren, Astrid'],
    'file_attachments2': 'http://example2.com',
    'id': '12345',
    'issn': '1732-4208',
    'keywords': ['Pippi Langstrumpf', 'Nordwind', 'Piraten'],
    'note': '1228150341',
    'number': '3',
    'place_published': 'Germany',
    'primary_title': 'The title of the reference',
    'publication_year': '2006//',
    'publisher': ['Dark Factory', 'Dark Factory GER'],
    'secondary_authors': 'Glattauer, Daniel',
    'start_page': 'e0815341',
    'type': 'JOUR',
    'url': 'http://example_url.com',
    'volume': '6'}

   >>> entries = readris(filepath)
   >>> entries_list = list(entries)
   >>> print(len(entries_list))
   2


Example entry
-------------

RIS entry
*********
::

   1.
   TY  - JOUR
   ID  - 12345
   T1  - Title of reference
   A1  - Marx, Karl
   A1  - Lindgren, Astrid
   A1  - Glattauer, Daniel
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


DICT entry
**********
::

   {
      'A1': ['Marx, Karl', 'Lindgren, Astrid', 'Glattauer, Daniel'],
      'CY': 'United States',
      'ID': '12345',
      'IS': '3',
      'JA': 'lorem',
      'JF': 'Lorem',
      'KW': ['Pippi', 'Nordwind', 'Piraten'],
      'L2': 'http://example.com',
      'M1': '1008150341',
      'N2': 'BACKGROUND: Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.  RESULTS: Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. CONCLUSIONS: Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium.',
      'PB': ['Fun Factory', 'Fun Factory USA'],
      'SN': '1932-6208',
      'SP': 'e0815',
      'T1': 'Title of reference',
      'TY': 'JOUR',
      'VL': '9',
      'Y1': '2014//'
   }

