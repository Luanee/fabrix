"""
Implements collection/array functions for Fabric expressions.
"""

from typing import Any

from fabrix.registry import registry


@registry.register("contains")
def contains(collection: str | dict | list, value: str) -> bool:
    """
    Check whether a collection contains a value.

    Parameters
    ----------
    context : Context
        Evaluation context (required).
    collection : Any
        The collection (list, set, dict keys, string, etc.).
    value : Any
        The value to look for.

    Returns
    -------
    bool
        True if collection contains value, else False.
    """
    if isinstance(collection, dict):
        return value in collection.keys()
    return value in collection


@registry.register("empty")
def empty(value: Any) -> bool:
    """
    Check whether a collection is empty.

    Parameters
    ----------
    context : Context
        Evaluation context (required).
    value : Any
        Collection or string to check.

    Returns
    -------
    bool
        True if empty or None, else False.
    """
    if value is None:
        return True
    if isinstance(value, (list, dict, set, str)):
        return len(value) == 0
    return False


@registry.register("first")
def first(value: Any) -> Any:
    """
    Return the first item from a collection or string.

    Parameters
    ----------
    context : Context
        Evaluation context (required).
    value : Any
        The collection or string.

    Returns
    -------
    any
        The first item, or None if empty.
    """
    if value is None or len(value) == 0:
        return None
    return value[0]


@registry.register("last")
def last(value: Any) -> Any:
    """
    Return the last item from a collection or string.

    Parameters
    ----------
    context : Context
        Evaluation context (required).
    value : Any
        The collection or string.

    Returns
    -------
    any
        The last item, or None if empty.
    """
    if value is None or len(value) == 0:
        return None
    return value[-1]


@registry.register("length")
def length(value: Any) -> int:
    """
    Return the number of items in a collection or string.

    Parameters
    ----------
    context : Context
        Evaluation context (required).
    value : Any
        The collection or string.

    Returns
    -------
    int
        Length of the value.
    """
    if value is None:
        return 0
    return len(value)


@registry.register("skip")
def skip(value: Any, count: int) -> Any:
    """
    Return all items after skipping a specified number.

    Parameters
    ----------
    context : Context
        Evaluation context (required).
    value : Any
        The collection or string.
    count : int
        Number of items to skip.

    Returns
    -------
    any
        The remaining items after skipping.
    """
    if value is None:
        return []
    return value[count:]


@registry.register("take")
def take(value: Any, count: int) -> Any:
    """
    Return the first N items from a collection or string.

    Parameters
    ----------
    context : Context
        Evaluation context (required).
    value : Any
        The collection or string.
    count : int
        Number of items to take.

    Returns
    -------
    any
        The first N items.
    """
    if value is None:
        return []
    return value[:count]


@registry.register("union")
def union(collection1: Any, collection2: Any) -> list:
    """
    Return a union of two collections.

    Parameters
    ----------
    context : Context
        Evaluation context (required).
    collection1 : Any
        First collection.
    collection2 : Any
        Second collection.

    Returns
    -------
    list
        List with all unique elements from both collections.
    """
    return list(set(collection1) | set(collection2))


@registry.register("intersection")
def intersection(collection1: Any, collection2: Any) -> list:
    """
    Return an intersection of two collections.

    Parameters
    ----------
    context : Context
        Evaluation context (required).
    collection1 : Any
        First collection.
    collection2 : Any
        Second collection.

    Returns
    -------
    list
        List of shared elements.
    """
    return list(set(collection1) & set(collection2))


@registry.register("distinct")
def distinct(value: Any) -> list:
    """
    Return a list of distinct elements from a collection or string.

    Parameters
    ----------
    context : Context
        Evaluation context (required).
    value : Any
        The collection or string.

    Returns
    -------
    list
        List of distinct items.
    """
    return list(dict.fromkeys(value))


@registry.register("join")
def join(value: Any, delimiter: str = ",") -> str:
    """
    Join a collection of items into a string, separated by delimiter.

    Parameters
    ----------
    context : Context
        Evaluation context (required).
    value : Any
        Collection of items.
    delimiter : str
        Separator to use.

    Returns
    -------
    str
        Joined string.
    """
    return delimiter.join(str(x) for x in value)
