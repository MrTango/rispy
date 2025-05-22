from copy import deepcopy
from pathlib import Path
from typing import ClassVar

import pytest

import rispy

DATA_DIR = Path(__file__).parent.resolve() / "data"


@pytest.fixture
def ris_data():
    return [
        {
            "type_of_reference": "JOUR",
            "authors": ["Shannon, Claude E.", "Doe, John"],
            "year": "1948/07//",
            "title": "A Mathematical Theory of Communication",
            "start_page": "379",
            "urls": ["https://example.com", "https://example2.com"],
        }
    ]


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

    entries = rispy.loads(actual, list_tags=list_tags)
    assert expected == entries[0]

    export = rispy.dumps(entries, list_tags=list_tags)
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

    export = rispy.dumps(entries, skip_unknown_tags=True)
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

    export = rispy.dumps(expected, enforce_list_tags=False, list_tags=[])
    entries = rispy.loads(export, list_tags=["AU", "SN"])
    assert expected == entries


def test_file_implementation_write():
    class CustomParser(rispy.RisParser):
        DEFAULT_IGNORE: ClassVar[list[str]] = ["JF", "ID", "KW"]

    class CustomWriter(rispy.RisWriter):
        DEFAULT_IGNORE: ClassVar[list[str]] = ["JF", "ID", "KW"]

    list_tags = ["SN", "T1", "A1", "UR"]

    fn = DATA_DIR / "example_full.ris"
    with open(fn) as f:
        entries = rispy.load(f, implementation=CustomParser, list_tags=list_tags)

    fn_write = DATA_DIR / "example_full_write.ris"

    with open(fn_write, "w") as f:
        rispy.dump(entries, f, implementation=CustomWriter, list_tags=list_tags)

    with open(fn_write) as f:
        reload = rispy.load(f, implementation=CustomParser, list_tags=list_tags)

    assert reload == entries


def test_write_single_unknown_tag(ris_data):
    ris_data[0]["unknown_tag"] = {"JP": ["CRISPR"]}
    text_output = rispy.dumps(ris_data)
    # check output is as expected
    lines = text_output.splitlines()
    assert lines[9] == "JP  - CRISPR"
    assert len(lines) == 11


def test_write_multiple_unknown_tag_same_type(ris_data):
    ris_data[0]["unknown_tag"] = {"JP": ["CRISPR", "PEOPLE"]}
    text_output = rispy.dumps(ris_data)

    # check output is as expected
    lines = text_output.splitlines()
    assert lines[9] == "JP  - CRISPR"
    assert lines[10] == "JP  - PEOPLE"
    assert len(lines) == 12


def test_write_multiple_unknown_tag_diff_type(ris_data):
    ris_data[0]["unknown_tag"] = {"JP": ["CRISPR"], "ED": ["Swinburne, Ricardo"]}
    text_output = rispy.dumps(ris_data)

    # check output is as expected
    lines = text_output.splitlines()
    assert lines[9] == "JP  - CRISPR"
    assert lines[10] == "ED  - Swinburne, Ricardo"
    assert len(lines) == 12


def test_default_dump(ris_data):
    text_output = rispy.dumps(ris_data)
    lines = text_output.splitlines()
    assert lines[2] == "AU  - Shannon, Claude E."
    assert lines[3] == "AU  - Doe, John"
    assert lines[7] == "UR  - https://example.com"
    assert lines[8] == "UR  - https://example2.com"
    assert len(lines) == 10


def test_delimited_dump(ris_data):
    # remove URLs from list_tags and give it a custom delimiter
    text_output = rispy.dumps(ris_data, list_tags=["AU"], delimiter_tags_mapping={"UR": ","})

    # check output is as expected
    lines = text_output.splitlines()
    assert lines[2] == "AU  - Shannon, Claude E."
    assert lines[3] == "AU  - Doe, John"
    assert lines[7] == "UR  - https://example.com,https://example2.com"
    assert len(lines) == 9


def test_dump_path(tmp_path, ris_data):
    # check that dump works with a Path object
    path = tmp_path / "file.ris"
    rispy.dump(ris_data, path)
    assert len(path.read_text()) > 0


def test_bad_dump(ris_data):
    with pytest.raises(ValueError, match="File must be a file-like object or a Path object"):
        rispy.dump(ris_data, 123)  # type: ignore
