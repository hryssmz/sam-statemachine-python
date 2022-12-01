# conftest.py
import json
import os
from typing import Any

from aws_lambda_typing.context import Client, ClientContext, Context, Identity
from aws_lambda_typing.events import APIGatewayProxyEventV1
import pytest

REGION = "ap-northeast-1"
API_PREFIX = "http://localhost:4566/restapis/yoikxuk77m/dev/_user_request_"
ARN_PREFIX = f"arn:aws:states:{REGION}:000000000000"
ENV_VARS = {
    # LocalStack endpoint
    "ENDPOINT": "http://localhost:4566",
    # DynamoDB table names
    "EXECUTION_TABLE": "ExecutionTable",
    "LOTTERY_TABLE": "LotteryTable",
    # State machine ARN
    "STATE_MACHINE_ARN": f"{ARN_PREFIX}:stateMachine:LotteryStateMachine",
}


@pytest.fixture()
def env() -> dict[str, str]:
    for k, v in ENV_VARS.items():
        os.environ[k] = v

    return ENV_VARS


@pytest.fixture()
def apigw_event() -> APIGatewayProxyEventV1:
    apigw_event = APIGatewayProxyEventV1(
        body=json.dumps({"message": "hello world"}),
        headers={
            "Accept": (
                "text/html,application/xhtml+xml,application/xml;q=0.9,"
                "image/webp,*/*;q=0.8"
            ),
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "en-US,en;q=0.8",
            "Cache-Control": "max-age=0",
            "CloudFront-Forwarded-Proto": "https",
            "CloudFront-Is-Desktop-Viewer": "true",
            "CloudFront-Is-Mobile-Viewer": "false",
            "CloudFront-Is-SmartTV-Viewer": "false",
            "CloudFront-Is-Tablet-Viewer": "false",
            "CloudFront-Viewer-Country": "US",
            "Host": "1234567890.execute-api.us-east-1.amazonaws.com",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Custom User Agent String",
            "Via": (
                "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net "
                "(CloudFront)"
            ),
            "X-Amz-Cf-Id": (
                "cDehVQoZnx43VYQb9j2-nvCh-9z396Uhbp027Y2JvkCPNLmGJHqlaA=="
            ),
            "X-Forwarded-For": "127.0.0.1, 127.0.0.2",
            "X-Forwarded-Port": "443",
            "X-Forwarded-Proto": "https",
        },
        httpMethod="GET",
        isBase64Encoded=False,
        multiValueHeaders={},
        multiValueQueryStringParameters={},
        path="/hello",
        pathParameters={"proxy": "/path/to/resource"},
        queryStringParameters={"foo": "bar"},
        requestContext={
            "accountId": "123456789012",
            "resourceId": "123456",
            "stage": "prod",
            "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
            "requestTime": "09/Apr/2015:12:34:56 +0000",
            "requestTimeEpoch": 1428582896000,
            "identity": {
                "cognitoIdentityPoolId": None,
                "accountId": None,
                "cognitoIdentityId": None,
                "caller": None,
                "accessKey": None,
                "sourceIp": "127.0.0.1",
                "cognitoAuthenticationType": None,
                "cognitoAuthenticationProvider": None,
                "userArn": None,
                "userAgent": "Custom User Agent String",
                "user": None,
            },
            "path": "/prod/hello",
            "resourcePath": "/hello",
            "httpMethod": "POST",
            "apiId": "1234567890",
            "protocol": "HTTP/1.1",
        },
        resource="/hello",
        stageVariables={"baz": "qux"},
    )
    return apigw_event


@pytest.fixture()
def context() -> Context:
    context = Context()
    context.aws_request_id = "AWS_REQUEST_ID"
    context.client_context = ClientContext(
        client=Client(
            app_package_name="APP_PACKAGE_NAME",
            app_title="APP_TITLE",
            app_version_code="APP_VERSION_CODE",
            app_version_name="APP_VERSION_NAME",
            installation_id="INSTALLATION_ID",
        ),
        custom={"key": "val"},
        env={"key": "val"},
    )
    context.function_name = "FUNCTION_NAME"
    context.function_version = "FUNCTION_VERSION"
    context.identity = Identity(
        cognito_identity_id="COGNITO_IDENTITY_ID",
        cognito_identity_pool_id="COGNITO_IDENTITY_POOL_ID",
    )
    context.invoked_function_arn = "INVOKED_FUNCTION_ARN"
    context.log_group_name = "LOG_GROUP_NAME"
    context.log_stream_name = "LOG_STREAM_NAME"
    context.memory_limit_in_mb = "MEMORY_LIMIT_IN_MB"
    return context


@pytest.fixture()
def client_config() -> dict[str, Any]:
    config = {
        "endpoint_url": ENV_VARS["ENDPOINT"],
        "region_name": REGION,
    }
    return config
