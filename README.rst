Python RIS files parser
=======================

It reads RIS files and provides Python dictionaries via a generator.
This works also for very larg ris files.

Usage
-----

from RISparser import readris

entries = readris('/home/tester/myrisfile.ris')

for entry in entries:
   # do what ever you want with this entry
   # an SQL INSERT for example

Example entry
-------------
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

