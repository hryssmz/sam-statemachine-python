# finalize/app.py
from datetime import datetime, timezone
import json
import logging
import os
from typing import Any

import boto3


def create_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger


def now_isoformat() -> str:
    utc_now = datetime.now(tz=timezone.utc)
    return utc_now.isoformat()


def update_item(execution_id: str, winnings: str) -> None:
    endpoint_url = os.getenv("ENDPOINT") or None
    dynamodb = boto3.resource("dynamodb", endpoint_url=endpoint_url)
    table = dynamodb.Table(os.getenv("EXECUTION_TABLE", ""))
    table.update_item(
        Key={"id": execution_id},
        UpdateExpression="SET #f = :f, #s = :s, #w = :w",
        ExpressionAttributeNames={
            "#f": "finishedAt",
            "#s": "status",
            "#w": "winnings",
        },
        ExpressionAttributeValues={
            ":f": now_isoformat(),
            ":s": "success",
            ":w": winnings,
        },
    )


def handler(event: dict[str, Any], context: Any) -> list[int]:
    logger = create_logger(context.function_name)
    logger.info(f"Lambda function started: {context.function_name}")
    logger.info(f"Lambda event: {event}")

    execution_id: str = event["executionId"]
    winnings = [number for row in event["winnings"] for number in row]
    update_item(execution_id, json.dumps(winnings, ensure_ascii=False))

    return winnings
