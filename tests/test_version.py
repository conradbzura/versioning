import itertools
from contextlib import ExitStack
from unittest.mock import PropertyMock

import pytest
from utils import Input, Undefined, parametrize

from versioning._version import (
    AlphanumericVersionSegment,
    NumericVersionSegment,
    PreReleaseVersionSegment,
    PythonicVersion,
    ReleaseCycle,
    SemanticVersion,
)


class TestNumericVersionSegment:
    @pytest.mark.parametrize(
        "arg, format, expected",
        [
            (1, "{}", "1"),
            (None, "{}", ""),
        ],
    )
    def test___new__(self, arg, format, expected):
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
    def test___eq__(self, left_arg, right_arg, expected):
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
    def test___lt__(self, left_arg, right_arg, expected):
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
    def test___new__(self, arg, format, expected):
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
    def test___eq__(self, left_arg, right_arg, expected):
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
    def test___lt__(self, left_arg, right_arg, expected):
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
    def test___new__(self, args, format, expected):
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
    def test___eq__(self, left_args, right_args, expected):
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
    def test___lt__(self, left_args, right_args, expected):
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


class TestReleaseCycle:

    @pytest.mark.parametrize(
        "left, right, expected",
        [
            (ReleaseCycle.Alpha, ReleaseCycle.Beta, True),
            (ReleaseCycle.Beta, ReleaseCycle.ReleaseCandidate, True),
            (ReleaseCycle.ReleaseCandidate, ReleaseCycle.Production, True),
            (ReleaseCycle.Production, ReleaseCycle.Alpha, False),
        ],
    )
    def test___lt__(self, left, right, expected):
        assert (left < right) == expected

    @pytest.mark.parametrize(
        "cycle, expected",
        [
            (ReleaseCycle.Alpha, "a"),
            (ReleaseCycle.Beta, "b"),
            (ReleaseCycle.ReleaseCandidate, "rc"),
            (ReleaseCycle.Production, "."),
        ],
    )
    def test_render(self, cycle, expected):
        assert cycle.render() == expected


