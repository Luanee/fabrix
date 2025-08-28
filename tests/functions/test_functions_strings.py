import pytest

from fabrix.context import Context
from fabrix.evaluate import evaluate


@pytest.fixture
def ctx() -> Context:
    return Context()


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@concat('foo', 'bar')", "foobar"),
        ("@concat('foo', 42)", "foo42"),
        ("@concat('a', 'b', 'c')", "abc"),
        ("@concat('Baba', '''s ', 'book store')", "Baba's book store"),
    ],
)
def test_concat(ctx: Context, expr: str, expected: str) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@endsWith('foobar', 'bar')", True),
        ("@endsWith('foobar', 'baz')", False),
        ("@endsWith('foobar', 'foobar')", True),
    ],
)
def test_endswith(ctx: Context, expr: str, expected: bool) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@indexOf('abcdef', 'cd')", 2),
        ("@indexOf('abcdef', 'gh')", 0),
        ("@indexOf('abcdef', 'a')", 0),
    ],
)
def test_indexof(ctx: Context, expr: str, expected: int) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@replace('aabbcc', 'bb', 'zz')", "aazzcc"),
        ("@replace('abcabc', 'abc', 'x')", "xx"),
        ("@replace('foo', 'bar', 'baz')", "foo"),
    ],
)
def test_replace(ctx: Context, expr: str, expected: str) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@split('a,b,c')", ["a", "b", "c"]),
        ("@split('one|two|three', '|')", ["one", "two", "three"]),
        ("@split('no-delim')", ["no-delim"]),
    ],
)
def test_split(ctx: Context, expr: str, expected: list[str]) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@startsWith('foobar', 'foo')", True),
        ("@startsWith('foobar', 'bar')", False),
        ("@startsWith('foobar', 'foobar')", True),
    ],
)
def test_startswith(ctx: Context, expr: str, expected: bool) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@substring('abcdef', 2, 3)", "cde"),
        ("@substring('abcdef', 2)", "cdef"),
        ("@substring('abcdef', 0, 2)", "ab"),
    ],
)
def test_substring(ctx: Context, expr: str, expected: str) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@toLower('FooBar')", "foobar"),
        ("@toLower('FOO')", "foo"),
        ("@toLower('bar')", "bar"),
    ],
)
def test_to_lower(ctx: Context, expr: str, expected: str) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@toUpper('FooBar')", "FOOBAR"),
        ("@toUpper('foo')", "FOO"),
        ("@toUpper('bar')", "BAR"),
    ],
)
def test_to_upper(ctx: Context, expr: str, expected: str) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@trim('  abc  ')", "abc"),
        ("@trim('\txyz\t')", "xyz"),
        ("@trim('no-trim')", "no-trim"),
    ],
)
def test_trim(ctx: Context, expr: str, expected: str) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@lastIndexOf('hello', 'h')", 0),
        ("@lastIndexOf('hello', 'l')", 3),
        ("@lastIndexOf('hello', 'y')", 0),
    ],
)
def test_last_index_of(ctx: Context, expr: str, expected: str) -> None:
    assert evaluate(expr, ctx) == expected


def test_guid(ctx: Context) -> None:
    expression = "@guid()"
    assert isinstance(evaluate(expression, ctx), str)
