import comfy.model_patcher


try:
    from pruna import SmashConfig, smash
except ImportError:
    print("pruna not installed, skip")


class SmashUnet:
    @classmethod

    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL",),
            }
        }

    RETURN_TYPES = ("MODEL",)
    FUNCTION = "apply_smashing"
    CATEGORY = "loaders"  

    def apply_smashing(self, model):
        '''
        Smash the model using Pruna.
        '''
        # hardcode the config for now
        smash_config = SmashConfig()
        smash_config['compilers'] = ['x-fast']

        smashed_model = smash(model.model, smash_config)
        patch = comfy.model_patcher.ModelPatcher(
            smashed_model,
            load_device="cuda",
            offload_device="cpu"
        )

        model_smashed = model.clone()
        model_smashed.set_model_patch(patch, "smashed_unet")

        return (model_smashed,)
