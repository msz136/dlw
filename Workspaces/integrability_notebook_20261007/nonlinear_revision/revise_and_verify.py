"""Expose report (7) definitions and compile just the changed Lean endpoint."""
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import time

import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
NOTEBOOK = ROOT / 'notebook' / '非线性化report.ipynb'
BUILDER = ROOT / 'Workspaces/notebook_reports_20261006/build_nonlinear_notebook.py'
PROOF = ROOT / 'Workspaces/report_notebook_20261002/lean_material/proofs/ReportNonlinearUW.lean'


def sha(data):
    if isinstance(data, str):
        data = data.encode('utf-8')
    return hashlib.sha256(data).hexdigest()


def digest(value):
    return sha(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')))


def main():
    before = nbformat.read(NOTEBOOK, 4)
    proposed = deepcopy(before)
    spec = importlib.util.spec_from_file_location('nonlinear_builder', BUILDER)
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    builder.add_uw_definitions(proposed.cells)
    changed = [c.id for c, old in zip(proposed.cells, before.cells) if c.source != old.source]
    assert changed == ['report-text-04', 'lean-uw'], changed
    nbformat.validate(proposed)
    nbformat.write(proposed, HERE / 'nonlinear.revised.input.ipynb')

    definition_sources = {}
    import re
    original_proof = PROOF.read_text('utf-8')
    for name in ['fluxUW', 'fluxOmega', 'reportN1', 'reportN2']:
        definition = re.search(r'^def ' + name + r' .*?(?=\n\n)', original_proof,
                               re.M | re.S).group(0)
        assert definition in builder.UW_RESIDUAL_DEFINITIONS
        definition_sources[name] = {'exact_source_match': True, 'sha256': sha(definition)}

    subset_ids = ['runtime-prepare', 'lean-uw-import', 'lean-uw-start', 'lean-uw']
    subset = nbformat.v4.new_notebook(
        cells=[deepcopy(c) for c in proposed.cells if c.id in subset_ids],
        metadata=deepcopy(before.metadata),
    )
    for cell in subset.cells:
        cell.outputs = []
        cell.execution_count = None
    nbformat.write(subset, HERE / 'targeted_lean.input.ipynb')
    km = KernelManager(kernel_name='python3')
    km.kernel_spec.argv = [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}']
    timings, starts = [], {}

    def on_start(cell, cell_index, **kwargs):
        starts[cell.id] = time.perf_counter()
        print(json.dumps({'execute_cell': cell.id}, ensure_ascii=False), flush=True)

    def on_executed(cell, cell_index, **kwargs):
        timings.append({'id': cell.id, 'seconds': round(time.perf_counter() - starts[cell.id], 3)})
        print(json.dumps({'executed_cell': cell.id, 'seconds': timings[-1]['seconds']},
                         ensure_ascii=False), flush=True)

    client = NotebookClient(subset, km=km, timeout=600, startup_timeout=60,
                            resources={'metadata': {'path': str(HERE)}}, allow_errors=False,
                            on_cell_start=on_start, on_cell_executed=on_executed)
    started = time.perf_counter()
    failure = None
    try:
        client.execute()
    except BaseException as error:
        failure = {'type': type(error).__name__, 'message': str(error)}
    nbformat.write(subset, HERE / 'targeted_lean.executed.ipynb')
    outputs = {c.id: c.outputs for c in subset.cells}
    output_text = ''.join(o.get('text', '') for c in subset.cells for o in c.outputs)
    (HERE / 'targeted_lean.stdout.txt').write_text(output_text, 'utf-8')
    errors = [o for c in subset.cells for o in c.outputs if o.output_type == 'error']
    validation = {
        'success': failure is None and not errors,
        'notebook': str(NOTEBOOK), 'before_sha256': sha(NOTEBOOK.read_bytes()),
        'changed_cell_ids': changed, 'new_cell_ids': [],
        'targeted_code_cell_ids': subset_ids, 'timings': timings,
        'targeted_seconds': round(time.perf_counter() - started, 3),
        'python': sys.executable, 'failure': failure, 'errors': errors,
        'proof_source': str(PROOF), 'proof_source_sha256': sha(PROOF.read_bytes()),
        'complete_definition_source_matches': definition_sources,
        'stdout': str(HERE / 'targeted_lean.stdout.txt'),
        'executed_targeted_notebook': str(HERE / 'targeted_lean.executed.ipynb'),
    }
    if not validation['success']:
        (HERE / 'revision_validation.json').write_text(json.dumps(validation, ensure_ascii=False, indent=2), 'utf-8')
        raise RuntimeError(f'Targeted Lean validation failed: {failure or errors}')
    assert 'sorryAx' not in output_text
    assert 'NotebookDisplay.reportN1' in output_text
    assert 'NotebookDisplay.reportN2' in output_text
    endpoint = next(c for c in subset.cells if c.id == 'lean-uw')
    current_endpoint = next(c for c in proposed.cells if c.id == 'lean-uw')
    current_endpoint.outputs = deepcopy(endpoint.outputs)
    current_endpoint.execution_count = endpoint.execution_count
    preserved = []
    for old, new in zip(before.cells, proposed.cells):
        if old.cell_type == 'code' and old.id != 'lean-uw':
            assert old == new, old.id
            preserved.append(old.id)
    assert [c.id for c in before.cells] == [c.id for c in proposed.cells]
    numeric_before = [c for c in before.cells if c.id.startswith('error-')]
    numeric_after = [c for c in proposed.cells if c.id.startswith('error-')]
    assert numeric_before == numeric_after
    nbformat.validate(proposed)
    nbformat.write(proposed, NOTEBOOK)
    validation.update(
        after_sha256=sha(NOTEBOOK.read_bytes()),
        unchanged_code_cells_preserved=preserved,
        numeric_cells_and_outputs_byte_equivalent=True,
        numeric_cells_digest=digest(numeric_after),
        code_cells=sum(c.cell_type == 'code' for c in proposed.cells),
        lean_cells=sum(c.cell_type == 'code' and c.source.startswith('%%lean') for c in proposed.cells),
        builder=str(BUILDER), builder_sha256=sha(BUILDER.read_bytes()),
        endpoint_source_sha256=sha(current_endpoint.source),
        endpoint_outputs_saved=True,
    )
    (HERE / 'revision_validation.json').write_text(json.dumps(validation, ensure_ascii=False, indent=2) + '\n', 'utf-8')
    print(json.dumps({k: validation[k] for k in ['success', 'changed_cell_ids', 'targeted_seconds', 'after_sha256']}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
