import random
import uuid
from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field, PrivateAttr


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
    )
    pipeline: str = Field(
        default=random_name("Pipeline"),
        alias="Pipeline",
    )
    run_id: str = Field(
        default=str(uuid.uuid4()),
        alias="RunId",
    )
    trigger_id: str = Field(
        default=str(uuid.uuid4()),
        alias="TriggerId",
    )
    trigger_name: str = Field(
        default=random_name("Trigger"),
        alias="TriggerName",
    )
    trigger_time: str = Field(
        default=now_iso(),
        alias="TriggerTime",
    )
    group_id: str = Field(
        default=str(uuid.uuid4()),
        alias="GroupId",
    )
    triggered_by_pipeline_name: str | None = Field(
        default=None,
        alias="TriggeredByPipelineName",
    )
    triggered_by_pipeline_run_id: str | None = Field(
        default=None,
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
    title: str = "Expression"


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

    variables: dict[str, Any] = Field(default_factory=dict)
    pipeline_parameters: dict[str, Any] = Field(default_factory=dict)
    pipeline_scope_variables: Scope = Scope()
    _traces_: list[ExpressionTraceback] = PrivateAttr(default_factory=list)
