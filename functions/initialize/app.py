# initialize/app.py
from datetime import datetime, timezone
import logging
import os
import random
from typing import Any

import boto3

MAX_BLOCK_SIZE = 5
MAX_AMOUNT = 30


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
    table = dynamodb.Table(os.getenv("EXECUTION_TABLE", ""))
    table.put_item(Item=item)


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    logger = create_logger(context.function_name)
    logger.info(f"Lambda function started: {context.function_name}")
    logger.info(f"Lambda event: {event}")

    amount: int = event["amount"]
    execution_id: str = event["executionId"]

    if amount < 0 or amount > MAX_AMOUNT:
        if amount < 0:
            message = "You cannot sell lotteries!"
        else:
            message = f"You don't have enough money to buy {amount} lotteries!"
        item = {
            "id": execution_id,
            "status": "error",
            "message": message,
        }
        put_item(item)
        raise Exception(message)
    else:
        item = {
            "id": execution_id,
            "amount": str(amount),
            "status": "pending",
            "startedAt": now_isoformat(),
        }
        put_item(item)

    lotteries = [
        {"number": i + 1, "code": random.randint(1, 9)} for i in range(amount)
    ]
    packs = [
        lotteries[i : i + MAX_BLOCK_SIZE]  # noqa: E203
        for i in range(0, amount, MAX_BLOCK_SIZE)
    ]

    return {"amount": amount, "packs": packs, "executionId": execution_id}
