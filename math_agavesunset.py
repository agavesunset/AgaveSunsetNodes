# math_agavesunset.py — based on Math Expression (pysssss), renamed & recategorized
import ast
import math
import random
import operator as op

# wildcard type (allows connecting various types; math uses numbers; images/latents can use .width/.height)
class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False
any = AnyType("*")

# operators allowed
operators = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Pow: op.pow,
    ast.BitXor: op.xor,
    ast.USub: op.neg,
    ast.Mod: op.mod,
    ast.BitAnd: op.and_,
    ast.BitOr: op.or_,
    ast.Invert: op.invert,
    ast.And: lambda a, b: 1 if a and b else 0,
    ast.Or:  lambda a, b: 1 if a or b else 0,
    ast.Not: lambda a: 0 if a else 1,
    ast.RShift: op.rshift,
    ast.LShift: op.lshift,
}

# math/utility functions available to expressions
functions = {
    "round":       {"args": (1, 2), "call": lambda a, b=None: round(a, b),     "hint": "number, dp? = 0"},
    "ceil":        {"args": (1, 1), "call": lambda a: math.ceil(a),            "hint": "number"},
    "floor":       {"args": (1, 1), "call": lambda a: math.floor(a),           "hint": "number"},
    "min":         {"args": (2, None), "call": lambda *args: min(*args),       "hint": "...numbers"},
    "max":         {"args": (2, None), "call": lambda *args: max(*args),       "hint": "...numbers"},
    "randomint":   {"args": (2, 2), "call": lambda a, b: random.randint(a, b), "hint": "min, max"},
    "randomchoice":{"args": (2, None), "call": lambda *args: random.choice(args), "hint": "...numbers"},
    "sqrt":        {"args": (1, 1), "call": lambda a: math.sqrt(a),            "hint": "number"},
    "int":         {"args": (1, 1), "call": lambda a=None: int(a),             "hint": "number"},
    "iif":         {"args": (3, 3), "call": lambda a, b, c=None: b if a else c,"hint": "value, truepart, falsepart"},
}

# autocomplete words metadata (for frontends that support it)
autocompleteWords = [{
    "text": x, "value": f"{x}()", "showValue": False, "hint": functions[x]["hint"], "caretOffset": -1
} for x in functions.keys()]

