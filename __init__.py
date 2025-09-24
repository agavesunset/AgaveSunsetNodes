"""AgaveSunset custom nodes for ComfyUI."""

 codex/build-comfyui-node-type_agavesunset-ldjebk
from .calculate_AgaveSunset import CalculateAgaveSunset
from .type_AgaveSunset import TypeAgaveSunset

NODE_CLASS_MAPPINGS = {
    "calculate_AgaveSunset": CalculateAgaveSunset,

from .type_AgaveSunset import TypeAgaveSunset

NODE_CLASS_MAPPINGS = {
 main
    "type_AgaveSunset": TypeAgaveSunset,
}


__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
]
