# compare_agavesunset.py
# Category: nodes_AgaveSunset
# Display name: compare_AgaveSunset
print("[AgaveSunset] loading compare_agavesunset.py")

# wildcard type (accepts any type)
class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False
any = AnyType("*")

def _to_number(x):
    """Best-effort convert to float, else raise."""
    # native numerics/bool
    if isinstance(x, (int, float, bool)):
        return float(x)
    # numpy scalar (if present)
    if hasattr(x, "item"):
        try:
            return float(x.item())
        except Exception:
            pass
    # single-element list/tuple
    if isinstance(x, (list, tuple)) and len(x) == 1 and isinstance(x[0], (int, float, bool)):
        return float(x[0])
    raise TypeError("Only numeric-like values can be ordered; for complex types use ==/!= or convert upstream.")

class CompareAgaveSunset:
    """
    Compare a and b with a selectable operator.
    - Inputs a, b: wildcard (any). Numbers are compared numerically; strings support ==/!= and ordering.
    - Operator: one of ==, !=, >, >=, <, <=
    - Output: BOOLEAN
    - If a/b are not connected, they default to 0.0.
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "operator": (["==", "!=", ">", ">=", "<", "<="],),
            },
            "optional": {
                "a": (any,),
                "b": (any,),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("result",)
    FUNCTION = "compare"
    CATEGORY = "nodes_AgaveSunset"

    def compare(self, operator, a=None, b=None):
        # default unconnected inputs to 0.0 for convenience
        a_val = 0.0 if a is None else a
        b_val = 0.0 if b is None else b

        # allow numeric comparison; support strings for eq/neq and ordering
        # decide comparison mode
        is_num_a = isinstance(a_val, (int, float, bool)) or hasattr(a_val, "item")
        is_num_b = isinstance(b_val, (int, float, bool)) or hasattr(b_val, "item")

        if operator in ("==", "!="):
            # direct Python equality for any types
            res = (a_val == b_val) if operator == "==" else (a_val != b_val)
            return (bool(res),)

        # ordering comparisons
        if is_num_a and is_num_b:
            a_num = _to_number(a_val)
            b_num = _to_number(b_val)
            if operator == ">":
                return (a_num > b_num,)
            elif operator == ">=":
                return (a_num >= b_num,)
            elif operator == "<":
                return (a_num < b_num,)
            elif operator == "<=":
                return (a_num <= b_num,)

        # strings can also be ordered lexicographically
        if isinstance(a_val, str) and isinstance(b_val, str):
            if operator == ">":
                return (a_val > b_val,)
            elif operator == ">=":
                return (a_val >= b_val,)
            elif operator == "<":
                return (a_val < b_val,)
            elif operator == "<=":
                return (a_val <= b_val,)

        # otherwise, unsupported ordering
        raise TypeError(f"Operator '{operator}' requires numeric or string inputs for ordering comparisons.")


# registration
NODE_CLASS_MAPPINGS = {
    "CompareAgaveSunset": CompareAgaveSunset
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CompareAgaveSunset": "compare_AgaveSunset"
}

print("[AgaveSunset] registered: CompareAgaveSunset => compare_AgaveSunset (nodes_AgaveSunset)")
