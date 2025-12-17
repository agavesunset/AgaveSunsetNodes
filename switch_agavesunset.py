# file: switch_agavesunset.py
from __future__ import annotations

from typing import Any, Optional


class AnyType(str):
    """Wildcard socket type for ComfyUI (matches anything)."""

    def __ne__(self, other: object) -> bool:
        return False


WILDCARD = AnyType("*")


class Switch_AS:
    """
    Multi-branch selector (Switch_AS)

    - Optional inputs: case0..case9, default
    - Required:
        index: selects caseN
        on_miss:
            use_default      -> use default if provided else first_connected else error
            first_connected  -> first connected case0..case9 else default else error
            last_connected   -> last connected case9..case0 else default else error
            error            -> error immediately
    """

    CATEGORY = "AgaveSunset/AS"
    FUNCTION = "switch"
    RETURN_TYPES = (WILDCARD,)
    RETURN_NAMES = ("output",)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "index": (
                    "INT",
                    {
                        "default": 0,
                        "min": 0,
                        "max": 9,  # we only have case0..case9
                        "step": 1,
                        "display": "number",
                    },
                ),
                "on_miss": (["use_default", "first_connected", "last_connected", "error"],),
            },
            "optional": {
                "case0": (WILDCARD,),
                "case1": (WILDCARD,),
                "case2": (WILDCARD,),
                "case3": (WILDCARD,),
                "case4": (WILDCARD,),
                "case5": (WILDCARD,),
                "case6": (WILDCARD,),
                "case7": (WILDCARD,),
                "case8": (WILDCARD,),
                "case9": (WILDCARD,),
                "default": (WILDCARD,),
            },
        }

    @staticmethod
    def _first_connected(cases: list[Optional[Any]]) -> tuple[Optional[Any], Optional[str]]:
        for i, v in enumerate(cases):
            if v is not None:
                return v, f"case{i}"
        return None, None

    @staticmethod
    def _last_connected(cases: list[Optional[Any]]) -> tuple[Optional[Any], Optional[str]]:
        for i in range(len(cases) - 1, -1, -1):
            if cases[i] is not None:
                return cases[i], f"case{i}"
        return None, None

    def switch(
        self,
        index: int,
        on_miss: str,
        case0=None,
        case1=None,
        case2=None,
        case3=None,
        case4=None,
        case5=None,
        case6=None,
        case7=None,
        case8=None,
        case9=None,
        default=None,
    ):
        cases = [case0, case1, case2, case3, case4, case5, case6, case7, case8, case9]
        idx = int(index)

        chosen = None
        chosen_src = None

        # direct selection
        if 0 <= idx < len(cases) and cases[idx] is not None:
            chosen = cases[idx]
            chosen_src = f"case{idx}"
        else:
            if on_miss == "use_default":
                if default is not None:
                    chosen, chosen_src = default, "default"
                else:
                    chosen, chosen_src = self._first_connected(cases)
                    if chosen is None:
                        raise ValueError("[Switch_AS] selected case missing and no default/connected case provided.")
            elif on_miss == "first_connected":
                chosen, chosen_src = self._first_connected(cases)
                if chosen is None and default is not None:
                    chosen, chosen_src = default, "default"
                if chosen is None:
                    raise ValueError("[Switch_AS] no connected branches to choose from.")
            elif on_miss == "last_connected":
                chosen, chosen_src = self._last_connected(cases)
                if chosen is None and default is not None:
                    chosen, chosen_src = default, "default"
                if chosen is None:
                    raise ValueError("[Switch_AS] no connected branches to choose from.")
            else:  # error
                raise ValueError("[Switch_AS] selected case is missing (on_miss=error).")

        ui_text = f"index: {idx}\nselected: {chosen_src}"
        return {"ui": {"text": [ui_text]}, "result": (chosen,)}


# ---- registration (auto-scanned by __init__.py) ----
NODE_CLASS_MAPPINGS = {
    # keep old node type key for backward compatibility
    "SwitchAgaveSunset": Switch_AS,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    # unify display name suffix to _AS
    "SwitchAgaveSunset": "Switch_AS",
}
