# INT4 W4A8 for Forge Neo
# INT4 ConvRot checkpoints (quantization format "convrot_w4a4", the small INT4 builds of MOSS-Image, Krea 2 and
# others): their metadata asks comfy-kitchen to quantize the activations to INT4 as well (W4A4, linear_dtype "int4").
# comfy-kitchen's other path for the same format keeps the INT4 weights and quantizes the activations to INT8 (W4A8,
# linear_dtype "int8"), which removes the activation part of the error; ComfyUI documents both (QUANTIZATION.md).
# A setting picks the path.
#
# The choice is written into the loaded model's weights at the first step of every sampling run, so a change applies
# at the next generation without reloading the checkpoint, whatever the architecture.
# Forge Neo's own --force-w4a8 launch option sets "int8" at load time; the checkpoint's value is gone by then, so
# with it the INT8 path is all there is and "As stored" can only say so.
# No Forge imports at module level: the CPU tests run it as is.

import dataclasses
import logging

__version__ = "0.1.1"

logger = logging.getLogger("int4_w4a8")

OPTION = "int4_w4a8_activations"
INT8 = "INT8 (W4A8)"
STORED = "As stored (W4A4)"
DEFAULT = INT8
LABEL = "[INT4 W4A8] Activations of INT4 ConvRot checkpoints"
INFO = ("INT8 = better image, same INT4 file; As stored = the checkpoint's own INT4 activations; "
        "takes effect at the next generation")

LAYOUT = "TensorCoreConvRotW4A4Layout"
# the checkpoint's own value, kept on the module the first time it is changed
STORED_ATTRIBUTE = "_int4_w4a8_stored_linear_dtype"


def _opts():
    try:
        from modules.shared import opts

        return opts
    except Exception:  # outside Forge Neo (CPU tests)
        return None


def choice() -> str:
    return getattr(_opts(), OPTION, DEFAULT)


def forced() -> bool:
    """Forge Neo was launched with --force-w4a8 (older Forge Neo: no such option)."""
    try:
        from backend.args import args

        return bool(getattr(args, "force_w4a8", False))
    except Exception:  # outside Forge Neo (CPU tests)
        return False


_forced_noted = False


def wanted(stored: str) -> str:
    return "int8" if choice() == INT8 else stored


def apply(model) -> int:
    """Set every ConvRot W4A4 weight of model to the chosen activation path; returns how many changed."""
    changed = 0
    for module in model.modules():
        weight = module._parameters.get("weight")
        if getattr(weight, "_layout_cls", None) != LAYOUT:
            continue
        params = weight._params
        stored = module.__dict__.setdefault(STORED_ATTRIBUTE, params.linear_dtype)
        linear_dtype = wanted(stored)
        if params.linear_dtype != linear_dtype:
            weight._params = dataclasses.replace(params, linear_dtype=linear_dtype)
            changed += 1
    return changed


def _diffusion_model():
    from modules import shared

    unet = getattr(getattr(shared.sd_model, "forge_objects", None), "unet", None)
    return getattr(getattr(unet, "model", None), "diffusion_model", None)


def on_cfg_denoiser(params) -> None:
    # script_callbacks.on_cfg_denoiser; the denoiser counts its calls from 0 in each sampling run (hires pass included)
    global _forced_noted
    if getattr(getattr(params, "denoiser", None), "step", None) != 0:
        return
    if choice() == STORED and not _forced_noted and forced():
        _forced_noted = True
        print("[INT4 W4A8] Forge Neo was launched with --force-w4a8: INT4 checkpoints stay on INT8 (W4A8), "
              "'As stored' needs a launch without it")
    try:
        model = _diffusion_model()
        if model is not None and apply(model):
            print(f"[INT4 W4A8] INT4 checkpoint activations: {choice()}")
    except Exception as e:
        # the generation goes on with the checkpoint's own path
        logger.warning(f"[INT4 W4A8] could not set the INT4 activations: {e}")


def register_option() -> None:
    import gradio as gr
    from modules import shared
    from modules.options import OptionInfo

    if OPTION not in shared.opts.data_labels:
        shared.opts.add_option(OPTION, OptionInfo(DEFAULT, LABEL, gr.Radio, {"choices": (INT8, STORED)},
                                                  section=("sd", "Stable Diffusion"), category_id="sd").info(INFO))


def register_callbacks() -> None:
    """Per script load: a UI reload clears script_callbacks and runs scripts/int4_w4a8.py again."""
    from modules import script_callbacks

    script_callbacks.on_cfg_denoiser(on_cfg_denoiser, name="int4_w4a8")
