from contextlib import contextmanager

import pytest

from fabrix.context import Context
from fabrix.evaluate import evaluate
from fabrix.exceptions import ExpressionSyntaxError, FunctionNotFoundError


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
    result = evaluate(expression, ctx)
    assert result == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@concat('Result: ', string(if(greater(add(1, mul(2, 5)), 10), add(100, 1), 0)))", "Result: 101.0"),
        ("@formatDateTime(addToTime(pipeline().parameters.timestamp, mul(2, 3), 'Day'), '%Y/%m/%d')", "2024/01/07"),
        ("@if(contains(distinct(createArray('a', 'b', 'b', 'c')), 'c'), 'Found', 'Not found')", "Found"),
        ("@if(and(greater(variables('foo'), 5), lessOrEquals(variables('foo'), 10)), 'ok', 'fail')", "ok"),
        (
            "@if(less(length(concat(pipeline().parameters.prefix, string(variables('val')))), 8), 'short', 'long')",
            "short",
        ),
    ],
)
def test_complex_nested_expressions(ctx: Context, expr: str, expected: str) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr, expected",
    [
        ("@activity('CopyData').output.rows[0].value", 10),
        ("@activity('CopyData').output.rows[pipeline().parameters.idx].value", 20),
        ("@activity('CopyData').output.meta.ok", True),
        ("@activity('CopyData').output.meta.tags[variables('row_index')]", "a"),
        ("@activity('Bobs Task').output.result.message", "done"),
        ("@activity('CopyData').output.rows[add(1,1)].value", 30),
    ],
)
def test_activity_expressions(ctx: Context, expr: str, expected: str | int | bool) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr, error_pattern",
    [
        ("@activity('Missing').output.rows[0].value", r"Activity 'Missing'.*not available"),
        ("@activity('CopyData').output.nonesuch", r"Missing field 'nonesuch'"),
        ("@activity('CopyData').output.rows['x'].value", r"Invalid index/field \['x'\]"),
        ("@activity('CopyData').output.rows[99].value", r"Invalid index/field \[99\]"),
    ],
)
def test_activity_expressions_errors(ctx: Context, expr: str, error_pattern: str) -> None:
    with pytest.raises(KeyError, match=error_pattern):
        evaluate(expr, ctx)


@pytest.mark.parametrize(
    "expr,exception,error",
    [
        (
            "@addd(add(1,1),1)",
            FunctionNotFoundError,
            r"Function 'addd'.*Did you mean 'add'\?",
        ),
        (
            "@base64ToString('aGVsbG8='",
            ExpressionSyntaxError,
            r"Unmatched '\(' at position \d+\.",
        ),
        (
            "Hallo: @pipeline().parameters.test}",
            ExpressionSyntaxError,
            r"Expression must start with '@' or contain an interpolation like '@\{ \.\.\. \}'.",
        ),
        (
            '@concat("Baba", "\'s", "book store")',
            ExpressionSyntaxError,
            r"Double quotes are not allowed. Use single quotes \('\).",
        ),
    ],
)
def test_expressions_validation(ctx: Context, expr: str, exception: type[Exception], error: str) -> None:
    with pytest.raises(exception, match=error):
        evaluate(expr, ctx)
