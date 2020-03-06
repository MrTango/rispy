from pathlib import Path

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
