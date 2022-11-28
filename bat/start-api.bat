@echo off
set DOCKER_NETWORK=localstack_network
set ENDPOINT=http://localstack:4566
set ENV_PATH=envs\env.json
set PORT=6000

sam local start-api ^
    --host 0.0.0.0 ^
    --port %PORT% ^
    --docker-network %DOCKER_NETWORK% ^
    --env-vars %ENV_PATH% ^
    --parameter-overrides ParameterKey=Endpoint,ParameterValue=%ENDPOINT%
