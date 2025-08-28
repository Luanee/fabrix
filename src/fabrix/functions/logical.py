"""
Implements logical and comparison functions for Fabric expressions.
"""

from typing import Any

from fabrix.registry import registry
from fabrix.utils import as_bool, as_float


@registry.register("and")
def and_func(expression_1: bool, expression_2: bool) -> bool:
    """
    Check whether all expressions are true.

    Parameters
    ----------
    expression_1 : bool
        First value.
    expression_2 : bool
        Second value.

    Returns
    -------
    bool
        True if all arguments are true, else False.
    """
    return all(as_bool(arg) for arg in (expression_1, expression_2))


@registry.register("equals")
def equals(a: Any, b: Any) -> bool:
    """
    Check whether both values are equivalent.

    Parameters
    ----------
    a : Any
        First value.
    b : Any
        Second value.

    Returns
    -------
    bool
        True if a and b are equivalent, else False.
    """
    return a == b


@registry.register("greater")
def greater(a: Any, b: Any) -> bool:
    """
    Check whether the first value is greater than the second value.

    Parameters
    ----------
    a : Any
        First value.
    b : Any
        Second value.

    Returns
    -------
    bool
        True if a > b, else False.
    """
    return as_float(a) > as_float(b)


@registry.register("greaterOrEquals")
def greater_or_equals(expression_1: bool, expression_2: bool) -> bool:
    """
    Check whether the first value is greater than or equal to the second value.

    Parameters
    ----------
    expression_1 : bool
        First value.
    expression_2 : bool
        Second value.

    Returns
    -------
    bool
        True if a >= b, else False.
    """
    return as_float(expression_1) >= as_float(expression_2)


@registry.register("if")
def if_func(condition: Any, if_true: Any, if_false: Any) -> Any:
    """
    Check whether an expression is true or false. Based on the result, return a specified value.

    Parameters
    ----------
    condition : Any
        Expression to evaluate.
    if_true : Any
        Value to return if condition is true.
    if_false : Any
        Value to return if condition is false.

    Returns
    -------
    any
        if_true if condition is true, else if_false.
    """
    return if_true if as_bool(condition) else if_false


@registry.register("less")
def less(a: Any, b: Any) -> bool:
    """
    Check whether the first value is less than the second value.

    Parameters
    ----------
    a : Any
        First value.
    b : Any
        Second value.

    Returns
    -------
    bool
        True if a < b, else False.
    """
    return float(a) < float(b)


@registry.register("lessOrEquals")
def less_or_equals(a: Any, b: Any) -> bool:
    """
    Check whether the first value is less than or equal to the second value.

    Parameters
    ----------
    a : Any
        First value.
    b : Any
        Second value.

    Returns
    -------
    bool
        True if a <= b, else False.
    """
    return as_float(a) <= as_float(b)


@registry.register("not")
def not_func(value: Any) -> bool:
    """
    Check whether an expression is false.

    Parameters
    ----------
    value : Any
        Expression or value to check.

    Returns
    -------
    bool
        True if value is not true, else False.
    """
    return not as_bool(value)


@registry.register("or")
def or_func(expression_1: bool, expression_2: bool) -> bool:
    """
    Check whether at least one expression is true.

    Parameters
    ----------
    expression_1 : bool
        First value.
    expression_2 : bool
        Second value.

    Returns
    -------
    bool
        True if any argument is true, else False.
    """
    return any(as_bool(arg) for arg in (expression_1, expression_2))
