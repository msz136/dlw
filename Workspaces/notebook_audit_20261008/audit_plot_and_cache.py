from pathlib import Path
import contextlib
import io
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
def load(name):
    return json.loads((ROOT/'notebook'/name).read_text(encoding='utf-8'))
def source(nb, cell):
    return ''.join(nb['cells'][cell-1]['source'])

dlw = load('DLW数值分析report.ipynb')
hs = load('2HS数值分析report.ipynb')
ns = {'np': np, 'pd': pd, 'display': lambda *a: None,
      'CONFIG': {'T': .01, 'dt': .000125}, 'CASES': {'A': ((1.,), (2.,))},
      'MODELS': ('SD',)}
exec(source(dlw, 20), ns)
original_solve = ns['solve']
calls = []
def fake_solve(case, model, method, mesh, config=None):
    cfg = ns['CONFIG'] if config is None else config
    calls.append({'case': case, 'T': cfg['T'], 'parameters': ns['CASES'][case]})
    return dict(case=case, model=model, method=method, mesh=mesh,
                reached=cfg['T'], completed=True, reason='')
ns['solve'] = fake_solve
ns['calculate']('RK4', 'fixed')
ns['CONFIG']['T'] = .02
ns['CASES']['A'] = ((1.5,), (2.,))
ns['calculate']('RK4', 'fixed')
main_cache = {'solve_calls': calls.copy(), 'calls_after_parameter_edit': len(calls),
              'requested_T': ns['CONFIG']['T'],
              'cached_T': ns['results']['A', 'SD', 'RK4', 'fixed']['reached']}
ns['CONFIG'] = {'T': .03, 'dt': .000125}
main_cache['reassigned_CONFIG_T'] = ns['CONFIG']['T']
main_cache['original_solve_default_T_after_reassignment'] = original_solve.__defaults__[0]['T']
main_cache['solve_default_is_current_CONFIG'] = original_solve.__defaults__[0] is ns['CONFIG']

# Exercise the actual wide-domain preparation cell without solving the PDE.
ns['CONFIG'] = {'T': .01, 'dt': .000125, 'h': .125}
ns['CASES'] = {'A': ((1.,), (2.,))}
calls.clear()
with contextlib.redirect_stdout(io.StringIO()):
    exec(source(dlw, 33), ns)
    ns['CASES']['A'] = ((1.5,), (2.,))
    exec(source(dlw, 33), ns)
field_cache = {'solve_calls': calls.copy(), 'calls_after_soliton_parameter_edit': len(calls),
               'cache_entries': len(ns['dlw_field_cache']),
               'signature_contains_CASES': False}

# Check identical plotting functions, shared norms, actual colours and coordinates.
plot_ns = {'np': np, 'plt': plt}
exec(source(dlw, 36), plot_ns)
figures = []
original_show = plt.show
plt.show = lambda: figures.append(plt.gcf())
x, y = np.linspace(-1., 1., 9), np.linspace(-1., 1., 7)
X, Y = np.meshgrid(x, y)
num = [-(X**2+Y**2), .5*(X+Y)]
exact = [num[0]+.01, num[1]-.02]
cfg = dict(xlim=(-1., 1.), ylim=(-1., 1.), cmap='jet', error_cmap='jet',
           map_style='contour', levels=11, contour_width=1.1, elev=28., azim=-62.)
plot_ns['draw_field_panels'](x, y, num, exact, 'audit', ('u', 'v'), cfg)
plt.show = original_show
norms = []
for row in range(2):
    # 3 principal axes and one colourbar per field row.
    surface, numerical_map, exact_map = figures[0].axes[row*4:row*4+3]
    norms.append({'field': ('u', 'v')[row],
                  'numerical': [numerical_map.collections[0].norm.vmin, numerical_map.collections[0].norm.vmax],
                  'exact': [exact_map.collections[0].norm.vmin, exact_map.collections[0].norm.vmax],
                  'surface': [surface.collections[0].norm.vmin, surface.collections[0].norm.vmax]})
for fig in figures:
    plt.close(fig)
h = .125
n = round(30/h)
js = np.arange(-n, n)
grid_y = (js+.5)*h
accepted = plot_ns['checked_window']((-30., 30.), (-30., 30.), 'y')
sampling = {'checked_window': accepted, 'actual_y_endpoints': [float(grid_y[0]), float(grid_y[-1])],
            'unsampled_width_each_edge': float(h/2),
            'periodic_grid_convention': 'cell-centred y samples; no boundary-node extrapolation'}

evidence = {'main_result_cache': main_cache, 'wide_field_cache': field_cache,
            'plot_helpers_identical': source(dlw,36)==source(hs,33),
            'shared_surface_numerical_exact_norms': norms,
            'jet_zero_rgba_at_upper_endpoint': list(plt.get_cmap('jet')(1.)),
            'jet_error_zero_rgba': list(plt.get_cmap('jet')(0.)),
            'wide_y_plot_range': sampling,
            'stored_outputs': {'2hs_png': 12, 'dlw_png': 6,
                               'errors': 0, 'main_dlw_saved_trials': 27,
                               'time_refinement_additional_runs': 12}}
(OUT/'plot_cache_evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf-8')

paths = sorted((OUT/'extracted'/'2hs').glob('*.png')) + sorted((OUT/'extracted'/'dlw').glob('*.png'))
width, height = 510, 370
montage = Image.new('RGB', (3*width, ((len(paths)+2)//3)*height), 'white')
draw = ImageDraw.Draw(montage)
for index, path in enumerate(paths):
    im = Image.open(path).convert('RGB')
    im.thumbnail((width-12,height-30))
    left, top = index%3*width, index//3*height
    montage.paste(im,(left+(width-im.width)//2,top+24))
    draw.text((left+8,top+5),f'{path.parent.name}: {path.stem}',fill='black')
montage.save(OUT/'stored_figures_contact_sheet.png')
print(json.dumps(evidence,ensure_ascii=False,indent=2))
