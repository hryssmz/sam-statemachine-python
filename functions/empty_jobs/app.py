# empty_jobs/app.py
import json
import logging
import os

from aws_lambda_typing.context import Context
from aws_lambda_typing.events import APIGatewayProxyEventV1
from aws_lambda_typing.responses import APIGatewayProxyResponseV1
import boto3

ENDPOINT = os.getenv("ENDPOINT") or None
JOB_TABLE = os.getenv("JOB_TABLE_NAME", "")


def create_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger


def empty_table() -> None:
    dynamodb = boto3.resource("dynamodb", endpoint_url=ENDPOINT)
    table = dynamodb.Table(JOB_TABLE)
    response = table.scan()
    items = response["Items"]
    for item in items:
        table.delete_item(Key={"id": item["id"]})


def handler(
    event: APIGatewayProxyEventV1, context: Context
) -> APIGatewayProxyResponseV1:
    logger = create_logger(context.function_name)
    logger.info(f"Lambda function started: {context.function_name}")

    empty_table()
    response: APIGatewayProxyResponseV1 = {
        "statusCode": 200,
        "headers": {},
        "body": json.dumps({}),
        "multiValueHeaders": {},
        "isBase64Encoded": False,
    }
    return response