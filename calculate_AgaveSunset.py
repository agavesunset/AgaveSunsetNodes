"""Calculation node definitions for AgaveSunset custom ComfyUI nodes.

The calculate_AgaveSunset node has to remain compatible with older
workflows that relied on the legacy "operation" drop-down while also
supporting the newer free-form expression workflow.
"""

from __future__ import annotations

import math
from typing import Any, Callable, Dict

Number = float
_EPSILON = 1e-9


def _safe_divide(numerator: Number, denominator: Number) -> Number:
    """Return ``numerator / denominator`` while guarding against zero division."""

    if abs(denominator) < _EPSILON:
        raise ValueError("Division by zero is not allowed.")
    return numerator / denominator


def _safe_modulo(numerator: Number, denominator: Number) -> Number:
    """Return ``numerator % denominator`` while guarding against zero division."""

    if abs(denominator) < _EPSILON:
        raise ValueError("Modulo by zero is not allowed.")
    return math.fmod(numerator, denominator)


def _clamp(value: Number, lower: Number, upper: Number) -> Number:
    """Clamp ``value`` between ``lower`` and ``upper`` (bounds order agnostic)."""

    low = min(lower, upper)
    high = max(lower, upper)
    return min(max(value, low), high)


def _build_safe_context(values: Dict[str, Number]) -> Dict[str, Any]:
    """Create a safe evaluation context for math expressions."""

    math_namespace = {
        name: getattr(math, name)
        for name in dir(math)
        if not name.startswith("_")
    }
    safe_builtins = {
        "abs": abs,
        "max": max,
        "min": min,
        "pow": pow,
        "round": round,
        "sum": sum,
    }

    helper_functions = {
        "clamp": _clamp,
    }

    context = {**math_namespace, **safe_builtins, **helper_functions}
    context.update(values)
    # Provide common aliases used by legacy workflows.
    alias_pairs = (("x", "a"), ("y", "b"), ("z", "c"), ("A", "a"), ("B", "b"), ("C", "c"))
    for alias, canonical in alias_pairs:
        context.setdefault(alias, values.get(canonical, 0.0))
    return context


OperationFunc = Callable[[Number, Number, Number], Number]


_OPERATION_FUNCTIONS: Dict[str, OperationFunc] = {
    "add_ab": lambda a, b, c: a + b,
    "add_abc": lambda a, b, c: a + b + c,
    "sub_ab": lambda a, b, c: a - b,
    "sub_abc": lambda a, b, c: a - b - c,
    "reverse_sub": lambda a, b, c: b - a,
    "mul_ab": lambda a, b, c: a * b,
    "mul_abc": lambda a, b, c: a * b * c,
    "div_ab": lambda a, b, c: _safe_divide(a, b),
    "div_abc": lambda a, b, c: _safe_divide(_safe_divide(a, b), c),
    "div_ba": lambda a, b, c: _safe_divide(b, a),
    "pow": lambda a, b, c: math.pow(a, b),
    "mod_ab": lambda a, b, c: _safe_modulo(a, b),
    "mod_abc": lambda a, b, c: _safe_modulo(_safe_modulo(a, b), c),
    "average": lambda a, b, c: (a + b + c) / 3.0,
    "average_ab": lambda a, b, c: (a + b) / 2.0,
    "max": lambda a, b, c: max(a, b, c),
    "min": lambda a, b, c: min(a, b, c),
    "clamp": lambda a, b, c: _clamp(a, b, c),
    "abs": lambda a, b, c: abs(a),
    "negate": lambda a, b, c: -a,
}

_DEFAULT_OPERATION_EXPRESSIONS: Dict[str, str] = {
    "add_ab": "a + b",
    "add_abc": "a + b + c",
    "sub_ab": "a - b",
    "sub_abc": "a - b - c",
    "reverse_sub": "b - a",
    "mul_ab": "a * b",
    "mul_abc": "a * b * c",
    "div_ab": "a / b",
    "div_abc": "a / b / c",
    "div_ba": "b / a",
    "pow": "a ** b",
    "mod_ab": "a % b",
    "mod_abc": "a % b % c",
    "average": "(a + b + c) / 3",
    "average_ab": "(a + b) / 2",
    "max": "max(a, b, c)",
    "min": "min(a, b, c)",
    "clamp": "clamp(a, b, c)",
    "abs": "abs(a)",
    "negate": "-a",
}