class MathAgaveSunset:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "expression": ("STRING", {
                    "multiline": True,
                    "dynamicPrompts": False,
                    "pysssss.autocomplete": {"words": autocompleteWords, "separator": ""}
                }),
            },
            "optional": {
                # keep wildcard style so a/b/c 可为任意可解析来源；负数/小数直接支持
                "a": (any,),
                "b": (any,),
                "c": (any,),
            },
            "hidden": {
                "extra_pnginfo": "EXTRA_PNGINFO",
                "prompt": "PROMPT",
            },
        }

    RETURN_TYPES = ("INT", "FLOAT")
    FUNCTION = "evaluate"
    CATEGORY = "nodes_AgaveSunset"
    OUTPUT_NODE = True  # 保持与原实现一致

    @classmethod
    def IS_CHANGED(s, expression, **kwargs):
        # 当表达式包含随机函数时，强制判定为变化
        if "random" in expression:
            return float("nan")
        return expression

    # —— helpers ——
    def get_widget_value(self, extra_pnginfo, prompt, node_name, widget_name):
        workflow = extra_pnginfo["workflow"] if "workflow" in extra_pnginfo else {"nodes": []}
        node_id = None
        for node in workflow["nodes"]:
            name = node["type"]
            if "properties" in node and "Node name for S&R" in node["properties"]:
                name = node["properties"]["Node name for S&R"]
            if name == node_name:
                node_id = node["id"]; break
            if "title" in node:
                name = node["title"]
            if name == node_name:
                node_id = node["id"]; break
        if node_id is not None:
            values = prompt[str(node_id)]
            if "inputs" in values and widget_name in values["inputs"]:
                value = values["inputs"][widget_name]
                if isinstance(value, list):
                    raise ValueError("Converted widgets not supported via named reference; use inputs instead.")
                return value
            raise NameError(f"Widget not found: {node_name}.{widget_name}")
        raise NameError(f"Node not found: {node_name}.{widget_name}")

    def get_size(self, target, prop):
        if isinstance(target, dict) and "samples" in target:  # latent
            return target["samples"].shape[3] * 8 if prop == "width" else target["samples"].shape[2] * 8
        else:  # image tensor
            return target.shape[2] if prop == "width" else target.shape[1]

    # —— evaluator ——
    def evaluate(self, expression, prompt, extra_pnginfo={}, a=None, b=None, c=None):
        # 允许负数/小数：不做任何裁剪，直接参与计算
        expression = expression.replace("\n", " ").replace("\r", "")
        node = ast.parse(expression, mode="eval").body
        lookup = {"a": a, "b": b, "c": c}

        def eval_op(node, l, r):
            l = eval_expr(l); r = eval_expr(r)
            l = l if isinstance(l, int) else float(l)
            r = r if isinstance(r, int) else float(r)
            return operators[type(node.op)](l, r)

        def eval_expr(node):
            if isinstance(node, ast.Constant) or isinstance(node, ast.Num):
                return node.n
            elif isinstance(node, ast.BinOp):
                return eval_op(node, node.left, node.right)
            elif isinstance(node, ast.BoolOp):
                return eval_op(node, node.values[0], node.values[1])
            elif isinstance(node, ast.UnaryOp):
                return operators[type(node.op)](eval_expr(node.operand))
            elif isinstance(node, ast.Attribute):
                if node.value.id in lookup:
                    if node.attr in ("width", "height"):
                        return self.get_size(lookup[node.value.id], node.attr)
                return self.get_widget_value(extra_pnginfo, prompt, node.value.id, node.attr)
            elif isinstance(node, ast.Name):
                if node.id in lookup:
                    val = lookup[node.id]
                    if isinstance(val, (int, float, complex)):
                        return val
                    else:
                        raise TypeError(f"Complex types (LATENT/IMAGE) need .width/.height, e.g. {node.id}.width")
                raise NameError(f"Name not found: {node.id}")
            elif isinstance(node, ast.Call):
                if node.func.id in functions:
                    fn = functions[node.func.id]; argc = len(node.args)
                    min_args, max_args = fn["args"]
                    if argc < min_args or (max_args is not None and argc > max_args):
                        toErr = " or more" if max_args is None else f" to {max_args}"
                        raise SyntaxError(f"Invalid function call: {node.func.id} requires {min_args}{toErr} arguments")
                    args = [eval_expr(arg) for arg in node.args]
                    return fn["call"](*args)
                raise NameError(f"Invalid function call: {node.func.id}")
            elif isinstance(node, ast.Compare):
                l = eval_expr(node.left); r = eval_expr(node.comparators[0])
                if   isinstance(node.ops[0], ast.Eq):   return 1 if l == r else 0
                elif isinstance(node.ops[0], ast.NotEq):return 1 if l != r else 0
                elif isinstance(node.ops[0], ast.Gt):   return 1 if l > r else 0
                elif isinstance(node.ops[0], ast.GtE):  return 1 if l >= r else 0
                elif isinstance(node.ops[0], ast.Lt):   return 1 if l < r else 0
                elif isinstance(node.ops[0], ast.LtE):  return 1 if l <= r else 0
                else:
                    raise NotImplementedError("Unsupported compare operator.")
            else:
                raise TypeError(node)

        r = eval_expr(node)
        return {"ui": {"value": [r]}, "result": (int(r), float(r))}

# registration
NODE_CLASS_MAPPINGS = {"MathAgaveSunset": MathAgaveSunset}
NODE_DISPLAY_NAME_MAPPINGS = {"MathAgaveSunset": "math_AgaveSunset"}
