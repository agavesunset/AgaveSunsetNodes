# file: show_any_agavesunset.py
from __future__ import annotations

import json
from typing import Any


class AnyType(str):
    """Wildcard socket type for ComfyUI (matches anything)."""

    def __ne__(self, other: object) -> bool:  # noqa: D401
        return False


WILDCARD = AnyType("*")


class ShowAny_AS:
    """
    Show Any (AS)
    - Input: anything(*) [forceInput=True]
    - Output: passthrough(*)
    - UI: returns ui.text for the frontend extension to render
    - IS_CHANGED: always NaN to force refresh (avoid cache)
    """

    CATEGORY = "AgaveSunset/AS"
    FUNCTION = "notify"
    OUTPUT_NODE = True

    RETURN_TYPES = (WILDCARD,)
    RETURN_NAMES = ("output",)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "anything": (WILDCARD, {"forceInput": True}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    @staticmethod
    def _stringify(v: Any) -> str:
        try:
            if isinstance(v, set):
                # make it JSON-friendly
                try:
                    v = sorted(v)
                except Exception:
                    v = list(v)

            if isinstance(v, (dict, list, tuple, set)):
                return json.dumps(v, ensure_ascii=False, indent=2)

            return str(v)
        except Exception as e:
            return f"<unprintable {type(v).__name__}: {e}>"

    def notify(self, anything: Any, unique_id=None, extra_pnginfo=None):
        text = self._stringify(anything)

        # IMPORTANT:
        # ui.text returns as a list to avoid any UI/transport edge-cases
        # (and keeps it consistent with many other ComfyUI nodes).
        return {
            "ui": {"text": [text]},
            "result": (anything,),
        }


# ---- registration (auto-scanned by __init__.py) ----
NODE_CLASS_MAPPINGS = {
    # keep the old node type key for backward compatibility
    "Show_AgaveSunset": ShowAny_AS,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    # display name unified to _AS
    "Show_AgaveSunset": "Show_AS",
}
