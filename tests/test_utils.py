import pytest

from rispy.utils import invert_dictionary


def test_invert_dictionary():
    d = {"a": "b"}
    assert invert_dictionary(d) == {"b": "a"}


def test_invert_dictionary_failure():
    d = {"a": "b", "c": "b"}
    with pytest.raises(ValueError, match="Dictionary cannot be inverted"):
        invert_dictionary(d)
