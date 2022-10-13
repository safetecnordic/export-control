def str_to_int_or_none(s: str) -> int | None:
    return int(s) if s is not None and s.isdecimal() else None
