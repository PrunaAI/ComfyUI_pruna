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
        # we assume that the input model is either a comfy.model_patcher.ModelPatcher
        # or a comfy.model.Model
        if isinstance(model, comfy.model_patcher.ModelPatcher):
            smashed_patcher = model.clone()
        else:
            smashed_patcher = model.patcher
            smashed_patcher = smashed_patcher.clone()

        # hardcode the config for now
        smash_config = SmashConfig()
        smash_config['compilers'] = ['x-fast']

        smashed_diffusion_model = smash(
            smashed_patcher.model.diffusion_model,
            smash_config
        )
        smashed_patcher.add_object_patch(
            "diffusion_model",
            smashed_diffusion_model._PrunaModel__model
        )

        return (smashed_patcher,)
