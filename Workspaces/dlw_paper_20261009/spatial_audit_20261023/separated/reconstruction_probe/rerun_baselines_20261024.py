from rerun_20261024 import *
from run_separated import norm
rows=[]
old=json.loads((HERE.parent/'spatial.json').read_text())
for c in 'ABCD':
 for method in ['Endpoint-SD','FD']:
  for dx,h in [(.1,.1),(.1,.05),(.1,.025),(.05,.1),(.025,.1)]:
   m=Model(c,method,dx,h);z=m.initial();full=m.rhs(0,z)
   vt=np.concatenate([fields(m,m.yv[i:i+32])[2][1] for i in range(0,len(m.yv),32)])
   total=norm(m,full-np.array([m.ut(m.y,0),vt]))
   prev=next(r for r in old if r['case']==c and r['method']==method and r['dx']==dx and r['h']==h)
   diff=max(abs(a-b) for a,b in zip(total,prev['total']))
   assert diff<1e-9,diff
   rows.append(dict(case=c,method=method,dx=dx,h=h,t=0,total=total,status='complete',previous_result_difference=diff))
   print(c,method,dx,h,total,flush=True)
(OUT/'baselines.json').write_text(json.dumps(rows,indent=2))
