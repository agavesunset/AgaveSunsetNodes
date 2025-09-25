class TypeAgaveSunset:
    """
    A compact node that merges four common parameter widgets into one:
    - Int
    - Float
    - String
    - Boolean

    It simply passes the inputs through as outputs, so you can feed them
    to other nodes without creating four separate parameter nodes.
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "int_value": ("INT", {
                    "default": 0,
                    "min": -2147483648,
                    "max": 2147483647,
                    "step": 1,
                    "display": "number"
                }),
                "float_value": ("FLOAT", {
                    "default": 0.0,
                    "min": -1e9,
                    "max": 1e9,
                    "step": 0.01,
                    "round": 0.001,
                    "display": "number"
                }),
                "string_value": ("STRING", {
                    "multiline": False,
                    "default": ""
                }),
                "boolean_value": ("BOOLEAN", {
                    "default": False
                }),
            },
        }

    RETURN_TYPES = ("INT", "FLOAT", "STRING", "BOOLEAN")
    RETURN_NAMES = ("int", "float", "string", "boolean")
    FUNCTION = "pass_through"
    CATEGORY = "nodes_AgaveSunset"

    def pass_through(self, int_value, float_value, string_value, boolean_value):
        # No processing: just return the values as-is
        return (int(int_value), float(float_value), str(string_value), bool(boolean_value))


NODE_CLASS_MAPPINGS = {
    "TypeAgaveSunset": TypeAgaveSunset
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TypeAgaveSunset": "type_AgaveSunset"
}
