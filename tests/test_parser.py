from pathlib import Path

import rispy


DATA_DIR = Path(__file__).parent.resolve() / "data"


def test_load_example_basic_ris():
    filepath = DATA_DIR / "example_basic.ris"
    expected = {
        "type_of_reference": "JOUR",
        "authors": ["Shannon,Claude E."],
        "year": "1948/07//",
        "title": "A Mathematical Theory of Communication",
        "alternate_title3": "Bell System Technical Journal",
        "start_page": "379",
        "end_page": "423",
        "volume": "27",
    }

    with open(filepath, "r") as f:
        entries = rispy.load(f)

    assert expected == entries[0]


def test_load_multiline_ris():
    filepath = DATA_DIR / "multiline.ris"
    expected = {
        "type_of_reference": "JOUR",
        "authors": ["Shannon,Claude E."],
        "year": "1948/07//",
        "title": "A Mathematical Theory of Communication",
        "alternate_title3": "Bell System Technical Journal",
        "start_page": "379",
        "end_page": "423",
        "notes_abstract": "first line, then second line and at the end the last line",
        "notes": ["first line", "* second line", "* last line"],
        "volume": "27",
    }
    with open(filepath, "r") as f:
        entries = rispy.load(f)

    assert expected == entries[0]


def test_load_example_full_ris():
    filepath = DATA_DIR / "example_full.ris"
    expected = [
        {
            "type_of_reference": "JOUR",
            "id": "12345",
            "primary_title": "Title of reference",
            "first_authors": ["Marx, Karl", "Lindgren, Astrid"],
            "secondary_authors": ["Glattauer, Daniel"],
            "publication_year": "2014//",
            "notes_abstract": "BACKGROUND: Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.  RESULTS: Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. CONCLUSIONS: Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium.",  # noqa: E501
            "keywords": ["Pippi", "Nordwind", "Piraten"],
            "alternate_title3": "Lorem",
            "alternate_title2": "lorem",
            "volume": "9",
            "number": "3",
            "start_page": "e0815",
            "place_published": "United States",
            "publisher": "Fun Factory",
            "issn": "1932-6208",
            "note": "1008150341",
            "file_attachments2": "http://example.com",
            "url": "http://example_url.com",
        },
        {
            "type_of_reference": "JOUR",
            "id": "12345",
            "primary_title": "The title of the reference",
            "first_authors": ["Marxus, Karlus", "Lindgren, Astrid"],
            "secondary_authors": ["Glattauer, Daniel"],
            "publication_year": "2006//",
            "notes_abstract": "BACKGROUND: Lorem dammed ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.  RESULTS: Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. CONCLUSIONS: Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium.",  # noqa: E501
            "keywords": ["Pippi Langstrumpf", "Nordwind", "Piraten"],
            "alternate_title3": "Lorem",
            "alternate_title2": "lorem",
            "volume": "6",
            "number": "3",
            "start_page": "e0815341",
            "place_published": "Germany",
            "publisher": "Dark Factory",
            "issn": "1732-4208",
            "note": "1228150341",
            "file_attachments2": "http://example2.com",
            "url": "http://example_url.com",
        },
    ]

    with open(filepath, "r") as f:
        entries = rispy.loads(f.read())
    assert expected == entries


def test_load_single_unknown_tag_ris():
    filepath = DATA_DIR / "example_single_unknown_tag.ris"
    expected = {
        "type_of_reference": "JOUR",
        "authors": ["Shannon,Claude E."],
        "year": "1948/07//",
        "title": "A Mathematical Theory of Communication",
        "alternate_title3": "Bell System Technical Journal",
        "start_page": "379",
        "end_page": "423",
        "volume": "27",
        "unknown_tag": {"JP": ["CRISPR", "Direct Current"]},
    }

    with open(filepath, "r") as f:
        entries = rispy.load(f)

    assert expected == entries[0]


def test_load_multiple_unknown_tags_ris():
    filepath = DATA_DIR / "example_multi_unknown_tags.ris"
    expected = {
        "type_of_reference": "JOUR",
        "authors": ["Shannon,Claude E."],
        "year": "1948/07//",
        "title": "A Mathematical Theory of Communication",
        "alternate_title3": "Bell System Technical Journal",
        "end_page": "423",
        "volume": "27",
        "unknown_tag": {"JP": ["CRISPR"], "DC": ["Direct Current"]},
    }
    with open(filepath, "r") as f:
        entries = rispy.load(f)
    assert expected == entries[0]


def test_starting_newline():
    fn = DATA_DIR / "example_starting_newlines.ris"
    with open(fn, "r") as f:
        entries = rispy.load(f)
    assert len(entries) == 1


def test_wos_ris():
    fn = DATA_DIR / "example_wos.ris"
    with open(fn, "r") as f:
        entries = rispy.load(f, implementation="wok")

    assert len(entries) == 2

    title = "Interactions stabilizing the structure of the core light-harvesting complex (LHl) of photosynthetic bacteria and its subunit (B820)"  # noqa: E501
    assert entries[0]["document_title"] == title

    title = "Proximal and distal influences on ligand binding kinetics in microperoxidase and heme model compounds"  # noqa: E501
    assert entries[1]["document_title"] == title


def test_implementation_constructor():
    # check that both calls are valid
    fn = DATA_DIR / "example_wos.ris"

    with open(fn, "r") as f:
        entries1 = rispy.load(f, implementation="wok")

    with open(fn, "r") as f:
        entries2 = rispy.load(f, implementation=rispy.RisImplementation.WOK)

    assert entries1 == entries2
