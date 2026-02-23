import json

filepath = "/Users/muhammadmuqorrobin/Documents/Robin/LatentArt/notebooks/LatentArt_Submission.ipynb"
with open(filepath, 'r') as f:
    nb = json.load(f)

cells_to_keep = []

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        # Clear out any stuck error outputs so it doesn't confuse the user visually
        cell['outputs'] = []
        cell['execution_count'] = None
        
        # We only want to keep the ACTUAL setup cell, not the crashed extra cell
        if 'source' in cell and len(cell['source']) > 0:
            source_code = "".join(cell['source'])
            
            # Remove the cell that was just the user's manual debugging attempt 
            # (the one that only had imports and failed)
            if "from utils import get_device, clear_memory" in source_code and "StableDiffusionPipeline" not in source_code:
                continue
                
            # For the main setup cell, let's make the sys.path injection robust
            if "import torch" in source_code and "from diffusers import" in source_code:
                new_source = []
                for line in cell['source']:
                    if "sys.path.append" in line or "import os" in line and "import gc" not in cell['source'] :
                        continue # We'll re-inject cleanly
                    new_source.append(line)
                
                # Insert our path fix right before from utils import
                insert_idx = 0
                for i, l in enumerate(new_source):
                    if "from utils import" in l:
                        insert_idx = i
                        break
                
                new_source.insert(insert_idx, "import os\n")
                new_source.insert(insert_idx+1, "import sys\n")
                new_source.insert(insert_idx+2, "sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))\n")
                new_source.insert(insert_idx+3, "sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '../src')))\n")
                
                cell['source'] = new_source
                
    cells_to_keep.append(cell)

nb['cells'] = cells_to_keep

with open(filepath, 'w') as f:
    json.dump(nb, f, indent=4)

print("Notebook paths fixed and cleaned.")
