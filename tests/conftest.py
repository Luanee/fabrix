# test_evaluator.py


import pytest

from fabrix.context import Context


@pytest.fixture
def ctx() -> Context:
    return Context(
        variables={"foo": 10, "bar": "baz", "val": 3.2},
        pipeline_parameters={
            "myString": "foo",
            "myNumber": 42,
            "threshold": 15,
            "prefix": "VAL:",
            "timestamp": "2024-01-01T12:00:00",
        },
    )
