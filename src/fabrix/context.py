import copy
import random
import uuid
from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field, PrivateAttr
from rich.text import Text
from rich.tree import Tree


def random_name(prefix="Pipeline") -> str:
    return f"{prefix}_{random.randint(10000, 99999)}"


def random_workspace() -> str:
    return f"ws-{uuid.uuid4().hex[:8]}"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class Scope(BaseModel):
    data_factory: str = Field(
        default=random_workspace(),
        alias="DataFactory",
        description="Name of the data or Synapse workspace the pipeline run is running in",
    )
    pipeline: str = Field(
        default=random_name("Pipeline"),
        description="Name of the pipeline",
        alias="Pipeline",
    )
    run_id: str = Field(
        default=str(uuid.uuid4()),
        description="ID of the specific pipeline run",
        alias="RunId",
    )
    trigger_id: str = Field(
        default=str(uuid.uuid4()),
        description="ID of the trigger that invoked the pipeline",
        alias="TriggerId",
    )
    trigger_name: str = Field(
        default=random_name("Trigger"),
        description="Name of the trigger that invoked the pipeline",
        alias="TriggerName",
    )
    trigger_time: str = Field(
        default=now_iso(),
        description="""
        Time of the trigger run that invoked the pipeline.
        This is the time at which the trigger actually fired to invoke the pipeline run,
        and it may differ slightly from the trigger's scheduled time.
        """,
        alias="TriggerTime",
    )
    group_id: str = Field(
        default=str(uuid.uuid4()),
        description="""
        ID of the group to which pipeline run belongs.
        In Microsoft Fabric, a 'group' refers to a collection of related resources
        that can be managed together. Groups are used to organize and control access to resources,
        making it easier to manage permissions and monitor activities across multiple pipelines.
        """,
        alias="GroupId",
    )
    triggered_by_pipeline_name: str | None = Field(
        default=None,
        description="""
        Name of the pipeline that triggers the pipeline run.
        Applicable when the pipeline run is triggered by an ExecutePipeline activity.
        Evaluate to Null when used in other circumstances. Note the question mark after @pipeline()
        """,
        alias="TriggeredByPipelineName",
    )
    triggered_by_pipeline_run_id: str | None = Field(
        default=None,
        description="""
        Run ID of the pipeline that triggers the pipeline run.
        Applicable when the pipeline run is triggered by an ExecutePipeline activity.
        Evaluate to Null when used in other circumstances. Note the question mark after @pipeline()
        """,
        alias="TriggeredByPipelineRunId",
    )

    def get_by_alias(self, alias: str) -> str | None:
        """
        Retrieve the value of a property by its alias name.

        Parameters
        ----------
        alias : str
            The field alias to retrieve.

        Returns
        -------
        str | None
            The value of the field with the given alias.

        Raises
        ------
        KeyError
            If the alias does not exist.
        """

        for field_name, model_field in Scope.model_fields.items():
            if model_field.alias == alias:
                return getattr(self, field_name)
        raise KeyError(f"Alias {alias!r} not found in {self.__class__.__name__}.")


