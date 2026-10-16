"""Keep the original full-run history and register a targeted Lean revision."""
import hashlib
import json
from pathlib import Path

import nbformat

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
EVIDENCE = ROOT / 'Workspaces/notebook_reports_20261006/nonlinear_execution_validation.json'
NOTEBOOK = ROOT / 'notebook/非线性化report.ipynb'


def sha(data):
    return hashlib.sha256(data.encode('utf-8') if isinstance(data, str) else data).hexdigest()


def main():
    old = json.loads((HERE / 'before_revision/nonlinear_execution_validation.json').read_text('utf-8'))
    revision = json.loads((HERE / 'revision_validation.json').read_text('utf-8'))
    assert revision['success']
    assert old['notebook_sha256'] == revision['before_sha256']
    assert sha(NOTEBOOK.read_bytes()) == revision['after_sha256']
    current = nbformat.read(NOTEBOOK, 4)
    endpoint = next(c for c in current.cells if c.id == 'lean-uw')
    target_row = next(r for r in old['code_cells'] if r['id'] == endpoint.id)
    target_row['source_sha256'] = sha(endpoint.source)
    target_row['execution_count'] = endpoint.execution_count
    assert all(o.output_type == 'stream' for o in endpoint.outputs)
    target_row['outputs'] = [dict(type=o.output_type, name=o.name, text=o.text) for o in endpoint.outputs]
    old['executed_notebook_sha256'] = old['notebook_sha256']
    old['notebook_sha256'] = revision['after_sha256']
    old['verification_mode'] = 'original full notebook execution plus targeted Lean source re-execution'
    old['post_execution_lean_revision'] = str(HERE / 'revision_validation.json')
    old['targeted_revision_seconds'] = revision['targeted_seconds']
    old['targeted_revision_cell_timings'] = revision['timings']
    old['original_full_execution_seconds'] = old['elapsed_seconds']
    old['preserved_numeric_cells_and_outputs'] = True
    EVIDENCE.write_text(json.dumps(old, ensure_ascii=False, indent=2) + '\n', 'utf-8')
    print(json.dumps({'success': True, 'evidence': str(EVIDENCE),
                      'notebook_sha256': old['notebook_sha256']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
