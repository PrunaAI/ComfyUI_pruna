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
            },
            "optional": {
                "compiler": ("STRING", {"default": "torch_compile"}),
            }
        }

    RETURN_TYPES = ("MODEL",)
    FUNCTION = "apply_smashing"
    CATEGORY = "loaders"

    def apply_smashing(self, model, compiler):
        '''
        Smash the model using Pruna.
        '''
        # we assume that the input model is either a comfy.model_patcher.ModelPatcher
        # or a comfy.model.Model
        if isinstance(model, comfy.model_patcher.ModelPatcher):
            smashed_patcher = model.clone()
        else:
            smashed_patcher = model.patcher
            smashed_patcher = smashed_patcher.clone()

        # use the selected compiler
        smash_config = SmashConfig()
        smash_config['compilers'] = [compiler]
    
        smashed_diffusion_model = smash(
            smashed_patcher.model.diffusion_model,
            smash_config,
        )

        smashed_patcher.add_object_patch(
            "diffusion_model",
            smashed_diffusion_model._PrunaModel__model
        )

        return (smashed_patcher,)
