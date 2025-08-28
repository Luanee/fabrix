import difflib
import re

from fabrix.exceptions import ExpressionSyntaxError, FunctionNotFoundError
from fabrix.registry import registry


def _check_at_or_interpolation(expr: str) -> None:
    """Rule: expression must start with '@' OR contain '@{...}' for interpolation."""
    s = expr.strip()
    if not (s.startswith("@") or "@{" in s):
        raise ExpressionSyntaxError("Expression must start with '@' or contain an interpolation like '@{ ... }'.")


def _check_parentheses(expr: str) -> None:
    """Rule: too many / missing parentheses."""
    stack = []
    for i, ch in enumerate(expr):
        if ch == "(":
            stack.append(i)
        elif ch == ")":
            if not stack:
                raise ExpressionSyntaxError(f"Unmatched ')' at position {i}.")
            stack.pop()
    if stack:
        pos = stack.pop()
        raise ExpressionSyntaxError(f"Unmatched '(' at position {pos}.")


def _check_interpolations(expr: str) -> None:
    """Validate @{ ... } blocks (balance of braces only for interpolations)."""
    # Quick scan for '@{...}' pairs (doesn't attempt nested braces)
    idx = 0
    while True:
        start = expr.find("@{", idx)
        if start == -1:
            return
        end = expr.find("}", start + 2)
        if end == -1:
            raise ExpressionSyntaxError(f"Interpolation '@{{' at position {start} not closed with '}}'.")
        idx = end + 1  # continue after this interpolation


def _check_quotes(expression: str) -> None:
    """Validate quotes: only single quotes, must be balanced."""
    if '"' in expression:
        raise ExpressionSyntaxError("Double quotes are not allowed. Use single quotes (').")

    # Replace escaped '' with a placeholder, so they don’t count
    tmp = re.sub(r"''", "", expression)

    # Count raw single quotes
    singles = tmp.count("'")

    if singles % 2 != 0:
        raise ExpressionSyntaxError("Mismatched single quote in expression.")


def validate_syntax(expression: str) -> None:
    """Run all top-level validations (no mutation)."""
    _check_at_or_interpolation(expression)
    _check_interpolations(expression)
    _check_parentheses(expression)
    _check_quotes(expression)


def validate_function(func_name: str) -> None:
    if registry.contains(func_name):
        return

    all_functions = list(registry.all_functions().keys())
    suggestions = difflib.get_close_matches(
        func_name,
        all_functions,
        n=1,
        cutoff=0.6,
    )
    suggestion = suggestions[0] if suggestions else None
    error_span = (0, len(func_name))

    suggestion = f" Did you mean '{suggestion}'?" if suggestion else ""
    message = f"Function '{func_name}' not found.{suggestion}"

    raise FunctionNotFoundError(message, span=error_span)
