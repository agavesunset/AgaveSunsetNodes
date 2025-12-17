# __init__.py (auto-discovery, fault-tolerant)

from __future__ import annotations

import importlib
import pkgutil

NODE_CLASS_MAPPINGS: dict = {}
NODE_DISPLAY_NAME_MAPPINGS: dict = {}

# Auto-scan modules in this package and merge mappings.
# - backward compatible: keep scanning *_agavesunset.py
# - forward compatible: also accept *_AS.py (if you rename files later)
# - fault tolerant: one bad module won't break the whole pack
_SUFFIXES = ("_agavesunset", "_AS")

for _, module_name, ispkg in pkgutil.iter_modules(__path__):
    if ispkg:
        continue
    if not module_name.endswith(_SUFFIXES):
        continue

    try:
        m = importlib.import_module(f".{module_name}", __name__)
    except Exception as e:
        print(f"[AgaveSunsetNodes] failed to import {module_name}: {e}")
        continue

    cls_map = getattr(m, "NODE_CLASS_MAPPINGS", None)
    disp_map = getattr(m, "NODE_DISPLAY_NAME_MAPPINGS", None)

    if isinstance(cls_map, dict):
        NODE_CLASS_MAPPINGS.update(cls_map)
    if isinstance(disp_map, dict):
        NODE_DISPLAY_NAME_MAPPINGS.update(disp_map)

WEB_DIRECTORY = "./web"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
