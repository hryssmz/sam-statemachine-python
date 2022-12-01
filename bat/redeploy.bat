@echo off
set ENDPOINT=http://localstack:4566
set LOCALSTACK_URL=http://localhost:4566
set STACK_NAME=samlocal-python

docker container restart localstack
samlocal deploy ^
    --config-env samlocal ^
    --parameter-overrides ^
        ParameterKey=Endpoint,ParameterValue=%ENDPOINT% ^
        ParameterKey=ApigwEndpoint,ParameterValue=%LOCALSTACK_URL% ^
    --resolve-s3 ^
    --stack-name %STACK_NAME%
