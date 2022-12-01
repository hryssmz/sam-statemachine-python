# unit/test_start_execution.py
import json
from typing import Any

from aws_lambda_typing.context import Context
from aws_lambda_typing.events import APIGatewayProxyEventV1
import boto3

from functions.start_execution import app


def test_start_execution(
    env: dict[str, str],
    apigw_event: APIGatewayProxyEventV1,
    context: Context,
    client_config: dict[str, Any],
) -> None:
    apigw_event["body"] = json.dumps({"amount": 1})
    response = app.handler(dict(apigw_event), context)
    assert response["statusCode"] == 200

    body = json.loads(response["body"])
    assert "execution_arn" in body

    execution_arn = body["execution_arn"]
    client = boto3.client("stepfunctions", **client_config)
    response = client.describe_execution(executionArn=execution_arn)
    assert response["status"] == "RUNNING"
