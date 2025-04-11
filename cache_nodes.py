import comfy.model_patcher

try:
    from pruna_pro import SmashConfig, smash
except ImportError:
    print("pruna_pro not installed, skipping")
    try:
        from pruna import SmashConfig, smash
    except ImportError:
        print("Neither pruna_pro nor pruna are installed, skipping")


class CacheModelMixin:
    def _clone_patcher(self, model):
        """Clone the model patcher from a given model instance."""
        if isinstance(model, comfy.model_patcher.ModelPatcher):
            return model.clone()
        else:
            # model is a BaseModel
            return model.patcher.clone()

    def _apply_common_caching(self, model, caching_method, hyperparams):
        """Apply a specific caching method to a model."""
        # Clone the model patcher
        model_patcher = self._clone_patcher(model)

        # Set up smash config
        smash_config = SmashConfig()

        try:
            smash_config["cachers"] = caching_method
        except KeyError:
            raise ValueError(
                f"{caching_method} caching requires pruna_pro to be installed"
            )

        # Merge the hyperparameters into smash config
        for key, value in hyperparams.items():
            smash_config[key] = value
        smash_config._prepare_saving = False

        # Add an attribute to patched to pass the info that it is a comfy model
        model_patcher.model.diffusion_model.is_comfy = True

        # Smash the model and update the internal reference
        smashed_model = smash(model_patcher.model.diffusion_model, smash_config)
        model_patcher.add_object_patch(
            "diffusion_model",
            smashed_model.__getattribute__("_PrunaProModel__internal_model_ref"),
        )

        return model_patcher


# CacheModelAdaptive now simply supplies its specific config parameters
class CacheModelAdaptive(CacheModelMixin):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("MODEL",),
                "threshold": (
                    "FLOAT",
                    {"default": 0.01, "step": 0.001, "min": 0.001, "max": 0.2},
                ),
                "max_skip_steps": (
                    "INT",
                    {"default": 4, "step": 1, "min": 1, "max": 5},
                ),
                "compiler": (
                    "STRING",
                    {
                        "default": "torch_compile",
                        "options": ["torch_compile", "stable_fast", "none"],
                    },
                ),
            }
        }

    RETURN_TYPES = ("MODEL",)
    FUNCTION = "apply_caching"
    CATEGORY = "Pruna"

    def apply_caching(self, model, threshold, max_skip_steps, compiler):
        # Prepare caching-specific configuration
        hyperparams = {
            "adaptive_threshold": threshold,
            "adaptive_max_skip_steps": max_skip_steps,
        }
        if compiler != "none":
            hyperparams["compiler"] = compiler
        model_patcher = self._apply_common_caching(
            model,
            caching_method="adaptive",
            hyperparams=hyperparams,
        )

        return (model_patcher,)


# CacheModelPeriodic also supplies its own configuration parameters
class CacheModelPeriodic(CacheModelMixin):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("MODEL",),
                "cache_interval": ("INT", {"default": 2, "min": 1, "max": 7}),
                "start_step": ("INT", {"default": 2, "min": 0, "max": 10}),
                "cache_mode": (
                    "STRING",
                    {"default": "default", "options": ["default", "taylor"]},
                ),
                "compiler": (
                    "STRING",
                    {
                        "default": "torch_compile",
                        "options": ["torch_compile", "stable_fast", "none"],
                    },
                ),
            }
        }

    RETURN_TYPES = ("MODEL",)
    FUNCTION = "apply_caching"
    CATEGORY = "Pruna"

    def apply_caching(self, model, cache_interval, start_step, cache_mode, compiler):
        # Prepare caching-specific configuration
        hyperparams = {
            "periodic_cache_interval": cache_interval,
            "periodic_start_step": start_step,
            "periodic_cache_mode": cache_mode,
        }
        if compiler != "none":
            hyperparams["compiler"] = compiler
        model_patcher = self._apply_common_caching(
            model,
            caching_method="periodic",
            hyperparams=hyperparams,
        )

        return (model_patcher,)


class CacheModelAuto(CacheModelMixin):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("MODEL",),
                "compiler": (
                    "STRING",
                    {
                        "default": "torch_compile",
                        "options": ["torch_compile", "stable_fast", "none"],
                    },
                ),
                "speed_factor": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0}),
                "cache_mode": (
                    "STRING",
                    {"default": "default", "options": ["default", "taylor"]},
                ),
            }
        }

    RETURN_TYPES = ("MODEL",)
    FUNCTION = "apply_caching"
    CATEGORY = "Pruna"

    def apply_caching(self, model, compiler, speed_factor, cache_mode):
        hyperparams = {
            "auto_speed_factor": speed_factor,
            "auto_cache_mode": cache_mode,
        }
        if compiler != "none":
            hyperparams["compiler"] = compiler
        model_patcher = self._apply_common_caching(
            model,
            caching_method="auto",
            hyperparams=hyperparams,
        )
        return (model_patcher,)
