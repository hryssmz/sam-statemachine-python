# unit/test_list_lotteries.py
import json

from aws_lambda_typing.context import Context
from aws_lambda_typing.events import APIGatewayProxyEventV1

from functions.list_lotteries import app


def test_list_lotteries(
    env: dict[str, str], apigw_event: APIGatewayProxyEventV1, context: Context
) -> None:
    response = app.handler(dict(apigw_event), context)
    assert response["statusCode"] == 200

    body = json.loads(response["body"])
    assert type(body) is list


def test_list_lotteries_with_execution_id(
    env: dict[str, str], apigw_event: APIGatewayProxyEventV1, context: Context
) -> None:
    apigw_event["queryStringParameters"] = {"execution-id": "dummy-id"}
    response = app.handler(dict(apigw_event), context)
    assert response["statusCode"] == 200

    body = json.loads(response["body"])
    assert type(body) is list
