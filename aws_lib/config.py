# config.py
IS_LOCAL = True
ENDPOINT = "http://localhost:4566" if IS_LOCAL else None
REGION = "ap-northeast-1"

DEFAULT_CLIENT_CONFIG = {
    "endpoint_url": ENDPOINT,
    "region_name": REGION,
}
