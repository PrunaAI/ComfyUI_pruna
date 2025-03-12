import comfy.model_patcher

try:
    from pruna_pro.smash import smash
    from pruna import SmashConfig
except ImportError:
    print("prona not installed, skipping")
    try:
        from pruna.smash import smash, SmashConfig
    except ImportError:
        print("Neither prona nor pruna are installed, skip")


class CompileModel:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL",),
                "compiler": ("STRING", {"default": "x_fast"}),
            }
        }

    RETURN_TYPES = ("MODEL",)
    FUNCTION = "apply_compilation"
    CATEGORY = "Pruna"

    def apply_compilation(self, model, compiler):
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

        smash_config = SmashConfig()
        smash_config['compiler'] = compiler
        smash_config._prepare_saving = False

        smashed_diffusion_model = smash(
            smashed_patcher.model.diffusion_model,
            smash_config,
        )

        smashed_patcher.add_object_patch(
            "diffusion_model",
            smashed_diffusion_model._PrunaProModel__internal_model_ref
        )

        return (smashed_patcher,)
