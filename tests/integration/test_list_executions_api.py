# integration/test_list_executions_api.py
import json

import requests

from tests.conftest import API_PREFIX


def test_list_executions_api() -> None:
    url = f"{API_PREFIX}/"
    response = requests.get(url)
    assert response.status_code == 200

    body = json.loads(response.text)
    assert type(body) is list
