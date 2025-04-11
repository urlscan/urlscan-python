from typing import Any


def cast_as_bool(v: Any) -> bool | None:
    if v is None:
        return None

    mapping = {"true": True, "1": True, "false": False, "0": False}
    lowered = str(v).lower()
    if lowered not in mapping:
        raise ValueError(f"Not a valid bool: {v}")

    return mapping[lowered]
