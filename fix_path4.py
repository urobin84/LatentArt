import json

filepath = "/Users/muhammadmuqorrobin/Documents/Robin/LatentArt/notebooks/LatentArt_Submission.ipynb"
with open(filepath, 'r') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code' and 'source' in cell:
        # We are going to completely replace the problem cell with a bulletproof setup
        source_code = "".join(cell['source'])
        if "from utils import get_device" in source_code and "StableDiffusionPipeline" in source_code:
            new_source = [
                "import torch\n",
                "import sys\n",
                "import gc\n",
                "from diffusers import StableDiffusionPipeline, StableDiffusionInpaintPipeline, StableDiffusionImg2ImgPipeline, EulerAncestralDiscreteScheduler\n",
                "from PIL import Image, ImageDraw\n",
                "import numpy as np\n",
                "import matplotlib.pyplot as plt\n",
                "\n",
                "# --- BULLETPROOF COLAB FIX ---\n",
                "# Instead of pathing issues, we just read the raw github file for utils.py and write it locally\n",
                "import os\n",
                "import urllib.request\n",
                "if 'google.colab' in sys.modules:\n",
                "    print(\"Downloading utils.py directly to /content...\")\n",
                "    urllib.request.urlretrieve('https://raw.githubusercontent.com/urobin84/LatentArt/main/src/utils.py', '/content/utils.py')\n",
                "    if '/content' not in sys.path:\n",
                "        sys.path.append('/content')\n",
                "else:\n",
                "    import os\n",
                "    local_path = os.path.abspath(os.path.join(os.getcwd(), '..', 'src'))\n",
                "    if os.path.exists(local_path) and local_path not in sys.path:\n",
                "        sys.path.append(local_path)\n",
                "\n",
                "from utils import get_device, clear_memory\n",
                "\n",
                "device = get_device()\n",
                "print(f\"\\nUsing device: {device}\")\n",
                "\n",
                "def load_scheduler(pipeline, scheduler_name=\"Euler A\"):\n",
                "    if scheduler_name == \"Euler A\":\n",
                "        pipeline.scheduler = EulerAncestralDiscreteScheduler.from_config(pipeline.scheduler.config)\n",
                "    print(f\"Scheduler set to: {scheduler_name}\")\n",
                "\n",
                "negative_prompt = \"photorealistic, realistic, photograph, 3d render, messy, blurry, low quality, bad art, ugly, sketch, grainy, unfinished, chromatic aberration\""
            ]
            cell['source'] = new_source

with open(filepath, 'w') as f:
    json.dump(nb, f, indent=4)

print("Notebook paths replaced with raw urllib download for Colab.")
