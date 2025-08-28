"""
Implements date and time functions for Fabric expressions.
"""

from datetime import datetime
from typing import Any, Literal

import pytz
from dateutil.relativedelta import relativedelta

from fabrix.registry import registry
from fabrix.utils import as_datetime, validate_timestamp_unit


@registry.register("addDays")
def add_days(timestamp: str, days: str) -> str:
    """
    Add a number of days to a timestamp.

    Parameters
    ----------
    timestamp : str
        Input datetime or ISO string.
    days : str
        Number of days to add.

    Returns
    -------
    str
        ISO formatted string.
    """
    d = as_datetime(timestamp)
    return (d + relativedelta(days=int(days))).isoformat()


@registry.register("addHours")
def add_hours(timestamp: str, hours: str) -> str:
    """
    Add a number of hours to a timestamp.
    """
    d = as_datetime(timestamp)
    return (d + relativedelta(hours=int(hours))).isoformat()


@registry.register("addMinutes")
def add_minutes(timestamp: str, minutes: str) -> str:
    """
    Add a number of minutes to a timestamp.
    """
    d = as_datetime(timestamp)
    return (d + relativedelta(minutes=int(minutes))).isoformat()


@registry.register("addSeconds")
def add_seconds(timestamp: str, seconds: str) -> str:
    """
    Add a number of seconds to a timestamp.
    """
    d = as_datetime(timestamp)
    return (d + relativedelta(seconds=int(seconds))).isoformat()


@registry.register("addToTime")
def add_to_time(
    timestamp: str,
    interval: int,
    unit: Literal["years", "months", "days", "hours", "minutes", "seconds"] | str,
) -> str:
    """
    Add a number of time units to a timestamp.
    """
    unit = validate_timestamp_unit(unit)

    d = as_datetime(timestamp)
    params: dict[str, Any] = {unit: interval}

    delta = relativedelta(**params)
    return (d + delta).isoformat()


@registry.register("convertFromUtc")
def convert_from_utc(timestamp: str, timezone: str) -> str:
    """
    Convert a timestamp from UTC to the target time zone.
    """
    d = as_datetime(timestamp)
    return d.astimezone(pytz.timezone(timezone)).isoformat()


@registry.register("convertTimeZone")
def convert_time_zone(timestamp: str, from_tz: str, to_tz: str) -> str:
    """
    Convert a timestamp from the source time zone to the target time zone.
    """
    d = as_datetime(timestamp, from_tz)
    return d.astimezone(pytz.timezone(to_tz)).isoformat()


@registry.register("convertToUtc")
def convert_to_utc(timestamp: Any, from_tz: str) -> str:
    """
    Convert a timestamp from the source time zone to UTC.
    """
    d = as_datetime(timestamp, from_tz)
    return d.astimezone(pytz.timezone("UTC")).isoformat()


@registry.register("dayOfMonth")
def day_of_month(timestamp: Any) -> int:
    """
    Return the day of the month component from a timestamp.
    """
    d = as_datetime(timestamp)
    return d.day


@registry.register("dayOfWeek")
def day_of_week(timestamp: Any) -> int:
    """
    Return the day of the week component from a timestamp (Monday=0, Sunday=6).
    """
    d = as_datetime(timestamp)
    return d.weekday()


@registry.register("dayOfYear")
def day_of_year(timestamp: Any) -> int:
    """
    Return the day of the year component from a timestamp.
    """
    d = as_datetime(timestamp)
    return d.timetuple().tm_yday


@registry.register("formatDateTime")
def format_date_time(timestamp: Any, fmt: str = "%Y-%m-%dT%H:%M:%S") -> str:
    """
    Return the timestamp as a string in optional format.
    """
    d = as_datetime(timestamp)
    return d.strftime(fmt)


@registry.register("getFutureTime")
def get_future_time(
    interval: int,
    unit: Literal["years", "months", "days", "hours", "minutes", "seconds"] | str,
    format_str: str = "%Y-%m-%dT%H:%M:%S",
) -> str:
    """
    Return the current timestamp plus the specified time units.
    """
    unit = validate_timestamp_unit(unit)

    now = datetime.now(pytz.timezone("UTC"))
    params: dict[str, Any] = {unit: interval}
    delta = relativedelta(**params)

    timestamp = now + delta
    return timestamp.strftime(format_str)


@registry.register("getPastTime")
def get_past_time(
    interval: int,
    unit: Literal["years", "months", "days", "hours", "minutes", "seconds"] | str,
    format_str: str = "%Y-%m-%dT%H:%M:%S",
) -> str:
    """
    Return the current timestamp minus the specified time units.
    """
    unit = validate_timestamp_unit(unit)

    now = datetime.now(pytz.timezone("UTC"))
    params: dict[str, Any] = {unit: interval}
    delta = relativedelta(**params)

    timestamp = now - delta
    return timestamp.strftime(format_str)


@registry.register("startOfDay")
def start_of_day(timestamp: Any) -> str:
    """
    Return the start of the day for a timestamp.
    """
    d = as_datetime(timestamp)
    return d.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()


@registry.register("startOfHour")
def start_of_hour(timestamp: Any) -> str:
    """
    Return the start of the hour for a timestamp.
    """
    d = as_datetime(timestamp)
    return d.replace(minute=0, second=0, microsecond=0).isoformat()


@registry.register("startOfMonth")
def start_of_month(timestamp: Any) -> str:
    """
    Return the start of the month for a timestamp.
    """
    d = as_datetime(timestamp)
    return d.replace(day=1, hour=0, minute=0, second=0, microsecond=0).isoformat()


@registry.register("subtractFromTime")
def subtract_from_time(
    timestamp: str,
    interval: int,
    unit: Literal["years", "months", "days", "hours", "minutes", "seconds"] | str,
) -> str:
    """
    Subtract a number of time units from a timestamp.
    """
    unit = validate_timestamp_unit(unit)

    d = as_datetime(timestamp)
    params: dict[str, Any] = {unit: interval}

    delta = relativedelta(**params)
    return (d - delta).isoformat()


@registry.register("ticks")
def ticks(timestamp: Any) -> int:
    """
    Return the ticks property value for a specified timestamp.
    """
    d = as_datetime(timestamp)
    # .NET ticks: 1 tick = 100ns since 0001-01-01T00:00:00
    epoch = datetime(1, 1, 1, tzinfo=pytz.timezone("UTC"))
    delta = d - epoch
    return int(delta.total_seconds() * 10**7)


@registry.register("utcNow")
def utc_now() -> str:
    """
    Return the current timestamp as a string.
    """
    return datetime.now(pytz.timezone("UTC")).isoformat()
