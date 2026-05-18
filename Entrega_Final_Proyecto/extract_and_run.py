#!/usr/bin/env python3
import json
import os

notebook_path = os.path.join(os.path.dirname(__file__), 'Modelo_Bayesiano_Jerarquico.ipynb')
script_path = os.path.join(os.path.dirname(__file__), 'run_model.py')

print(f"Reading notebook from: {notebook_path}")
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

code_cells = []
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        # Join lines of code
        source = cell['source']
        if isinstance(source, list):
            source = "".join(source)
        code_cells.append(source)

full_code = "\n\n# " + "="*40 + "\n\n".join(code_cells)

# Replace interactive plt.show() with non-blocking or simple plot saves 
# (though they already have savefig in the code, so it's perfectly fine!)
# We'll prepend matplotlib non-interactive backend so it doesn't try to open GUI windows
header = """import matplotlib
matplotlib.use('Agg') # Use non-interactive backend
"""

with open(script_path, 'w', encoding='utf-8') as f:
    f.write(header + full_code)

print(f"Successfully generated: {script_path}")
