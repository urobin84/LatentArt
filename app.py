import streamlit as st
import torch
import warnings
import time
from PIL import Image
from src.utils import get_device, clear_memory
from src.engine import (
    setup_pipeline,
    load_scheduler,
    generate_advanced_image,
    setup_refiner_pipeline,
    generate_refined_image
)

# Suppress NumPy cast warning specifically seen on macOS MPS devices
warnings.filterwarnings("ignore", message="invalid value encountered in cast")

st.set_page_config(
    page_title="LatentArt | Advanced AI Studio",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Premium UI ---
st.markdown("""
<style>
    /* Main Content Styling */
    .main {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    h1 {
        text-align: center;
        background: -webkit-linear-gradient(45deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 3rem !important;
        margin-bottom: 0px !important;
    }
    .subtitle {
        text-align: center;
        color: #8b949e;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Elegant Button Styling */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #4ECDC4 0%, #556270 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(78, 205, 196, 0.4);
    }
    
    /* Custom Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
    
    /* Metrics Box */
    div[data-testid="metric-container"] {
        background-color: #21262d;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# --- Initialize Session State ---
if "pipe_t2i" not in st.session_state:
    st.session_state.pipe_t2i = None
if "pipe_img2img" not in st.session_state:
    st.session_state.pipe_img2img = None
if "base_image" not in st.session_state:
    st.session_state.base_image = None
if "device" not in st.session_state:
    st.session_state.device = get_device()
if "models_loaded" not in st.session_state:
    st.session_state.models_loaded = False

device = st.session_state.device

st.markdown("<h1>🌌 LatentArt Studio</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Advanced Image Generation & Refinement Pipeline powered by Stable Diffusion</div>", unsafe_allow_html=True)

# Top Bar Metrics
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
col_m1.metric("Hardware Acceleration", f"🚀 {device.upper()}")
col_m2.metric("Base Model", "v1.5 (RunwayML)")
col_m3.metric("Precision", "FP16 (Half)")
col_m4.metric("Status", "🟢 Ready" if st.session_state.models_loaded else "🔴 Not Loaded")

st.markdown("---")

# --- Setup UI Sidebar / Controls ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Apple_logo_grey.svg/1024px-Apple_logo_grey.svg.png" if device =="mps" else "https://upload.wikimedia.org/wikipedia/commons/2/21/Nvidia_logo.svg", width=50)
st.sidebar.title("⚙️ Workflow Settings")

prompt = st.sidebar.text_area("🌟 Master Prompt", value="A futuristic city in the style of cyberpunk, vivid neon lights, high detail, masterpiece, 8k resolution, cinematic lighting")
negative_prompt = st.sidebar.text_area("🚫 Negative Prompt", value="photorealistic, realistic, photograph, 3d render, messy, blurry, low quality, bad art, ugly, sketch, grainy, unfinished, chromatic aberration, poorly drawn")

st.sidebar.markdown("### 🔧 Advanced Tuning")
with st.sidebar.expander("Model Hyperparameters", expanded=False):
    guidance_scale = st.slider("Guidance Scale (CFG)", min_value=1.0, max_value=20.0, value=7.5, step=0.5, help="Higher values force the model to listen to the prompt strictly.")
    inference_steps = st.slider("Inference Steps", min_value=10, max_value=100, value=30, step=1, help="More steps = higher quality but slower generation.")
    seed = st.number_input("Random Seed", value=222, step=1, help="Set to a specific number for reproducible results.")

scheduler_choice = st.sidebar.selectbox("📉 Sampling Method (Scheduler)", ["Euler A", "DPM++", "DDIM"])

st.sidebar.markdown("---")
st.sidebar.markdown("### 🧠 Memory Engine")
# --- Load Model Button ---
if st.sidebar.button("🔌 Initialize Engine (Load 4GB Weights)"):
    with st.spinner("Downloading/Loading Weights into RAM/VRAM..."):
        try:
            start_load = time.time()
            clear_memory()
            
            st.session_state.pipe_t2i = setup_pipeline(device=device)
            st.session_state.pipe_t2i = load_scheduler(st.session_state.pipe_t2i, scheduler_choice)
            
            st.session_state.pipe_img2img = setup_refiner_pipeline(
                device=device,
                base_components=st.session_state.pipe_t2i.components
            )
            st.session_state.models_loaded = True
            
            st.sidebar.success(f"Models loaded in {time.time() - start_load:.2f}s!")
            st.rerun() # Refresh to update metrics
        except Exception as e:
            st.sidebar.error(f"Error loading models: {e}")

# --- Generate Images Logic (TABS Layout) ---
tab1, tab2 = st.tabs(["✨ Stage 1: Base Generation (Text-to-Image)", "🪄 Stage 2: Refinement (Image-to-Image)"])

with tab1:
    col_t1, col_t2 = st.columns([1, 2])
    with col_t1:
        st.markdown("### Base Generation")
        st.write("Constructs the initial structural composition from pure noise based on your text prompt.")
        st.info("The base model is good with overall composition but might lack micro-details.")
        
        generate_btn = st.button("🚀 Generate Draft Concept", use_container_width=True)
    
    with col_t2:
        if generate_btn:
            if not st.session_state.models_loaded:
                st.error("⚠️ Please click 'Initialize Engine' in the sidebar first!")
            else:
                with st.spinner("Weaving Latent Space into Reality (Processing on M1)..."):
                    clear_memory()
                    load_scheduler(st.session_state.pipe_t2i, scheduler_choice)
                    start_time = time.time()
                    try:
                        img = generate_advanced_image(
                            st.session_state.pipe_t2i,
                            prompt,
                            negative_prompt,
                            guidance_scale,
                            inference_steps,
                            seed
                        )
                        st.session_state.base_image = img
                        st.success(f"Concept drafted in {time.time() - start_time:.1f} seconds!")
                    except RuntimeError as e:
                        if "out of memory" in str(e).lower():
                            st.error("GPU Out of Memory! Try lowering the inference steps.")
                        else:
                            st.error(f"Generation Error: {e}")

        if st.session_state.base_image:
            st.image(st.session_state.base_image, caption="Stage 1: Base Concept Draft (512x512)", use_container_width=True)
            
            with open("outputs/basic_t2i.png", "wb") as f: # Failsafe save just in case
               st.session_state.base_image.save(f, format="PNG")

with tab2:
    col_r1, col_r2 = st.columns([1, 2])
    with col_r1:
        st.markdown("### Heavy Refinement")
        st.write("Upscales the base image and adds extreme high-frequency details (textures, lighting, sharp edges) using an Image-To-Image pass.")
        strength = st.slider("Denoising Strength (Change Tolerance)", 0.0, 1.0, 0.75, 0.05, help="0.0 applies no changes. 1.0 completely replaces the image with a new generation.")
        
        refine_btn = st.button("💎 Run High-Res Refiner", type="primary", use_container_width=True)
    
    with col_r2:
        if refine_btn:
            if not st.session_state.models_loaded:
                st.error("⚠️ Please click 'Initialize Engine' in the sidebar first!")
            elif st.session_state.base_image is None:
                st.warning("🖼️ You must generate a Base Draft in Stage 1 first!")
            else:
                with st.spinner("Enhancing details and removing artifacts..."):
                    clear_memory() 
                    input_img = st.session_state.base_image.resize((768, 768)) # Upscale
                    start_time = time.time()
                    try:
                        refined = generate_refined_image(
                            st.session_state.pipe_img2img,
                            prompt,
                            negative_prompt,
                            input_img,
                            strength=strength,
                            guidance_scale=guidance_scale,
                            num_inference_steps=inference_steps,
                            seed=seed
                        )
                        st.image(refined, caption=f"Stage 2: Refined Masterpiece (768x768 | Strength: {strength})", use_container_width=True)
                        st.success(f"Refinement finished in {time.time() - start_time:.1f} seconds!")
                        
                        st.session_state.refined_image = refined
                    except RuntimeError as e:
                        st.error(f"Refinement Error: {e}")
