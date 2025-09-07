"""
Main expression evaluator for the fabric_expression_builder package.
"""

import re
from typing import Any

from fabrix.console import generate_context_output
from fabrix.context import Context
from fabrix.exceptions import ExpressionSyntaxError, FunctionNotFoundError
from fabrix.functions import *  # noqa: F403
from fabrix.registry import registry
from fabrix.schemas import Expression, Flags
from fabrix.utils import as_float, as_int, clean_expression
from fabrix.validations import validate_function, validate_syntax


def evaluate(
    expression: Expression | str,
    context: Context | None = None,
    show_output: bool = False,
    raise_errors: bool = True,
) -> str | int | float | bool | Any | None:
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
    context.add_trace(title)

    expr = expression.expression

    try:
        validate_syntax(expr)
    except ExpressionSyntaxError as exc:
        context.active_trace.add_parse_node(expr)
        context.active_trace.add_error(label=expr, message=str(exc), span=None)
        if raise_errors:
            raise exc from exc
        return None

    if not isinstance(expr, str):
        return expr

    if "@@" in expr:
        return expr.replace("@@", "@")

    if "@{" in expr:

        def replace_inner_expression(match) -> str:
            inner_expr = match.group(1).strip()
            result = str(_eval(inner_expr, context, raise_errors))
            return result

        return re.sub(r"@{([^}]+)}", replace_inner_expression, expr)

    if expr.startswith("@"):
        expr = expr[1:]

    result = _eval(expr, context, raise_errors)

    if expression.variable:
        context.set_variable(expression.variable, result)

    if show_output:
        generate_context_output(context)

    return result


def _eval(
    expr: str,
    context: Context,
    raise_errors: bool,
) -> Any:
    expr = clean_expression(expr)

    # ----------- Literal/other -----------
    result = _evaluate_literal(expr, context)
    if result is not Flags.NO_MATCH:
        return result

    context.active_trace.add_parse_node(expr)

    # --- Pipeline parameter ---
    result = _evaluate_pipeline_parameter(expr, context)
    if result is not Flags.NO_MATCH:
        context.active_trace.pop()
        return result

    # --- Pipeline scope variable ---
    result = _evaluate_pipeline_scope_parameter(expr, context)
    if result is not Flags.NO_MATCH:
        context.active_trace.pop()
        return result

    # --- Variable ---
    result = _evaluate_variable(expr, context)
    if result is not Flags.NO_MATCH:
        context.active_trace.pop()
        return result

    # --- Activity ---
    result = _evaluate_activity(expr, context, raise_errors)
    if result is not Flags.NO_MATCH:
        context.active_trace.pop()
        return result

    # ----------- Function call -----------
    result = _evaluate_function(expr, context, raise_errors)
    if result is not Flags.NO_MATCH:
        return result

    context.active_trace.pop()
    return expr


def _evaluate_pipeline_parameter(
    expression: str,
    context: Context,
) -> Any:
    param_match = re.match(r"pipeline\(\)\.parameters\.([a-zA-Z_][a-zA-Z0-9_]*)", expression)

    if not param_match:
        return Flags.NO_MATCH

    key = param_match.group(1)
    result = context.get_parameter(key)
    context.active_trace.add_parameter_node(key, result=result)
    return result


def _evaluate_pipeline_scope_parameter(
    expression: str,
    context: Context,
) -> Any:
    scope_match = re.match(r"pipeline\(\)\.([a-zA-Z_][a-zA-Z0-9_]*)", expression)
    if not scope_match:
        return Flags.NO_MATCH

    key = scope_match.group(1)
    result = context.get_pipeline_scope_variable(key)
    context.active_trace.add_scope_node(key, result=result)
    return result


def _evaluate_variable(
    expression: str,
    context: Context,
) -> Any:
    var_match = re.match(r"variables\(['\"](.+?)['\"]\)", expression)
    if not var_match:
        return Flags.NO_MATCH

    key = var_match.group(1)
    result = context.get_variable(key)
    context.active_trace.add_variable_node(key, result=result)
    return result


