# awslambda/actions.py
import base64
from collections.abc import Callable
import json
from typing import Any

import boto3
from config import DEFAULT_CLIENT_CONFIG
import jmespath

FUNCTION_NAME = "ProcessJobFunction"
PAYLOAD: dict[str, Any] = {}
CONFIG = {**DEFAULT_CLIENT_CONFIG}


def invoke() -> str:
    client = boto3.client("lambda", **CONFIG)
    response = client.invoke(
        FunctionName=FUNCTION_NAME,
        InvocationType="RequestResponse",
        LogType="Tail",
        Payload=json.dumps(PAYLOAD).encode("utf-8"),
    )
    log_result = base64.b64decode(response["LogResult"]).decode("utf-8")
    print(log_result)
    result = {
        "StatusCode": response["StatusCode"],
        "Payload": json.loads(response["Payload"].read().decode("utf-8")),
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


def invoke_async() -> str:
    client = boto3.client("lambda", **CONFIG)
    response = client.invoke(
        FunctionName=FUNCTION_NAME,
        InvocationType="Event",
        Payload=json.dumps(PAYLOAD).encode("utf-8"),
    )
    result = {"StatusCode": response["StatusCode"]}
    return json.dumps(result, ensure_ascii=False, indent=2)


def list_functions() -> str:
    client = boto3.client("lambda", **CONFIG)
    response = client.list_functions()
    result = jmespath.search("Functions[*].FunctionName", response)
    return json.dumps(result, ensure_ascii=False, indent=2)


def list_functions_arn() -> str:
    client = boto3.client("lambda", **CONFIG)
    response = client.list_functions()
    result = jmespath.search("Functions[*].FunctionArn", response)
    return json.dumps(result, ensure_ascii=False, indent=2)


LAMBDA_ACTIONS: dict[str, Callable[[], str]] = {
    "invoke": invoke,
    "invoke_async": invoke_async,
    "list_functions": list_functions,
    "list_functions_arn": list_functions_arn,
}
