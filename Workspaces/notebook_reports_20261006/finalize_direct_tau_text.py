"""Sync reviewed mathematical wording without changing executed code or outputs."""
from pathlib import Path
import hashlib
import json
import nbformat
from tau_report_cells import TEXT_UPDATE

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
path = ROOT/'notebook/DLW数值分析report.ipynb'
nb = nbformat.read(path, as_version=4)
code_before = [(c.source, c.outputs) for c in nb.cells if c.cell_type=='code']
for c in nb.cells:
    key = c.id.removeprefix('dlw-')
    if c.cell_type=='markdown' and key in TEXT_UPDATE:
        c.source = TEXT_UPDATE[key].strip()
assert code_before == [(c.source, c.outputs) for c in nb.cells if c.cell_type=='code']
nbformat.write(nb, path)
digest = hashlib.sha256(path.read_bytes()).hexdigest()
for name in ('dlw_build_validation.json','dlw_execution_validation.json'):
    manifest_path = HERE/name
    data = json.loads(manifest_path.read_text('utf-8'))
    data['notebook_sha256'] = digest
    data['reviewed_markdown_synced'] = True
    data['executed_code_and_outputs_unchanged'] = True
    manifest_path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Reviewed wording synced; code and outputs unchanged')
