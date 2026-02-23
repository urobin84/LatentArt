import torch
import os

def get_device():
    """
    Detects the best available device for PyTorch.
    Returns: 'cuda' for NVIDIA GPU, 'mps' for Mac M1/M2, or 'cpu' as fallback.
    """
    if torch.cuda.is_available():
        return "cuda"
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return "mps"
    else:
        return "cpu"

def clear_memory():
    """
    Clears GPU/MPS memory to avoid OOM.
    """
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    elif torch.backends.mps.is_available():
        # MPS doesn't have an exact equivalent to empty_cache(),
        # but manual garbage collection often helps.
        import gc
        gc.collect()

if __name__ == "__main__":
    device = get_device()
    print(f"Detected device: {device}")
