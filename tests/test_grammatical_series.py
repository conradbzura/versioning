from utils import Input
from versioning._version import grammatical_series


def test_grammatical_series(expected):
    inputs = [
        ("apple",),
        ("apple", "banana"),
        ("apple", "banana", "cherry"),
        ("apple", "banana, mango", "cherry"),
    ]
    assert expected == {
        f"grammatical_series({Input(*i)})": grammatical_series(*i)
        for i in inputs
    }