class TestPythonicVersion:
    KWARG_BOUNDS = {
        "epoch": (Undefined,),
        "major_release": (Undefined, None, 2),
        "minor_release": (Undefined, None, 3),
        "release_cycle": (Undefined, None, "."),
        "patch_release": (Undefined, None, 4),
        "post_release": (Undefined, None, 5),
        "dev_release": (Undefined, None, 6),
        "local_identifier": (Undefined, None, "foo"),
    }
    ARG_BOUNDS = KWARG_BOUNDS.values()

    @property
    def inputs(self):
        yield from parametrize(*self.ARG_BOUNDS)
        yield from parametrize(**self.KWARG_BOUNDS)

    def test___init__(self, expected):
        input_families = (
            {
                "epoch": (Undefined, None, 1),
                "major_release": (Undefined, 2),
                "minor_release": (3,),
                "release_cycle": (".",),
                "patch_release": (4,),
                "post_release": (Undefined, None, 5),
                "dev_release": (Undefined, None, 6),
                "local_identifier": (Undefined, None, "foo"),
            },
            {
                "major_release": (None,),
            },
            {
                "minor_release": (
                    Undefined,
                    None,
                    3,
                ),
                "release_cycle": (
                    Undefined,
                    None,
                    ".",
                ),
                "patch_release": (
                    Undefined,
                    None,
                    4,
                ),
            },
        )
        actual = {}
        for input_family in input_families:
            for input in parametrize(**input_family):
                try:
                    assert PythonicVersion(**input.kwargs)
                except Exception as e:
                    actual[f"PythonicVersion({input})"] = f"raises {repr(e)}"
        assert expected == actual

    def test___eq__(self, mocker):
        version = PythonicVersion(major_release=1, minor_release=0)
        segments = [
            mocker.patch.object(
                PythonicVersion, key, new_callable=PropertyMock
            )
            for key, value in PythonicVersion.segments.items()
        ]
        assert version == version
        assert all(s.return_value.__eq__.called for s in segments)

    @pytest.mark.parametrize(
        ("left", "right", "expected"),
        (
            (PythonicVersion(1, 0), PythonicVersion(1, 0), False),
            (PythonicVersion(1, 1), PythonicVersion(1, 0), False),
            (PythonicVersion(1, 0), PythonicVersion(1, 1), True),
        ),
    )
    def test___lt__(self, left, right, expected):
        assert expected == (left < right)

    def test___getitem__(self, expected):
        version = PythonicVersion(
            major_release=1,
            minor_release=0,
            patch_release=0,
            release_cycle=".",
        )
        assert version["major_release"] == NumericVersionSegment(1, "{}")
        assert version["minor_release"] == NumericVersionSegment(0, ".{}")
        assert version["patch_release"] == NumericVersionSegment(0, "{}")

    def test___iter__(self):
        version = PythonicVersion(
            major_release=1,
            minor_release=0,
            patch_release=0,
            release_cycle=".",
        )
        segments = list(version)
        assert "major_release" in segments
        assert "minor_release" in segments
        assert "patch_release" in segments

    @pytest.mark.parametrize(
        ("input", "output"),
        (
            (Input(), "<PythonicVersion: '0'>"),
            (
                Input(epoch=0),
                "<PythonicVersion: '0!0'>",
            ),
            (
                Input(epoch=1),
                "<PythonicVersion: '1!0'>",
            ),
            (
                Input(major_release=0),
                "<PythonicVersion: '0'>",
            ),
            (
                Input(major_release=1),
                "<PythonicVersion: '1'>",
            ),
            (
                Input(minor_release=0, release_cycle=0, patch_release=0),
                "<PythonicVersion: '0.0a0'>",
            ),
            (
                Input(minor_release=1, release_cycle=2, patch_release=3),
                "<PythonicVersion: '0.1rc3'>",
            ),
            (
                Input(post_release=0),
                "<PythonicVersion: '0.post0'>",
            ),
            (
                Input(post_release=1),
                "<PythonicVersion: '0.post1'>",
            ),
            (
                Input(dev_release=0),
                "<PythonicVersion: '0.dev0'>",
            ),
            (
                Input(dev_release=1),
                "<PythonicVersion: '0.dev1'>",
            ),
            (
                Input(local_identifier="0"),
                "<PythonicVersion: '0+0'>",
            ),
            (
                Input(local_identifier="a"),
                "<PythonicVersion: '0+a'>",
            ),
            (
                Input(local_identifier="A"),
                "<PythonicVersion: '0+A'>",
            ),
            (
                Input(local_identifier="0aA"),
                "<PythonicVersion: '0+0aA'>",
            ),
            (
                Input(
                    epoch=1,
                    major_release=2,
                    minor_release=3,
                    release_cycle=".",
                    patch_release=4,
                    post_release=5,
                    dev_release=6,
                    local_identifier="foo",
                ),
                "<PythonicVersion: '1!2.3.4.post5.dev6+foo'>",
            ),
        ),
    )
    def test___repr__(self, input, output):
        assert output == repr(PythonicVersion(*input.args, **input.kwargs))

    @pytest.mark.parametrize(
        ("input", "output"),
        (
            (Input(), "0"),
            (
                Input(epoch=0),
                "0!0",
            ),
            (
                Input(epoch=1),
                "1!0",
            ),
            (
                Input(major_release=0),
                "0",
            ),
            (
                Input(major_release=1),
                "1",
            ),
            (
                Input(minor_release=0, release_cycle=0, patch_release=0),
                "0.0a0",
            ),
            (
                Input(minor_release=1, release_cycle=2, patch_release=3),
                "0.1rc3",
            ),
            (
                Input(post_release=0),
                "0.post0",
            ),
            (
                Input(post_release=1),
                "0.post1",
            ),
            (
                Input(dev_release=0),
                "0.dev0",
            ),
            (
                Input(dev_release=1),
                "0.dev1",
            ),
            (
                Input(local_identifier="0"),
                "0+0",
            ),
            (
                Input(local_identifier="a"),
                "0+a",
            ),
            (
                Input(local_identifier="A"),
                "0+A",
            ),
            (
                Input(local_identifier="0aA"),
                "0+0aA",
            ),
            (
                Input(
                    epoch=1,
                    major_release=2,
                    minor_release=3,
                    release_cycle=".",
                    patch_release=4,
                    post_release=5,
                    dev_release=6,
                    local_identifier="foo",
                ),
                "1!2.3.4.post5.dev6+foo",
            ),
        ),
    )
    def test___str__(self, input, output):
        assert output == str(PythonicVersion(*input.args, **input.kwargs))

    def test_segments(self, expected):
        assert expected == list(PythonicVersion.segments)

    def test_keys(self):
        version = PythonicVersion(
            major_release=1,
            minor_release=0,
            patch_release=0,
            release_cycle=".",
        )
        keys = version.keys()
        assert "major_release" in keys
        assert "minor_release" in keys
        assert "patch_release" in keys

    def test_items(self):
        version = PythonicVersion(
            major_release=1,
            minor_release=0,
            patch_release=0,
            release_cycle=".",
        )
        items = version.items()
        assert ("major_release", NumericVersionSegment(1, "{}")) in items
        assert ("minor_release", NumericVersionSegment(0, ".{}")) in items
        assert ("patch_release", NumericVersionSegment(0, "{}")) in items

    def test_values(self):
        version = PythonicVersion(
            major_release=1,
            minor_release=0,
            patch_release=0,
            release_cycle=".",
        )
        values = version.values()
        assert NumericVersionSegment(1, "{}") in values
        assert NumericVersionSegment(0, ".{}") in values
        assert NumericVersionSegment(0, "{}") in values


