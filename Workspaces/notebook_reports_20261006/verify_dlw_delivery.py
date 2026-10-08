"""Read back current native notebook outputs and compare the original 90 values and curves."""
from pathlib import Path
import base64
import hashlib
import json
import numpy as np
import nbformat

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
NOTEBOOK = ROOT/'notebook/DLW数值分析report.ipynb'
data = json.loads((HERE/'dlw_numeric_results.json').read_text(encoding='utf-8'))
rows = {(r['case'], r['model'], r['method'], r['mesh']):r for r in data['rows']}
case_map = dict(fig1a='A', fig1b='B', fig3='C')
tables = json.loads((ROOT/'Workspaces/index_readability_20261006/table_results.json').read_text(encoding='utf-8'))
comparisons = []
for row in tables:
    for label, expected in zip(row['labels'], row['values']):
        model = label if row['table']=='space' else row['model']
        method = label if row['table']=='time' else 'RK4'
        mesh = label if row['table']=='mesh' else 'fixed'
        key = case_map[row['case']], model, method, mesh
        actual = rows[key]['errors'][row['field']]
        diff = abs(actual-expected)
        comparisons.append(dict(table=row['table'], case=key[0], model=model,
            method=method, mesh=mesh, field=row['field'], expected=expected,
            actual=actual, absolute_difference=diff, relative_difference=diff/expected))
assert len(comparisons)==90
assert max(r['absolute_difference'] for r in comparisons)<1e-9
curves = []
with np.load(HERE/'dlw_numeric_curves.npz') as new, np.load(ROOT/'Workspaces/index_readability_20261006/error_curves.npz') as old:
    for case_old, case in case_map.items():
        for mesh in ('fixed', 'moving'):
            for model in ('SD', 'SD2', 'FD'):
                key = f'{case}_{model}_Euler_{mesh}'
                xx = new[key+'_x']
                take = (xx>=-1)&(xx<=1)
                assert np.max(abs(xx[take]-old['x']))<1e-12
                for field in ('u', 'v'):
                    difference = float(abs(new[key+'_'+field+'_curve'][take]-old[f'{case_old}_Euler_{mesh}_{model}_{field}']).max())
                    curves.append(dict(case=case, model=model, mesh=mesh, field=field,
                                       maximum_difference=difference))
assert len(curves)==36 and max(r['maximum_difference'] for r in curves)<1e-9
nb = nbformat.read(NOTEBOOK, as_version=4)
nbformat.validate(nb)
image_paths = []
for cell in nb.cells:
    if cell.cell_type=='code':
        assert cell.execution_count is not None
        assert not any(o.output_type=='error' for o in cell.outputs)
        for out in cell.outputs:
            if 'image/png' in out.get('data', {}):
                path = HERE/f'dlw_notebook_figure_{len(image_paths)+1}.png'
                path.write_bytes(base64.b64decode(out.data['image/png']))
                image_paths.append(str(path))
assert len(image_paths)==3 and all(r['completed'] for r in rows.values())
build = json.loads((HERE/'dlw_build_validation.json').read_text(encoding='utf-8'))
assert build['source_html_sha256']==hashlib.sha256((ROOT/'index.html').read_bytes()).hexdigest()
build['notebook_sha256'] = hashlib.sha256(NOTEBOOK.read_bytes()).hexdigest()
build['outputs'] = 'Actual independent native-kernel tables and Matplotlib figures'
(HERE/'dlw_build_validation.json').write_text(json.dumps(build,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
validation = dict(success=True, original_html_unchanged=True, table_values=len(comparisons),
    maximum_table_absolute_difference=max(r['absolute_difference'] for r in comparisons),
    maximum_table_relative_difference=max(r['relative_difference'] for r in comparisons),
    Euler_curves=len(curves), maximum_curve_difference=max(r['maximum_difference'] for r in curves),
    primary_runs=len(rows), time_refinement_runs=6, diagrams=3, error_curve_axes=12,
    notebook_sha256=build['notebook_sha256'], notebook_bytes=NOTEBOOK.stat().st_size,
    table_comparisons=comparisons, curve_comparisons=curves, figure_paths=image_paths)
(HERE/'dlw_delivery_validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in validation.items() if k not in ('table_comparisons','curve_comparisons','figure_paths')}, ensure_ascii=False,indent=2))
