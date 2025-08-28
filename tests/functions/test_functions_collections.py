import pytest

from fabrix.context import Context
from fabrix.evaluate import evaluate


@pytest.fixture
def ctx() -> Context:
    return Context()


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@contains(createArray(1, 2, 3), 2)", True),
        ("@contains(createArray('a', 'b'), 'c')", False),
        ("@contains('hello', 'e')", True),
    ],
)
def test_contains(ctx: Context, expr: str, expected: bool) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@empty('')", True),
        ("@empty(createArray())", True),
        ("@empty('x')", False),
    ],
)
def test_empty(ctx: Context, expr: str, expected: bool) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@length('foo')", 3),
        ("@length(createArray(1, 2, 3))", 3),
        ("@length('')", 0),
    ],
)
def test_length(ctx: Context, expr: str, expected: int) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@first(createArray('a', 'b', 'c'))", "a"),
        ("@first('xyz')", "x"),
        ("@first(createArray())", None),
    ],
)
def test_first(ctx: Context, expr: str, expected: str | None) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@last(createArray('a', 'b', 'c'))", "c"),
        ("@last('xyz')", "z"),
        ("@last(createArray())", None),
    ],
)
def test_last(ctx: Context, expr: str, expected: str | None) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@distinct(createArray(1, 1, 2, 2, 3))", [1, 2, 3]),
        ("@distinct('aabbcc')", ["a", "b", "c"]),
        ("@distinct(createArray())", []),
    ],
)
def test_distinct(ctx: Context, expr: str, expected: list) -> None:
    assert evaluate(expr, ctx) == expected
