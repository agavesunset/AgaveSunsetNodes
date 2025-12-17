# math_agavesunset.py — based on Math Expression (pysssss), refactored for AgaveSunsetNodes

from __future__ import annotations

import ast
import math
import operator as op
import random
from typing import Any, Dict


class AnyType(str):
    def __ne__(self, other: object) -> bool:
        return False


WILDCARD = AnyType("*")

# operators allowed
_OPERATORS = {
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
    ast.Or: lambda a, b: 1 if a or b else 0,
    ast.Not: lambda a: 0 if a else 1,
    ast.RShift: op.rshift,
    ast.LShift: op.lshift,
}

# functions allowed in expressions
_FUNCTIONS: Dict[str, Dict[str, Any]] = {
    "round": {"args": (1, 2), "call": lambda a, b=None: round(a, b), "hint": "number, dp? = 0"},
    "ceil": {"args": (1, 1), "call": lambda a: math.ceil(a), "hint": "number"},
    "floor": {"args": (1, 1), "call": lambda a: math.floor(a), "hint": "number"},
    "min": {"args": (2, None), "call": lambda *args: min(*args), "hint": "...numbers"},
    "max": {"args": (2, None), "call": lambda *args: max(*args), "hint": "...numbers"},
    "randomint": {"args": (2, 2), "call": lambda a, b: random.randint(a, b), "hint": "min, max"},
    "randomchoice": {"args": (2, None), "call": lambda *args: random.choice(args), "hint": "...numbers"},
    "sqrt": {"args": (1, 1), "call": lambda a: math.sqrt(a), "hint": "number"},
    "int": {"args": (1, 1), "call": lambda a=None: int(a), "hint": "number"},
    "iif": {"args": (3, 3), "call": lambda a, b, c=None: b if a else c, "hint": "cond, true, false"},
}

autocompleteWords = [
    {"text": x, "value": f"{x}()", "showValue": False, "hint": _FUNCTIONS[x]["hint"], "caretOffset": -1}
    for x in _FUNCTIONS.keys()
]


