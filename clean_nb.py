import json

filepath = "/Users/muhammadmuqorrobin/Documents/Robin/LatentArt/notebooks/LatentArt_Submission.ipynb"
with open(filepath, 'r') as f:
    nb = json.load(f)

# The correct github clone text
new_source = [
    "try:\n",
    "    import google.colab\n",
    "    IN_COLAB = True\n",
    "    print(\"Running in Google Colab\\n\")\n",
    "    \n",
    "    import os\n",
    "    if not os.path.exists('/content/LatentArt'):\n",
    "        !git clone https://github.com/urobin84/LatentArt.git /content/LatentArt\n",
    "    \n",
    "    %cd /content/LatentArt\n",
    "    !pip install -r requirements.txt\n",
    "except ImportError:\n",
    "    IN_COLAB = False\n",
    "    print(\"Running locally\")"
]

# 1. Update the correct init cell
for cell in nb['cells']:
    if cell['cell_type'] == 'code' and 'source' in cell:
        if any('import google.colab' in line for line in cell['source']) and any('IN_COLAB' in line for line in cell['source']):
            cell['source'] = new_source

# 2. Remove the user's problematic manual "Drive Mount" cell which has the hardcoded /content/drive path
cells_to_keep = []
for cell in nb['cells']:
    if cell['cell_type'] == 'code' and 'source' in cell:
        # If it's the bad user block containing 'importlib.reload' and old drive mount stuff, skip it
        if any('drive.mount(' in line for line in cell['source']) and not any('IN_COLAB' in line for line in cell['source']):
            continue
    cells_to_keep.append(cell)

nb['cells'] = cells_to_keep

with open(filepath, 'w') as f:
    json.dump(nb, f, indent=4)

print("Notebook cleaned and updated.")
