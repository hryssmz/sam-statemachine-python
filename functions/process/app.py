# process/app.py
from datetime import datetime, timezone
import logging
import os
import time
from typing import Any
import uuid

import boto3

SLEEP_SEC = 1
WINNING_CODE = 7


def create_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger


def now_isoformat() -> str:
    utc_now = datetime.now(tz=timezone.utc)
    return utc_now.isoformat()


def put_item(item: dict[str, str]) -> None:
    endpoint_url = os.getenv("ENDPOINT") or None
    dynamodb = boto3.resource("dynamodb", endpoint_url=endpoint_url)
    table = dynamodb.Table(os.getenv("LOTTERY_TABLE", ""))
    table.put_item(Item=item)


def handler(event: dict[str, Any], context: Any) -> list[Any]:
    logger = create_logger(context.function_name)
    logger.info(f"Lambda function started: {context.function_name}")
    logger.info(f"Lambda event: {event}")

    pack: list[dict[str, Any]] = event["pack"]
    execution_id: str = event["executionId"]
    winnings: list[int] = []

    for lottery in pack:
        number: int = lottery["number"]
        code: int = lottery["code"]

        time.sleep(SLEEP_SEC)

        winning = "1" if code == WINNING_CODE else "0"
        item = {
            "id": str(uuid.uuid4()),
            "executionId": execution_id,
            "number": str(number),
            "code": str(code),
            "winning": winning,
            "createdAt": now_isoformat(),
        }
        put_item(item)

        if winning == "1":
            winnings.append(number)

    return winnings
