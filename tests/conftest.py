import contextlib
import inspect
import os

import debugpy
import pytest
import yaml


class UndefinedType:
    """Represents an undefined value in tests."""

    def __repr__(self):
        return "Undefined"
    

Undefined = UndefinedType()


class folded(str):
    """Represents a folded string in YAML."""
    pass


def folded_unicode_representer(dumper, data):
    """Represents folded unicode strings in YAML."""
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=">")


yaml.add_representer(folded, folded_unicode_representer)


class ExpectedResult:
    """
    Context manager for comparing against stored expected results in tests.

    Args:
        test_class: The test class.
        test_function: The test function.
        test_input: The test input.
        copy_actual_to_expected (bool): Whether to copy actual results to expected results.
    """

    actual: list | dict | UndefinedType = Undefined

    def __init__(
        self,
        test_class,
        test_function,
        test_input,
        copy_actual_to_expected=False,
    ):
        filename = ".".join(
            [
                test_class.__module__,
                test_class.__name__,
                test_function.__name__,
                "yaml",
            ]
            if test_class
            else [test_function.__module__, "yaml"]
        )
        filename = filename.replace("tests.", "")
        filedir = os.path.dirname(
            os.path.realpath(inspect.getfile(test_function))
        )
        self.filepath = os.path.join(filedir, filename)
        self._key = repr(test_input) if test_input else Undefined
        self.copy_actual_to_expected = copy_actual_to_expected

    def __enter__(self):
        return self

    def __exit__(self, *_):
        if self.actual is not Undefined and self.copy_actual_to_expected:
            try:
                with open(self.filepath, "r") as file:
                    expected = yaml.load(file, Loader=yaml.FullLoader)
            except FileNotFoundError:
                expected = {}
            if self._key is not Undefined:
                expected[self._key] = self.actual
            else:
                if isinstance(self.actual, dict):
                    expected = {k: folded(v) for k, v in self.actual.items()}
                elif isinstance(self.actual, list):
                    expected = self.actual
                else:
                    raise RuntimeError(
                        "Actual result must be a list or a dictionary."
                    )
            if self.copy_actual_to_expected:
                with open(self.filepath, "w") as file:
                    try:
                        yaml.dump(expected, file, sort_keys=True, indent=4)
                    except TypeError:
                        file.seek(0)
                        file.truncate()
                        yaml.dump({}, file)
                        raise

    def __eq__(self, actual):
        try:
            assert self.__expected == actual
        except AssertionError:
            self.actual = actual
            raise
        else:
            return True

    @property
    def __expected(self):
        try:
            with open(self.filepath, "r") as file:
                return (
                    yaml.load(file, Loader=yaml.FullLoader)[self._key]
                    if self._key is not Undefined
                    else yaml.load(file, Loader=yaml.FullLoader)
                )
        except FileNotFoundError:
            return Undefined

    @contextlib.contextmanager
    def key(self, key):
        default_key = self._key
        self._key = key
        yield
        self._key = default_key


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """Configures pytest to wait for a debugger to attach if the 
    --wait-for-debugger option is set."""
    if config.getoption("--wait-for-debugger"):
        print("Waiting for debugger to attach...")
        debugpy.listen(("0.0.0.0", 5678))
        debugpy.wait_for_client()
        print("Debugger attached.")


@pytest.fixture
def expected(request):
    """Fixture for handling expected results in tests."""
    with ExpectedResult(
        request.cls,
        request.function,
        request.node.funcargs,
        request.config.getoption("copy_actual_to_expected"),
    ) as expected:
        yield expected


def pytest_addoption(parser):
    """Adds custom command-line options to pytest."""
    parser.addoption(
        "--copy-actual-to-expected",
        dest="copy_actual_to_expected",
        action="store_true",
    )
    parser.addoption(
        "-D",
        "--wait-for-debugger",
        action="store_true",
        default=False,
        help="Wait for a debugpy client to attach before running tests",
    )
