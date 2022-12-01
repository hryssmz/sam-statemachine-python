# dynamodb/actions.py
from collections.abc import Callable
import json

import boto3
from config import DEFAULT_CLIENT_CONFIG
import jmespath
from json_utils import convert

TABLE_NAME = "LotteryTable"
CONFIG = {**DEFAULT_CLIENT_CONFIG}


def empty_table() -> str:
    dynamodb = boto3.resource("dynamodb", **CONFIG)
    table = dynamodb.Table(TABLE_NAME)
    for id in jmespath.search("Items[*].id", table.scan()):
        table.delete_item(Key={"id": id})
    return TABLE_NAME


def empty_tables() -> str:
    client = boto3.client("dynamodb", **CONFIG)
    dynamodb = boto3.resource("dynamodb", **CONFIG)
    response = client.list_tables()
    table_names = jmespath.search("TableNames", response)
    for table_name in table_names:
        table = dynamodb.Table(table_name)
        for id in jmespath.search("Items[*].id", table.scan()):
            table.delete_item(Key={"id": id})
    return json.dumps(table_names, ensure_ascii=False, indent=2)


def scan_table() -> str:
    dynamodb = boto3.resource("dynamodb", **CONFIG)
    table = dynamodb.Table(TABLE_NAME)
    response = table.scan()
    result = jmespath.search("Items", convert(response))
    return json.dumps(result, ensure_ascii=False, indent=2)


DYNAMODB_ACTIONS: dict[str, Callable[[], str]] = {
    "empty_table": empty_table,
    "empty_tables": empty_tables,
    "scan_table": scan_table,
}
