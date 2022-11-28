# dynamodb/actions.py
from collections.abc import Callable
import json

import boto3
from config import DEFAULT_CLIENT_CONFIG
import jmespath

TABLE_NAME = "JobTable"
CONFIG = {**DEFAULT_CLIENT_CONFIG}


def empty_table() -> str:
    dynamodb = boto3.resource("dynamodb", **CONFIG)
    table = dynamodb.Table(TABLE_NAME)
    res = table.scan()
    for id in jmespath.search("Items[*].id", res):
        table.delete_item(Key={"id": id})
    return TABLE_NAME


def scan_table() -> str:
    dynamodb = boto3.resource("dynamodb", **CONFIG)
    table = dynamodb.Table(TABLE_NAME)
    response = table.scan()
    result = jmespath.search("Items", response)
    return json.dumps(result, ensure_ascii=False, indent=2)


DYNAMODB_ACTIONS: dict[str, Callable[[], str]] = {
    "empty_table": empty_table,
    "scan_table": scan_table,
}
