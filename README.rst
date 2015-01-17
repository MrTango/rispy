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
   {'A1': ['Marx, Karl', 'Lindgren, Astrid', 'Glattauer, Daniel'],
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
    'Y1': '2014//'}
   {'A1': ['Marxus, Karlus', 'Lindgren, Astrid', 'Glattauer, Daniel'],
    'CY': 'Germany',
    'ID': '12345',
    'IS': '3',
    'JA': 'lorem',
    'JF': 'Lorem',
    'KW': ['Pippi Langstrumpf', 'Nordwind', 'Piraten'],
    'L2': 'http://example2.com',
    'M1': '1228150341',
    'N2': 'BACKGROUND: Lorem dammed ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.  RESULTS: Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. CONCLUSIONS: Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium.',
    'PB': ['Dark Factory', 'Dark Factory GER'],
    'SN': '1732-4208',
    'SP': 'e0815341',
    'T1': 'The title of the reference',
    'TY': 'JOUR',
    'VL': '6',
    'Y1': '2006//'}

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

