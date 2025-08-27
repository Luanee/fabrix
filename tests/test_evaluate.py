from contextlib import contextmanager

import pytest

from fabrix.context import Context
from fabrix.evaluate import evaluate


@pytest.mark.parametrize(
    "expression,expected",
    [
        ("@pipeline().parameters.myString", "foo"),
        ("@{pipeline().parameters.myString}", "foo"),
        ("@pipeline().parameters.myNumber", 42),
        ("@{pipeline().parameters.myNumber}", "42"),
        ("Answer is: @{pipeline().parameters.myNumber}", "Answer is: 42"),
        ("@concat('Answer is: ', string(pipeline().parameters.myNumber))", "Answer is: 42"),
        ("Answer is: @@{pipeline().parameters.myNumber}", "Answer is: @{pipeline().parameters.myNumber}"),
    ],
)
def test_fabric_expressions(ctx: Context, expression: str, expected: str | int) -> None:
    with pytest.raises(NotImplementedError):
        evaluate(expression, ctx)
