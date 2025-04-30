import sys
import traceback

NODE_CLASS_MAPPINGS = {}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {}

try:
    from .cache_nodes import CacheModelAdaptive, CacheModelAuto, CacheModelPeriodic
    from .compile_node import PrunaCompileModel

    PRUNA_NODE_CLASS_MAPPINGS = {
        "PrunaCompileModel": PrunaCompileModel,
        "CacheModelAdaptive": CacheModelAdaptive,
        "CacheModelPeriodic": CacheModelPeriodic,
        "CacheModelAuto": CacheModelAuto,
    }

    PRUNA_NODE_DISPLAY_NAME_MAPPINGS = {
        "PrunaCompileModel": "Pruna Compile",
        "CacheModelAdaptive": "Pruna Cache Adaptive",
        "CacheModelPeriodic": "Pruna Cache Periodic",
        "CacheModelAuto": "Pruna Cache Auto",
    }
    NODE_CLASS_MAPPINGS.update(PRUNA_NODE_CLASS_MAPPINGS)
    NODE_DISPLAY_NAME_MAPPINGS.update(PRUNA_NODE_DISPLAY_NAME_MAPPINGS)
except Exception:
    print("ComfyUI_pruna: Pruna node import failed.")
    traceback.print_exception(*sys.exc_info())

if len(NODE_CLASS_MAPPINGS) == 0:
    raise Exception("import failed")
