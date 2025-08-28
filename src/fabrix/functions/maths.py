"""
Implements mathematical functions for Fabric expressions.
"""

import math
from typing import Any

from fabrix.registry import registry


@registry.register("add")
def add(
    *args: Any,
) -> float:
    """
    Add two or more numbers, and return the sum.

    Parameters
    ----------
    *args : Any
        Numbers to add.

    Returns
    -------
    float
        The sum of all arguments.
    """
    return sum(float(arg) for arg in args)


@registry.register("sub")
def sub(
    a: Any,
    b: Any,
) -> float:
    """
    Subtract one or more numbers from another number.

    Parameters
    ----------
    a : Any
        Minuend.
    b : Any
        Subtrahend.

    Returns
    -------
    float
        The result after subtracting all arguments after the first from the first.
    """
    result = float(a) - float(b)
    return result


@registry.register("mul")
def mul(
    *args: Any,
) -> float:
    """
    Multiply two or more numbers, and return the product.

    Parameters
    ----------
    *args : Any
        Numbers to multiply.

    Returns
    -------
    float
        The product of all arguments.
    """
    result = 1.0
    for arg in args:
        result *= float(arg)
    return result


@registry.register("div")
def div(
    numerator: Any,
    denominator: Any,
) -> float:
    """
    Divide one number by another, and return the result.

    Parameters
    ----------
    numerator : Any
        The dividend.
    denominator : Any
        The divisor.

    Returns
    -------
    float
        The quotient.
    """
    return float(numerator) / float(denominator)


@registry.register("mod")
def mod(
    a: Any,
    b: Any,
) -> float:
    """
    Return the remainder from dividing two numbers.

    Parameters
    ----------
    a : Any
        Dividend.
    b : Any
        Divisor.

    Returns
    -------
    float
        The remainder.
    """
    return float(a) % float(b)


@registry.register("max")
def max_func(
    *args: Any,
) -> float:
    """
    Return the maximum value among all arguments.

    Parameters
    ----------
    *args : Any
        Numbers to compare.

    Returns
    -------
    float
        The maximum value.
    """
    return max(float(arg) for arg in args)


@registry.register("min")
def min_func(
    *args: Any,
) -> float:
    """
    Return the minimum value among all arguments.

    Parameters
    ----------
    *args : Any
        Numbers to compare.

    Returns
    -------
    float
        The minimum value.
    """
    return min(float(arg) for arg in args)


@registry.register("abs")
def abs_func(
    value: Any,
) -> float:
    """
    Return the absolute value of a number.

    Parameters
    ----------
    value : Any
        The value.

    Returns
    -------
    float
        The absolute value.
    """
    return abs(float(value))


@registry.register("round")
def round_func(
    value: Any,
    digits: int | None = None,
) -> float:
    """
    Round a number to the nearest integer or to a specified number of decimal places.

    Parameters
    ----------
    value : Any
        The number to round.
    digits : Any, optional
        Number of decimal digits. Defaults to 0 (nearest integer).

    Returns
    -------
    float
        The rounded number.
    """
    if digits is not None:
        return round(float(value), int(digits))
    return round(float(value))


@registry.register("ceiling")
def ceiling(
    value: Any,
) -> float:
    """
    Return the smallest integer greater than or equal to the specified number.

    Parameters
    ----------
    value : Any
        The number to round up.

    Returns
    -------
    float
        The smallest integer greater than or equal to value.
    """
    return math.ceil(float(value))


@registry.register("floor")
def floor(
    value: Any,
) -> float:
    """
    Return the largest integer less than or equal to the specified number.

    Parameters
    ----------
    value : Any
        The number to round down.

    Returns
    -------
    float
        The largest integer less than or equal to value.
    """
    return math.floor(float(value))
