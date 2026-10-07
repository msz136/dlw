"""Verify the newly executed report, exported scalars, and saved error curves."""
from pathlib import Path
import base64
import hashlib
import json
import numpy as np
import nbformat
from dlw_numeric_cells import CELLS

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PATH = ROOT/'notebook/DLW数值分析report.ipynb'
EVIDENCE = HERE/'gsg_second_order'
EVIDENCE.mkdir(exist_ok=True)
data = json.loads((HERE/'dlw_numeric_results.json').read_text('utf-8'))
rows = {(r['case'], r['model'], r['method'], r['mesh']):r for r in data['rows']}
expected_rows = {(case, model, method, mesh) for case in ('A', 'B', 'C')
    for model, method in (('SD', 'Midpoint'), ('SD2', 'RK4'), ('FD', 'RK4'))
    for mesh in ('fixed', 'moving')}
expected_rows.update((case, model, 'Euler', 'fixed')
    for case in ('A', 'B', 'C') for model in ('SD2', 'FD'))
assert len(data['rows']) == len(rows) == 24
assert set(rows) == expected_rows
assert all(r['completed'] and abs(r['reached']-.01)<1e-13 for r in rows.values())
assert all(r['min_J']>0 and set(r['errors']) == {'u', 'v'}
           and np.isfinite(list(r['errors'].values())).all()
           and min(r['errors'].values()) >= 0 for r in rows.values())
assert max(r['initial_error'] for r in rows.values())<1e-9
assert all(k[2]=='Midpoint' for k in rows if k[1]=='SD')
orders = data['order_rows']
assert len(orders)==12
order_keys = {(r['算例'], r['方案'], r['时间算法'], r['场']) for r in orders}
assert len(order_keys) == 12
assert order_keys == {(case, model, method, field) for case in ('A', 'B', 'C')
    for model, method in (('SD', 'Midpoint'), ('SD2', 'Euler')) for field in ('u', 'v')}
assert all(r['dt 与 dt/2 场差'] > 0 and r['dt/2 与 dt/4 场差'] > 0
           and np.isclose(r['观测阶'], np.log2(r['dt 与 dt/2 场差']/r['dt/2 与 dt/4 场差']),
                          rtol=0, atol=1e-12) for r in orders)
sd_orders = [r['观测阶'] for r in orders if r['方案']=='SD']
sd2_orders = [r['观测阶'] for r in orders if r['方案']=='SD2']
assert all(1.85<p<2.15 for p in sd_orders)
assert all(.85<p<1.15 for p in sd2_orders)
curve_differences = []
archive_path = HERE/'dlw_numeric_curves.npz'
with np.load(archive_path) as curves:
    expected_keys = set()
    reference_x = None
    for key, row in rows.items():
        label = '_'.join(key)
        expected_keys.update(label+suffix for suffix in ('_x', '_u_curve', '_v_curve'))
        x = curves[label+'_x']
        assert x.shape == (4001,) and np.isfinite(x).all() and np.diff(x).min() > 0
        assert x[0] == -10 and x[-1] == 10
        if reference_x is None:
            reference_x = x.copy()
        assert np.array_equal(x, reference_x)
        for field in ('u', 'v'):
            curve = curves[label+'_'+field+'_curve']
            assert curve.shape == x.shape and np.isfinite(curve).all() and curve.min() >= 0
            maximum = float(curve.max())
            difference = abs(maximum-row['errors'][field])
            assert np.isclose(maximum, row['errors'][field], rtol=1e-12, atol=1e-14), (key, field)
            curve_differences.append(difference)
    assert set(curves.files) == expected_keys
nb = nbformat.read(PATH, as_version=4)
nbformat.validate(nb)
by_id = {c.id:c for c in nb.cells}
source_hashes = {}
for name, source in CELLS.items():
    cell = by_id['dlw-'+name]
    assert cell.cell_type == 'code' and cell.source.strip() == source.strip(), name+' is stale'
    source_hashes[cell.id] = hashlib.sha256(cell.source.encode()).hexdigest()
