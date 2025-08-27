"""
Conversion utilities for robust type casting in fabric_expression_builder (feb).
"""

import datetime
import json
import re
from typing import Any, Literal

import pytz


def as_int(value: Any) -> int:
    """
    Convert a value to int safely.

    Parameters
    ----------
    value : Any
        The value to convert.

    Returns
    -------
    int
        The integer representation.

    Raises
    ------
    ValueError
        If conversion fails.
    """
    if value is None or value == "":
        raise ValueError("Cannot convert None or empty string to int.")

    if isinstance(value, int):
        return value

    if isinstance(value, (float)):
        return int(value)

    if isinstance(value, str):
        try:
            return int(value)
        except Exception:
            try:
                return int(float(value))
            except Exception:
                try:
                    return int(as_bool(value))
                except Exception:
                    pass

    raise ValueError(f"Cannot convert {value!r} to int.")


def as_float(value: Any) -> float:
    """
    Convert a value to float safely.

    Parameters
    ----------
    value : Any
        The value to convert.

    Returns
    -------
    float
        The float representation.

    Raises
    ------
    ValueError
        If conversion fails.
    """
    if value is None or value == "":
        raise ValueError("Cannot convert None or empty string to float.")

    if isinstance(value, float):
        return value

    if isinstance(value, (bool, int)):
        return float(value)

    if isinstance(value, str):
        try:
            return float(value)
        except Exception:
            try:
                return float(as_bool(value))
            except Exception:
                pass

    raise ValueError(f"Cannot convert {value!r} to float.")


def as_bool(value: Any) -> bool:
    """
    Convert a value to bool safely.

    Parameters
    ----------
    value : Any
        The value to convert.

    Returns
    -------
    bool
        The boolean representation.

    Raises
    ------
    ValueError
        If conversion fails.
    """
    if value is None:
        return False

    if isinstance(value, bool):
        return value

    if isinstance(value, (int, float)):
        return value != 0

    if isinstance(value, str):
        if value.strip().lower() in {"true", "1", "yes", "y", "on"}:
            return True
        if value.strip().lower() in {"false", "0", "no", "n", "off"}:
            return False
        raise ValueError(f"Cannot interpret string {value!r} as bool.")

    raise ValueError(f"Cannot convert {value!r} to bool.")


def as_string(value: Any) -> str:
    """
    Convert a value to string safely.

    Parameters
    ----------
    value : Any
        The value to convert.

    Returns
    -------
    str
        The string representation.
    """
    if value is None:
        return ""

    if isinstance(value, bool):
        return "true" if value else "false"

    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=True)

    return str(value)


def as_datetime(
    value: str | int | float | datetime.datetime,
    timezone: str = "UTC",
    format: str | None = None,
) -> datetime.datetime:
    if isinstance(value, datetime.datetime):
        return value
    if isinstance(value, (int, float)):
        date = datetime.datetime.fromtimestamp(value)
        return pytz.timezone(timezone).localize(date)

    format = format or "%Y-%m-%dT%H:%M:%S"
    for format in (format, "%Y-%m-%dT%H:%M:%S+%H:%M", "%Y-%m-%dT%H:%M:%S%z"):
        try:
            date = datetime.datetime.strptime(str(value), format)
            return pytz.timezone(timezone).localize(date)
        except ValueError as exc:
            if "Not naive datetime (tzinfo is already set)" in exc.args:
                return datetime.datetime.strptime(str(value), format)
            continue
        except Exception as exc:
            continue
    raise ValueError(f"Cannot parse datetime: {value!r} with format: {format!r}")


def validate_timestamp_unit(unit: Literal["years", "months", "days", "hours", "minutes", "seconds"] | str):
    unit = unit.lower()
    if not unit.endswith("s"):
        unit += "s"

    if unit not in ("years", "months", "days", "hours", "minutes", "seconds"):
        raise ValueError(f"Invalid unit: {unit}")

    return unit


def clean_expression(expression: str) -> str:
    """
    Remove all linebreaks, encoded linebreaks, and whitespace sequences,
    except those between single quotes.
    """
    parts = re.split(r"('(?:[^'\\]|\\.)*')", expression)
    cleaned = []
    for i, part in enumerate(parts):
        if i % 2 == 0:
            part = re.sub(r"(\\n|\\r|\n|\r|\s+)", "", part)
        cleaned.append(part)
    return "".join(cleaned).strip()


def find_diff_span(a: str, b: str) -> tuple[int, int]:
    for i, (ca, cb) in enumerate(zip(a, b)):
        if ca != cb:
            return (i, min(len(a), len(b)))
    if len(a) != len(b):
        return (min(len(a), len(b)), len(a))
    return (0, len(a))
