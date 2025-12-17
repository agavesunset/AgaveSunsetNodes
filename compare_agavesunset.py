# compare_agavesunset.py

from __future__ import annotations

from typing import Any, Optional


class AnyType(str):
    """Wildcard socket type for ComfyUI (matches anything)."""

    def __ne__(self, other: object) -> bool:
        return False


WILDCARD = AnyType("*")


def _unwrap_singleton(x: Any) -> Any:
    if isinstance(x, (list, tuple)) and len(x) == 1:
        return x[0]
    return x


def _to_number(x: Any) -> float:
    """
    Best-effort numeric conversion:
    - int/float/bool
    - numpy scalar via .item()
    - numeric strings ("3.14")
    - singleton list/tuple wrapping numeric
    """
    x = _unwrap_singleton(x)

    if isinstance(x, (int, float, bool)):
        return float(x)

    if hasattr(x, "item"):
        try:
            return float(x.item())
        except Exception:
            pass

    if isinstance(x, str):
        s = x.strip()
        # allow numeric strings
        try:
            return float(s)
        except Exception as e:
            raise TypeError(f"String is not numeric: {x!r}") from e

    raise TypeError(
        "Only numeric-like values can be ordered. "
        "For complex types use ==/!= or convert upstream."
    )


class Compare_AS:
    """
    Compare two values with an operator.
    - Inputs a,b: wildcard (optional). Unconnected defaults to 0.0.
    - Operator: ==, !=, >, >=, <, <=
    - Output: BOOLEAN
    """

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("result",)
    FUNCTION = "compare"
    CATEGORY = "AgaveSunset/AS"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "operator": (["==", "!=", ">", ">=", "<", "<="],),
            },
            "optional": {
                "a": (WILDCARD,),
                "b": (WILDCARD,),
            },
        }

    def compare(self, operator: str, a: Optional[Any] = None, b: Optional[Any] = None):
        a_val = 0.0 if a is None else a
        b_val = 0.0 if b is None else b

        # equality: allow any python types
        if operator == "==":
            res = (a_val == b_val)
        elif operator == "!=":
            res = (a_val != b_val)
        else:
            # ordering: prefer numeric if both parse as numbers
            try:
                a_num = _to_number(a_val)
                b_num = _to_number(b_val)
                if operator == ">":
                    res = a_num > b_num
                elif operator == ">=":
                    res = a_num >= b_num
                elif operator == "<":
                    res = a_num < b_num
                elif operator == "<=":
                    res = a_num <= b_num
                else:
                    raise ValueError(f"Unknown operator: {operator}")
            except Exception:
                # fallback: lexicographic only when both are strings
                if isinstance(a_val, str) and isinstance(b_val, str):
                    if operator == ">":
                        res = a_val > b_val
                    elif operator == ">=":
                        res = a_val >= b_val
                    elif operator == "<":
                        res = a_val < b_val
                    elif operator == "<=":
                        res = a_val <= b_val
                    else:
                        raise ValueError(f"Unknown operator: {operator}")
                else:
                    raise TypeError(
                        f"Operator {operator!r} requires numeric or string inputs for ordering."
                    )

        ui_text = f"{a_val!r} {operator} {b_val!r} -> {bool(res)}"
        return {"ui": {"text": [ui_text]}, "result": (bool(res),)}


# registration (keep old type key; unify display name suffix)
NODE_CLASS_MAPPINGS = {"CompareAgaveSunset": Compare_AS}
NODE_DISPLAY_NAME_MAPPINGS = {"CompareAgaveSunset": "Compare_AS"}
