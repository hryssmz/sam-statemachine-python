# json_utils.py
from datetime import datetime
from decimal import Decimal
import json
from typing import Any, Optional, Union


def serializer(o: Any) -> Optional[Union[str, int, float]]:
    if isinstance(o, datetime):
        return o.isoformat()
    elif isinstance(o, Decimal):
        if o % 1 == 0:
            return int(o)
        else:
            return float(o)
    return None


def convert(o: Any) -> Any:
    json_str = json.dumps(o, default=serializer)
    return json.loads(json_str)
