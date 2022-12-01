ENDPOINT="http://localstack:4566"
LOCALSTACK_URL="http://localstack:4566"
STACK_NAME="samlocal-python"

docker container restart localstack
LOCALSTACK_HOSTNAME="localstack" samlocal deploy \
    --config-env samlocal \
    --parameter-overrides \
        "ParameterKey=Endpoint,ParameterValue=${ENDPOINT}" \
        "ParameterKey=ApigwEndpoint,ParameterValue=${LOCALSTACK_URL}" \
    --region ap-northeast-1 \
    --resolve-s3 \
    --stack-name "${STACK_NAME}"
