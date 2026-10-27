from pathlib import Path
import sys,json,importlib.util
import numpy as np
H=Path(__file__).parent;P=H.parent
OLD=P/'report_refresh_20261024/natural_selection_20261025/figures'
sys.path.insert(0,str(OLD))
from figure_data import section_at_zero,exact_fields
from plot_comparisons import max_table
(H/'data').mkdir(exist_ok=True)
for case in ['A','D','Gaussian','Sinusoidal']:
 d=dict(np.load(OLD/'data'/f'{case}.npz'));f=np.load(H/f'{case}.npz')
 xi=np.array([int(np.argmin(abs(f['x']-v))) for v in d['x']]);assert np.max(abs(f['x'][xi]-d['x']))<1e-10
 for j,q in enumerate(['u','v']):
  yy=d[f'fd_y_{q}'];yi=np.array([int(np.argmin(abs(f['y']-v))) for v in yy]);assert np.max(abs(f['y'][yi]-yy))<1e-10
  d[f'fe_y_{q}']=yy;d[f'fe_error_final_{q}']=(f['z'][j]-f['ref'][j])[yi][:,xi]
  line,_=section_at_zero(f['y'],f['z'][j]);d[f'fe_line_final_{q}']=line[xi]
  ref=exact_fields(case,d['x'],[0],.01)[j][0]
  d[f'fe_line_error_final_{q}']=line[xi]-ref
 np.savez_compressed(H/'data'/f'{case}.npz',**d)
source=P/'spatial_ad_uv_20261025/heatmap_lowend_fix_20261025/plot_figures.py'
txt=source.read_text(encoding='utf8')
txt=txt.replace('grid=fig.add_gridspec(4,6,','grid=fig.add_gridspec(4,8,').replace('grid[row,:3]','grid[row,:4]').replace('grid[row,3:]','grid[row,4:]')
txt=txt.replace('101+3*row+i','101+4*row+i').replace('ncol=4','ncol=5').replace('fontsize=9.5,columnspacing=1.4','fontsize=9,columnspacing=1.1')
txt=txt.replace('figsize=(10.1,10.7)','figsize=(11.5,10.7)')
txt=txt.replace('color=color,lw=1.25,marker=None','color=color,lw=1.25,ls=(\'--\' if prefix==\'fe\' else \'-\'),marker=None')
(H/'plot_renderer.py').write_text(txt,encoding='utf8')
spec=importlib.util.spec_from_file_location('fe_plot_renderer',H/'plot_renderer.py');plot=importlib.util.module_from_spec(spec);spec.loader.exec_module(plot)
plot.OLD=H;plot.METHODS.append(('fe','FE','#9467BD','D'))
def tables(stage):
 t=max_table(stage)
 for c in ['A','D','Gaussian','Sinusoidal']:
  r=json.loads((H/f'{c}.json').read_text())
  for j,q in enumerate(['u','v']):t[c,'FE',q]=r['error'][j]
 return t
plot.max_table=tables
records=[plot.make(c) for c in ['A','D','Gaussian','Sinusoidal']]
(H/'figure_manifest.json').write_text(json.dumps(records,indent=2),encoding='utf8')
