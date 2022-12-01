# unit/test_empty_tables.py
import json
from typing import Any

from aws_lambda_typing.context import Context
from aws_lambda_typing.events import APIGatewayProxyEventV1
import boto3
import pytest

from functions.empty_tables import app


@pytest.fixture()
def put_item(env: dict[str, str], client_config: dict[str, Any]) -> None:
    dynamodb = boto3.resource("dynamodb", **client_config)
    table = dynamodb.Table(env["EXECUTION_TABLE"])
    table.put_item(Item={"id": "foo"})


def test_empty_tables(
    put_item: None, apigw_event: APIGatewayProxyEventV1, context: Context
) -> None:
    response = app.handler(dict(apigw_event), context)
    assert response["statusCode"] == 200

    body = json.loads(response["body"])
    assert type(body) is list
