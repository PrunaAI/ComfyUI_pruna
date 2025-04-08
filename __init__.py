import sys
import traceback

NODE_CLASS_MAPPINGS = {}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {}

try:
    from .cache_nodes import CacheModelAdaptive, CacheModelPeriodic
    from .compile_node import CompileModel

    PRUNA_NODE_CLASS_MAPPINGS = {
        "CompileModel": CompileModel,
        "CacheModelAdaptive": CacheModelAdaptive,
        "CacheModelPeriodic": CacheModelPeriodic,
    }

    PRUNA_NODE_DISPLAY_NAME_MAPPINGS = {
        "CompileModel": "Pruna Compile",
        "CacheModelAdaptive": "Pruna Cache Adaptive",
        "CacheModelPeriodic": "Pruna Cache Periodic",
    }
    NODE_CLASS_MAPPINGS.update(PRUNA_NODE_CLASS_MAPPINGS)
    NODE_DISPLAY_NAME_MAPPINGS.update(PRUNA_NODE_DISPLAY_NAME_MAPPINGS)
except Exception:
    print("ComfyUI_pruna: Pruna node import failed.")
    traceback.print_exception(*sys.exc_info())

if len(NODE_CLASS_MAPPINGS) == 0:
    raise Exception("import failed")
