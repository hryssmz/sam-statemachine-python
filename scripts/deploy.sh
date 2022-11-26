#!/bin/sh
docker container restart localstack
LOCALSTACK_HOSTNAME=localstack samlocal deploy --stack-name samlocal-python --resolve-s3
