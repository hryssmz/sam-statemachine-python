# integration/test_empty_tables_api.py
import json

import requests

from tests.conftest import API_PREFIX


def test_empty_tables_api() -> None:
    url = f"{API_PREFIX}/empty/"
    response = requests.post(url)
    assert response.status_code == 200

    body = json.loads(response.text)
    assert type(body) is list
