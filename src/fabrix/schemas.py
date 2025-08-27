from enum import StrEnum

from pydantic import BaseModel


class Flags(StrEnum):
    NO_MATCH = "no_match"


class Expression(BaseModel):
    expression: str
    name: str | None = None
    variable: str | None = None
