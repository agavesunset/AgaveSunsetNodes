# demux_agavesunset.py — one input to multiple outputs (8-channel demux)
# Category: nodes_AgaveSunset
# Display name: demux_AgaveSunset

# Wildcard type that accepts any connection (same approach as other nodes)
class AnyType(str):
    def __ne__(self, other) -> bool:
        return False

WILDCARD = AnyType("*")

# Attempt to get ExecutionBlocker class for blocking unused branches
try:
    from comfy_execution import graph as graph_module
    ExecutionBlocker = graph_module.ExecutionBlocker
except ImportError:
    try:
        from execution import ExecutionBlocker  # fallback for older ComfyUI versions
    except ImportError:
        # Define a dummy ExecutionBlocker if not available
        class ExecutionBlocker:
            def __init__(self, message): 
                self.message = message

class DemuxAgaveSunset:
    """
    Routes an input to one of 8 outputs based on an integer selection.
    Only the selected output propagates the input; all others output a blocker to halt execution.
    Also provides the selected index as an output.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": (WILDCARD, ),  # accept any type as input
                "select": ("INT", { "default": 0, "min": 0, "max": 9, "step": 1, "display": "number" })
            }
        }

    # Eight wildcard outputs and one INT output (selected index)
    RETURN_TYPES = (WILDCARD,)*10 + ("INT",)
    RETURN_NAMES = tuple(f"out{i}" for i in range(0, 10)) + ("selected_index",)
    FUNCTION = "demux"
    CATEGORY = "nodes_AgaveSunset"

    def demux(self, input, select):
        # Ensure select is an int in [0,9]
        sel = int(select)
        if sel < 0 or sel > 9:
            raise ValueError(f"[demux_AgaveSunset] 'select' must be between 0 and 9 (got {sel})")

        # Resolve actual input value (if it's a list with one element, unwrap it)
        value = input
        if isinstance(input, list) and len(input) > 0:
            value = input[0]

        # Create a blocker instance for unused outputs (silent blocking with None message)
        blocker = ExecutionBlocker(None)

        # Prepare results: all 10 outputs default to blocker
        outputs = [blocker] * 10
        # Place the real input on the selected channel
        outputs[sel] = value

        # Append the selected index as the ninth output
        outputs.append(sel)

        # Provide a UI text indicating the selection
        ui_text = f"select: {sel}\nselected: out{sel}"
        return { "ui": { "text": ui_text }, "result": tuple(outputs) }

# Registration (to integrate with AgaveSunsetNodes pack)
NODE_CLASS_MAPPINGS = { "DemuxAgaveSunset": DemuxAgaveSunset }
NODE_DISPLAY_NAME_MAPPINGS = { "DemuxAgaveSunset": "demux_AgaveSunset" }
