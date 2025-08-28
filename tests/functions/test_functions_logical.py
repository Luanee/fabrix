import pytest

from fabrix.context import Context
from fabrix.evaluate import evaluate


@pytest.fixture
def ctx() -> Context:
    return Context()


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@and(true, true)", True),
        ("@and(true, false)", False),
        ("@and(false, false)", False),
    ],
)
def test_and(ctx: Context, expr: str, expected: bool) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@equals(1, 1)", True),
        ("@equals(1, 2)", False),
        ("@equals('foo', 'foo')", True),
    ],
)
def test_equals(ctx: Context, expr: str, expected: bool) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@greater(2, 1)", True),
        ("@greater(1, 2)", False),
        ("@greater(3, 3)", False),
    ],
)
def test_greater(ctx: Context, expr: str, expected: bool) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@if(true, 'yes', 'no')", "yes"),
        ("@if(false, 'yes', 'no')", "no"),
        ("@if(1, 'one', 'zero')", "one"),
    ],
)
def test_if_func(ctx: Context, expr: str, expected: str) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@less(1, 2)", True),
        ("@less(2, 1)", False),
        ("@less(3, 3)", False),
    ],
)
def test_less(ctx: Context, expr: str, expected: bool) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@not(true)", False),
        ("@not(false)", True),
        ("@not(0)", True),
    ],
)
def test_not_func(ctx: Context, expr: str, expected: bool) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@or(true, false)", True),
        ("@or(false, false)", False),
        ("@or(true, true)", True),
    ],
)
def test_or(ctx: Context, expr: str, expected: bool) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@greaterOrEquals(5, 2)", True),
        ("@greaterOrEquals(2, 2)", True),
        ("@greaterOrEquals(1, 3)", False),
    ],
)
def test_greater_or_equals(ctx: Context, expr: str, expected: bool) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@lessOrEquals(2, 5)", True),
        ("@lessOrEquals(2, 2)", True),
        ("@lessOrEquals(3, 1)", False),
    ],
)
def test_less_or_equals(ctx: Context, expr: str, expected: bool) -> None:
    assert evaluate(expr, ctx) == expected
