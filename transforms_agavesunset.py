# file: transforms_agavesunset.py
from __future__ import annotations

from typing import Any, Tuple, List


class AnyType(str):
    """Wildcard socket type for ComfyUI (matches anything)."""

    def __ne__(self, other: object) -> bool:
        return False


WILDCARD = AnyType("*")


class Transforms_AS:
    """
    Universal converter (Transforms_input_AS)

    - Optional input:
        value(*): if connected, used as source
        value_text(STRING): fallback when value is not connected
    - Required:
        parse_hint: AUTO/INT/FLOAT/BOOLEAN/STRING (how to parse value_text when value is not connected)
    - Outputs:
        passthrough(*), INT, FLOAT, BOOLEAN, STRING
    - Never raises: shows warnings in ui.text when parsing/conversion falls back.
    """

    CATEGORY = "AgaveSunset/AS"
    FUNCTION = "transform"

    RETURN_TYPES = (WILDCARD, "INT", "FLOAT", "BOOLEAN", "STRING")
    RETURN_NAMES = ("passthrough", "as_int", "as_float", "as_bool", "as_string")

    _BOOL_TRUE = {"1", "true", "yes", "on", "t", "y", "是", "真", "开启", "开", "对", "赞成"}
    _BOOL_FALSE = {"0", "false", "no", "off", "f", "n", "", "否", "假", "关闭", "关", "错", "反对"}

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "parse_hint": (["AUTO", "INT", "FLOAT", "BOOLEAN", "STRING"], {"default": "AUTO"}),
            },
            "optional": {
                "value": (WILDCARD,),
                "value_text": ("STRING", {"default": "", "multiline": False}),
            },
        }

    @staticmethod
    def _normalize_digits(s: str) -> str:
        # full-width digits/symbols -> half-width; trim spaces
        trans = str.maketrans("０１２３４５６７８９－．，＋+", "0123456789-.,++")
        return s.translate(trans).strip()

    def _parse_bool(self, raw: str) -> Tuple[bool, str | None]:
        low = raw.lower()
        if low in self._BOOL_TRUE:
            return True, None
        if low in self._BOOL_FALSE:
            return False, None
        return (
            False,
            f"BOOLEAN parse failed for {raw!r}; expected 是/否 真/假 开/关 对/错 true/false yes/no on/off 1/0",
        )

    def _from_text(self, text: str, hint: str) -> Tuple[Any, List[str]]:
        warns: List[str] = []
        raw = text
        txt = self._normalize_digits(text)

        if hint == "BOOLEAN":
            v, w = self._parse_bool(txt)
            if w:
                warns.append(w)
            return v, warns

        if hint == "INT":
            try:
                return int(txt.replace(",", "")), warns
            except Exception as e:
                warns.append(f"INT parse failed for {raw!r}: {e}; fallback 0")
                return 0, warns

        if hint == "FLOAT":
            try:
                return float(txt.replace(",", "")), warns
            except Exception as e:
                warns.append(f"FLOAT parse failed for {raw!r}: {e}; fallback 0.0")
                return 0.0, warns

        if hint == "STRING":
            return raw, warns

        # AUTO: bool -> int -> float -> string
        v_bool, w = self._parse_bool(txt)
        if w is None:
            return v_bool, warns

        try:
            return int(txt.replace(",", "")), warns
        except Exception:
            pass

        try:
            return float(txt.replace(",", "")), warns
        except Exception:
            pass

        return raw, warns

    def _to_int(self, v: Any) -> Tuple[int, str | None]:
        try:
            if isinstance(v, bool):
                return int(v), None
            if isinstance(v, int):
                return v, None
            if isinstance(v, float):
                return int(v), None
            if isinstance(v, str):
                nv, warns = self._from_text(v, "INT")
                return int(nv), (warns[0] if warns else None)
            return 0, f"INT fallback 0 for type {type(v).__name__}"
        except Exception as e:
            return 0, f"INT conversion error: {e}; fallback 0"

    def _to_float(self, v: Any) -> Tuple[float, str | None]:
        try:
            if isinstance(v, bool):
                return (1.0 if v else 0.0), None
            if isinstance(v, (int, float)):
                return float(v), None
            if isinstance(v, str):
                nv, warns = self._from_text(v, "FLOAT")
                return float(nv), (warns[0] if warns else None)
            return 0.0, f"FLOAT fallback 0.0 for type {type(v).__name__}"
        except Exception as e:
            return 0.0, f"FLOAT conversion error: {e}; fallback 0.0"

    def _to_bool(self, v: Any) -> Tuple[bool, str | None]:
        try:
            if isinstance(v, bool):
                return v, None
            if isinstance(v, (int, float)):
                return (v != 0), None
            if isinstance(v, str):
                nv, warns = self._from_text(v, "BOOLEAN")
                return bool(nv), (warns[0] if warns else None)
            return bool(v), None
        except Exception as e:
            return False, f"BOOLEAN conversion error: {e}; fallback False"

    @staticmethod
    def _to_string(v: Any) -> Tuple[str, str | None]:
        try:
            s = str(v)
            if len(s) > 4096:
                s = s[:4093] + "..."
            return s, None
        except Exception as e:
            return "", f"STRING conversion error: {e}; fallback ''"

    def transform(self, parse_hint: str, value: Any = None, value_text: str = ""):
        warns: List[str] = []

        if value is not None:
            src = value
            src_desc = f"from input ({type(value).__name__})"
        else:
            src, w = self._from_text(value_text, parse_hint)
            src_desc = f"from text {value_text!r} -> {type(src).__name__}"
            warns.extend(w)

        as_int, wi = self._to_int(src)
        if wi:
            warns.append(wi)

        as_float, wf = self._to_float(src)
        if wf:
            warns.append(wf)

        as_bool, wb = self._to_bool(src)
        if wb:
            warns.append(wb)

        as_str, ws = self._to_string(src)
        if ws:
            warns.append(ws)

        ui_lines = [
            "Transforms_input_AS",
            f"source: {src_desc}",
            f"passthrough: {repr(src)}",
            f"as_int: {as_int}",
            f"as_float: {as_float}",
            f"as_bool: {as_bool}",
            f"as_string: {as_str!r}",
        ]
        for w in warns:
            if w:
                ui_lines.append(f"⚠ {w}")

        ui_text = "\n".join(ui_lines)
        return {"ui": {"text": [ui_text]}, "result": (src, as_int, as_float, as_bool, as_str)}


# ---- registration (auto-scanned by __init__.py) ----
NODE_CLASS_MAPPINGS = {
    # keep old node type key for backward compatibility
    "Transforms_input_AgaveSunset": Transforms_AS,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    # unify display name suffix to _AS
    "Transforms_input_AgaveSunset": "Transforms_input_AS",
}
