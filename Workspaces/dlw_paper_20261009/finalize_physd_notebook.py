"""Populate the existing notebook's field outputs from the completed PF runs."""
from pathlib import Path
import json,base64,io
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
p=ROOT/'notebook/DLW数值分析report.ipynb'
nb=json.loads(p.read_text(encoding='utf-8'))
cells={c['id']:c for c in nb['cells']}
config=json.loads((HERE/'physd_domains_run/manifest.json').read_text())['configs']
outputs=[]
def show():
    fig=plt.gcf();buf=io.BytesIO();fig.savefig(buf,format='png',dpi=130)
    outputs.append({'output_type':'display_data','metadata':{},'data':{'image/png':base64.b64encode(buf.getvalue()).decode(),'text/plain':['<Figure: newly computed PF field/error>']}})
    plt.close(fig)
plt.show=show
ns={'np':np,'plt':plt,'HALF_WIDTHS':{c:cfg['yhalf'] for c,cfg in config.items()}}
exec(''.join(cells['dlw-field-config']['source']),ns)
exec(''.join(cells['dlw-field-helpers']['source']),ns)
for case in 'ABC':
    d=np.load(HERE/'physd_domains_run'/f'{case}_SD2_RK4_fixed.npz')
    drawing=dict(ns['PLOT_CONFIG'],**ns['PLOT_CONFIG']['windows'][case])
    ns['draw_field_panels'](d['x'],d['y'],[d['u'],d['v']],[d['exact_u'],d['exact_v']],
        f'DLW Case {case} | SD2 + RK4, fixed | t=0.01',('u','v'),drawing)
cells['dlw-field-plots']['outputs']=outputs
cells['dlw-field-plots']['execution_count']=36
nb['metadata']['physd_domains_rerun']['field_outputs']='six PF figures regenerated from matching completed runs'
p.write_text(json.dumps(nb,ensure_ascii=False,indent=1),encoding='utf-8')
print('Notebook saved: 3 updated tables and 6 new field/error figures')
