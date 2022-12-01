# unit/test_list_executions.py
import json

from aws_lambda_typing.context import Context
from aws_lambda_typing.events import APIGatewayProxyEventV1

from functions.list_executions import app


def test_list_executions(
    env: dict[str, str], apigw_event: APIGatewayProxyEventV1, context: Context
) -> None:
    response = app.handler(dict(apigw_event), context)
    assert response["statusCode"] == 200

    body = json.loads(response["body"])
    assert type(body) is list
