# file: show_any_agavesunset.py
import json

# 真·通配类型（不要用字面量 "*"）
class AnyType(str):
    def __ne__(self, other) -> bool:
        return False
WILDCARD = AnyType("*")


class ShowAny_AgaveSunset:
    """
    Show Any (AgaveSunset)
    - 单输入口 anything(*)【必须接线：forceInput=True】
    - 前端扩展会在执行时创建“只读黑框”并显示下面这段 ui.text
    - 右侧输出口：原样透传（*）
    - IS_CHANGED：返回 NaN，避免缓存导致不刷新
    """

    CATEGORY = "AgaveSunset/utils"
    FUNCTION = "notify"
    OUTPUT_NODE = True

    # 透传输出（*）
    RETURN_TYPES = (WILDCARD,)
    RETURN_NAMES = ("output",)

    # （关键）只声明一个输入口；黑框不是这里的 widget，而是前端扩展动态创建
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

    # 让节点每次都被视为变化，强制刷新
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    # 把任意值变成可读字符串
    @staticmethod
    def _stringify(v):
        try:
            if isinstance(v, (dict, list, tuple, set)):
                return json.dumps(v, ensure_ascii=False, indent=2)
            return str(v)
        except Exception as e:
            return f"<unprintable {type(v).__name__}: {e}>"

    def notify(self, anything, unique_id=None, extra_pnginfo=None):
        text = self._stringify(anything)

        # 返回 ui.text（前端扩展会读取 message.text 来渲染黑框）
        # 同时原样透传输出 anything 以便继续串联
        return {
            "ui": {"text": text},
            "result": (anything,),
        }


# ---- 注册（你的自动扫描 __init__.py 会汇总它们）----
NODE_CLASS_MAPPINGS = {
    "Show_AgaveSunset": ShowAny_AgaveSunset,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "Show_AgaveSunset": "Show_AgaveSunset",
}
