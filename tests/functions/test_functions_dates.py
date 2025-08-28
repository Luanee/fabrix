import datetime
from collections.abc import Generator
from typing import Any

import pytest
import pytz

from fabrix.context import Context
from fabrix.evaluate import evaluate


@pytest.fixture
def ctx() -> Context:
    return Context()


# Patch datetime.now to a fixed time for deterministic tests
class FixedDatetime(datetime.datetime):
    @classmethod
    def now(cls, tz=None):
        return cls(2024, 1, 1, 12, 0, 0, tzinfo=pytz.timezone("UTC"))


@pytest.fixture(autouse=True)
def patch_datetime_now(monkeypatch) -> Generator[None, Any, None]:
    import fabrix.functions.dates as date_functions

    monkeypatch.setattr(date_functions, "datetime", FixedDatetime)
    yield


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@addDays('2024-01-01T00:00:00', 1)", "2024-01-02T00:00:00+00:00"),
        ("@addDays('2024-01-01T00:00:00', -1)", "2023-12-31T00:00:00+00:00"),
        ("@addDays('2024-02-28T00:00:00', 1)", "2024-02-29T00:00:00+00:00"),  # Leap year!
    ],
)
def test_add_days(ctx: Context, expr: str, expected: str) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@addHours('2024-01-01T00:00:00', 1)", "2024-01-01T01:00:00+00:00"),
        ("@addHours('2024-01-01T00:00:00', -1)", "2023-12-31T23:00:00+00:00"),
        ("@addHours('2024-02-28T00:00:00', 1)", "2024-02-28T01:00:00+00:00"),  # Leap year!
    ],
)
def test_add_hours(ctx: Context, expr: str, expected: str) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@addMinutes('2024-01-01T00:00:00', 1)", "2024-01-01T00:01:00+00:00"),
        ("@addMinutes('2024-01-01T00:00:00', -1)", "2023-12-31T23:59:00+00:00"),
        ("@addMinutes('2024-02-28T00:00:00', 100)", "2024-02-28T01:40:00+00:00"),  # Leap year!
    ],
)
def test_add_minutes(ctx: Context, expr: str, expected: str) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@addSeconds('2024-01-01T00:00:00', 1)", "2024-01-01T00:00:01+00:00"),
        ("@addSeconds('2024-01-01T00:00:00', -1)", "2023-12-31T23:59:59+00:00"),
        ("@addSeconds('2024-02-29T00:00:00', 1)", "2024-02-29T00:00:01+00:00"),  # Leap year!
    ],
)
def test_add_seconds(ctx: Context, expr: str, expected: str) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@dayOfMonth('2024-01-02T00:00:00')", 2),
        ("@dayOfMonth('2024-12-31T12:34:56')", 31),
        ("@dayOfMonth('2024-02-29T23:59:59')", 29),
    ],
)
def test_day_of_month(ctx: Context, expr: str, expected: int) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@formatDateTime('2024-02-29T23:59:59', '%Y-%m-%d')", "2024-02-29"),
        ("@formatDateTime('2024-01-01T12:00:00', '%H:%M')", "12:00"),
        ("@formatDateTime('2024-12-31T23:59:59', '%d/%m/%Y')", "31/12/2024"),
    ],
)
def test_format_datetime(ctx: Context, expr: str, expected: str) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        (
            "@getFutureTime(1, 'days', '%Y-%m-%dT%H:%M:%S')",
            "2024-01-02T12:00:00",
        ),
        (
            "@getFutureTime(2, 'months', '%Y-%m-%dT%H:%M:%S')",
            "2024-03-01T12:00:00",
        ),
        (
            "@getFutureTime(3, 'years', '%Y-%m-%dT%H:%M:%S')",
            "2027-01-01T12:00:00",
        ),
    ],
)
def test_get_future_time(ctx: Context, expr: str, expected: str) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        (
            "@getPastTime(1, 'days', '%Y-%m-%dT%H:%M:%S')",
            "2023-12-31T12:00:00",
        ),
        (
            "@getPastTime(2, 'months', '%Y-%m-%dT%H:%M:%S')",
            "2023-11-01T12:00:00",
        ),
        (
            "@getPastTime(3, 'years', '%Y-%m-%dT%H:%M:%S')",
            "2021-01-01T12:00:00",
        ),
    ],
)
def test_get_past_time(ctx: Context, expr: str, expected: str) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        (
            "@subtractFromTime('2024-01-01T12:00:00', 1, 'days')",
            "2023-12-31T12:00:00+00:00",
        ),
        (
            "@subtractFromTime('2024-03-01T12:00:00', 2, 'months')",
            "2024-01-01T12:00:00+00:00",
        ),
        (
            "@subtractFromTime('2027-01-01T12:00:00', 3, 'years')",
            "2024-01-01T12:00:00+00:00",
        ),
    ],
)
def test_subtract_from_time(ctx: Context, expr: str, expected: str) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        (
            "@addToTime('2024-01-01T12:00:00', 1, 'days')",
            "2024-01-02T12:00:00+00:00",
        ),
        (
            "@addToTime('2024-01-01T12:00:00', 2, 'months')",
            "2024-03-01T12:00:00+00:00",
        ),
        (
            "@addToTime('2024-01-01T12:00:00', 3, 'years')",
            "2027-01-01T12:00:00+00:00",
        ),
    ],
)
def test_add_to_time(ctx: Context, expr: str, expected: str) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        (
            "@convertFromUtc('2024-01-01T12:00:00', 'Europe/Berlin')",
            "2024-01-01T13:00:00+01:00",
        ),
        (
            "@convertFromUtc('2024-06-01T12:00:00', 'Europe/Berlin')",
            "2024-06-01T14:00:00+02:00",
        ),
        (
            "@convertFromUtc('2024-01-01T00:00:00', 'America/New_York')",
            "2023-12-31T19:00:00-05:00",
        ),
    ],
)
def test_convert_from_utc(ctx: Context, expr: str, expected: str) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        (
            "@convertTimeZone('2024-01-01T12:00:00', 'UTC', 'Europe/Berlin')",
            "2024-01-01T13:00:00+01:00",
        ),
        (
            "@convertTimeZone('2024-01-01T12:00:00', 'Europe/Berlin', 'UTC')",
            "2024-01-01T11:00:00+00:00",
        ),
        (
            "@convertTimeZone('2024-01-01T12:00:00', 'UTC', 'America/New_York')",
            "2024-01-01T07:00:00-05:00",
        ),
    ],
)
def test_convert_time_zone(ctx: Context, expr: str, expected: str) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        (
            "@convertToUtc('2024-01-01T13:00:00', 'Europe/Berlin')",
            "2024-01-01T12:00:00+00:00",
        ),
        (
            "@convertToUtc('2024-01-01T07:00:00', 'America/New_York')",
            "2024-01-01T12:00:00+00:00",
        ),
        (
            "@convertToUtc('2024-01-01T12:00:00', 'UTC')",
            "2024-01-01T12:00:00+00:00",
        ),
    ],
)
def test_convert_to_utc(ctx: Context, expr: str, expected: str) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@dayOfWeek('2024-01-01T12:00:00')", 0),  # Monday=0 in Python/ADF
        ("@dayOfWeek('2024-01-02T12:00:00')", 1),
        ("@dayOfWeek('2024-01-07T12:00:00')", 6),
    ],
)
def test_day_of_week(ctx: Context, expr: str, expected: int) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@dayOfYear('2024-01-01T12:00:00')", 1),
        ("@dayOfYear('2024-12-31T12:00:00')", 366),  # Leap year!
        ("@dayOfYear('2023-12-31T12:00:00')", 365),
    ],
)
def test_day_of_year(ctx: Context, expr: str, expected: int) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@startOfDay('2024-01-01T12:34:56')", "2024-01-01T00:00:00+00:00"),
        ("@startOfDay('2024-02-28T23:59:59')", "2024-02-28T00:00:00+00:00"),
        ("@startOfDay('2024-12-31T12:00:00')", "2024-12-31T00:00:00+00:00"),
    ],
)
def test_start_of_day(ctx: Context, expr: str, expected: str) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@startOfHour('2024-01-01T12:34:56')", "2024-01-01T12:00:00+00:00"),
        ("@startOfHour('2024-02-28T23:59:59')", "2024-02-28T23:00:00+00:00"),
        ("@startOfHour('2024-12-31T00:45:00')", "2024-12-31T00:00:00+00:00"),
    ],
)
def test_start_of_hour(ctx: Context, expr: str, expected: str) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@startOfMonth('2024-01-31T12:00:00')", "2024-01-01T00:00:00+00:00"),
        ("@startOfMonth('2024-02-29T23:59:59')", "2024-02-01T00:00:00+00:00"),
        ("@startOfMonth('2024-12-15T12:00:00')", "2024-12-01T00:00:00+00:00"),
    ],
)
def test_start_of_month(ctx: Context, expr: str, expected: str) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@ticks('0001-01-01T00:00:00')", 0),
        ("@ticks('2024-01-01T00:00:00')", 638396640000000000),
        ("@ticks('1970-01-01T00:00:00')", 621355968000000000),
    ],
)
def test_ticks(ctx: Context, expr: str, expected: int) -> None:
    assert evaluate(expr, ctx) == expected


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("@utcNow()", "2024-01-01T12:00:00+00:00"),
    ],
)
def test_utc_now(ctx: Context, expr: str, expected: str) -> None:
    assert evaluate(expr, ctx) == expected
