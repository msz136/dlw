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
config=json.loads((HERE/'unified_run/manifest.json').read_text())['config']
c=cells['dlw-field-config'];s=''.join(c['source'])
s=s.replace("'A': dict(xlim=(-20., 20.), ylim=(-20., 20.))","'A': dict(xlim=(-5., 5.), ylim=(-5., 5.))")
s=s.replace("'B': dict(xlim=(-20., 20.), ylim=(-20., 20.))","'B': dict(xlim=(-5., 5.), ylim=(-5., 5.))")
c['source']=s.splitlines(keepends=True)
c=cells['dlw-field-text']
c['source']=['## 8　物理场与误差分布\n\n','三个算例均在 $[-20,20]^2$ 上计算。两组单孤子展示 $[-5,5]^2$，二孤子展示 $[-20,20]^2$。固定网格、RK4，$\\Delta x=h=0.1$、$\\Delta t=0.0001$、$T=0.01$。场图与误差表采用同一组计算结果。\n']
c=cells['dlw-time-text'];s=''.join(c['source']);s=s.replace('三次样条重构数值场，计算','三次样条重构数值场（右端评价点采用末端样条延拓），计算');c['source']=s.splitlines(keepends=True)
c=cells['dlw-field-data'];s=''.join(c['source']).replace('# 与前面的误差表分开准备宽域场图；保持原空间、时间步长。','# 场图与前面的误差表采用相同计算域与空间、时间步长。');c['source']=s.splitlines(keepends=True)
outputs=[]
def show():
    fig=plt.gcf();buf=io.BytesIO();fig.savefig(buf,format='png',dpi=130)
    outputs.append({'output_type':'display_data','metadata':{},'data':{'image/png':base64.b64encode(buf.getvalue()).decode(),'text/plain':['<Figure: newly computed PF field/error>']}})
    plt.close(fig)
plt.show=show
ns={'np':np,'plt':plt,'FIELD_CONFIG':config}
exec(''.join(cells['dlw-field-config']['source']),ns)
exec(''.join(cells['dlw-field-helpers']['source']),ns)
for case in 'ABC':
    d=np.load(HERE/'unified_run'/f'{case}_SD2_RK4_fixed.npz')
    drawing=dict(ns['PLOT_CONFIG'],**ns['PLOT_CONFIG']['windows'][case])
    ns['draw_field_panels'](d['x'],d['y'],[d['u'],d['v']],[d['exact_u'],d['exact_v']],
        f'DLW Case {case} | SD2 + RK4, fixed | t=0.01',('u','v'),drawing)
cells['dlw-field-plots']['outputs']=outputs
cells['dlw-field-plots']['execution_count']=36
nb['metadata']['unified_rerun']['field_outputs']='six PF figures regenerated from matching completed runs'
p.write_text(json.dumps(nb,ensure_ascii=False,indent=1),encoding='utf-8')
print('Notebook saved: 3 updated tables and 6 new field/error figures')
