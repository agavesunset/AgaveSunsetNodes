"""AgaveSunset custom nodes for ComfyUI."""

from .type_AgaveSunset import TypeAgaveSunset

NODE_CLASS_MAPPINGS = {
    "type_AgaveSunset": TypeAgaveSunset,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "type_AgaveSunset": "type_AgaveSunset",
}

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
]
