#!/bin/sh
BASEDIR="/home/hryssmz/docker/smz/projects/samlocal-python"
CONTAINER_HOST="172.17.0.1"
DOCKER_NETWORK="localstack_network"
ENDPOINT="http://localstack:4566"
ENV_PATH="envs/env.json"
PORT="13002"

sam local start-api \
    --host 0.0.0.0 \
    --port "${PORT}" \
    --container-host "${CONTAINER_HOST}" \
    --container-host-interface 0.0.0.0 \
    --docker-network "${DOCKER_NETWORK}" \
    --docker-volume-basedir "${BASEDIR}/.aws-sam/build" \
    --env-vars "${ENV_PATH}" \
    --parameter-overrides "ParameterKey=Endpoint,ParameterValue='${ENDPOINT}'"
