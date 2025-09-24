"""Calculation node definitions for AgaveSunset custom ComfyUI nodes."""

from __future__ import annotations

import math
from typing import Any, Dict


def _build_safe_context(values: Dict[str, float]) -> Dict[str, Any]:
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
        "round": round,
    }

    math_namespace.update(safe_builtins)
    math_namespace.update(values)
    return math_namespace


class CalculateAgaveSunset:
    """Evaluate math expressions using the provided variables."""

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
                        "default": "a + b + c",
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
        a: float,
        b: float,
        c: float,
        expression: str,
    ) -> tuple[float]:
        """Evaluate the user-provided math expression safely."""

        if not expression.strip():
            raise ValueError("Expression must not be empty.")

        context = _build_safe_context({"a": a, "b": b, "c": c})

        try:
            result = eval(expression, {"__builtins__": {}}, context)  # noqa: PGH001, S307
        except Exception as exc:  # noqa: BLE001
            raise ValueError(
                f"Failed to evaluate expression '{expression}': {exc}"
            ) from exc

        try:
            result_float = float(result)
        except (TypeError, ValueError) as exc:
            raise ValueError("Expression result cannot be converted to float") from exc

        return (result_float,)
