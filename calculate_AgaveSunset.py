"""Calculation node definitions for AgaveSunset custom ComfyUI nodes."""

from __future__ import annotations

import math
from typing import Any, Dict


class CalculateAgaveSunset:
    """Perform math expressions using up to three input variables."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "a": ("FLOAT", {"default": 0.0}),
                "b": ("FLOAT", {"default": 0.0}),
                "c": ("FLOAT", {"default": 0.0}),
                "expression": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "a + b + c",
                        "placeholder": "Enter a Python expression using a, b, c",
                    },
                ),
            }
        }

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("result",)
    FUNCTION = "compute"
    CATEGORY = "AgaveSunset"

    def compute(self, a: float, b: float, c: float, expression: str):
        """Evaluate the provided expression within a constrained environment."""

        context = self._build_context(a=a, b=b, c=c)
        try:
            value = eval(expression, {"__builtins__": {}}, context)
        except Exception as exc:  # pragma: no cover - runtime evaluation errors
            raise ValueError(f"Failed to evaluate expression '{expression}': {exc}") from exc

        if isinstance(value, (int, float)):
            return (float(value),)

        raise ValueError(
            "Expression result must be a number; received " f"{type(value).__name__}."
        )

    def _build_context(self, **variables: float) -> Dict[str, Any]:
        """Build the local evaluation context for the expression."""

        math_functions = {
            name: getattr(math, name)
            for name in (
                "ceil",
                "floor",
                "sqrt",
                "log",
                "log10",
                "exp",
                "sin",
                "cos",
                "tan",
                "asin",
                "acos",
                "atan",
                "sinh",
                "cosh",
                "tanh",
                "pow",
            )
        }

        safe_builtins = {
            "abs": abs,
            "max": max,
            "min": min,
            "round": round,
        }

        context: Dict[str, Any] = {**variables, **math_functions, **safe_builtins}
        context["math"] = math
        return context
