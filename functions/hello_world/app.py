# hello_world/app.py
import json
import logging

from aws_lambda_typing.context import Context
from aws_lambda_typing.events import APIGatewayProxyEventV1
from aws_lambda_typing.responses import APIGatewayProxyResponseV1
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_global_ip() -> str:
    response = requests.get("http://ifconfig.me")
    return response.text


def handler(
    event: APIGatewayProxyEventV1, context: Context
) -> APIGatewayProxyResponseV1:
    logger.info("Begin execute handler")
    body = {
        "path": event["path"],
        "log_stream_name": context.log_stream_name,
        "global_ip": get_global_ip(),
        "message": "Hello World",
    }
    headers = {"X-Custom-Header": "My custom value"}
    response: APIGatewayProxyResponseV1 = {
        "statusCode": 200,
        "headers": headers,
        "body": json.dumps(body),
        "multiValueHeaders": {},
        "isBase64Encoded": False,
    }
    return response
