import datetime as dt
from enum import Enum
from typing import Any


def sanitize_dict(d: dict):
    for k, v in d.items():
        d[k] = sanitize_item(v)


def sanitize_item(item: Any) -> Any:
    """Sanitizes a value to use simple data.

    Args:
        item: Item to be sanatized.
        default: Optional function to be used when there is
            no case for an item type. Defaults to `None`.

    Returns:
        Any: Sanitized value.

    """
    if isinstance(item, dt.date):
        if isinstance(item, dt.datetime) and not item.tzinfo:
            return item.astimezone(dt.timezone.utc).isoformat()
        else:
            return item.isoformat()
    elif isinstance(item, Enum):
        return item.value
    elif hasattr(item, 'to_dict'):
        return item.to_dict()
    else:
        return item
