import base64

import pytest

from fabrix.context import Context
from fabrix.evaluate import evaluate


@pytest.fixture
def ctx() -> Context:
    return Context()


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@int('42')", 42),
        ("@int(3.5)", 3),
        ("@int(true)", 1),
    ],
)
def test_int(ctx: Context, expr: str, expected: int) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@float('3.14')", 3.14),
        ("@float(10)", 10.0),
        ("@float(true)", 1.0),
    ],
)
def test_float(ctx: Context, expr: str, expected: float) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@bool('true')", True),
        ("@bool(0)", False),
        ("@bool('yes')", True),
    ],
)
def test_bool(ctx: Context, expr: str, expected: bool) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@string(42)", "42"),
        ("@string(true)", "true"),
        ("@string({ 'name': 'Sophie Owen' })", "{'name':'Sophie Owen'}"),
    ],
)
def test_string(ctx: Context, expr: str, expected: str) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@base64('foo')", base64.b64encode(b"foo").decode()),
        ("@base64('bar')", base64.b64encode(b"bar").decode()),
        ("@base64('')", base64.b64encode(b"").decode()),
    ],
)
def test_base64(ctx: Context, expr: str, expected: str) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@base64ToString('Zm9v')", "foo"),
        ("@base64ToString('YmFy')", "bar"),
        ("@base64ToString('')", ""),
    ],
)
def test_base64_to_string(ctx: Context, expr: str, expected: str) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@coalesce(null, true, false)", True),
        ("@coalesce(null, 'hello', 'world')", "hello"),
        ("@coalesce(null, null, null)", None),
    ],
)
def test_coalesce(ctx: Context, expr: str, expected: str) -> None:
    assert evaluate(expr, ctx) == expected
