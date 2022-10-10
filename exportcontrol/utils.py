from typing import Any

def to_int_or_default(value: Any, default: int) -> int:
    try:
        value = int(value)
        return value
    except Exception:
        return default
