@echo off
set LOCALSTACK_URL=http://localhost:4566
set STACK_NAME=samlocal-python

aws cloudformation describe-stacks ^
    --endpoint %LOCALSTACK_URL% ^
    --query Stacks[0].Outputs ^
    --output text ^
    --stack-name %STACK_NAME%
