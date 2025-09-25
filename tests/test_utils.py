import datetime
import json
from typing import Any

import pytest
import pytz

from fabrix.utils import as_bool, as_datetime, as_float, as_int, as_string, validate_timestamp_unit


@pytest.mark.parametrize(
    "value,expected",
    [
        (42, 42),
        (3.7, 3),
        (True, 1),
        (False, 0),
        ("17", 17),
        ("3.9", 3),
        ("True", 1),
    ],
)
def test_as_int_valid(value: Any, expected: int) -> None:
    assert as_int(value) == expected


@pytest.mark.parametrize("value", [None, "", "abc", [], {}])
def test_as_int_invalid(value: Any) -> None:
    with pytest.raises(ValueError):
        as_int(value)


@pytest.mark.parametrize(
    "value,expected",
    [
        (3.14, 3.14),
        (7, 7.0),
        (False, 0.0),
        ("1.23", 1.23),
        ("0", 0.0),
    ],
)
def test_as_float_valid(value: Any, expected: float) -> None:
    assert as_float(value) == expected


@pytest.mark.parametrize("value", [None, "", "abc", [], {}])
def test_as_float_invalid(value: Any) -> None:
    with pytest.raises(ValueError):
        as_float(value)


@pytest.mark.parametrize(
    "value,expected",
    [
        (True, True),
        (False, False),
        (1, True),
        (0, False),
        (3.5, True),
        (0.0, False),
        ("true", True),
        ("yes", True),
        ("1", True),
        ("false", False),
        ("off", False),
        ("0", False),
        (None, False),
    ],
)
def test_as_bool_valid(value: Any, expected: bool) -> None:
    assert as_bool(value) == expected


@pytest.mark.parametrize("value", ["abc", [], {}])
def test_as_bool_invalid(value: Any) -> None:
    with pytest.raises(ValueError):
        as_bool(value)


@pytest.mark.parametrize(
    "value,expected",
    [
        (None, ""),
        ("foo", "foo"),
        (42, "42"),
        (True, "true"),
        ({"a": 1}, json.dumps({"a": 1}, ensure_ascii=True)),
        ([1, 2, 3], json.dumps([1, 2, 3], ensure_ascii=True)),
    ],
)
def test_as_string(value: Any, expected: str) -> None:
    assert as_string(value) == expected


def test_as_datetime_from_string() -> None:
    dt = as_datetime("2024-01-01T12:00:00", "UTC")
    assert dt.year == 2024 and dt.month == 1 and dt.day == 1 and dt.hour == 12 and dt.tzinfo is not None


def test_as_datetime_from_timestamp() -> None:
    dt = as_datetime("2024-01-01T10:20:00", "UTC")
    assert dt == datetime.datetime(2024, 1, 1, 10, 20, tzinfo=pytz.timezone("UTC"))


def test_as_datetime_from_datetime() -> None:
    now = datetime.datetime(2024, 1, 1, 12, 0, 0)
    dt = as_datetime(now)
    assert dt == now


def test_as_datetime_invalid() -> None:
    with pytest.raises(ValueError):
        as_datetime("notadatetime")


# --- validate_timestamp_unit ---
@pytest.mark.parametrize(
    "value,expected",
    [
        ("year", "years"),
        ("days", "days"),
        ("hour", "hours"),
        ("minutes", "minutes"),
        ("SECONDS", "seconds"),
    ],
)
def test_validate_timestamp_unit_valid(value, expected):
    assert validate_timestamp_unit(value) == expected


@pytest.mark.parametrize("value", ["foo", "monther", "abc"])
def test_validate_timestamp_unit_invalid(value):
    with pytest.raises(ValueError):
        validate_timestamp_unit(value)
