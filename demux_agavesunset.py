# demux_agavesunset.py — one input to multiple outputs (10-way demux)

from __future__ import annotations

from typing import Any


class AnyType(str):
    def __ne__(self, other: object) -> bool:
        return False


WILDCARD = AnyType("*")

# Try to import ExecutionBlocker (ComfyUI varies by version)
try:
    from comfy_execution import graph as graph_module

    ExecutionBlocker = graph_module.ExecutionBlocker
except Exception:
    try:
        from execution import ExecutionBlocker  # older fallback
    except Exception:

        class ExecutionBlocker:  # type: ignore
            def __init__(self, message):
                self.message = message


class Demux_AS:
    """
    Routes an input to one of 10 outputs based on integer selection [0..9].
    - Only selected output propagates the input.
    - Other outputs return an ExecutionBlocker to stop unused branches.
    - Also outputs selected_index.
    """

    FUNCTION = "demux"
    CATEGORY = "AgaveSunset/AS"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": (WILDCARD,),
                "select": ("INT", {"default": 0, "min": 0, "max": 9, "step": 1, "display": "number"}),
            }
        }

    RETURN_TYPES = (WILDCARD,) * 10 + ("INT",)
    RETURN_NAMES = tuple(f"out{i}" for i in range(10)) + ("selected_index",)

    def demux(self, input: Any, select: int):
        sel = int(select)
        if not (0 <= sel <= 9):
            raise ValueError(f"[Demux_AS] 'select' must be between 0 and 9 (got {sel})")

        value = input
        # Only unwrap singleton lists to avoid destroying intentional lists
        if isinstance(value, list) and len(value) == 1:
            value = value[0]

        blocker = ExecutionBlocker(None)
        outputs = [blocker for _ in range(10)]
        outputs[sel] = value
        outputs.append(sel)

        ui_text = f"select: {sel}\nselected: out{sel}"
        return {"ui": {"text": [ui_text]}, "result": tuple(outputs)}


NODE_CLASS_MAPPINGS = {"DemuxAgaveSunset": Demux_AS}
NODE_DISPLAY_NAME_MAPPINGS = {"DemuxAgaveSunset": "Demux_AS"}
