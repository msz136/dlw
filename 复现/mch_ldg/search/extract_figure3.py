"""Read vector path coordinates, never execute PostScript.

Axis calibration from explicit ticks of Ex3H1normP3.eps:
time 0:6250, time 1:10141, time 2:14032, time 3:17923,
E=0:6803, E=.05:10351. Integer EPS positions imply rounding uncertainty.
This recovers a plotted curve, NOT the authors' numerical arrays.
"""
import tarfile,re,json
from pathlib import Path
import numpy as np

root=Path(__file__).resolve().parent
with tarfile.open(root/'arxiv_source_response.bin','r:gz') as tf:
    text=tf.extractfile('figs/Ex3H1normP3.eps').read().decode('latin1')
lines=text.splitlines();start=next(i for i,l in enumerate(lines) if l.startswith('2 z x [461'))
points=[]
for line in lines[start+1:]:
    if 'clp' in line:break
    m=re.fullmatch(r'(\d+) (\d+) [ml]',line.strip())
    if m:points.append([float(m[1]),float(m[2])])
points=np.asarray(points)
tt=(points[:,0]-6250)/3891.2
ee=(points[:,1]-6803)/70960
np.savetxt(root/'figure3_dissipative_digitized.csv',np.c_[tt,ee],delimiter=',',header='time,plotted_ordinate',comments='')
meta=dict(source='https://arxiv.org/src/2608.28077v2',figure='3 bottom-left dissipative curve',points=len(tt),
          first_time=float(tt[0]),last_time=float(tt[-1]),last_ordinate=float(ee[-1]),
          y_rounding_resolution=1/70960,x_rounding_resolution=1/3891.2,
          caveat='Axis-calibrated vector plot; interpretation of ordinate still unconfirmed. Not original simulation data.')
(root/'figure3_digitization.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
print(json.dumps(meta,indent=2))
