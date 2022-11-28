#!/bin/sh
ENDPOINT="http://localstack:4566"
STACK_NAME="samlocal-python"

LOCALSTACK_HOSTNAME="localstack" samlocal deploy \
    --config-env samlocal \
    --parameter-overrides "ParameterKey=Endpoint,ParameterValue='${ENDPOINT}'" \
    --resolve-s3 \
    --stack-name "${STACK_NAME}"
