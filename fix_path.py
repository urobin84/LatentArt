import json

filepath = "/Users/muhammadmuqorrobin/Documents/Robin/LatentArt/notebooks/LatentArt_Submission.ipynb"
with open(filepath, 'r') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code' and 'source' in cell:
        # Find the sys.path line
        updated_source = []
        for line in cell['source']:
            if "sys.path.append('../src')" in line:
                updated_source.append("import os\n")
                updated_source.append("sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))\n")
                # Also fallback if running locally from notebooks dir
                updated_source.append("sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '../src')))\n")
            else:
                updated_source.append(line)
        cell['source'] = updated_source

with open(filepath, 'w') as f:
    json.dump(nb, f, indent=4)

print("Path fixed in notebook.")
