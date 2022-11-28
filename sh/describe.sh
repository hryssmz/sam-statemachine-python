#!/bin/sh
LOCALSTACK_URL="http://localstack:4566"
STACK_NAME="samlocal-python"

aws cloudformation describe-stacks \
    --endpoint "${LOCALSTACK_URL}" \
    --query "Stacks[0].Outputs" \
    --output text \
    --stack-name "${STACK_NAME}"
