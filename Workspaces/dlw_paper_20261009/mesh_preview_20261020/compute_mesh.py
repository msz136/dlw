"""Actual notebook PE/SAMM run, case C; no synthetic mesh data."""
from pathlib import Path
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import json, numpy as np
P=Path(__file__).resolve().parent
root=P.parents[2]
nb=json.loads((root/'notebook/DLW数值分析report.ipynb').read_text(encoding='utf-8'))
cells={c.get('id'):''.join(c.get('source',[])) for c in nb['cells']}
ns={}
for key in ['imports','config','reference','spatial','sd_fd','sd','sd2_lift','sd2_evolution','fd','mesh','time']:
 exec(cells['dlw-'+key].replace('from IPython.display import display','display=lambda *a,**k:None'),ns)
cfg=ns['case_config']('C')
p=ns['Problem']('C','SD','moving',cfg)
state=p.initial();x0=p.X.x.copy(); times=[0.]; xs=[x0.copy()]
for n in range(round(cfg['T']/cfg['dt'])):
 state=ns['step'](p.stage,n*cfg['dt'],state,cfg['dt'],'RK4')
 assert np.isfinite(state).all()
 if (n+1)%10==0:
  p.fields(state,(n+1)*cfg['dt']); times.append((n+1)*cfg['dt']);xs.append(p.X.x.copy())
u,v=p.fields(state,cfg['T']); xf=p.X.x.copy()
gh=ns['ghost_u'](p.m.G,p.m.js,xf,cfg['T'],u)
rho=(1-(v-ns['delta0'](u,gh,p.m.h))/4).mean(axis=0)
xx=np.linspace(-30,30,401); jy=np.arange(-300,300,3)
ue,ve=p.m.G.uv(jy,xx,cfg['T'])
uniform=p.X.xi.copy()
np.savez_compressed(P/'case_C_mesh.npz',uniform=uniform,x0=x0,xf=xf,times=times,xs=xs,rho=rho,xfield=xx,yfield=(jy+.5)*cfg['h'],u=ue,v=ve)
metrics={'case':'C','p':[6,4],'q':[-5,-3],'config':cfg,'node_count':len(xf),'min_J':float(p.X.J.min()),'min_spacing':float(np.diff(xf).min()),'max_spacing':float(np.diff(xf).max()),'max_initial_redistribution':float(abs(x0-uniform).max()),'max_evolution_displacement':float(abs(xf-x0).max()),'rho_min':float(rho.min()),'rho_max':float(rho.max()),'source':'notebook/DLW数值分析report.ipynb; PE/SD; RK4; actual coupled field-node evolution','background':'semi-discrete exact u at T, shared by both mesh panels'}
(P/'metrics.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(metrics,ensure_ascii=False))
