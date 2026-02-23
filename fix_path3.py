import json

filepath = "/Users/muhammadmuqorrobin/Documents/Robin/LatentArt/notebooks/LatentArt_Submission.ipynb"
with open(filepath, 'r') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code' and 'source' in cell:
        # Check if this is the imports cell
        if any('from diffusers import' in line for line in cell['source']):
            new_source = []
            for line in cell['source']:
                if "sys.path.append" not in line:
                    new_source.append(line)
            
            # Inject the absolute explicit paths
            insert_idx = 0
            for i, l in enumerate(new_source):
                if "from utils import" in l:
                    insert_idx = i
                    break
            
            # Remove any duplicate os/sys imports if they exist right before it
            while insert_idx > 0 and ("import os" in new_source[insert_idx-1] or "import sys" in new_source[insert_idx-1]):
                new_source.pop(insert_idx-1)
                insert_idx -= 1
                
            new_source.insert(insert_idx, "import sys\n")
            new_source.insert(insert_idx+1, "import os\n")
            new_source.insert(insert_idx+2, "# Directly append the absolute Colab path and the exact relative path for local Jupyter\n")
            new_source.insert(insert_idx+3, "colab_path = '/content/LatentArt/src'\n")
            new_source.insert(insert_idx+4, "local_path = os.path.abspath(os.path.join(os.getcwd(), '..', 'src'))\n")
            new_source.insert(insert_idx+5, "if os.path.exists(colab_path) and colab_path not in sys.path:\n")
            new_source.insert(insert_idx+6, "    sys.path.append(colab_path)\n")
            new_source.insert(insert_idx+7, "elif os.path.exists(local_path) and local_path not in sys.path:\n")
            new_source.insert(insert_idx+8, "    sys.path.append(local_path)\n")
            
            cell['source'] = new_source

with open(filepath, 'w') as f:
    json.dump(nb, f, indent=4)

print("Notebook paths fixed with absolute Colab path.")
