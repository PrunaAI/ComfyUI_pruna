import comfy.model_patcher

try:
    from pruna_pro import SmashConfig, smash
except ImportError:
    print("pruna_pro not installed, skipping")
    try:
        from pruna import SmashConfig, smash
    except ImportError:
        print("Neither pruna_pro nor pruna are installed, skipping")


# Base mixin that contains the common functionality
class CacheModelMixin:
    def _clone_patcher(self, model):
        """Clone the model patcher from a given model instance."""
        if isinstance(model, comfy.model_patcher.ModelPatcher):
            return model.clone()
        else:
            # Assume model has a .patcher attribute, then clone it.
            return model.patcher.clone()

    def _apply_common_caching(self, model, caching_type, config_params, error_message):
        """
        Apply common caching steps:
           - Clone the model patcher.
           - Create a smash config and set the caching type.
           - Update config with caching-specific parameters.
           - Smash and patch the model.
        """
        patched = self._clone_patcher(model)

        # Set up the smash configuration object
        smash_config = SmashConfig()

        try:
            smash_config["cachers"] = caching_type
        except KeyError:
            raise ValueError(error_message)

        # Merge the given caching-specific parameters into the config
        for key, value in config_params.items():
            smash_config[key] = value

        # "Smash" the model and update the internal reference
        smashed_diffusion_model = smash(patched.model.diffusion_model, smash_config)
        model_ref_name = "_PrunaProModel__internal_model_ref"
        patched.add_object_patch(
            "diffusion_model", smashed_diffusion_model.__getattribute__(model_ref_name)
        )

        return patched


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
            }
        }

    RETURN_TYPES = ("MODEL",)
    FUNCTION = "apply_caching"
    CATEGORY = "Pruna"

    def apply_caching(self, model, threshold, max_skip_steps):
        # Prepare caching-specific configuration
        config_params = {
            "adaptive_threshold": threshold,
            "adaptive_max_skip_steps": max_skip_steps,
        }
        patched = self._apply_common_caching(
            model,
            caching_type="adaptive",
            config_params=config_params,
            error_message="Adaptive caching requires pruna_pro to be installed",
        )

        return (patched,)


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
            }
        }

    RETURN_TYPES = ("MODEL",)
    FUNCTION = "apply_caching"
    CATEGORY = "Pruna"

    def apply_caching(self, model, cache_interval, start_step, cache_mode):
        # Prepare caching-specific configuration
        config_params = {
            "periodic_cache_interval": cache_interval,
            "periodic_start_step": start_step,
            "periodic_cache_mode": cache_mode,
        }
        patched = self._apply_common_caching(
            model,
            caching_type="periodic",
            config_params=config_params,
            error_message="Periodic caching requires pruna_pro to be installed",
        )

        return (patched,)


class CacheModelAuto(CacheModelMixin):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {"model": ("MODEL",)},
            "optional": {
                "speed_factor": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0}),
                "cache_mode": (
                    "STRING",
                    {"default": "default", "options": ["default", "taylor"]},
                ),
            },
        }

    RETURN_TYPES = ("MODEL",)
    FUNCTION = "apply_caching"
    CATEGORY = "Pruna"

    def apply_caching(self, model, speed_factor, cache_mode):
        config_params = {
            "auto_speed_factor": speed_factor,
            "auto_cache_mode": cache_mode,
        }
        patched = self._apply_common_caching(
            model,
            caching_type="auto",
            config_params=config_params,
            error_message="Auto caching requires pruna_pro to be installed",
        )
        return (patched,)
