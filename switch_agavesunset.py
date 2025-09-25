# switch_agavesunset.py — multi-branch selector (like a 'switch')
# Category: nodes_AgaveSunset
# Display name: switch_AgaveSunset

# Wildcard type that connects to anything
class AnyType(str):
    def __ne__(self, other) -> bool:
        return False
WILDCARD = AnyType("*")

class SwitchAgaveSunset:
    """
    Select a value from multiple branches by an integer index.
    - Inputs 'case0'..'case9' are optional wildcard sockets.
    - 'index' chooses which case to output.
    - If the chosen case is missing, handle it according to 'on_miss':
        * use_default: use 'default' if connected, otherwise try first_connected, else error
        * first_connected: use the first non-empty case (case0..case9)
        * last_connected:  use the last  non-empty case (case9..case0)
        * error: raise an error
    Output: selected value (passthrough type)
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "index": ("INT", {
                    "default": 0, "min": 0, "max": 99,
                    "step": 1, "display": "number"
                }),
                "on_miss": (["use_default", "first_connected", "last_connected", "error"],),
            },
            "optional": {
                # up to 10 branches; add more if needed
                "case0": (WILDCARD,),
                "case1": (WILDCARD,),
                "case2": (WILDCARD,),
                "case3": (WILDCARD,),
                "case4": (WILDCARD,),
                "case5": (WILDCARD,),
                "case6": (WILDCARD,),
                "case7": (WILDCARD,),
                "case8": (WILDCARD,),
                "case9": (WILDCARD,),
                "default": (WILDCARD,),
            }
        }

    RETURN_TYPES = (WILDCARD,)
    RETURN_NAMES = ("output",)
    FUNCTION = "switch"
    CATEGORY = "nodes_AgaveSunset"

    def switch(self, index, on_miss,
               case0=None, case1=None, case2=None, case3=None, case4=None,
               case5=None, case6=None, case7=None, case8=None, case9=None,
               default=None):
        cases = [case0, case1, case2, case3, case4, case5, case6, case7, case8, case9]
        chosen = None
        chosen_src = None

        # Preferred path: direct index when it exists and connected
        if 0 <= int(index) < len(cases) and cases[int(index)] is not None:
            chosen = cases[int(index)]
            chosen_src = f"case{int(index)}"
        else:
            # Fallback handling
            if on_miss == "use_default":
                if default is not None:
                    chosen = default
                    chosen_src = "default"
                else:
                    # try first_connected as a helpful fallback
                    for i, v in enumerate(cases):
                        if v is not None:
                            chosen = v
                            chosen_src = f"case{i}"
                            break
                    if chosen is None:
                        raise ValueError("[switch_AgaveSunset] selected case missing and no default/connected case provided.")
            elif on_miss == "first_connected":
                for i, v in enumerate(cases):
                    if v is not None:
                        chosen = v
                        chosen_src = f"case{i}"
                        break
                if chosen is None:
                    if default is not None:
                        chosen = default
                        chosen_src = "default"
                    else:
                        raise ValueError("[switch_AgaveSunset] no connected branches to choose from.")
            elif on_miss == "last_connected":
                for i in range(len(cases)-1, -1, -1):
                    if cases[i] is not None:
                        chosen = cases[i]
                        chosen_src = f"case{i}"
                        break
                if chosen is None:
                    if default is not None:
                        chosen = default
                        chosen_src = "default"
                    else:
                        raise ValueError("[switch_AgaveSunset] no connected branches to choose from.")
            else:  # "error"
                raise ValueError("[switch_AgaveSunset] selected case is missing (on_miss=error).")

        ui_text = f"index: {int(index)}\nselected: {chosen_src}"
        return {"ui": {"text": ui_text}, "result": (chosen,)}

# Registration
NODE_CLASS_MAPPINGS = {"SwitchAgaveSunset": SwitchAgaveSunset}
NODE_DISPLAY_NAME_MAPPINGS = {"SwitchAgaveSunset": "switch_AgaveSunset"}
