# demux8_agavesunset.py
# 一进八出（Demux 8-way）— 零依赖、与旧节点风格一致
# Category: nodes_AgaveSunset
# Display name 在 __init__.py 里设置为 "demux8_AgaveSunset"

# 与老节点一致的通配类型（不依赖外部模块）
class AnyType(str):
    def __ne__(self, other) -> bool:
        return False
WILDCARD = AnyType("*")

class Demux8AgaveSunset:
    """
    把单一输入 input1 路由到 8 个输出口之一（out1..out8），其余输出为 None。
    - 输入：
        input1: 任意类型（WILDCARD）
        route : INT，选择 1..8 中的一路（越界自动夹到合法范围）
        labels: STRING，逗号分隔的通道名，可用于 UI 提示（可选）
    - 输出：
        out1..out8: 仅选中的那一路得到 input1，其它为 None
        selected_label: STRING，实际选中的通道名
        selected_index: INT，实际选中的 1 起始索引
    """
    CATEGORY = "nodes_AgaveSunset"
    FUNCTION = "route"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input1": (WILDCARD, ),
                "route": ("INT", {
                    "default": 1, "min": 1, "max": 8,
                    "step": 1, "display": "number"
                }),
            },
            "optional": {
                "labels": ("STRING", {"default": "out1,out2,out3,out4,out5,out6,out7,out8"}),
            }
        }

    # 输出：8 个任意 + label + index
    RETURN_TYPES = (WILDCARD, WILDCARD, WILDCARD, WILDCARD,
                    WILDCARD, WILDCARD, WILDCARD, WILDCARD,
                    "STRING", "INT")
    RETURN_NAMES = ("out1", "out2", "out3", "out4",
                    "out5", "out6", "out7", "out8",
                    "selected_label", "selected_index")

    def route(self, input1, route=1, labels="out1,out2,out3,out4,out5,out6,out7,out8"):
        # 1) 解析/补齐标签
        raw = [x.strip() for x in (labels or "").split(",") if x.strip()]
        if len(raw) < 8:
            raw += [f"out{i+1}" for i in range(len(raw), 8)]
        label_list = raw[:8]

        # 2) 安全夹取索引 1..8
        try:
            idx = int(route)
        except Exception:
            idx = 1
        idx = max(1, min(8, idx))

        # 3) 构造输出
        outs = [None] * 8
        outs[idx - 1] = input1
        sel_label = label_list[idx - 1]
        sel_index = idx

        ui_text = f"route: {idx}\nselected: {sel_label}"
        return {"ui": {"text": ui_text}, "result": (*outs, sel_label, sel_index)}
