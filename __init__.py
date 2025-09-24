"""AgaveSunset custom nodes for ComfyUI."""

from .calculate_AgaveSunset import CalculateAgaveSunset
from .type_AgaveSunset import TypeAgaveSunset

NODE_CLASS_MAPPINGS = {
    "type_AgaveSunset": TypeAgaveSunset,
    "calculate_AgaveSunset": CalculateAgaveSunset,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "type_AgaveSunset": "type_AgaveSunset",
    "calculate_AgaveSunset": "calculate_AgaveSunset",
}

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
]
