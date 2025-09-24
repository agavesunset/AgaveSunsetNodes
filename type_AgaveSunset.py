"""Node definitions for AgaveSunset custom ComfyUI nodes."""

from __future__ import annotations


class TypeAgaveSunset:
    """Combine common primitive type widgets into a single node."""

    @classmethod
    def INPUT_TYPES(cls):
        number_widget = {
            "display": "number",
            "step": 0.01,
            "min": -1_000_000_000.0,
            "max": 1_000_000_000.0,
            "default": 0.0,
        }
        int_widget = {
            "display": "number",
            "step": 1,
            "min": -1_000_000_000,
            "max": 1_000_000_000,
            "default": 0,
        }

        return {
            "required": {
                "float_value": ("FLOAT", number_widget),
                "boolean_value": ("BOOLEAN", {"default": False}),
                "string_value": ("STRING", {"default": ""}),
                "int_value": ("INT", int_widget),
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
