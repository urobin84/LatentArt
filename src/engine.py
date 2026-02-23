import torch
from diffusers import (
    StableDiffusionPipeline, 
    EulerAncestralDiscreteScheduler, 
    DPMSolverMultistepScheduler, 
    DDIMScheduler
)

def setup_pipeline(model_id="runwayml/stable-diffusion-v1-5", device="cpu"):
    """
    Inisialisasi pipeline berdasarkan device.
    """
    dtype = torch.float16 if device in ["cuda", "mps"] else torch.float32
    
    pipe = StableDiffusionPipeline.from_pretrained(
        model_id, 
        torch_dtype=dtype
    )
    
    if device == "mps":
        pipe = pipe.to("mps")
        # Optimization disabled to prevent slowdowns on M-chips with enough memory
    elif device == "cuda":
        pipe = pipe.to("cuda")
        pipe.enable_xformers_memory_efficient_attention()
    
    return pipe

def load_scheduler(pipe, scheduler_name):
    """
    Mengganti algoritma sampling tanpa reload model.
    Kriteria: Euler A, DPM++, DDIM
    """
    if scheduler_name == "Euler A":
        pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(pipe.scheduler.config)
    elif scheduler_name == "DPM++":
        pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    elif scheduler_name == "DDIM":
        pipe.scheduler = DDIMScheduler.from_config(pipe.scheduler.config)
    return pipe

def generate_simple_image(pipe, prompt, negative_prompt, seed):
    """
    Fungsi generasi gambar dengan parameter default bawaan model.
    """
    generator = torch.Generator(device=pipe.device).manual_seed(seed)
    
    image = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        generator=generator
    ).images[0]
    
    return image

def generate_advanced_image(pipe, prompt, negative_prompt, guidance_scale, num_inference_steps, seed):
    """
    Fungsi generasi gambar dengan kontrol penuh parameter.
    """
    generator = torch.Generator(device=pipe.device).manual_seed(seed)
    
    image = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        guidance_scale=guidance_scale,
        num_inference_steps=num_inference_steps,
        generator=generator
    ).images[0]
    
    return image