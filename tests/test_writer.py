import os

import rispy


def nice_keys(to_change, mapping=rispy.TAG_KEY_MAPPING):
    return {mapping[k]: v for k, v in to_change.items()}


def nice_list(to_change, mapping=rispy.TAG_KEY_MAPPING):
    return [nice_keys(d, mapping) for d in to_change]


def test_dump_example_full_ris(tmp_path):
    entry1 = {
        "TY": "JOUR",
        "ID": "12345",
        "T1": "Title of reference",
        "A1": ["Marx, Karl", "Lindgren, Astrid"],
        "A2": ["Glattauer, Daniel"],
        "Y1": "2014//",
        "N2": "BACKGROUND: Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.  RESULTS: Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. CONCLUSIONS: Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium.",  # noqa: E501
        "KW": ["Pippi", "Nordwind", "Piraten"],
        "JF": "Lorem",
        "JA": "lorem",
        "VL": "9",
        "IS": "3",
        "SP": "e0815",
        "CY": "United States",
        "PB": "Fun Factory",
        "SN": "1932-6208",
        "M1": "1008150341",
        "L2": "http://example.com",
        "UR": "http://example_url.com",
    }

    entry2 = {
        "TY": "JOUR",
        "ID": "12345",
        "T1": "The title of the reference",
        "A1": ["Marxus, Karlus", "Lindgren, Astrid"],
        "A2": ["Glattauer, Daniel"],
        "Y1": "2006//",
        "N2": "BACKGROUND: Lorem dammed ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.  RESULTS: Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. CONCLUSIONS: Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium.",  # noqa: E501
        "KW": ["Pippi Langstrumpf", "Nordwind", "Piraten"],
        "JF": "Lorem",
        "JA": "lorem",
        "VL": "6",
        "IS": "3",
        "SP": "e0815341",
        "CY": "Germany",
        "PB": "Dark Factory",
        "SN": "1732-4208",
        "M1": "1228150341",
        "L2": "http://example2.com",
        "UR": "http://example_url.com",
    }

    fp = tmp_path / "test_dump.ris"

    results = nice_list([entry1, entry2])

    with open(fp, "w") as bibliography_file:
        rispy.dump(results, bibliography_file)

    with open(fp, "r") as test_file:
        lines = test_file.read().splitlines()

        assert lines[0] == "1."
        assert lines[1] == "TY  - JOUR"
        assert lines[23] == "ER  - "


def test_dumps_example_full_ris():
    entry1 = {
        "TY": "JOUR",
        "ID": "12345",
        "T1": "Title of reference",
        "A1": ["Marx, Karl", "Lindgren, Astrid"],
        "A2": ["Glattauer, Daniel"],
        "Y1": "2014//",
        "N2": "BACKGROUND: Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.  RESULTS: Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. CONCLUSIONS: Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium.",  # noqa: E501
        "KW": ["Pippi", "Nordwind", "Piraten"],
        "JF": "Lorem",
        "JA": "lorem",
        "VL": "9",
        "IS": "3",
        "SP": "e0815",
        "CY": "United States",
        "PB": "Fun Factory",
        "SN": "1932-6208",
        "M1": "1008150341",
        "L2": "http://example.com",
        "UR": "http://example_url.com",
    }

    entry2 = {
        "TY": "JOUR",
        "ID": "12345",
        "T1": "The title of the reference",
        "A1": ["Marxus, Karlus", "Lindgren, Astrid"],
        "A2": ["Glattauer, Daniel"],
        "Y1": "2006//",
        "N2": "BACKGROUND: Lorem dammed ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.  RESULTS: Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. CONCLUSIONS: Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium.",  # noqa: E501
        "KW": ["Pippi Langstrumpf", "Nordwind", "Piraten"],
        "JF": "Lorem",
        "JA": "lorem",
        "VL": "6",
        "IS": "3",
        "SP": "e0815341",
        "CY": "Germany",
        "PB": "Dark Factory",
        "SN": "1732-4208",
        "M1": "1228150341",
        "L2": "http://example2.com",
        "UR": "http://example_url.com",
    }

    results = nice_list([entry1, entry2])

    bytestring = rispy.dumps(results)
    lines = bytestring.split("\n")

    assert lines[0] == "1."
    assert lines[1] == "TY  - JOUR"
    assert lines[23] == "ER  - "


def test_dumps_multiple_unknown_tags_ris(tmp_path):

    fp = tmp_path / "test_dump_unknown_tags.ris"

    results = [{"title": "test", "abstract": "test", "does_not_exists": "test"}]

    with open(fp, "w") as bibliography_file:
        rispy.dump(results, bibliography_file)

    with open(fp, "r") as test_file:
        lines = test_file.read().splitlines()

        assert lines[0] == "1."
        assert lines[1] == "TY  - JOUR"
        assert lines[4] == "ER  - "


def test_dump_and_load(tmp_path):

    temp_fp = tmp_path / "test_dump_and_load.ris"

    source_fp = os.path.join("tests", "data", "example_full.ris")

    with open(source_fp, "r") as bibliography_file1:
        entries = rispy.load(bibliography_file1)

    with open(temp_fp, "w") as bibliography_file2:
        rispy.dump(entries, bibliography_file2)

    with open(temp_fp, "r") as bibliography_file3:
        entries = list(rispy.load(bibliography_file3))
        entries[0]["place_published"] = "United States"
