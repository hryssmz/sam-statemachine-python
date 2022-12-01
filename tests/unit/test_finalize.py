# unit/test_finalize.py
from aws_lambda_typing.context import Context

from functions.finalize import app


def test_finalize(env: dict[str, str], context: Context) -> None:
    event = {"winnings": [[2]], "executionId": "dummy-id"}
    response = app.handler(event, context)
    assert response == [2]