class Math_AS:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "expression": (
                    "STRING",
                    {
                        "multiline": True,
                        "dynamicPrompts": False,
                        "pysssss.autocomplete": {"words": autocompleteWords, "separator": ""},
                    },
                )
            },
            "optional": {
                "a": (WILDCARD,),
                "b": (WILDCARD,),
                "c": (WILDCARD,),
            },
            "hidden": {
                "extra_pnginfo": "EXTRA_PNGINFO",
                "prompt": "PROMPT",
            },
        }

    RETURN_TYPES = ("INT", "FLOAT")
    FUNCTION = "evaluate"
    CATEGORY = "AgaveSunset/AS"
    OUTPUT_NODE = True

    @classmethod
    def IS_CHANGED(cls, expression: str, **kwargs):
        # if expression includes random, treat as always changed
        if "random" in (expression or ""):
            return float("nan")
        return expression

    # ---- helpers ----
    def get_widget_value(self, extra_pnginfo, prompt, node_name: str, widget_name: str):
        workflow = extra_pnginfo["workflow"] if isinstance(extra_pnginfo, dict) and "workflow" in extra_pnginfo else {"nodes": []}
        node_id = None

        for node in workflow.get("nodes", []):
            name = node.get("type")

            props = node.get("properties") or {}
            if "Node name for S&R" in props:
                name = props["Node name for S&R"]

            if name == node_name:
                node_id = node.get("id")
                break

            title = node.get("title")
            if title == node_name:
                node_id = node.get("id")
                break

        if node_id is None:
            raise NameError(f"Node not found: {node_name}.{widget_name}")

        values = prompt.get(str(node_id), {})
        inputs = values.get("inputs", {})
        if widget_name not in inputs:
            raise NameError(f"Widget not found: {node_name}.{widget_name}")

        value = inputs[widget_name]
        if isinstance(value, list):
            raise ValueError("Converted widgets not supported via named reference; use inputs instead.")
        return value

    def get_size(self, target, prop: str):
        # latent dict: {"samples": tensor[B,C,H,W]} -> width/height = W*8 / H*8
        if isinstance(target, dict) and "samples" in target:
            samples = target["samples"]
            return samples.shape[3] * 8 if prop == "width" else samples.shape[2] * 8
        # image tensor: [B,H,W,C] or similar
        return target.shape[2] if prop == "width" else target.shape[1]

    # ---- evaluator ----
    def evaluate(self, expression: str, prompt, extra_pnginfo=None, a=None, b=None, c=None):
        expr = (expression or "").replace("\n", " ").replace("\r", "")
        node = ast.parse(expr, mode="eval").body
        lookup = {"a": a, "b": b, "c": c}

        def as_number(x):
            if isinstance(x, bool):
                return int(x)
            if isinstance(x, int):
                return x
            return float(x)

        def eval_expr(n):
            # constants
            if isinstance(n, ast.Constant):
                return n.value
            if isinstance(n, ast.Num):  # py<3.8 compat
                return n.n

            # binary ops
            if isinstance(n, ast.BinOp):
                l = as_number(eval_expr(n.left))
                r = as_number(eval_expr(n.right))
                return _OPERATORS[type(n.op)](l, r)

            # unary ops
            if isinstance(n, ast.UnaryOp):
                v = eval_expr(n.operand)
                fn = _OPERATORS.get(type(n.op))
                if fn is None:
                    raise TypeError(f"Unsupported unary op: {type(n.op).__name__}")
                return fn(as_number(v))

            # bool ops (And/Or can have >2 values)
            if isinstance(n, ast.BoolOp):
                fn = _OPERATORS.get(type(n.op))
                if fn is None:
                    raise TypeError(f"Unsupported bool op: {type(n.op).__name__}")
                v = eval_expr(n.values[0])
                for nxt in n.values[1:]:
                    v = fn(v, eval_expr(nxt))
                return v

            # comparisons (support chained)
            if isinstance(n, ast.Compare):
                left = eval_expr(n.left)
                for op_node, comp in zip(n.ops, n.comparators):
                    right = eval_expr(comp)
                    if isinstance(op_node, ast.Eq):
                        ok = left == right
                    elif isinstance(op_node, ast.NotEq):
                        ok = left != right
                    elif isinstance(op_node, ast.Gt):
                        ok = left > right
                    elif isinstance(op_node, ast.GtE):
                        ok = left >= right
                    elif isinstance(op_node, ast.Lt):
                        ok = left < right
                    elif isinstance(op_node, ast.LtE):
                        ok = left <= right
                    else:
                        raise NotImplementedError("Unsupported compare operator.")
                    if not ok:
                        return 0
                    left = right
                return 1

            # names
            if isinstance(n, ast.Name):
                if n.id in lookup:
                    val = lookup[n.id]
                    if isinstance(val, (int, float, bool, complex)):
                        return val
                    raise TypeError(f"Complex types need .width/.height, e.g. {n.id}.width")
                raise NameError(f"Name not found: {n.id}")

            # attribute access: a.width / a.height OR NodeName.WidgetName
            if isinstance(n, ast.Attribute):
                if not isinstance(n.value, ast.Name):
                    raise TypeError("Unsupported attribute base.")
                base = n.value.id
                attr = n.attr

                if base in lookup and attr in ("width", "height"):
                    return self.get_size(lookup[base], attr)

                return self.get_widget_value(extra_pnginfo or {}, prompt, base, attr)

            # function calls
            if isinstance(n, ast.Call):
                if not isinstance(n.func, ast.Name):
                    raise NameError("Invalid function call.")
                fname = n.func.id
                if fname not in _FUNCTIONS:
                    raise NameError(f"Invalid function call: {fname}")

                fn = _FUNCTIONS[fname]
                argc = len(n.args)
                min_args, max_args = fn["args"]
                if argc < min_args or (max_args is not None and argc > max_args):
                    to_err = " or more" if max_args is None else f" to {max_args}"
                    raise SyntaxError(f"Invalid function call: {fname} requires {min_args}{to_err} arguments")

                args = [eval_expr(arg) for arg in n.args]
                return fn["call"](*args)

            raise TypeError(f"Unsupported expression node: {type(n).__name__}")

        r = eval_expr(node)
        return {"ui": {"value": [r]}, "result": (int(r), float(r))}


NODE_CLASS_MAPPINGS = {"MathAgaveSunset": Math_AS}
NODE_DISPLAY_NAME_MAPPINGS = {"MathAgaveSunset": "Math_AS"}
