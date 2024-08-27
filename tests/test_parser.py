from pathlib import Path

import pytest

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

    # test with file object
    with open(filepath) as f:
        entries = rispy.load(f)
    assert expected == entries[0]

    # test with pathlib object
    p = Path(filepath)
    entries = rispy.load(p)
    assert expected == entries[0]


def test_loads():
    ristext = (DATA_DIR / "example_basic.ris").read_text()
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

    assert expected == rispy.loads(ristext)[0]


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
    with open(filepath) as f:
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
            "urls": ["http://example_url.com"],
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
            "urls": ["http://example_url.com"],
        },
    ]

    with open(filepath) as f:
        entries = rispy.load(f)
    assert expected == entries


def test_load_example_extraneous_data_ris():
    filepath = DATA_DIR / "example_extraneous_data.ris"
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
            "urls": ["http://example_url.com"],
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
            "urls": ["http://example_url.com"],
        },
    ]

    with open(filepath) as f:
        entries = rispy.load(f)
    assert expected == entries


def test_load_example_full_ris_without_whitespace():
    # Parse files without whitespace after ER tag.
    # Resolves https://github.com/MrTango/rispy/pull/25

    filepath = DATA_DIR / "example_full_without_whitespace.ris"
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
            "urls": ["http://example_url.com"],
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
            "urls": ["http://example_url.com"],
        },
    ]

    with open(filepath) as f:
        entries = rispy.load(f)
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

    with open(filepath) as f:
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
    with open(filepath) as f:
        entries = rispy.load(f)
    assert expected == entries[0]


def test_starting_newline():
    fn = DATA_DIR / "example_starting_newlines.ris"
    with open(fn) as f:
        entries = rispy.load(f)
    assert len(entries) == 1


def test_strip_bom():
    expected = {
        "type_of_reference": "JOUR",
        "doi": "10.1186/s40981-020-0316-0",
    }

    filepath = DATA_DIR / "example_bom.ris"

    # we properly decode the content of this file as UTF-8, but leave the BOM
    with open(filepath, encoding="utf-8-sig") as f:
        entries = rispy.load(f)

    assert expected == entries[0]


def test_wos_ris():
    fn = DATA_DIR / "example_wos.ris"
    with open(fn) as f:
        entries = rispy.load(f, implementation=rispy.WokParser)

    assert len(entries) == 2

    title = "Interactions stabilizing the structure of the core light-harvesting complex (LHl) of photosynthetic bacteria and its subunit (B820)"  # noqa: E501
    assert entries[0]["document_title"] == title

    title = "Proximal and distal influences on ligand binding kinetics in microperoxidase and heme model compounds"  # noqa: E501
    assert entries[1]["document_title"] == title


def test_unkown_skip():
    filepath = DATA_DIR / "example_multi_unknown_tags.ris"
    expected = {
        "type_of_reference": "JOUR",
        "authors": ["Shannon,Claude E."],
        "year": "1948/07//",
        "title": "A Mathematical Theory of Communication",
        "alternate_title3": "Bell System Technical Journal",
        "end_page": "423",
        "volume": "27",
    }

    with open(filepath) as f:
        entries = rispy.load(f, skip_unknown_tags=True)
    assert expected == entries[0]


def test_type_conversion():
    refs = [
        {"type_of_reference": "JOUR", "id": "12345", "primary_title": "Title of reference"},
        {
            "type_of_reference": "BOOK",
            "id": "12345",
            "primary_title": "The title of the reference",
        },
        {"type_of_reference": "Journal", "id": "12345", "primary_title": "Title of reference"},
        {"type_of_reference": "TEST", "id": "12345", "primary_title": "Title of reference"},
    ]

    # test conversion
    test1 = rispy.utils.convert_reference_types(refs)
    test1_types = [i["type_of_reference"] for i in test1]
    assert test1_types == [
        "Journal",
        "Whole book",
        "Journal",
        "TEST",
    ]

    # test reverse
    test2 = rispy.utils.convert_reference_types(test1, reverse=True)
    assert test2[0:2] == refs[0:2]
    assert test2[3] == refs[3]
    assert test2[2]["type_of_reference"] == "JOUR"

    # test strict
    with pytest.raises(KeyError):
        rispy.utils.convert_reference_types(refs, strict=True)
    refs_clean = refs[0:3]
    test3 = rispy.utils.convert_reference_types(refs_clean, strict=True)

    # test strict in reverse
    test4 = rispy.utils.convert_reference_types(test3, strict=True, reverse=True)
    assert test4[0:2] == refs_clean[0:2]
    assert test4[2]["type_of_reference"] == "JOUR"


def test_encodings():
    p = DATA_DIR / "example_utf_chars.ris"

    with open(p, encoding="utf-8-sig") as file:
        expected = rispy.load(file)

    with pytest.raises(UnicodeDecodeError):
        rispy.load(p, encoding="cp1252")

    entries = rispy.load(p, encoding="utf-8-sig")

    assert entries == expected


def test_list_tag_enforcement():
    filepath = DATA_DIR / "example_custom_list_tags.ris"

    expected = {
        "type_of_reference": "JOUR",
        "authors": ["Marx, Karl", "Marxus, Karlus"],
        "issn": ["12345", "ABCDEFG", "666666"],
    }

    entries = rispy.load(filepath, enforce_list_tags=False, list_tags=[])
    assert expected == entries[0]


def test_url_tag():
    filepath = DATA_DIR / "example_urls.ris"
    with open(filepath) as f:
        entries = rispy.load(f)

    assert len(entries) == 4
    assert entries[0]["urls"] == ["http://example.com"]
    assert entries[1]["urls"] == ["http://example.com", "http://www.example.com"]
    assert entries[2]["urls"] == ["http://example.com", "http://www.example.com"]
    assert entries[3]["urls"] == ["http://example.com", "http://www.example.com"]


def test_empty_tag():
    filepath = DATA_DIR / "example_empty_tag.ris"
    with open(filepath) as f:
        entries = rispy.load(f)

    assert len(entries) == 1
    assert entries[0]["number"] == "9"
    assert entries[0]["start_page"] == ""
