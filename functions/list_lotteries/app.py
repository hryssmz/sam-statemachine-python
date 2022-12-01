# list_loterries/app.py
import json
import logging
import os
from typing import Any

from aws_lambda_typing.context import Context
from aws_lambda_typing.events import APIGatewayProxyEventV1
from aws_lambda_typing.responses import APIGatewayProxyResponseV1
import boto3

ENDPOINT = os.getenv("ENDPOINT") or None
LOTTERY_TABLE = os.getenv("LOTTERY_TABLE", "")


def create_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger


def scan_table() -> list[Any]:
    dynamodb = boto3.resource("dynamodb", endpoint_url=ENDPOINT)
    table = dynamodb.Table(LOTTERY_TABLE)
    response = table.scan()
    items: list[Any] = response["Items"]
    return items


def handler(
    event: APIGatewayProxyEventV1, context: Context
) -> APIGatewayProxyResponseV1:
    logger = create_logger(context.function_name)
    logger.info(f"Lambda function started: {context.function_name}")
    query_params = event["queryStringParameters"]
    items = scan_table()

    if query_params is not None and "execution-id" in query_params:
        execution_id = query_params["execution-id"]
        items = [item for item in items if item["executionId"] == execution_id]

    response: APIGatewayProxyResponseV1 = {
        "statusCode": 200,
        "headers": {},
        "body": json.dumps(items),
        "multiValueHeaders": {},
        "isBase64Encoded": False,
    }
    return response
