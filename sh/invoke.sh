#!/bin/sh
BASEDIR="/home/hryssmz/docker/smz/projects/samlocal-python"
CONTAINER_HOST="172.17.0.1"
DOCKER_NETWORK="localstack_network"
ENDPOINT="http://localstack:4566"
ENV_PATH="envs/env.json"
EVENT_PATH="events/event.json"
FUNCTION_ID="ListExecutionsFunction"

sam local invoke "${FUNCTION_ID}" \
    --container-host "${CONTAINER_HOST}" \
    --container-host-interface 0.0.0.0 \
    --docker-network "${DOCKER_NETWORK}" \
    --docker-volume-basedir "${BASEDIR}/.aws-sam/build" \
    --event "${EVENT_PATH}" \
    --env-vars "${ENV_PATH}" \
    --parameter-overrides \
        "ParameterKey=Endpoint,ParameterValue=${ENDPOINT}" \
        "ParameterKey=EnvironmentType,ParameterValue=sam" \
    --region ap-northeast-1
