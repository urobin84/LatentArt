import json

filepath = "/Users/muhammadmuqorrobin/Documents/Robin/LatentArt/notebooks/LatentArt_Submission.ipynb"
with open(filepath, 'r') as f:
    nb = json.load(f)

# The new github clone with PAT authentication
new_source = [
    "try:\n",
    "    import google.colab\n",
    "    IN_COLAB = True\n",
    "    print(\"Running in Google Colab\\n\")\n",
    "    \n",
    "    import os\n",
    "    GITHUB_TOKEN = \"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\"\n",
    "    GITHUB_USER = \"urobin84\"\n",
    "    REPO_NAME = \"LatentArt\"\n",
    "    \n",
    "    if not os.path.exists(f'/content/{REPO_NAME}'):\n",
    "        !git clone https://{GITHUB_TOKEN}@github.com/{GITHUB_USER}/{REPO_NAME}.git /content/{REPO_NAME}\n",
    "    \n",
    "    %cd /content/{REPO_NAME}\n",
    "    \n",
    "    # Configure git so we can push back\n",
    "    !git config --global user.name \"{GITHUB_USER}\"\n",
    "    !git config --global user.email \"{GITHUB_USER}@users.noreply.github.com\"\n",
    "    \n",
    "    !pip install -r requirements.txt\n",
    "except ImportError:\n",
    "    IN_COLAB = False\n",
    "    print(\"Running locally\")"
]

for cell in nb['cells']:
    if cell['cell_type'] == 'code' and 'source' in cell:
        # Update the Colab Init block
        if any('import google.colab' in line for line in cell['source']) and any('IN_COLAB' in line for line in cell['source']):
            cell['source'] = new_source

with open(filepath, 'w') as f:
    json.dump(nb, f, indent=4)

print("Notebook auth injected.")
