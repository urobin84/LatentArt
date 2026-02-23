import torch
from diffusers import (
    StableDiffusionPipeline, 
    StableDiffusionImg2ImgPipeline,
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

def setup_refiner_pipeline(model_id="runwayml/stable-diffusion-v1-5", device="cpu"):
    """
    Inisialisasi pipeline Img2Img untuk proses refinement.
    """
    dtype = torch.float16 if device in ["cuda", "mps"] else torch.float32
    
    pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
        model_id, 
        torch_dtype=dtype
    )
    
    if device == "mps":
        pipe = pipe.to("mps")
    elif device == "cuda":
        pipe = pipe.to("cuda")
        pipe.enable_xformers_memory_efficient_attention()
    
    return pipe

def generate_refined_image(pipe, prompt, negative_prompt, init_image, strength=0.8, guidance_scale=8.0, num_inference_steps=50, seed=222):
    """
    Fungsi penyempurnaan gambar (Refiner) dengan menggunakan img2img.
    """
    generator = torch.Generator(device=pipe.device).manual_seed(seed)
    
    # Pastikan ukuran init_image memadai sebelum refine (misal 768x768 atau 512x512)
    # Pipeline ini akan menerima output PIL Image dari T2I
    image = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        image=init_image,
        strength=strength,
        guidance_scale=guidance_scale,
        num_inference_steps=num_inference_steps,
        generator=generator
    ).images[0]
    
    return image