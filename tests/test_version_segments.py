import pytest

from versioning._version import (
    AlphanumericVersionSegment,
    NumericVersionSegment,
    PreReleaseVersionSegment,
)


class TestNumericVersionSegment:
    @pytest.mark.parametrize(
        "arg, format, expected",
        [
            (1, "{}", "1"),
            (None, "{}", ""),
        ],
    )
    def test_new(self, arg, format, expected):
        if arg is not None and arg < 0:
            with pytest.raises(ValueError):
                NumericVersionSegment(arg, format)
        else:
            segment = NumericVersionSegment(arg, format)
            assert segment.render() == expected

    @pytest.mark.parametrize(
        "left_arg, right_arg, expected",
        [
            (1, 1, True),
            (1, 2, False),
        ],
    )
    def test_eq(self, left_arg, right_arg, expected):
        left = NumericVersionSegment(left_arg, format="{}")
        right = NumericVersionSegment(right_arg, format="{}")
        assert (left == right) == expected

    @pytest.mark.parametrize(
        "left_arg, right_arg, expected",
        [
            (1, 2, True),
            (2, 1, False),
        ],
    )
    def test_lt(self, left_arg, right_arg, expected):
        left = NumericVersionSegment(left_arg, format="{}")
        right = NumericVersionSegment(right_arg, format="{}")
        assert (left < right) == expected

    @pytest.mark.parametrize(
        "arg, format, expected",
        [
            (1, "{}", "1"),
            (None, "{}", ""),
        ],
    )
    def test_render(self, arg, format, expected):
        segment = NumericVersionSegment(arg, format)
        assert segment.render() == expected


class TestAlphanumericVersionSegment:
    @pytest.mark.parametrize(
        "arg, format, expected",
        [
            ("alpha", "{}", "alpha"),
            (None, "{}", ""),
        ],
    )
    def test_new(self, arg, format, expected):
        if arg == "":
            with pytest.raises(ValueError):
                AlphanumericVersionSegment(arg, format)
        else:
            segment = AlphanumericVersionSegment(arg, format)
            assert segment.render() == expected

    @pytest.mark.parametrize(
        "left_arg, right_arg, expected",
        [
            ("alpha", "alpha", True),
            ("alpha", "beta", False),
        ],
    )
    def test_eq(self, left_arg, right_arg, expected):
        left = AlphanumericVersionSegment(left_arg, format="{}")
        right = AlphanumericVersionSegment(right_arg, format="{}")
        assert (left == right) == expected

    @pytest.mark.parametrize(
        "left_arg, right_arg, expected",
        [
            ("alpha", "beta", True),
            ("beta", "alpha", False),
        ],
    )
    def test_lt(self, left_arg, right_arg, expected):
        left = AlphanumericVersionSegment(left_arg, format="{}")
        right = AlphanumericVersionSegment(right_arg, format="{}")
        assert (left < right) == expected

    @pytest.mark.parametrize(
        "arg, format, expected",
        [
            ("alpha", "{}", "alpha"),
            (None, "{}", ""),
        ],
    )
    def test_render(self, arg, format, expected):
        segment = AlphanumericVersionSegment(arg, format)
        assert segment.render() == expected


class TestPreReleaseVersionSegment:
    @pytest.mark.parametrize(
        "args, format, expected",
        [
            (("alpha", 1), "-{}", "-alpha.1"),
            ((), "-{}", ""),
        ],
    )
    def test_new(self, args, format, expected):
        segment = PreReleaseVersionSegment(*args, format=format)
        assert segment.render() == expected

    @pytest.mark.parametrize(
        "left_args, right_args, expected",
        [
            (("alpha", 1), ("alpha", 1), True),
            (("alpha", 1), ("beta", 2), False),
            (("alpha", 1), (), False),
        ],
    )
    def test_eq(self, left_args, right_args, expected):
        left = PreReleaseVersionSegment(*left_args)
        right = PreReleaseVersionSegment(*right_args)
        assert (left == right) == expected

    @pytest.mark.parametrize(
        "left_args, right_args, expected",
        [
            (("alpha", 1), ("beta", 2), True),
            ((), ("alpha", 1), False),
            (("alpha", 1), ("alpha", 1), False),
            (("alpha", 1), ("alpha",), False),
        ],
    )
    def test_lt(self, left_args, right_args, expected):
        left = PreReleaseVersionSegment(*left_args)
        right = PreReleaseVersionSegment(*right_args)
        assert (left < right) == expected

    @pytest.mark.parametrize(
        "args, format, expected",
        [
            (("alpha", 1), "-{}", "-alpha.1"),
            ((), "-{}", ""),
        ],
    )
    def test_render(self, args, format, expected):
        segment = PreReleaseVersionSegment(*args, format=format)
        assert segment.render() == expected
