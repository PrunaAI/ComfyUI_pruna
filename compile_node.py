import comfy.model_patcher

USE_PRUNA_PRO = False
try:
    from pruna_pro import SmashConfig, smash

    USE_PRUNA_PRO = True
except ImportError:
    print("pruna_pro not installed, skipping")
    try:
        from pruna import SmashConfig, smash
    except ImportError:
        print("Neither pruna_pro nor pruna are installed, skipping")


class PrunaCompileModel:
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
    SUPPORTED_COMPILERS = {
        "x_fast",
        "torch_compile",
        "x-fast",
    }  # x-fast is deprecated, but still supported

    def apply_compilation(self, model, compiler):
        """
        Smash the model using Pruna.
        """
        # we assume that the input model is either a comfy.model_patcher.ModelPatcher
        # or a comfy.model.Model
        if isinstance(model, comfy.model_patcher.ModelPatcher):
            smashed_patcher = model.clone()
        else:
            smashed_patcher = model.patcher
            smashed_patcher = smashed_patcher.clone()

        smash_config = SmashConfig()

        if compiler not in self.SUPPORTED_COMPILERS:
            raise ValueError(
                f"Compiler {compiler} is not a valid compiler. Supported compilers are: {self.SUPPORTED_COMPILERS}"
            )

        try:
            smash_config["compiler"] = compiler
        except KeyError:
            raise ValueError(f"Compiler {compiler} is available only with pruna_pro")

        smash_config._prepare_saving = False
        smashed_diffusion_model = smash(
            smashed_patcher.model.diffusion_model,
            smash_config,
        )

        model_ref_name = (
            "_PrunaProModel__internal_model_ref" if USE_PRUNA_PRO else "model"
        )

        smashed_patcher.add_object_patch(
            "diffusion_model", smashed_diffusion_model.__getattribute__(model_ref_name)
        )

        return (smashed_patcher,)
