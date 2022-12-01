@echo off
set DOCKER_NETWORK=localstack_network
set ENDPOINT=http://localstack:4566
set ENV_PATH=envs\env.json
set EVENT_PATH=events\event.json
set FUNCTION_ID=ListExecutionsFunction

sam local invoke %FUNCTION_ID% ^
    --docker-network %DOCKER_NETWORK% ^
    --event %EVENT_PATH% ^
    --env-vars %ENV_PATH% ^
    --parameter-overrides ^
        ParameterKey=Endpoint,ParameterValue=%ENDPOINT% ^
        ParameterKey=EnvironmentType,ParameterValue=sam ^
    --region ap-northeast-1
