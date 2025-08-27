"""
Main expression evaluator for the fabrix package.
"""

from typing import Any

from fabrix.context import Context
from fabrix.exceptions import ExpressionSyntaxError, FunctionNotFoundError
from fabrix.schemas import Expression, Flags


def evaluate(
    expression: Expression | str,
    context: Context | None = None,
    show_output: bool = False,
    raise_errors: bool = True,
) -> Any:
    """
    Evaluate an expression string in a given context, optionally tracing the steps.

    Parameters
    ----------
    expression : str
        The expression to evaluate.
    context : Context
        The context for evaluation.
    trace : TraceContext, optional
        If provided, records the evaluation steps.

    Returns
    -------
    Any
        The result of evaluation.
    """
    if isinstance(expression, str):
        expression = Expression(expression=expression)

    title = "Expression"
    if expression.name:
        title = f"Expression: {expression.name}"

    context = context or Context()
    raise NotImplementedError("This package is still work in progress")
