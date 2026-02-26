# import torch
import gc
from diffusers import (
    StableDiffusionPipeline,
    StableDiffusionInpaintPipeline,
    EulerAncestralDiscreteScheduler,
    DPMSolverMultistepScheduler,
    DDIMScheduler
)
from PIL import Image, ImageFilter

# MODEL LOADER (JANGAN DIUBAH)
def load_models_cached():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Loading models to {device}")

    pipe_txt2img = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16
    ).to(device)
    pipe_txt2img.enable_attention_slicing()

    pipe_inpaint = StableDiffusionInpaintPipeline.from_pretrained(
        "runwayml/stable-diffusion-inpainting", torch_dtype=torch.float16
    ).to(device)
    pipe_inpaint.enable_attention_slicing()

    return pipe_txt2img, pipe_inpaint

# Ini mencegah error "Function not found" jika hanya mengerjakan Basic
def flush_memory(): pass
def set_scheduler(pipe, name): return pipe
def run_inpainting(pipe, img, mask, prompt, strength): return None
def prepare_outpainting(img, expand=128): return img, None
