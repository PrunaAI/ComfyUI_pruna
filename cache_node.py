import comfy.model_patcher

try:
    from pruna_pro.smash import smash
    from pruna import SmashConfig
except ImportError:
    print("pruna_pro not installed, skipping")
    try:
        from pruna.smash import smash, SmashConfig
    except ImportError:
        print("Neither pruna_pro nor pruna are installed, skip")


class CacheModel:    

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL",),               
                "threshold": ("FLOAT", {
                    "default": 0.01,
                    "step": 0.001,
                    "min": 0.001,
                    "max": 0.2
                }),
                "max_skip_steps": ("INT", {
                    "default": 4,
                    "step": 1,
                    "min": 1,
                    "max": 5
                }),
            }
        }

    @classmethod
    def IS_CHANGED(cls, model, threshold, max_skip_steps):
        # Force node to re-run on every execution by returning NaN
        # For more details, see:
        #   - https://github.com/comfyanonymous/ComfyUI/issues/1962#issuecomment-1809574013
        #   - https://github.com/comfyanonymous/ComfyUI/issues/2024
        return float("nan")
    
    RETURN_TYPES = ("MODEL",)
    FUNCTION = "apply_caching"
    CATEGORY = "Pruna"
    reset_cache: bool = False  # flag to reset the cache

    def apply_caching(self, model, threshold, max_skip_steps):
        """
        Modify forward pass of the model to use adaptive caching.
        """

        if self.reset_cache:            
            model.model.cache_helper.reset_cache()
            return (model,)

        if isinstance(model, comfy.model_patcher.ModelPatcher):
            smashed_patcher = model.clone()
        else:
            smashed_patcher = model.patcher
            smashed_patcher = smashed_patcher.clone()

        # set up the smash config
        smash_config = SmashConfig()
        smash_config['cachers'] = 'adaptive'
        smash_config['adaptive_threshold'] = threshold
        smash_config['adaptive_max_skip_steps'] = max_skip_steps

        # smash the model
        smashed_model = smash(smashed_patcher.model, smash_config)

        # patch the model
        smashed_patcher.model = smashed_model._PrunaProModel__internal_model_ref
        self.reset_cache = True

        return (smashed_patcher,)
