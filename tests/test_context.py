import pytest
from rich.text import Text
from rich.tree import Tree

from fabrix.context import Context, ExpressionTraceback, Scope


@pytest.mark.parametrize(
    "alias_attr",
    [
        ("DataFactory", "data_factory"),
        ("Pipeline", "pipeline"),
        ("RunId", "run_id"),
        ("TriggerId", "trigger_id"),
        ("TriggerName", "trigger_name"),
    ],
)
def test_scope_get_by_alias_known(alias_attr: tuple[str, str]) -> None:
    alias, attr = alias_attr
    s = Scope()
    assert s.get_by_alias(alias) == getattr(s, attr)


def test_scope_get_by_alias_unknown_raises() -> None:
    s = Scope()
    with pytest.raises(KeyError, match="Alias 'Nope' not found"):
        s.get_by_alias("Nope")


def test_context_get_set_variable(ctx: Context) -> None:
    ctx.set_variable("x", 1)
    assert ctx.get_variable("x") == 1

    # setdefault semantics: second set won't overwrite
    ctx.set_variable("x", 999)
    assert ctx.get_variable("x") == 1


def test_context_get_variable_missing_raises(ctx: Context) -> None:
    with pytest.raises(KeyError, match="No variable with name y initialized"):
        ctx.get_variable("y")


def test_context_add_trace_and_active_trace() -> None:
    c = Context()
    c.add_trace("My Trace")
    # active_trace is set and is the same object appended
    assert len(c._traces_) == 1
    assert isinstance(c.active_trace, ExpressionTraceback)
    assert c.active_trace is c._traces_[0]
    # root label text matches
    assert isinstance(c.active_trace.root, Tree)
    assert isinstance(c.active_trace.root.label, Text)
    assert "My Trace" in c.active_trace.root.label.plain


def test_trace_add_parse_and_literal_nodes() -> None:
    t = ExpressionTraceback("Expr")
    # Start parse node
    t.add_parse_node("substring('abc', 1, 2)")
    parse_node = t._active_node
    # Add literal inside
    t.add_literal_node("'abc'")
    t.add_literal_node("1")
    t.add_literal_node("2")

    root = t.root
    assert len(root.children) >= 1
    parse_node = root.children[0]

    assert "Parse: substring" in str(parse_node.label)
    # literal node should be attached under parse node (then pop)
    assert len(parse_node.children) >= 1
    lit = parse_node.children[0]
    assert str(lit.label) == "'abc'"


def test_trace_add_function_and_auto_pop_on_result() -> None:
    t = ExpressionTraceback("Expr")
    # create a parse parent, then function
    t.add_parse_node("add(1, 2)")
    node = t.add_function_node("add", result=3)
    # After result, function node should have been popped from stack
    # but still present under the parse node
    root = t.root
    parse_node = root.children[0]
    func_node = parse_node.children[0]
    assert func_node is node
    assert "Function: add" in func_node.label.plain  # type: ignore
    assert "➜ 3" in func_node.label.plain  # type: ignore


def test_trace_variable_parameter_scope_nodes_and_results() -> None:
    t = ExpressionTraceback("Expr")
    t.add_parse_node("concat(variables('foo'), pipeline().parameters.bar)")
    # function
    func_node = t.add_function_node("concat(variables('foo'), pipeline().parameters.bar)")
    # variable value
    t.add_variable_node("foo", result="baz")
    # parameter (no pop on result=None)
    t.add_parameter_node("bar", result="bar")
    t.add_function_node("concat(variables('foo'), pipeline().parameters.bar)", result="bazbar", node=func_node)

    # We expect three children appended in order
    labels = [str(ch.label) for ch in func_node.children]
    print(labels)
    assert any("variables('foo')" in L for L in labels)
    assert any("pipeline().parameters.bar" in L for L in labels)
    # variable node shows result arrow
    var_node = next(ch for ch in func_node.children if "variables('foo')" in ch.label.plain)  # type: ignore
    assert "➜ 'baz'" in var_node.label.plain  # type: ignore


def test_trace_add_error_with_span_highlight() -> None:
    t = ExpressionTraceback("Expr")
    bad_expr = "concatt('a','b')"
    t.add_parse_node(bad_expr)
    t.add_error(bad_expr, "Function 'concatt' not found. Did you mean 'concat'?", span=(0, 7))
    # The error is added as a child on the parse node
    parse_node = t.root.children[0]
    # Last child should be error label, with same plain text as bad_expr
    err_label = parse_node.children[-1].label
    assert err_label.plain == bad_expr  # type: ignore
    # And it has a child node with the message
    err_msg_node = parse_node.children[-1].children[0]
    assert "Function 'concatt' not found" in err_msg_node.label.plain  # type: ignore
