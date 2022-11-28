# process_job/app.py
from datetime import datetime, timezone
import logging
import os
import time
from typing import Any
import uuid

from aws_lambda_typing.context import Context
import boto3

ENDPOINT = os.getenv("ENDPOINT") or None
JOB_TABLE = os.getenv("JOB_TABLE_NAME", "")


def create_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger


def now_isoformat() -> str:
    utc_now = datetime.now(tz=timezone.utc)
    return utc_now.isoformat()


def put_item(id: str) -> None:
    dynamodb = boto3.resource("dynamodb", endpoint_url=ENDPOINT)
    table = dynamodb.Table(JOB_TABLE)
    item = {"id": id, "created_at": now_isoformat()}
    table.put_item(Item=item)


def update_item(id: str) -> None:
    dynamodb = boto3.resource("dynamodb", endpoint_url=ENDPOINT)
    table = dynamodb.Table(JOB_TABLE)
    table.update_item(
        Key={"id": id},
        UpdateExpression="set updated_at = :updated_at",
        ExpressionAttributeValues={":updated_at": now_isoformat()},
    )


def handler(event: dict[str, Any], context: Context) -> None:
    logger = create_logger(context.function_name)
    logger.info(f"Lambda function started: {context.function_name}")

    job_id: str = event.get("job_id", str(uuid.uuid4()))
    sleep_sec: int = event.get("sleep_sec", 3)
    put_item(job_id)
    time.sleep(sleep_sec)
    update_item(job_id)
