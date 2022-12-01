# start_execution/app.py
import json
import logging
import os
from typing import Any

from aws_lambda_typing.context import Context
from aws_lambda_typing.events import APIGatewayProxyEventV1
from aws_lambda_typing.responses import APIGatewayProxyResponseV1
import boto3

ENDPOINT = os.getenv("ENDPOINT") or None
STATE_MACHINE_ARN = os.getenv("STATE_MACHINE_ARN", "")


def create_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger


def start_execution(input: str) -> dict[str, str]:
    client = boto3.client("stepfunctions", endpoint_url=ENDPOINT)
    response: dict[str, Any] = client.start_execution(
        stateMachineArn=STATE_MACHINE_ARN, input=input
    )

    execution_arn: str = response["executionArn"]
    execution_name = execution_arn.split(":")[-1]

    return {
        "execution_arn": execution_arn,
        "execution_name": execution_name,
        "start_date": response["startDate"].isoformat(),
    }


def handler(
    event: APIGatewayProxyEventV1, context: Context
) -> APIGatewayProxyResponseV1:
    logger = create_logger(context.function_name)
    logger.info(f"Lambda function started: {context.function_name}")

    execution_info = start_execution(event["body"])
    response: APIGatewayProxyResponseV1 = {
        "statusCode": 200,
        "headers": {},
        "body": json.dumps(execution_info),
        "multiValueHeaders": {},
        "isBase64Encoded": False,
    }
    return response
