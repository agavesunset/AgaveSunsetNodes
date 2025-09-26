# __init__.py (auto-discovery version)

import importlib
import pkgutil

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

# 自动扫描当前包内的所有 *_agavesunset.py 模块并合并它们的映射
for _, module_name, ispkg in pkgutil.iter_modules(__path__):
    if ispkg:
        continue
    if not module_name.endswith("_agavesunset"):
        continue
    m = importlib.import_module(f".{module_name}", __name__)
    cls_map = getattr(m, "NODE_CLASS_MAPPINGS", None)
    disp_map = getattr(m, "NODE_DISPLAY_NAME_MAPPINGS", None)
    if isinstance(cls_map, dict):
        NODE_CLASS_MAPPINGS.update(cls_map)
    if isinstance(disp_map, dict):
        NODE_DISPLAY_NAME_MAPPINGS.update(disp_map)
WEB_DIRECTORY = "./web"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