_OPERATION_ALIASES: Dict[str, str] = {
    "add": "add_ab",
    "addition": "add_ab",
    "plus": "add_ab",
    "a+b": "add_ab",
    "a + b": "add_ab",
    "sum": "add_ab",
    "sum_ab": "add_ab",
    "add_ab": "add_ab",
    "add(a,b)": "add_ab",
    "a+b+c": "add_abc",
    "a + b + c": "add_abc",
    "sum3": "add_abc",
    "add3": "add_abc",
    "sum_abc": "add_abc",
    "subtract": "sub_ab",
    "minus": "sub_ab",
    "a-b": "sub_ab",
    "a - b": "sub_ab",
    "sub": "sub_ab",
    "subtract_abc": "sub_abc",
    "a-b-c": "sub_abc",
    "a - b - c": "sub_abc",
    "b-a": "reverse_sub",
    "b - a": "reverse_sub",
    "reverse_sub": "reverse_sub",
    "swap_sub": "reverse_sub",
    "multiply": "mul_ab",
    "mul": "mul_ab",
    "a*b": "mul_ab",
    "a * b": "mul_ab",
    "product": "mul_ab",
    "multiply3": "mul_abc",
    "a*b*c": "mul_abc",
    "a * b * c": "mul_abc",
    "product3": "mul_abc",
    "divide": "div_ab",
    "division": "div_ab",
    "a/b": "div_ab",
    "a / b": "div_ab",
    "div": "div_ab",
    "divide3": "div_abc",
    "a/b/c": "div_abc",
    "a / b / c": "div_abc",
    "divabc": "div_abc",
    "b/a": "div_ba",
    "b / a": "div_ba",
    "div_ba": "div_ba",
    "power": "pow",
    "pow": "pow",
    "a^b": "pow",
    "a ** b": "pow",
    "a**b": "pow",
    "mod": "mod_ab",
    "modulo": "mod_ab",
    "a%b": "mod_ab",
    "a % b": "mod_ab",
    "mod3": "mod_abc",
    "a%b%c": "mod_abc",
    "a % b % c": "mod_abc",
    "average": "average",
    "avg": "average",
    "mean": "average",
    "average3": "average",
    "avg3": "average",
    "average_ab": "average_ab",
    "avg_ab": "average_ab",
    "avg2": "average_ab",
    "max": "max",
    "maximum": "max",
    "max3": "max",
    "min": "min",
    "minimum": "min",
    "min3": "min",
    "clamp": "clamp",
    "clamp_a": "clamp",
    "clamp(a,b,c)": "clamp",
    "abs": "abs",
    "absolute": "abs",
    "neg": "negate",
    "negative": "negate",
    "negate": "negate",
    "invert": "negate",
    "custom_expression": "custom_expression",
    "custom": "custom_expression",
    "expression": "custom_expression",
}


def _normalize_operation(operation: str) -> str:
    """Normalize an operation string to its canonical key."""

    if not isinstance(operation, str):
        return "add_ab"

    op_key = operation.strip().lower()
    op_key_compact = op_key.replace(" ", "")
    return _OPERATION_ALIASES.get(op_key, _OPERATION_ALIASES.get(op_key_compact, op_key))


def _evaluate_expression(expression: str, values: Dict[str, Number]) -> Number:
    """Safely evaluate a user-provided expression."""

    if not isinstance(expression, str) or not expression.strip():
        raise ValueError("Expression must not be empty.")

    context = _build_safe_context(values)
    try:
        result = eval(expression, {"__builtins__": {}}, context)  # noqa: PGH001, S307
    except Exception as exc:  # noqa: BLE001
        raise ValueError(f"Failed to evaluate expression '{expression}': {exc}") from exc

    try:
        return float(result)
    except (TypeError, ValueError) as exc:
        raise ValueError("Expression result cannot be converted to float.") from exc


class CalculateAgaveSunset:
    """Perform arithmetic between up to three variables with legacy support."""

    @classmethod
    def INPUT_TYPES(cls):
        number_widget = {
            "display": "number",
            "step": 0.01,
            "min": -1_000_000_000.0,
            "max": 1_000_000_000.0,
            "default": 0.0,
        }
        return {
            "required": {
                "a": ("FLOAT", number_widget),
                "b": ("FLOAT", number_widget),
                "c": ("FLOAT", number_widget),
                "operation": (
                    [
                        "add_ab",
                        "add_abc",
                        "sub_ab",
                        "sub_abc",
                        "reverse_sub",
                        "mul_ab",
                        "mul_abc",
                        "div_ab",
                        "div_abc",
                        "div_ba",
                        "pow",
                        "mod_ab",
                        "mod_abc",
                        "average",
                        "average_ab",
                        "max",
                        "min",
                        "clamp",
                        "abs",
                        "negate",
                        "custom_expression",
                    ],
                    {"default": "add_ab"},
                ),
                "expression": (
                    "STRING",
                    {
                        "default": "a + b",
                        "multiline": True,
                    },
                ),
            }
        }

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("result",)
    FUNCTION = "calculate"
    CATEGORY = "AgaveSunset"

    def calculate(
        self,
        a: Number,
        b: Number,
        c: Number,
        operation: str,
        expression: str = "",
    ) -> tuple[Number]:
        """Execute the configured calculation and return the resulting float."""

        op_key = _normalize_operation(operation)
        values = {"a": a, "b": b, "c": c}
        expr = expression.strip()

        if expr:
            canonical_expr = _DEFAULT_OPERATION_EXPRESSIONS.get(op_key)
            if (
                op_key == "custom_expression"
                or op_key not in _OPERATION_FUNCTIONS
                or canonical_expr is None
                or expr.replace(" ", "") != canonical_expr.replace(" ", "")
            ):
                return (_evaluate_expression(expr, values),)

        if op_key == "custom_expression":
            expr = expr or operation
            return (_evaluate_expression(expr, values),)

        if op_key in _OPERATION_FUNCTIONS:
            result = _OPERATION_FUNCTIONS[op_key](a, b, c)
            return (float(result),)

        # Fallback: treat the provided operation as an expression for legacy data.
        expr_source = expr or operation
        return (_evaluate_expression(expr_source, values),)
