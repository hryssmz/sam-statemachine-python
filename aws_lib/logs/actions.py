# logs/actions.py
from collections.abc import Callable
import json

import boto3
from config import DEFAULT_CLIENT_CONFIG
import jmespath

LIMIT = 50
LOG_GROUP_NAME = "/aws/lambda/ProcessJobFunction"
LOG_STREAM_NAME = "2022/11/27/[LATEST]ae1967a8"
CONFIG = {**DEFAULT_CLIENT_CONFIG}


def describe_log_groups() -> str:
    client = boto3.client("logs", **CONFIG)
    response = client.describe_log_groups(limit=LIMIT)
    result = jmespath.search("logGroups[*].logGroupName", response)
    return json.dumps(result, ensure_ascii=False, indent=2)


def describe_log_streams() -> str:
    client = boto3.client("logs", **CONFIG)
    response = client.describe_log_streams(
        logGroupName=LOG_GROUP_NAME,
        orderBy="LastEventTime",
        limit=LIMIT,
    )
    result = jmespath.search(("logStreams[*].logStreamName"), response)
    return json.dumps(result, ensure_ascii=False, indent=2)


def get_log_events() -> str:
    client = boto3.client("logs", **CONFIG)
    response = client.get_log_events(
        logGroupName=LOG_GROUP_NAME, logStreamName=LOG_STREAM_NAME, limit=LIMIT
    )
    result: str = jmespath.search("events[*].message | join('\n', @)", response)
    return result


def last_logs() -> str:
    client = boto3.client("logs", **CONFIG)
    res = client.describe_log_streams(
        logGroupName=LOG_GROUP_NAME,
        orderBy="LastEventTime",
        descending=True,
        limit=1,
    )
    log_stream_name = jmespath.search(("logStreams[0].logStreamName"), res)
    response = client.get_log_events(
        logGroupName=LOG_GROUP_NAME, logStreamName=log_stream_name, limit=LIMIT
    )
    result: str = jmespath.search("events[*].message | join('\n', @)", response)
    return result


LOGS_ACTIONS: dict[str, Callable[[], str]] = {
    "describe_log_groups": describe_log_groups,
    "describe_log_streams": describe_log_streams,
    "get_log_events": get_log_events,
    "last_logs": last_logs,
}