def _evaluate_activity(
    expression: str,
    context: Context,
    raise_errors: bool,
) -> Any:
    activity_pattern = re.compile(
        r"^activity\(\s*'(?P<activity>(?:[^']|'{2})*)'\s*\)\.output(?P<path>.*)$", re.IGNORECASE
    )
    segment_pattern = re.compile(r"(?:\.([A-Za-z_][A-Za-z0-9_]*)|\[\s*(.*?)\s*\])", re.VERBOSE)
    activity_match = activity_pattern.match(expression)
    if not activity_match:
        return Flags.NO_MATCH

    activity_name = activity_match.group("activity")
    path = activity_match.group("path")
    output = context.get_activity_output(activity_name)
    node = context.active_trace.add_activity_node(activity_name, path=path)

    path_segments: list[str] = []
    for segment in segment_pattern.finditer(path):
        field = segment.group(1)
        inner = (segment.group(2) or "").strip()
        if field:
            try:
                if isinstance(output, dict):
                    output = output.get(field)
                else:
                    output = getattr(output, field)
                if output is None:
                    raise
            except Exception as e:
                raise KeyError(f"Missing field '{field}' on activity('{activity_name}').output path.") from e
            path_segments.append(field)
        else:
            field = _eval(inner, context, raise_errors)
            try:
                if isinstance(output, (list, tuple)):
                    output = output[int(field)]
                elif isinstance(output, dict):
                    output = output.get(field)
                if output is None:
                    raise
            except Exception as e:
                raise KeyError(f"Invalid index/field [{field!r}] on activity('{activity_name}').output path.") from e
            path_segments.append(f"[{str(field)}]")

    activity_path = f".{'.'.join(path_segments)}"
    context.active_trace.add_activity_node(activity_name, path=activity_path, result=output, node=node)
    context.active_trace.pop()
    return output


def _evaluate_function(
    expression: str,
    context: Context,
    raise_errors: bool,
) -> Any:
    """
    Evaluates a function with the given name and arguments in the provided context.

    Parameters
    ----------
    func_name : str
        The name of the function to evaluate.
    args : list[str]
        The arguments to pass to the function.
    context : Context
        The evaluation context.

    Returns
    -------
    Any
        The result of the function evaluation.
    """
    func_match = re.match(r"([a-zA-Z_][a-zA-Z0-9_]*)\((.*)\)", expression)
    if not func_match:
        return Flags.NO_MATCH

    func_name, args_str = func_match.groups()

    node = context.active_trace.add_function_node(func_name)

    try:
        validate_function(func_name)
    except FunctionNotFoundError as exc:
        context.active_trace.add_error(expression, str(exc), span=exc.span)
        if raise_errors:
            raise exc from exc
        return

    args = _parse_args(args_str)
    resolved_args = [_eval(arg, context, raise_errors) for arg in args]

    fn = registry.get(func_name)

    result = fn(*resolved_args)

    context.active_trace.add_function_node(func_name, result=result, node=node)
    context.active_trace.pop()
    return result


def _parse_args(args_str: str) -> list[str]:
    """
    Naively splits the arguments string for top-level commas (improve as needed).

    Parameters
    ----------
    args_str : str
        Arguments string inside a function call.

    Returns
    -------
    list[str]
        List of argument substrings.
    """
    # Simple split; improve for nested functions, strings, etc.
    args = []
    depth = 0
    current = ""
    in_str = False
    str_char = ""
    for c in args_str:
        if in_str:
            if c == str_char:
                in_str = False
            current += c
        elif c in {"'", '"'}:
            in_str = True
            str_char = c
            current += c
        elif c == "(":
            depth += 1
            current += c
        elif c == ")":
            depth -= 1
            current += c
        elif c == "," and depth == 0:
            args.append(current.strip())
            current = ""
        else:
            current += c
    if current.strip():
        args.append(current.strip())
    return args


def _evaluate_literal(expression: str, context: Context) -> Any:
    """
    Resolves a literal, variable, or parameter from the context.
    Improve with full Data Factory/Fabric syntax later.

    Parameters
    ----------
    expression : str
        The expression or value string.
    context : Context
        The evaluation context.

    Returns
    -------
    Any
        The resolved value, or expression if not found.
    """
    mode: Flags = Flags.NO_MATCH
    result: Any = None
    expression = expression.strip()

    if result is None:
        literal_match = re.match(r"^'(?P<literal>(.*?))'$", expression)
        if literal_match:
            result = re.sub(r"'+", "'", literal_match.group(1))
            mode = Flags.LITERAL_MATCH

    if result is None:
        if expression.lower() in ("true", "false"):
            result = expression.lower() == "true"
            mode = Flags.BOOLEAN_MATCH

    if result is None:
        num_pat = r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?"
        num_match = re.fullmatch(num_pat, expression)
        if num_match:
            # if it contains '.' or 'e/E', prefer float
            if any(c in expression for c in (".", "e", "E")):
                result = as_float(expression)
            else:
                result = as_int(expression)
            mode = Flags.NUMBER_MATCH

    if result is None:
        if expression.lower() == "null":
            result = None
            mode = Flags.NULL_MATCH

    if mode is Flags.NO_MATCH:
        return Flags.NO_MATCH

    context.active_trace.add_literal_node(expression)
    return result
