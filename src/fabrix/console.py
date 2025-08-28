from typing import Any

from rich.columns import Columns
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from fabrix.context import Context


def repr_value(val: Any) -> str:
    if isinstance(val, (dict, list)):
        return Text.from_markup("[dim]JSON[/dim]").plain
    if val is None:
        return "null"
    return str(val)


def repr_type(val: Any) -> str:
    return type(val).__name__ if val is not None else "NoneType"


def table_from_dict(data: dict[str, Any], with_types: bool) -> Table:
    table = Table(
        title_style="bold magenta",
        header_style="bold",
        show_header=True,
        expand=True,
        box=None,
    )
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Value", style="green")

    if with_types:
        table.add_column("Type", style="yellow", no_wrap=True)

    if not data:
        table.add_row("[dim]— empty —[/dim]", "", "")
        return table

    for k in sorted(data.keys(), key=lambda s: s.lower()):
        v = data[k]
        if with_types:
            table.add_row(k, repr_value(v), repr_type(v))
        else:
            table.add_row(k, repr_value(v))
    return table


def generate_variable_panel(context: Context) -> Panel:
    table = table_from_dict(context.variables, with_types=True)
    return Panel(
        table,
        border_style="magenta",
        title="Variables",
        padding=(1, 1),
    )


def generate_parameters_panel(context: Context) -> Panel:
    table = table_from_dict(context.pipeline_parameters, with_types=True)
    return Panel(
        table,
        border_style="magenta",
        title="Pipeline Parameters",
        padding=(1, 1),
    )


def generate_scope_panel(context: Context) -> Panel:
    table = table_from_dict(context.pipeline_scope_variables.model_dump(by_alias=True), with_types=False)
    return Panel(
        table,
        border_style="magenta",
        title="Scope Parameters",
        padding=(1, 1),
    )


def generate_expressions_panel(context: Context) -> Panel:
    group = Group()
    number_of_traces = len(context._traces_)
    for index, trace in enumerate(context._traces_):
        group.renderables.append(trace.root)

        if index < number_of_traces - 1:
            group.renderables.append(Text(""))

    return Panel(
        group,
        border_style="magenta",
        title="Expressions",
        padding=(1, 1),
    )


def generate_context_output(context: Context) -> None:
    console = Console()

    left_panels = Group(
        generate_variable_panel(context),
        generate_parameters_panel(context),
    )
    right_panel = generate_scope_panel(context)
    bottom_panel = generate_expressions_panel(context)

    top_row = Columns([left_panels, right_panel], expand=True)
    group = Group(top_row, bottom_panel)

    console.print(group)
