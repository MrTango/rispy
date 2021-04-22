from pathlib import Path
from copy import deepcopy

import pytest
import rispy


DATA_DIR = Path(__file__).parent.resolve() / "data"


def test_dump_and_load():
    # check that we can write the same file we read
    source_fp = DATA_DIR / "example_full.ris"

    # read text
    actual = source_fp.read_text()

    # map to RIS structure and dump
    entries = rispy.loads(actual)
    export = rispy.dumps(entries)

    assert actual == export


def test_dumps_multiple_unknown_tags_ris(tmp_path):

    fp = tmp_path / "test_dump_unknown_tags.ris"

    results = [{"title": "my-title", "abstract": "my-abstract", "does_not_exists": "test"}]

    # check that we get a warning
    with pytest.warns(UserWarning, match="label `does_not_exists` not exported"):
        with open(fp, "w") as f:
            rispy.dump(results, f)

    # check that we get everything back except missing key
    text = Path(fp).read_text()
    entries = rispy.loads(text)
    assert entries[0] == {
        "type_of_reference": "JOUR",
        "title": "my-title",
        "abstract": "my-abstract",
    }

    # check file looks as expected
    lines = text.splitlines()
    assert lines[0] == "1."
    assert lines[1] == "TY  - JOUR"
    assert lines[4] == "ER  - "
    assert len(lines) == 5


def test_custom_list_tags():
    filepath = DATA_DIR / "example_custom_list_tags.ris"
    list_tags = deepcopy(rispy.LIST_TYPE_TAGS)
    list_tags.append("SN")

    expected = {
        "type_of_reference": "JOUR",
        "authors": ["Marx, Karl", "Marxus, Karlus"],
        "issn": ["12345", "ABCDEFG", "666666"],
    }

    actual = filepath.read_text()

    parser = rispy.Ris(list_tags=list_tags)
    writer = rispy.RISWriter(list_tags=list_tags)

    entries = rispy.loads(actual, implementation=parser)
    assert expected == entries[0]

    export = rispy.dumps(entries, implementation=writer)
    assert export == actual


def test_skip_unknown_tags():
    entries = [
        {
            "type_of_reference": "JOUR",
            "authors": ["Marx, Karl", "Marxus, Karlus"],
            "issn": "12222",
            "unknown_tag": {"JP": ["CRISPR"], "DC": ["Direct Current"]},
        }
    ]
    expected = [
        {
            "type_of_reference": "JOUR",
            "authors": ["Marx, Karl", "Marxus, Karlus"],
            "issn": "12222",
        }
    ]

    class Writer(rispy.RISWriter):
        SKIP_UNKNOWN_TAGS = True

    export = rispy.dumps(entries, implementation=Writer())
    reload = rispy.loads(export)

    assert reload == expected


def test_writing_all_list_tags():
    expected = [
        {
            "type_of_reference": "JOUR",
            "authors": ["Marx, Karl", "Marxus, Karlus"],
            "issn": ["12345", "ABCDEFG", "666666"],
        }
    ]

    class Writer(rispy.RISWriter):
        ENFORCE_LIST_TAGS = False

    writer = Writer(list_tags=[])
    parser = rispy.Ris(list_tags=["AU", "SN"])

    export = rispy.dumps(expected, implementation=writer)
    entries = rispy.loads(export, implementation=parser)
    assert expected == entries
