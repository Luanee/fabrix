"""
Custom exception types for the fabric_expression_builder package.
"""


class BaseExpressionError(Exception):
    """
    Base exception for all errors raised by the expression builder.
    """

    message: str

    def __init__(self, message: str) -> None:
        self.message = message


class FunctionNotFoundError(BaseExpressionError):
    """
    Raise when a requested function does not exist.

    Parameters
    ----------
    function_name : str
        The name of the missing function.
    """

    def __init__(
        self,
        message: str,
        span: tuple[int, int] | None = None,
    ) -> None:
        super().__init__(message)
        self.span = span


class ExpressionSyntaxError(BaseExpressionError):
    """User-friendly syntax error for Fabric/ADF expressions."""
