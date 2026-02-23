import torch
from src.utils import get_device, clear_memory
from src.engine import setup_inpaint_pipeline, generate_inpainted_image
from PIL import Image, ImageDraw
import os

def test_inpainting():
    device = get_device()
    print(f"Device: {device}")
    
    print("Setting up Inpaint Pipeline...")
    pipe = setup_inpaint_pipeline(device=device)
    
    print("Creating dummy image and mask...")
    init_image = Image.new("RGB", (512, 512), (100, 100, 100))
    mask_image = Image.new("RGB", (512, 512), (0, 0, 0))
    draw = ImageDraw.Draw(mask_image)
    draw.rectangle([128, 128, 384, 384], fill="white")
    
    prompt = "A majestic golden phoenix bird rising from flames"
    negative_prompt = "photorealistic, realistic, photograph, 3d render, messy, blurry, low quality, bad art, ugly, sketch, grainy, unfinished, chromatic aberration"
    
    print("Generating inpainted image (this may take a moment)...")
    # Using float32 for CPU and a smaller step count just for verification
    steps = 10 if device == "cpu" else 30
    
    result = generate_inpainted_image(
        pipe=pipe,
        prompt=prompt,
        negative_prompt=negative_prompt,
        init_image=init_image,
        mask_image=mask_image,
        num_inference_steps=steps,
        seed=9
    )
    
    os.makedirs("outputs", exist_ok=True)
    result.save("outputs/test_inpaint.png")
    print("Inpainting test successful. Saved to outputs/test_inpaint.png")
    
    clear_memory()

if __name__ == "__main__":
    test_inpainting()
