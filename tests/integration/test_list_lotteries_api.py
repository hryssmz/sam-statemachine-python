# integration/test_list_lotteries_api.py
import json

import requests

from tests.conftest import API_PREFIX


def test_list_lotteries_api() -> None:
    url = f"{API_PREFIX}/lotteries/"
    response = requests.get(url)
    assert response.status_code == 200

    body = json.loads(response.text)
    assert type(body) is list
