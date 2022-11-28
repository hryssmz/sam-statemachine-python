#!/bin/sh
STACK_NAME="samlocal-python"

LOCALSTACK_HOSTNAME=localstack samlocal delete \
    --config-env samlocal \
    --stack-name "${STACK_NAME}"
