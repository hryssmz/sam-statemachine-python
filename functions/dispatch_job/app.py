# dispatch_job/app.py
import json
import logging
import os

from aws_lambda_typing.context import Context
from aws_lambda_typing.events import APIGatewayProxyEventV1
from aws_lambda_typing.responses import APIGatewayProxyResponseV1
import boto3

ENDPOINT = os.getenv("ENDPOINT") or None
JOB_FUNCTION = os.getenv("JOB_FUNCTION_NAME", "")


def create_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger


def dispatch_job(job_id: str) -> int:
    client = boto3.client("lambda", endpoint_url=ENDPOINT)
    payload = {"job_id": job_id, "sleep_sec": 10}
    response = client.invoke(
        FunctionName=JOB_FUNCTION,
        InvocationType="Event",
        Payload=json.dumps(payload).encode("utf-8"),
    )
    status_code: int = response["StatusCode"]
    return status_code


def handler(
    event: APIGatewayProxyEventV1, context: Context
) -> APIGatewayProxyResponseV1:
    logger = create_logger(context.function_name)
    logger.info(f"Lambda function started: {context.function_name}")

    dispatch_job(context.aws_request_id)
    response: APIGatewayProxyResponseV1 = {
        "statusCode": 200,
        "headers": {},
        "body": json.dumps({}),
        "multiValueHeaders": {},
        "isBase64Encoded": False,
    }
    return response
