import sys
import traceback

NODE_CLASS_MAPPINGS = {}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {}

try:
    from .cache_node import CacheModel
    from .compile_node import CompileModel

    PRUNA_NODE_CLASS_MAPPINGS = {
        "CompileModel": CompileModel,
        "CacheModel": CacheModel,
    }

    PRUNA_NODE_DISPLAY_NAME_MAPPINGS = {
        "CompileModel": "Pruna Compile",
        "CacheModel": "Pruna Cache",
    }
    NODE_CLASS_MAPPINGS.update(PRUNA_NODE_CLASS_MAPPINGS)
    NODE_DISPLAY_NAME_MAPPINGS.update(PRUNA_NODE_DISPLAY_NAME_MAPPINGS)
except Exception:
    print("ComfyUI_pruna: Pruna node import failed.")
    traceback.print_exception(*sys.exc_info())

if len(NODE_CLASS_MAPPINGS) == 0:
    raise Exception("import failed")
