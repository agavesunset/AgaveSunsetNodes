"""Node definitions for AgaveSunset custom ComfyUI nodes."""

from __future__ import annotations


class TypeAgaveSunset:
    """Combine common primitive type widgets into a single node."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "float_value": ("FLOAT", {"default": 0.0, "step": 0.01}),
                "boolean_value": ("BOOLEAN", {"default": False}),
                "string_value": ("STRING", {"default": ""}),
                "int_value": ("INT", {"default": 0}),
            }
        }

    RETURN_TYPES = ("FLOAT", "BOOLEAN", "STRING", "INT")
    RETURN_NAMES = ("float", "boolean", "string", "int")
    FUNCTION = "produce"
    CATEGORY = "AgaveSunset"

    def produce(
        self,
        float_value: float,
        boolean_value: bool,
        string_value: str,
        int_value: int,
    ):
        """Return the configured primitive values."""

        return float_value, boolean_value, string_value, int_value