notebook_hash = hashlib.sha256(PATH.read_bytes()).hexdigest()
all_source_hashes = {c.id: hashlib.sha256(c.source.encode()).hexdigest() for c in nb.cells}
exported_results_hash = hashlib.sha256((HERE/'dlw_numeric_results.json').read_bytes()).hexdigest()
exported_curves_hash = hashlib.sha256(archive_path.read_bytes()).hexdigest()
execution_path = HERE/'dlw_execution_validation.json'
execution = json.loads(execution_path.read_text('utf-8'))
assert execution['success'] and execution['sources_unchanged'] and execution['outputs_saved']
assert execution['notebook_sha256'] == notebook_hash
assert execution['independent_native_kernel']
assert execution['source_hashes'] == data['source_hashes'] == all_source_hashes
assert execution['exported_results_sha256'] == exported_results_hash
assert execution['exported_curves_sha256'] == exported_curves_hash
assert any(r['cell'] == 'dlw-validation-export' for r in execution['timings'])
spatial_audit_path = EVIDENCE/'verify_second_order_spatial.json'
tau_audit_path = EVIDENCE/'verify_dlw_tau.json'
spatial_audit = json.loads(spatial_audit_path.read_text('utf-8'))
tau_audit = json.loads(tau_audit_path.read_text('utf-8'))
assert spatial_audit['success'] and tau_audit['passed']
assert len(tau_audit['rows']) == 6
assert set(spatial_audit['notebook_definition_sources_sha256']) == {
    'dlw-spatial', 'dlw-sd', 'dlw-sd2_lift', 'dlw-sd2_evolution'}
assert set(tau_audit['notebook_definition_sources_sha256']) == set(source_hashes)
for audit in (spatial_audit, tau_audit):
    assert all(source_hashes[name] == digest for name, digest in
               audit['notebook_definition_sources_sha256'].items())
assert 'class SDModel:' in by_id['dlw-sd'].source
assert 'def rhs' not in by_id['dlw-sd'].source
assert 'P_{j,t}' not in by_id['dlw-sd-text'].source
assert 'G_{j+1}^{n+1}' in by_id['dlw-sd-text'].source
texts = '\n'.join(c.source for c in nb.cells if c.cell_type=='markdown')
assert '不能由' not in texts and '不能代替' not in texts and 'index.html' not in texts
figures = []
for cell in nb.cells:
    if cell.cell_type!='code':
        continue
    assert cell.execution_count is not None
    assert not any(o.output_type=='error' for o in cell.outputs)
    for out in cell.outputs:
        if 'image/png' in out.get('data', {}):
            path = EVIDENCE/f'dlw_notebook_figure_{len(figures)+1}.png'
            path.write_bytes(base64.b64decode(out.data['image/png']))
            figures.append(str(path))
assert len(figures)==3
validation = dict(success=True, primary_runs=len(rows), temporal_refinement_runs=12,
    initial_maximum_evaluation_node_error=max(r['initial_error'] for r in rows.values()),
    scalar_curve_maxima_comparisons=len(curve_differences),
    maximum_scalar_curve_difference=max(curve_differences),
    sd_midpoint_order_range=[min(sd_orders),max(sd_orders)],
    sd2_euler_order_range=[min(sd2_orders),max(sd2_orders)], diagrams=len(figures),
    code_cells=sum(c.cell_type=='code' for c in nb.cells), all_code_executed=True,
    notebook_sha256=notebook_hash, notebook_code_sources_sha256=source_hashes,
    exported_results_sha256=exported_results_hash,
    exported_curves_sha256=exported_curves_hash,
    native_execution_sha256=hashlib.sha256(execution_path.read_bytes()).hexdigest(),
    independent_spatial_audit_sha256=hashlib.sha256(spatial_audit_path.read_bytes()).hexdigest(),
    independent_tau_audit_sha256=hashlib.sha256(tau_audit_path.read_bytes()).hexdigest(),
    independent_raw_bilinear_max_relative_residual=max(p['maximum_B_relative_to_term_sum']
        for r in tau_audit['rows'] for p in r['raw_bilinear_pairs']),
    fresh_native_exports_checked=True, figure_paths=figures)
(EVIDENCE/'dlw_delivery_validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(validation,ensure_ascii=False,indent=2))
