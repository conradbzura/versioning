import pytest
from src.versioning._version import parser, __version_parsers__

@parser("test")
def _() -> str:
    return "1.0.0"

def test_parser():
    assert "test" in __version_parsers__
    assert __version_parsers__["test"]() == "1.0.0"
