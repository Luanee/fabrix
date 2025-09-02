from enum import StrEnum

from pydantic import BaseModel


class Flags(StrEnum):
    NO_MATCH = "no_match"
    LITERAL_MATCH = "literal_match"
    BOOLEAN_MATCH = "boolean_match"
    NUMBER_MATCH = "number_match"
    NULL_MATCH = "null_match"


class Expression(BaseModel):
    expression: str
    name: str | None = None
    variable: str | None = None
