# sfn/actions.py
from collections.abc import Callable
import json
from typing import Any

import boto3
from config import DEFAULT_CLIENT_CONFIG
import jmespath
from utils.json_utils import convert

STATE_MACHINE_NAME = "LotteryStateMachine"
EXECUTION_NAME = "0671bfa8-5160-4573-bb54-0d63e1613ec4"

ARN_PREFIX = "arn:aws:states:ap-northeast-1:000000000000"
STATE_MACHINE_ARN = "{}:stateMachine:{}".format(ARN_PREFIX, STATE_MACHINE_NAME)
EXECUTION_ARN = "{}:execution:{}:{}".format(
    ARN_PREFIX, STATE_MACHINE_NAME, EXECUTION_NAME
)
CONFIG = {**DEFAULT_CLIENT_CONFIG}


def format_execution_history(response: Any) -> list[Any]:
    items = jmespath.search(
        "events[*].{id: id, type: type, state: (*.name)[0], "
        + "input: (*.input)[0], output: (*.output)[0], timestamp: timestamp}",
        convert(response),
    )
    return [
        {
            "id": item["id"],
            "type": item["type"],
            **({} if item["state"] is None else {"state": item["state"]}),
            **({} if item["input"] is None else {"input": item["input"]}),
            **({} if item["output"] is None else {"output": item["output"]}),
            "timestamp": item["timestamp"],
        }
        for item in items
    ]


def describe_execution() -> str:
    client = boto3.client("stepfunctions", **CONFIG)
    response = client.describe_execution(executionArn=EXECUTION_ARN)
    result = jmespath.search("@", convert(response))
    return json.dumps(result, ensure_ascii=False, indent=2)


def get_execution_history() -> str:
    client = boto3.client("stepfunctions", **CONFIG)
    response = client.get_execution_history(executionArn=EXECUTION_ARN)
    result = format_execution_history(response)
    return json.dumps(result, ensure_ascii=False, indent=2)


def last_execution() -> str:
    client = boto3.client("stepfunctions", **CONFIG)
    res = client.list_executions(stateMachineArn=STATE_MACHINE_ARN)
    execution_arn: str = jmespath.search("executions[0].executionArn", res)
    response = client.get_execution_history(executionArn=execution_arn)
    result = format_execution_history(response)
    return json.dumps(result, ensure_ascii=False, indent=2)


def list_executions() -> str:
    client = boto3.client("stepfunctions", **CONFIG)
    response = client.list_executions(stateMachineArn=STATE_MACHINE_ARN)
    result = jmespath.search("executions[*].name", response)
    return json.dumps(result, ensure_ascii=False, indent=2)


def list_executions_arn() -> str:
    client = boto3.client("stepfunctions", **CONFIG)
    response = client.list_executions(stateMachineArn=STATE_MACHINE_ARN)
    result = jmespath.search("executions[*].executionArn", response)
    return json.dumps(result, ensure_ascii=False, indent=2)


def list_state_machines() -> str:
    client = boto3.client("stepfunctions", **CONFIG)
    response = client.list_state_machines()
    result = jmespath.search("stateMachines[*].name", response)
    return json.dumps(result, ensure_ascii=False, indent=2)


def list_state_machines_arn() -> str:
    client = boto3.client("stepfunctions", **CONFIG)
    response = client.list_state_machines()
    result = jmespath.search("stateMachines[*].stateMachineArn", response)
    return json.dumps(result, ensure_ascii=False, indent=2)


SFN_ACTIONS: dict[str, Callable[[], str]] = {
    "describe_execution": describe_execution,
    "get_execution_history": get_execution_history,
    "last_execution": last_execution,
    "list_executions": list_executions,
    "list_executions_arn": list_executions_arn,
    "list_state_machines": list_state_machines,
    "list_state_machines_arn": list_state_machines_arn,
}
