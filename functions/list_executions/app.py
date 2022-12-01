# list_executions/app.py
import json
import logging
import os
from typing import Any

import boto3


def create_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger


def scan_table() -> list[dict[str, Any]]:
    endpoint_url = os.getenv("ENDPOINT") or None
    dynamodb = boto3.resource("dynamodb", endpoint_url=endpoint_url)
    table = dynamodb.Table(os.getenv("EXECUTION_TABLE", ""))
    items: list[dict[str, Any]] = table.scan()["Items"]
    return items


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    logger = create_logger(context.function_name)
    logger.info(f"Lambda function started: {context.function_name}")
    logger.info(f"Lambda event: {event}")

    items = scan_table()
    response = {
        "statusCode": 200,
        "headers": {},
        "body": json.dumps(items),
        "multiValueHeaders": {},
        "isBase64Encoded": False,
    }
    return response
