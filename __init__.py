"""AgaveSunset custom nodes for ComfyUI."""

 codex/build-comfyui-node-type_agavesunset-ldjebk
from .calculate_AgaveSunset import CalculateAgaveSunset
from .type_AgaveSunset import TypeAgaveSunset

NODE_CLASS_MAPPINGS = {
    "calculate_AgaveSunset": CalculateAgaveSunset,
    "type_AgaveSunset": TypeAgaveSunset,
}


NODE_DISPLAY_NAME_MAPPINGS = {
    "calculate_AgaveSunset": "calculate_AgaveSunset",
    "type_AgaveSunset": "type_AgaveSunset",
}

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
]


