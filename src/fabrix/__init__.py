from collections.abc import Sequence
from typing import Any, overload

from fabrix.console import generate_context_output
from fabrix.context import Context
from fabrix.evaluate import evaluate
from fabrix.schemas import Expression
from fabrix.version import __version__

__all__: list[str] = [
    "Context",
    "Expression",
    "evaluate",
    "__version__",
]


@overload
def run(
    *expressions: Expression,
    context: Context | None = ...,
    show_output: bool = ...,
) -> Any: ...


@overload
def run(
    *expressions: str,
    context: Context | None = ...,
    show_output: bool = ...,
) -> Any: ...


@overload
def run(
    *expressions: str | Expression,
    context: Context | None = ...,
    show_output: bool = ...,
) -> Any: ...


def run(
    *expressions: Expression | str,
    context: Context | None = None,
    show_output: bool = False,
) -> Any:
    """
    Evaluate a sequence of expressions (strings or `Expression` objects).

    Rules
    -----
    - Strings are coerced to `Expression(expression=<str>)`.
    - If an `Expression.result` is set, the evaluated value is stored in
      `context.variables[Expression.result]`.
    - If `Expression.debug=True` (or `show_output=True`), a Rich `TraceContext` is used
      and shown (only if `show_output=True`).

    Parameters
    ----------
    expressions : *str | Expression
        Variadic list of expressions to evaluate in order.
    context : Context, optional
        Evaluation context. If omitted, a fresh `Context()` is created.
    show_output : bool, default False
        If True, prints Rich traces for any expression.

    Returns
    -------
    Any
        The result of the **last** expression evaluated.

    Raises
    ------
    ValueError
        If no expressions were provided.
    TypeError
        If an item cannot be coerced into `Expression`.
    """

    def create_expressions(expressions: Sequence[str | Expression]) -> list[Expression]:
        coerced: list[Expression] = []
        for index, item in enumerate(expressions):
            if isinstance(item, Expression):
                coerced.append(item)
            elif isinstance(item, str):
                coerced.append(Expression(expression=item, name=f"{index:>003}"))
            else:
                raise TypeError(f"Unsupported expression type: {type(item).__name__}")
        return coerced

    context = context or Context()

    result = None
    for expression in create_expressions(expressions):
        result = evaluate(expression, context)
        if expression.variable:
            context.set_variable(expression.variable, result)

    if show_output:
        generate_context_output(context)

    return result
