# maprange_agavesunset.py — map value from [src_min,src_max] to [dst_min,dst_max]
# Category: nodes_AgaveSunset
# Display name: maprange_AgaveSunset

class MapRangeAgaveSunset:
    """
    Map an input value from one range to another.
    t = (value - src_min) / (src_max - src_min)
    if clamp: t = min(max(t, 0), 1)
    result = dst_min + t * (dst_max - dst_min)
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": ("FLOAT", {"default": 0.0, "step": 0.01, "round": 0.001, "display": "number"}),
                "src_min": ("FLOAT", {"default": 0.0}),
                "src_max": ("FLOAT", {"default": 1.0}),
                "dst_min": ("FLOAT", {"default": 0.0}),
                "dst_max": ("FLOAT", {"default": 1.0}),
                "clamp": (["disable", "enable"],),
            }
        }

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("value",)
    FUNCTION = "map_value"
    CATEGORY = "nodes_AgaveSunset"

    def map_value(self, value, src_min, src_max, dst_min, dst_max, clamp):
        src_min = float(src_min); src_max = float(src_max)
        if src_max == src_min:
            raise ValueError("src_max must be different from src_min")

        t = (float(value) - src_min) / (src_max - src_min)
        if clamp == "enable":
            t = max(0.0, min(1.0, t))
        result = float(dst_min) + t * (float(dst_max) - float(dst_min))
        text = f"mapped: {result}"
        return {"ui": {"text": text}, "result": (result,)}

NODE_CLASS_MAPPINGS = {"MapRangeAgaveSunset": MapRangeAgaveSunset}
NODE_DISPLAY_NAME_MAPPINGS = {"MapRangeAgaveSunset": "maprange_AgaveSunset"}
