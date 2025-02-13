import traceback
import sys

NODE_CLASS_MAPPINGS = {}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {}

try:
    from .node import CompileModel

    PRUNA_NODE_CLASS_MAPPINGS = {
        "CompileModel": CompileModel,
    }

    PRUNA_NODE_DISPLAY_NAME_MAPPINGS = {
        "CompileModel": "Pruna Compile",
    }
    NODE_CLASS_MAPPINGS.update(PRUNA_NODE_CLASS_MAPPINGS)
    NODE_DISPLAY_NAME_MAPPINGS.update(PRUNA_NODE_DISPLAY_NAME_MAPPINGS)
except Exception as e:
    print("ComfyUI_pruna: Pruna node import failed.")
    traceback.print_exception(*sys.exc_info())

if len(NODE_CLASS_MAPPINGS) == 0:
    raise Exception("import failed")

