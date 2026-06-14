import json, re, os, base64

NB_PATH = os.path.join(os.path.dirname(__file__), 'bai_tap_cuoi_ki.ipynb')
OUT_IMG = os.path.join(os.path.dirname(__file__), '..', 'public', 'results')
OUT_DATA = os.path.join(os.path.dirname(__file__), '..', 'src', 'data')

os.makedirs(OUT_IMG, exist_ok=True)
os.makedirs(OUT_DATA, exist_ok=True)

with open(NB_PATH, encoding='utf-8') as f:
    nb = json.load(f)

# Map exercise number -> image filenames from plt.savefig calls in code
savefig_map = {}
current_bai = None

for cell in nb['cells']:
    src = ''.join(cell.get('source', []))
    if cell['cell_type'] == 'markdown':
        m = re.search(r'B[aà]i\s+(\d+)', src)
        if m:
            current_bai = int(m.group(1))
    elif cell['cell_type'] == 'code' and current_bai:
        saves = re.findall(r"plt\.savefig\(['\"]([^'\"]+)['\"]", src)
        if saves:
            savefig_map.setdefault(current_bai, []).extend(saves)

print("Image filenames from savefig:")
for bai, names in sorted(savefig_map.items()):
    print(f"  Bai {bai}: {names}")

# Now extract: code cells, text outputs, images per exercise
exercises = {}  # {bai_num: {'code': [str], 'text_outputs': [str], 'images': [(filename, base64)]}}
current_bai = None
img_counter = {}  # track which image we're on per exercise

for cell in nb['cells']:
    src = ''.join(cell.get('source', []))
    
    if cell['cell_type'] == 'markdown':
        m = re.search(r'B[aà]i\s+(\d+)', src)
        if m:
            current_bai = int(m.group(1))
            exercises[current_bai] = {'code': [], 'text_outputs': [], 'images': []}
            img_counter[current_bai] = 0
        continue
    
    if cell['cell_type'] != 'code' or current_bai is None:
        continue
    
    exercises[current_bai]['code'].append(src)
    
    for output in cell.get('outputs', []):
        if output.get('output_type') == 'stream' and output.get('name') == 'stdout':
            text = ''.join(output.get('text', []))
            exercises[current_bai]['text_outputs'].append(text)
        
        if output.get('output_type') == 'display_data':
            data = output.get('data', {})
            if 'image/png' in data:
                b64 = ''.join(data['image/png'])
                # Determine filename
                idx = img_counter[current_bai]
                if current_bai in savefig_map and idx < len(savefig_map[current_bai]):
                    fname = savefig_map[current_bai][idx]
                else:
                    fname = f'bai{current_bai}_img{idx}.png'
                exercises[current_bai]['images'].append((fname, b64))
                img_counter[current_bai] = idx + 1

# Save images
for bai, data in exercises.items():
    for fname, b64 in data['images']:
        fpath = os.path.join(OUT_IMG, fname)
        with open(fpath, 'wb') as f:
            f.write(base64.b64decode(b64))
        print(f"Saved: {fpath}")

# Generate codeBlocks.ts
with open(os.path.join(OUT_DATA, 'codeBlocks.ts'), 'w', encoding='utf-8') as f:
    f.write('// Auto-generated from bai_tap_cuoi_ki.ipynb\n\n')
    f.write('export const codeBlocks: Record<number, string> = {\n')
    for bai in sorted(exercises.keys()):
        code = '\n'.join(exercises[bai]['code'])
        escaped = code.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')
        f.write(f'  {bai}: `{escaped}`,\n')
    f.write('}\n')

# Generate results.ts with text outputs
with open(os.path.join(OUT_DATA, 'results.ts'), 'w', encoding='utf-8') as f:
    f.write('// Auto-generated from bai_tap_cuoi_ki.ipynb\n\n')
    f.write('export interface ExerciseResult {\n')
    f.write('  type: \'text\' | \'image\'\n')
    f.write('  title?: string\n')
    f.write('  content: string\n')
    f.write('}\n\n')
    f.write('export const results: Record<number, ExerciseResult[]> = {\n')
    for bai in sorted(exercises.keys()):
        results_list = []
        for text in exercises[bai]['text_outputs']:
            escaped = text.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')
            # Truncate very long outputs
            if len(escaped) > 5000:
                escaped = escaped[:5000] + '\\n... (truncated)'
            results_list.append(f'    {{ type: \'text\', content: `{escaped}` }}')
        for fname, _ in exercises[bai]['images']:
            results_list.append(f'    {{ type: \'image\', content: \'/results/{fname}\' }}')
        f.write(f'  {bai}: [\n')
        f.write(',\n'.join(results_list))
        f.write('\n  ],\n')
    f.write('}\n')

# Print summary
print(f"\nSummary:")
print(f"  Exercises: {len(exercises)}")
for bai in sorted(exercises.keys()):
    d = exercises[bai]
    print(f"  Bai {bai}: {len(d['code'])} code cells, {len(d['text_outputs'])} text outputs, {len(d['images'])} images")
print(f"\nGenerated files:")
print(f"  {os.path.join(OUT_DATA, 'codeBlocks.ts')}")
print(f"  {os.path.join(OUT_DATA, 'results.ts')}")
print(f"  {len([f for d in exercises.values() for f in d['images']])} images in {OUT_IMG}")
