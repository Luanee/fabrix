"""
Function registry for the fabric_expression_builder package.

Handles registration and lookup of expression functions by name.
"""

from typing import Any, Callable, Dict, Optional


class FunctionRegistry:
    """
    Registry for available functions in the expression builder.

    Functions can be registered and retrieved by name. Case-insensitive.
    """

    def __init__(self) -> None:
        self._functions: Dict[str, Callable[..., Any]] = {}

    def register(self, name: Optional[str] = None) -> Callable:
        """
        Decorator to register a function with the registry.

        Parameters
        ----------
        name : str, optional
            The function name for expressions. If None, uses the decorated function's name.

        Returns
        -------
        Callable
            The decorator for use on functions.
        """

        def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
            key = (name or fn.__name__).lower()
            self._functions[key] = fn
            return fn

        return decorator

    def add(self, name: str, fn: Callable[..., Any]) -> None:
        """
        Register a function explicitly.

        Parameters
        ----------
        name : str
            The function name.
        fn : Callable
            The function to register.
        """
        self._functions[name.lower()] = fn

    def get(self, name: str) -> Callable[..., Any]:
        """
        Retrieve a function by name.

        Parameters
        ----------
        name : str
            The function name.

        Returns
        -------
        Callable
            The registered function.

        Raises
        ------
        KeyError
            If no function with the given name exists.
        """
        key = name.lower()
        if key not in self._functions:
            raise KeyError(f"Function '{name}' is not registered in the registry.")
        return self._functions[key]

    def contains(self, name: str) -> bool:
        """
        Check if a function is registered under the given name.

        Parameters
        ----------
        name : str
            The function name.

        Returns
        -------
        bool
            True if registered, else False.
        """
        return name.lower() in self._functions

    def all_functions(self) -> Dict[str, Callable[..., Any]]:
        """
        Get all registered functions.

        Returns
        -------
        dict[str, Callable]
            A mapping of function names to callables.
        """
        return dict(self._functions)


# Singleton registry instance (used by function groups and evaluator)
registry = FunctionRegistry()
