# unit/test_process.py
from typing import Any

from aws_lambda_typing.context import Context

from functions.process import app


def test_process(env: dict[str, str], context: Context, mocker: Any) -> None:
    mocker.patch("time.sleep")
    event = {
        "pack": [{"number": 1, "code": 1}, {"number": 2, "code": 7}],
        "executionId": "dummy-id",
    }
    response = app.handler(event, context)
    assert response == [2]
