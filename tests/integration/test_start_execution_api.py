# integration/test_start_execution_api.py
import json

import requests

from tests.conftest import API_PREFIX


def test_start_execution_api() -> None:
    url = f"{API_PREFIX}/"
    response = requests.post(url, json={"amount": 1})
    assert response.status_code == 200

    body = json.loads(response.text)
    assert "execution_arn" in body
