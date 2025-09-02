import pytest

from fabrix.context import Context
from fabrix.evaluate import evaluate


@pytest.fixture
def ctx() -> Context:
    return Context()


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@add(2, 3)", 5),
        ("@add(1.5, 2.5)", 4.0),
        ("@add(-1, 2)", 1),
    ],
)
def test_add(ctx: Context, expr: str, expected: int | float) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@sub(10, 2)", 8),
        ("@sub(5.5, 1.5)", 4.0),
        ("@sub(0, 7)", -7),
    ],
)
def test_sub(ctx: Context, expr: str, expected: int | float) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@mul(2, 3)", 6.0),
        ("@mul(4, 0.5)", 2.0),
        ("@mul(-2, 3)", -6.0),
    ],
)
def test_mul(ctx: Context, expr: str, expected: int | float) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@div(10, 2)", 5.0),
        ("@div(7, 2)", 3.5),
        ("@div(-6, 3)", -2.0),
    ],
)
def test_div(ctx: Context, expr: str, expected: int | float) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@mod(10, 3)", 1.0),
        ("@mod(7, 7)", 0.0),
        ("@mod(5, 2)", 1.0),
    ],
)
def test_mod(ctx: Context, expr: str, expected: int | float) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@max(1, 2, 3)", 3.0),
        ("@max(-5, 0, 5)", 5.0),
        ("@max(4.5, 2.1, 2.9)", 4.5),
    ],
)
def test_max(ctx: Context, expr: str, expected: int | float) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@min(1, 2, 3)", 1.0),
        ("@min(-5, 0, 5)", -5.0),
        ("@min(4.5, 2.1, 2.9)", 2.1),
    ],
)
def test_min(ctx: Context, expr: str, expected: int | float) -> None:
    assert evaluate(expr, ctx) == expected
