# action.py
import sys

from awslambda.actions import LAMBDA_ACTIONS
from dynamodb.actions import DYNAMODB_ACTIONS
from logs.actions import LOGS_ACTIONS

ACTIONS = {
    **DYNAMODB_ACTIONS,
    **LAMBDA_ACTIONS,
    **LOGS_ACTIONS,
}


def main() -> None:
    action_name = sys.argv[1].replace("-", "_")
    result = ACTIONS[action_name]()
    print(result)


if __name__ == "__main__":
    main()
