# file: transforms_agavesunset.py

class AnyType(str):
    def __ne__(self, other) -> bool:
        return False

WILDCARD = AnyType("*")


class Transforms_AgaveSunset:
    """
    Universal converter:
      - Accepts ANY input via 'value' (wildcard). If not connected, read 'value_text'.
      - Outputs: passthrough(*), INT, FLOAT, BOOLEAN, STRING
      - Robust parsing for numbers & booleans (CN/EN); never raises, shows UI warnings.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                # 用于手动输入时的类型提示（AUTO 自动推断）
                "parse_hint": (["AUTO", "INT", "FLOAT", "BOOLEAN", "STRING"], {"default": "AUTO"}),
            },
            "optional": {
                # 可接任何类型的输入。如果连接了，此值优先。
                "value": (WILDCARD,),
                # 未接线时作为备选：文本输入
                "value_text": ("STRING", {"default": "", "multiline": False}),
            },
        }

    RETURN_TYPES = (WILDCARD, "INT", "FLOAT", "BOOLEAN", "STRING")
    RETURN_NAMES = ("passthrough", "as_int", "as_float", "as_bool", "as_string")
    FUNCTION = "transform"
    CATEGORY = "AgaveSunset/utils"

    # ---------- helpers ----------
    _BOOL_TRUE = {
        "1", "true", "yes", "on", "t", "y",
        "是", "真", "开启", "开", "对", "赞成",
    }
    _BOOL_FALSE = {
        "0", "false", "no", "off", "f", "n", "",
        "否", "假", "关闭", "关", "错", "反对",
    }

    def _normalize_digits(self, s: str) -> str:
        # 全角数字/符号 → 半角；去首尾空白
        trans = str.maketrans("０１２３４５６７８９－．，＋+", "0123456789-.,++")
        return s.translate(trans).strip()

    def _from_text(self, text: str, hint: str):
        """Return a python value parsed from text according to hint/AUTO, plus warnings list."""
        warns = []
        raw = text
        txt = self._normalize_digits(text)

        def parse_bool(s: str):
            low = s.lower()
            if low in self._BOOL_TRUE:
                return True, None
            if low in self._BOOL_FALSE:
                return False, None
            return False, f"BOOLEAN parse failed for {raw!r}; expected 是/否 真/假 开/关 对/错 true/false yes/no on/off 1/0"

        if hint == "BOOLEAN":
            v, w = parse_bool(txt)
            if w:
                warns.append(w)
            return v, warns

        if hint == "INT":
            try:
                v = int(txt.replace(",", ""))
                return v, warns
            except Exception as e:
                warns.append(f"INT parse failed for {raw!r}: {e}; fallback 0")
                return 0, warns

        if hint == "FLOAT":
            try:
                v = float(txt.replace(",", ""))
                return v, warns
            except Exception as e:
                warns.append(f"FLOAT parse failed for {raw!r}: {e}; fallback 0.0")
                return 0.0, warns

        if hint == "STRING":
            return raw, warns

        # AUTO：先判 bool，再 int，再 float，否则字符串
        v_bool, w = parse_bool(txt)
        if w is None:
            return v_bool, warns

        try:
            v_int = int(txt.replace(",", ""))
            return v_int, warns
        except Exception:
            pass

        try:
            v_float = float(txt.replace(",", ""))
            return v_float, warns
        except Exception:
            pass

        return raw, warns

    def _to_int(self, v):
        try:
            if isinstance(v, bool):
                return int(v), None
            if isinstance(v, (int,)):
                return v, None
            if isinstance(v, float):
                return int(v), None
            if isinstance(v, str):
                nv, warns = self._from_text(v, "INT")
                return int(nv), (warns[0] if warns else None)
            # 其它类型：不可直转，回退 0
            return 0, f"INT fallback 0 for type {type(v).__name__}"
        except Exception as e:
            return 0, f"INT conversion error: {e}; fallback 0"

    def _to_float(self, v):
        try:
            if isinstance(v, bool):
                return 1.0 if v else 0.0, None
            if isinstance(v, (int, float)):
                return float(v), None
            if isinstance(v, str):
                nv, warns = self._from_text(v, "FLOAT")
                return float(nv), (warns[0] if warns else None)
            return 0.0, f"FLOAT fallback 0.0 for type {type(v).__name__}"
        except Exception as e:
            return 0.0, f"FLOAT conversion error: {e}; fallback 0.0"

    def _to_bool(self, v):
        try:
            if isinstance(v, bool):
                return v, None
            if isinstance(v, (int, float)):
                return (v != 0), None
            if isinstance(v, str):
                nv, warns = self._from_text(v, "BOOLEAN")
                return bool(nv), (warns[0] if warns else None)
            # 其它类型：Python 真值规则
            return bool(v), None
        except Exception as e:
            return False, f"BOOLEAN conversion error: {e}; fallback False"

    def _to_string(self, v):
        try:
            if isinstance(v, (int, float, bool, str)):
                return str(v), None
            # 其它对象：使用 repr/str，避免过长
            s = str(v)
            if len(s) > 512:
                s = s[:509] + "..."
            return s, None
        except Exception as e:
            return "", f"STRING conversion error: {e}; fallback ''"

    # ---------- main ----------
    def transform(self, parse_hint, value=None, value_text=""):
        warns = []

        # 选择数据源：优先接线的 value；否则用 value_text 解析
        if value is not None:
            src = value
            src_desc = f"from input ({type(value).__name__})"
        else:
            src, w = self._from_text(value_text, parse_hint)
            src_desc = f"from text {value_text!r} → {type(src).__name__}"
            warns.extend(w)

        # 转换
        as_int, wi = self._to_int(src);        wi and warns.append(wi)
        as_float, wf = self._to_float(src);    wf and warns.append(wf)
        as_bool, wb = self._to_bool(src);      wb and warns.append(wb)
        as_str, ws = self._to_string(src);     ws and warns.append(ws)

        # UI 展示
        ui_lines = [
            "Transforms (AgaveSunset)",
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

        return {"ui": {"text": ui_text},
                "result": (src, as_int, as_float, as_bool, as_str)}


# --- registration (for auto-scanning __init__.py) ---
NODE_CLASS_MAPPINGS = {
    "Transforms_input_AgaveSunset": Transforms_AgaveSunset,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "Transforms_input_AgaveSunset": "Transforms_input_AgaveSunset",
}
