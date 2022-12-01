# apigateway/actions.py
from collections.abc import Callable
import json

import boto3
from config import DEFAULT_CLIENT_CONFIG
import jmespath

API_NAME = "HelloWorldApi"
RESOURCE_PATH = "/"
HTTP_METHOD = "POST"


CONFIG = {**DEFAULT_CLIENT_CONFIG}


def get_method() -> str:
    client = boto3.client("apigateway", **CONFIG)
    res1 = client.get_rest_apis()
    rest_api_id: str = jmespath.search(
        f"(items[?name=='{API_NAME}'].id)[0]", res1
    )
    res2 = client.get_resources(restApiId=rest_api_id)
    resource_id: str = jmespath.search(
        f"(items[?path=='{RESOURCE_PATH}'].id)[0]", res2
    )
    response = client.get_method(
        restApiId=rest_api_id, resourceId=resource_id, httpMethod=HTTP_METHOD
    )
    result = jmespath.search("@", response)
    return json.dumps(result, ensure_ascii=False, indent=2)


def get_resources() -> str:
    client = boto3.client("apigateway", **CONFIG)
    res = client.get_rest_apis()
    rest_api_id: str = jmespath.search(
        f"(items[?name=='{API_NAME}'].id)[0]", res
    )
    response = client.get_resources(restApiId=rest_api_id)
    result = jmespath.search(
        "items[*].{id: id, path: path, methods: keys(resourceMethods)}",
        response,
    )
    return json.dumps(result, ensure_ascii=False, indent=2)


def get_rest_apis() -> str:
    client = boto3.client("apigateway", **CONFIG)
    response = client.get_rest_apis()
    result = jmespath.search("items[*].{id: id, name: name}", response)
    return json.dumps(result, ensure_ascii=False, indent=2)


APIGATEWAY_ACTIONS: dict[str, Callable[[], str]] = {
    "get_method": get_method,
    "get_resources": get_resources,
    "get_rest_apis": get_rest_apis,
}
