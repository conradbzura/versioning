import itertools
from typing import Final

Undefined: Final = object()


def parametrize(*arg_bounds, **kwarg_bounds):
    """
    Generates combinations of arguments and keyword arguments for parameterized
    tests.

    Args:
        *arg_bounds: Boundaries for positional arguments.
        **kwarg_bounds: Boundaries for keyword arguments.

    Yields:
        Input: An Input instance containing a combination of arguments and
        keyword arguments.

    Examples:
        >>> for input in parametrize((1, 2), a=(3, 4)):
        ...     print(input)
        1, a=3
        1, a=4
        2, a=3
        2, a=4
    """
    arg_combinations = map(
        lambda args: (
            tuple(args)
            if Undefined not in args
            else tuple(args[: args.index(Undefined)])
        ),
        itertools.product(*arg_bounds),
    )
    kwarg_combinations = map(
        lambda kwargs: ((k, v) for k, v in kwargs if v is not Undefined),
        itertools.product(
            *(itertools.product((k,), v) for k, v in kwarg_bounds.items())
        ),
    )
    for args, kwargs in itertools.product(
        set(arg_combinations), kwarg_combinations
    ):
        yield Input(*args, **dict(kwargs))


def swap_quotes(string):
    return string.translate(str.maketrans({"'": '"', '"': "'"}))


class Input:
    """
    Represents a combination of arguments and keyword arguments for
    parameterized tests.

    Args:
        *args: Positional arguments.
        **kwargs: Keyword arguments.

    Examples:
        >>> input = Input(1, 2, a=3, b=4)
        >>> print(input)
        1, 2, a=3, b=4
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        return ", ".join(
            (
                *(swap_quotes(repr(v)) for v in self.args),
                *(
                    f"{k}={swap_quotes(repr(v))}"
                    for k, v in self.kwargs.items()
                ),
            )
        )
