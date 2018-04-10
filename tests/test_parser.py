# -*- coding: utf-8 -*-
from collections import defaultdict
import os
from RISparser import readris, TAG_KEY_MAPPING

pj = os.path.join

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


class TestRISparser():

    def cmp_dict(self, d0, d1):
        for key, value in d0.items():
            assert key in d1
            self.compare(value, d1.pop(key))
        assert not len(d1)

    def cmp_list(self, l0, l1):
        assert len(l0) == len(l1)
        for v0, v1 in zip(l0, l1):
            self.compare(v0, v1)

    def compare(self, v0, v1):
        assert type(v0) == type(v1)
        if hasattr(v0, 'items'):
            self.cmp_dict(v0, v1)
            return

        if isinstance(v0, (list, dict)):
            self.cmp_list(v0, v1)
            return
        assert v0 == v1

    def nice_keys(self, to_change, mapping=TAG_KEY_MAPPING):
        return {mapping[k]: v for k, v in to_change.items()}

    def nice_list(self, to_change, mapping=TAG_KEY_MAPPING):
        return [self.nice_keys(d, mapping) for d in to_change]

    def test_parse_example_basic_ris(self):
        filepath = os.path.join(CURRENT_DIR, 'example_basic.ris')
        result_entry = self.nice_keys({
            'TY': 'JOUR',
            'AU': ['Shannon,Claude E.'],
            'PY': '1948/07//',
            'TI': 'A Mathematical Theory of Communication',
            'JF': 'Bell System Technical Journal',
            'SP': '379',
            'EP': '423',
            'VL': '27',
        })

        with open(filepath, 'r') as bibliography_file:
            entries = list(readris(bibliography_file))
            self.compare([result_entry], entries)

    def test_parse_multiline_ris(self):
        filepath = os.path.join(CURRENT_DIR, 'multiline.ris')
        result_entry = self.nice_keys({
            'TY': 'JOUR',
            'AU': ['Shannon,Claude E.'],
            'PY': '1948/07//',
            'TI': 'A Mathematical Theory of Communication',
            'JF': 'Bell System Technical Journal',
            'N2': 'first line, then second line and at the end the last line',
            'N1': ['first line', '* second line', '* last line'],
            'SP': '379',
            'EP': '423',
            'VL': '27',
        })
        with open(filepath, 'r') as f:
            entries = list(readris(f))
            self.compare([result_entry], entries)

    def test_parse_example_full_ris(self):
        filepath = os.path.join(CURRENT_DIR, 'example_full.ris')
        entry1 = {
            'TY': 'JOUR',
            'ID': '12345',
            'T1': 'Title of reference',
            'A1': ['Marx, Karl', 'Lindgren, Astrid'],
            'A2': ['Glattauer, Daniel'],
            'Y1': '2014//',
            'N2': 'BACKGROUND: Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.  RESULTS: Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. CONCLUSIONS: Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium.',
            'KW': ['Pippi', 'Nordwind', 'Piraten'],
            'JF': 'Lorem',
            'JA': 'lorem',
            'VL': '9',
            'IS': '3',
            'SP': 'e0815',
            'CY': 'United States',
            'PB': 'Fun Factory',
            'SN': '1932-6208',
            'M1': '1008150341',
            'L2': 'http://example.com',
            'UR': 'http://example_url.com',
        }

        entry2 = {
            'TY': 'JOUR',
            'ID': '12345',
            'T1': 'The title of the reference',
            'A1': ['Marxus, Karlus', 'Lindgren, Astrid'],
            'A2': ['Glattauer, Daniel'],
            'Y1': '2006//',
            'N2': 'BACKGROUND: Lorem dammed ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.  RESULTS: Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. CONCLUSIONS: Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium.',
            'KW': ['Pippi Langstrumpf', 'Nordwind', 'Piraten'],
            'JF': 'Lorem',
            'JA': 'lorem',
            'VL': '6',
            'IS': '3',
            'SP': 'e0815341',
            'CY': 'Germany',
            'PB': 'Dark Factory',
            'SN': '1732-4208',
            'M1': '1228150341',
            'L2': 'http://example2.com',
            'UR': 'http://example_url.com',
        }

        results = self.nice_list([entry1, entry2])
        with open(filepath, 'r') as bibliography_file:
            entries = list(readris(bibliography_file))
            self.compare(results, entries)

    def test_parse_single_unknown_tag_ris(self):
        filepath = os.path.join(CURRENT_DIR, 'example_single_unknown_tag.ris')
        unknowns = defaultdict(list)
        unknowns['JP'].append('CRISPR')
        unknowns['JP'].append('Direct Current')
        result_entry = self.nice_keys({
            'TY': 'JOUR',
            'AU': ['Shannon,Claude E.'],
            'PY': '1948/07//',
            'TI': 'A Mathematical Theory of Communication',
            'JF': 'Bell System Technical Journal',
            'SP': '379',
            'EP': '423',
            'VL': '27',
            # {'JP': ['CRISPR', 'Direct Current']}
            'UK': unknowns,
        })

        with open(filepath, 'r') as bibliography_file:
            entries = list(readris(bibliography_file))
            self.compare([result_entry], entries)

    def test_parse_multiple_unknown_tags_ris(self):
        filepath = os.path.join(CURRENT_DIR, 'example_multi_unknown_tags.ris')
        unknowns = defaultdict(list)
        unknowns['JP'].append('CRISPR')
        unknowns['DC'].append('Direct Current')
        result_entry = self.nice_keys({
            'TY': 'JOUR',
            'AU': ['Shannon,Claude E.'],
            'PY': '1948/07//',
            'TI': 'A Mathematical Theory of Communication',
            'JF': 'Bell System Technical Journal',
            'SP': '379',
            'EP': '423',
            'VL': '27',
            # {'JP': ['CRISPR'], 'DC': ['Direct Current']}
            'UK': unknowns,
        })

        with open(filepath, 'r') as bibliography_file:
            entries = list(readris(bibliography_file))
            self.compare([result_entry], entries)

    def test_starting_newline(self):
        fn = os.path.join(CURRENT_DIR, 'example_starting_newlines.ris')
        with open(fn, 'r') as f:
            entries = list(readris(f))
        assert len(entries) == 1
