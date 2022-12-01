# start_execution/app.py
import json
import logging
import os
from typing import Any

import boto3


def create_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger


def start_execution(input: str) -> dict[str, str]:
    endpoint_url = os.getenv("ENDPOINT") or None
    state_machine_arn = os.getenv("STATE_MACHINE_ARN", "")
    client = boto3.client("stepfunctions", endpoint_url=endpoint_url)
    response: dict[str, Any] = client.start_execution(
        stateMachineArn=state_machine_arn, input=input
    )

    execution_arn: str = response["executionArn"]
    execution_name = execution_arn.split(":")[-1]

    execution_info = {
        "execution_arn": execution_arn,
        "execution_name": execution_name,
        "start_date": response["startDate"].isoformat(),
    }
    return execution_info


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    logger = create_logger(context.function_name)
    logger.info(f"Lambda function started: {context.function_name}")
    logger.info(f"Lambda event: {event}")

    execution_info = start_execution(event["body"])
    response = {
        "statusCode": 200,
        "headers": {},
        "body": json.dumps(execution_info),
        "multiValueHeaders": {},
        "isBase64Encoded": False,
    }
    return response
