# action.py
import sys

from apigateway.actions import APIGATEWAY_ACTIONS
from awslambda.actions import LAMBDA_ACTIONS
from dynamodb.actions import DYNAMODB_ACTIONS
from logs.actions import LOGS_ACTIONS
from sfn.actions import SFN_ACTIONS

ACTIONS = {
    **APIGATEWAY_ACTIONS,
    **DYNAMODB_ACTIONS,
    **LAMBDA_ACTIONS,
    **LOGS_ACTIONS,
    **SFN_ACTIONS,
}


def main() -> None:
    action_name = sys.argv[1].replace("-", "_")
    result = ACTIONS[action_name]()
    print(result)


if __name__ == "__main__":
    main()