class TestSemanticVersion:
    KWARG_BOUNDS = {
        "major_release": (Undefined, None, 2),
        "minor_release": (Undefined, None, 3),
        "patch_release": (Undefined, None, 4),
        "pre_release": (Undefined, None, 5, "alpha"),
        "build": (Undefined, None, "foo"),
    }
    ARG_BOUNDS = KWARG_BOUNDS.values()

    @property
    def inputs(self):
        yield from parametrize(*self.ARG_BOUNDS)
        yield from parametrize(**self.KWARG_BOUNDS)

    def test___init__(self, expected):
        input_families = (
            {
                "major_release": (Undefined, 2),
                "minor_release": (3,),
                "patch_release": (4,),
                "pre_release": (Undefined, None, 5, "alpha"),
                "build": (Undefined, None, "foo"),
            },
            {
                "major_release": (None,),
            },
            {
                "minor_release": (
                    Undefined,
                    None,
                    3,
                ),
                "patch_release": (
                    Undefined,
                    None,
                    4,
                ),
            },
        )
        actual = {}
        for input_family in input_families:
            for input in parametrize(**input_family):
                try:
                    assert SemanticVersion(**input.kwargs)
                except Exception as e:
                    actual[f"SemanticVersion({input})"] = f"raises {repr(e)}"
        assert expected == actual

    def test___eq__(self, mocker):
        version = SemanticVersion(major_release=1, minor_release=0)
        segments = [
            mocker.patch.object(
                SemanticVersion, key, new_callable=PropertyMock
            )
            for key, value in SemanticVersion.segments.items()
        ]
        assert version == version
        assert all(s.return_value.__eq__.called for s in segments)

    @pytest.mark.parametrize(
        ("left", "right", "expected"),
        (
            (SemanticVersion(1, 0), SemanticVersion(1, 0), False),
            (SemanticVersion(1, 1), SemanticVersion(1, 0), False),
            (SemanticVersion(1, 0), SemanticVersion(1, 1), True),
        ),
    )
    def test___lt__(self, left, right, expected):
        assert expected == (left < right)

    def test___getitem__(self, expected):
        version = SemanticVersion(
            major_release=1,
            minor_release=0,
            patch_release=0,
        )
        assert version["major_release"] == NumericVersionSegment(1, "{}")
        assert version["minor_release"] == NumericVersionSegment(0, ".{}")
        assert version["patch_release"] == NumericVersionSegment(0, "{}")

    def test___iter__(self):
        version = SemanticVersion(
            major_release=1,
            minor_release=0,
            patch_release=0,
        )
        segments = list(version)
        assert "major_release" in segments
        assert "minor_release" in segments
        assert "patch_release" in segments

    @pytest.mark.parametrize(
        ("input", "output"),
        (
            (Input(), "<SemanticVersion: '0'>"),
            (
                Input(major_release=0),
                "<SemanticVersion: '0'>",
            ),
            (
                Input(major_release=1),
                "<SemanticVersion: '1'>",
            ),
            (
                Input(minor_release=0, patch_release=0),
                "<SemanticVersion: '0.0.0'>",
            ),
            (
                Input(minor_release=1, patch_release=3),
                "<SemanticVersion: '0.1.3'>",
            ),
            (
                Input(pre_release=0),
                "<SemanticVersion: '0-0'>",
            ),
            (
                Input(pre_release=1),
                "<SemanticVersion: '0-1'>",
            ),
            (
                Input(build="0"),
                "<SemanticVersion: '0+0'>",
            ),
            (
                Input(build="a"),
                "<SemanticVersion: '0+a'>",
            ),
            (
                Input(build="A"),
                "<SemanticVersion: '0+A'>",
            ),
            (
                Input(build="0aA"),
                "<SemanticVersion: '0+0aA'>",
            ),
            (
                Input(
                    major_release=2,
                    minor_release=3,
                    patch_release=4,
                    pre_release="alpha",
                    build="foo",
                ),
                "<SemanticVersion: '2.3.4-alpha+foo'>",
            ),
        ),
    )
    def test___repr__(self, input, output):
        assert output == repr(SemanticVersion(*input.args, **input.kwargs))

    @pytest.mark.parametrize(
        ("input", "output"),
        (
            (Input(), "0"),
            (
                Input(major_release=0),
                "0",
            ),
            (
                Input(major_release=1),
                "1",
            ),
            (
                Input(minor_release=0, patch_release=0),
                "0.0.0",
            ),
            (
                Input(minor_release=1, patch_release=3),
                "0.1.3",
            ),
            (
                Input(pre_release=0),
                "0-0",
            ),
            (
                Input(pre_release=1),
                "0-1",
            ),
            (
                Input(build="0"),
                "0+0",
            ),
            (
                Input(build="a"),
                "0+a",
            ),
            (
                Input(build="A"),
                "0+A",
            ),
            (
                Input(build="0aA"),
                "0+0aA",
            ),
            (
                Input(
                    major_release=2,
                    minor_release=3,
                    patch_release=4,
                    pre_release="alpha",
                    build="foo",
                ),
                "2.3.4-alpha+foo",
            ),
        ),
    )
    def test___str__(self, input, output):
        assert output == str(SemanticVersion(*input.args, **input.kwargs))

    def test_segments(self, expected):
        assert expected == list(SemanticVersion.segments)

    def test_keys(self):
        version = SemanticVersion(
            major_release=1,
            minor_release=0,
            patch_release=0,
        )
        keys = version.keys()
        assert "major_release" in keys
        assert "minor_release" in keys
        assert "patch_release" in keys

    def test_items(self):
        version = SemanticVersion(
            major_release=1,
            minor_release=0,
            patch_release=0,
        )
        items = version.items()
        assert ("major_release", NumericVersionSegment(1, "{}")) in items
        assert ("minor_release", NumericVersionSegment(0, ".{}")) in items
        assert ("patch_release", NumericVersionSegment(0, "{}")) in items

    def test_values(self):
        version = SemanticVersion(
            major_release=1,
            minor_release=0,
            patch_release=0,
        )
        values = version.values()
        assert NumericVersionSegment(1, "{}") in values
        assert NumericVersionSegment(0, ".{}") in values
        assert NumericVersionSegment(0, "{}") in values