class ExpressionTraceback:
    """Build and render a tree-like traceback of expression parsing and evaluation.

    This class uses `rich.tree.Tree` and `rich.text.Text` to build a styled,
    hierarchical tree representation of an expression evaluation process.
    Nodes are created for parse steps, functions, variables, parameters,
    literals, and errors. It can be used to trace evaluation logic in a
    readable, colored console format.

    Attributes
    ----------
    title : str
        Default root title for the tree ("Expression").
    _root : Tree
        Root node of the expression tree.
    _active_node : Tree
        Currently active node where children will be appended.
    stack : list[Tree]
        Stack of active tree nodes for nesting control.
    """

    title: str = "Expression"

    def __init__(self, title: str | None = None) -> None:
        """Initialize the expression traceback tree.

        Parameters
        ----------
        title : str | None, optional
            Optional title for the root node. Defaults to "Expression".
        """
        self._root = Tree(Text(title or self.title, style="bold cyan"))
        self._active_node = self._root
        self.stack: list[Tree] = [self._root]

    @property
    def root(self) -> Tree:
        """Return the root tree node."""
        return self._root

    def _get_or_create(self, mode: Literal["get", "create"]) -> Tree:
        """Get the active node or create a new child node.

        Parameters
        ----------
        mode : {"get", "create"}
            If "get", returns the current active node.
            If "create", creates a new child node and makes it active.

        Returns
        -------
        Tree
            The retrieved or newly created tree node.
        """
        if mode == "get":
            return self._active_node

        parent = self.stack[-1]
        child = parent.add(Text())
        self.stack.append(child)
        self._active_node = child
        return child

    def _set_node_label(
        self,
        node: Tree,
        label: Text,
        result: Any | None = None,
        result_style: str | None = None,
    ) -> None:
        """Set the label of a tree node, optionally appending a result.

        Parameters
        ----------
        node : Tree
            The node to set the label for.
        label : Text
            The label text.
        result : Any | None, optional
            Result value to append to the label.
        result_style : str | None, optional
            Style to apply to the result text.
        """
        node.label = label
        if result is not None:
            node.label = label.append(f" ➜ {result!r}", style=result_style)

    def pop(self) -> None:
        """Pop the last node off the stack if not at the root."""
        if len(self.stack) > 1:
            self.stack.pop()
            self._active_node = self.stack[-1]  # <-- keep active node in sync

    def add_parse_node(self, label: str | Text) -> None:
        """Add a parse step node.

        Parameters
        ----------
        label : str | Text
            Label for the parse step.
        """
        label = Text(f"Parse: {label}", style="yellow")
        node = self._get_or_create("create")
        self._set_node_label(node, label)

    def add_function_node(self, label: str | Text, result: Any | None = None, node: Tree | None = None) -> Tree:
        """Add a function node with optional result.

        Parameters
        ----------
        label : str | Text
            Function name label.
        result : Any | None, optional
            Result of the function call.
        node : Tree | None, optional
            Existing node to use instead of creating one.

        Returns
        -------
        Tree
            The created or reused function node.
        """
        label = Text("Function: ", style="magenta").append(Text(f"{label}", style="white"))
        node = node if node else self._get_or_create("create")
        self._set_node_label(node, label, result, result_style="green")

        if result is not None:
            self.pop()

        return node

    def add_variable_node(self, label: str | Text, result: Any | None = None) -> None:
        """Add a variable node with optional result.

        Parameters
        ----------
        label : str | Text
            Variable name.
        result : Any | None, optional
            Evaluated value of the variable.
        """
        label = (
            Text("variables('", style="blue").append(Text(f"{label}", style="white")).append(Text("')", style="blue"))
        )
        node = self._get_or_create("create")
        self._set_node_label(node, label, result, result_style="green")
        self.pop()

    def add_scope_node(self, label: str | Text, result: Any | None = None) -> None:
        """Add a pipeline scope node (e.g., `pipeline().<scope>`).

        Parameters
        ----------
        label : str | Text
            Pipeline scope name.
        result : Any | None, optional
            Evaluated value of the pipeline scope.
        """
        label = Text("pipeline().", style="blue").append(Text(f"{label}", style="white"))
        node = self._get_or_create("create")
        self._set_node_label(node, label, result, result_style="green")
        self.pop()

    def add_parameter_node(self, label: str | Text, result: Any | None = None) -> None:
        """Add a pipeline parameter node (e.g., `pipeline().parameters.<param>`).

        Parameters
        ----------
        label : str | Text
            Pipeline parameter name.
        result : Any | None, optional
            Evaluated value of the pipeline parameter.
        """
        label = Text("pipeline().parameters.", style="blue").append(Text(f"{label}", style="white"))
        node = self._get_or_create("create")
        self._set_node_label(node, label, result, result_style="green")
        self.pop()

    def add_activity_node(
        self, label: str | Text, path: str | Text, result: Any | None = None, node: Tree | None = None
    ) -> Tree:
        label = (
            Text("activity('", style="blue")
            .append(Text(f"{label}", style="white"))
            .append(Text("').output", style="blue"))
            .append(Text(f"{path}", style="white"))
        )
        node = node if node else self._get_or_create("create")
        self._set_node_label(node, label, result, result_style="green")

        if result is not None:
            self.pop()

        return node

    def add_literal_node(self, label: str | Text) -> None:
        """Add a literal value node.

        Parameters
        ----------
        label : str | Text
            Literal value as text.
        """
        label = Text(f"{label}", style="green")
        node = self._get_or_create("create")
        self._set_node_label(node, label)
        self.pop()

    def add_error(self, label: str, message: str, span: tuple[int, int] | None = None) -> None:
        """Add an error node to the tree.

        Highlights the error span in the label if provided, and adds
        a child node with the error message.

        Parameters
        ----------
        label : str
            Expression text containing the error.
        message : str
            Error message to display.
        span : tuple[int, int] | None, optional
            Optional (start, end) indices to highlight the error span.
        """
        if span:
            start, end = span
            error_text = Text(label[:start])
            error_text.append(label[start:end], style="bold red")
            error_text.append(label[end:])
        else:
            error_text = Text(label, style="bold red")
        error_node = self.stack[-1].add(error_text)
        error_msg_text = Text(message, style="red")
        error_node.add(error_msg_text)
        self.pop()


