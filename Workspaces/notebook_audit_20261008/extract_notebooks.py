from pathlib import Path
import base64
import hashlib
import json

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
FILES = {
    '2hs': '2HS数值分析report.ipynb',
    'dlw': 'DLW数值分析report.ipynb',
    'theory': 'DLW理论.ipynb',
}
inventory = {}
for key, name in FILES.items():
    path = ROOT / 'notebook' / name
    raw = path.read_bytes()
    nb = json.loads(raw)
    folder = OUT / 'extracted' / key
    folder.mkdir(parents=True, exist_ok=True)
    source, outputs, cells = [], [], []
    for index, cell in enumerate(nb['cells'], 1):
        src = ''.join(cell.get('source', []))
        source.append(f'===== CELL {index} [{cell["cell_type"]}] id={cell.get("id", "")} =====\n{src}\n')
        row = {'cell': index, 'type': cell['cell_type'], 'id': cell.get('id'),
               'source_lines': len(src.splitlines()), 'execution_count': cell.get('execution_count'),
               'outputs': []}
        for oi, output in enumerate(cell.get('outputs', []), 1):
            desc = {'index': oi, 'type': output.get('output_type')}
            if 'text' in output:
                outputs.append(f'===== CELL {index} OUTPUT {oi} =====\n' + ''.join(output['text']))
            if output.get('output_type') == 'error':
                desc.update(ename=output.get('ename'), evalue=output.get('evalue'))
            for mime, data in output.get('data', {}).items():
                if mime in ('text/plain', 'text/html'):
                    outputs.append(f'===== CELL {index} OUTPUT {oi} {mime} =====\n' + ''.join(data))
                elif mime == 'image/png':
                    img = folder / f'cell_{index:02d}_output_{oi:02d}.png'
                    img.write_bytes(base64.b64decode(''.join(data)))
                    desc['image'] = str(img)
                desc.setdefault('mimes', []).append(mime)
            row['outputs'].append(desc)
        cells.append(row)
    (folder / 'source.txt').write_text('\n'.join(source), encoding='utf-8')
    (folder / 'outputs.txt').write_text('\n'.join(outputs), encoding='utf-8')
    inventory[key] = {'path': str(path), 'sha256': hashlib.sha256(raw).hexdigest(),
                      'metadata': nb.get('metadata', {}), 'cells': cells}
(OUT / 'inventory.json').write_text(json.dumps(inventory, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({k: {'cells': len(v['cells']), 'sha256': v['sha256'],
                       'errors': [c['cell'] for c in v['cells'] if any(o['type'] == 'error' for o in c['outputs'])],
                       'image_count': sum('image' in o for c in v['cells'] for o in c['outputs'])}
                  for k, v in inventory.items()}, ensure_ascii=False, indent=2))
