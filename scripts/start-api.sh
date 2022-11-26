#!/bin/sh
BASEDIR="/home/hryssmz/docker/smz/projects/samlocal-python"

sam local start-api \
    --host 0.0.0.0 \
    --port 13002 \
    --container-host 172.17.0.1 \
    --container-host-interface 0.0.0.0 \
    --docker-volume-basedir "${BASEDIR}/.aws-sam/build"
