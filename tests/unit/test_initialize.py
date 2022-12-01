# unit/test_initialize.py
from aws_lambda_typing.context import Context
import jsonschema
import pytest

from functions.initialize import app


def test_initialize(env: dict[str, str], context: Context) -> None:
    event = {"amount": 1, "executionId": "dummy-id"}
    response = app.handler(event, context)
    schema = {
        "type": "object",
        "properties": {
            "amount": {"type": "integer"},
            "executionId": {"type": "string"},
            "packs": {
                # example: [[{"code": 7, "number": 2}]]
                "type": "array",
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "code": {"type": "integer"},
                            "number": {"type": "integer"},
                        },
                        "required": ["code", "number"],
                    },
                },
            },
        },
        "required": ["amount", "executionId", "packs"],
    }
    jsonschema.validate(response, schema)


def test_initialize_with_negative_amount(
    env: dict[str, str], context: Context
) -> None:
    event = {"amount": -1, "executionId": "dummy-id"}

    with pytest.raises(Exception):
        app.handler(event, context)


def test_initialize_with_large_amount(
    env: dict[str, str], context: Context
) -> None:
    event = {"amount": 999, "executionId": "dummy-id"}

    with pytest.raises(Exception):
        app.handler(event, context)
