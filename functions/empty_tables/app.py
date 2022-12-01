# empty_tables/app.py
import json
import logging
import os
from typing import Any

import boto3


def create_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger


def empty_tables() -> list[str]:
    table_names = [
        os.getenv("EXECUTION_TABLE", ""),
        os.getenv("LOTTERY_TABLE", ""),
    ]
    endpoint_url = os.getenv("ENDPOINT") or None
    dynamodb = boto3.resource("dynamodb", endpoint_url=endpoint_url)

    for table_name in table_names:
        table = dynamodb.Table(table_name)
        items = table.scan()["Items"]
        for item in items:
            table.delete_item(Key={"id": item["id"]})

    return table_names


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    logger = create_logger(context.function_name)
    logger.info(f"Lambda function started: {context.function_name}")
    logger.info(f"Lambda event: {event}")

    table_names = empty_tables()
    response = {
        "statusCode": 200,
        "headers": {},
        "body": json.dumps(table_names),
        "multiValueHeaders": {},
        "isBase64Encoded": False,
    }
    return response
