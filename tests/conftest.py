# test_evaluator.py


import pytest

from fabrix.context import Context


@pytest.fixture
def ctx() -> Context:
    return Context(
        variables={
            "foo": 10,
            "bar": "baz",
            "val": 3.2,
            "row_index": 0,
        },
        pipeline_parameters={
            "myString": "foo",
            "myNumber": 42,
            "threshold": 15,
            "prefix": "VAL:",
            "timestamp": "2024-01-01T12:00:00",
            "idx": 1,
            "key": "value",
        },
        activities={
            "CopyData": {
                "output": {
                    "rows": [{"value": 10}, {"value": 20}, {"value": 30}],
                    "meta": {"ok": True, "tags": ["a", "b", "c"]},
                }
            },
            "Bobs Task": {
                "output": {
                    "result": {
                        "message": "done",
                    }
                }
            },
        },
    )