class Context(BaseModel):
    """
    Holds evaluation context, including variables, pipeline parameters, pipeline scope variables, and data.

    Attributes
    ----------
    variables : dict[str, Any]
        User variables available via variables('xyz').
    pipeline_parameters : dict[str, Any]
        Parameters provided by the pipeline, available via pipeline().parameters.xyz.
    pipeline_scope_variables : Scope
        Built-in pipeline-level variables (see below).
    """

    activities: dict[str, Any] = Field(default_factory=dict)
    variables: dict[str, Any] = Field(default_factory=dict)
    pipeline_parameters: dict[str, Any] = Field(default_factory=dict)
    pipeline_scope_variables: Scope = Scope()

    _traces_: list[ExpressionTraceback] = PrivateAttr(default_factory=list)

    def set_activity_output(self, activity_name: str, output: Any) -> None:
        """
        Store or update an activity's output payload.
        """
        self.activities.setdefault(activity_name, {}).update({"output": output})

    def get_activity_output(self, name: str) -> Any:
        """
        Retrieve the `.output` object for a given activity.

        Raises
        ------
        KeyError if the activity or its output is missing.
        """
        activity = self.activities.get(name)
        if not activity:
            raise KeyError(f"Activity '{name}' or its output is not available in context.activities.")

        return activity.get("output")

    def get_pipeline_scope_variable(
        self,
        name: Literal[
            "DataFactory",
            "Pipeline",
            "RunId",
            "TriggerId",
            "TriggerName",
            "TriggerTime",
            "GroupId",
            "TriggeredByPipelineName",
            "TriggeredByPipelineRunId",
        ]
        | str,
    ) -> str:
        """
        Get a pipeline scope variable by name from the context.

        Parameters
        ----------
        name : str
            The pipeline scope variable name.

        Returns
        -------
        Any or None
            The value if present, else None.
        """
        parameter = self.pipeline_scope_variables.get_by_alias(name)
        if not parameter:
            raise AttributeError(f"Invalid pipeline scope variable, got {name}, expected one of: x")
        return parameter

    def set_variable(self, name: str, value: int | str | bool | float | None) -> None:
        self.variables.setdefault(name, value)

    def get_variable(self, name: str) -> int | str | bool | float | None:
        """
        Get a variable by name from the context.

        Parameters
        ----------
        name : str
            The variable name.

        Returns
        -------
        Any or None
            The variable value if present, else None.
        """
        if name not in self.variables:
            raise KeyError(f"No variable with name {name} initialized.")
        return self.variables.get(name)

    def get_parameter(self, name: str) -> int | str | bool | float | None:
        """
        Get a base pipeline parameter by name from the context.

        Parameters
        ----------
        name : str
            The base pipeline parameter name.

        Returns
        -------
        Any or None
            The parameter value if present, else None.
        """
        if name not in self.pipeline_parameters:
            raise KeyError(f"No parameters with name {name} initialized.")
        return self.pipeline_parameters.get(name)

    def add_trace(self, title: str | None = None) -> None:
        trace = ExpressionTraceback(title)
        self._traces_.append(trace)
        self._active_trace = trace

    @property
    def active_trace(self) -> ExpressionTraceback:
        return self._active_trace
