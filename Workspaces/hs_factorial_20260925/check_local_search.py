"""Control the nearest-to-winning original-scheme cases; validate new inverse."""
import json
from pathlib import Path
import numpy as np
from scan_local_advantage import LocalReference,run,SPACES,PS

HERE=Path(__file__).resolve().parent
OUT=HERE/'out'/'local_p_search'
checks=[]
for p in PS:
    s=1-2/p;ref=LocalReference((p,),shift=-s/2)
    for t in (0,.05,.25):
        X=np.linspace(-5,5,4001)
        u,x,rho=ref.continuous_X(X,t)
        un,rn,Xn=ref.continuous_x(x,t)
        dif=max(np.max(abs(un-u)),np.max(abs(rn-rho)),np.max(abs(Xn-X)))
        assert dif<1e-10,(p,t,dif)
        checks.append(dict(p=p,t=t,max_difference=float(dif)))
rows=[]
for p in (28.,40.):
    for a,dt in ((.02,.003125),(.01,.003125),(.005,.003125)):
        for space in SPACES:
            print('control',p,a,space,flush=True)
            rows.append(run(p,space,a,dt))
for space in SPACES:
    rows.append(run(40.,space,.02,.003125,half_extra=1))
out=dict(reference_checks=checks,rows=rows)
(OUT/'controls.json').write_text(json.dumps(out,indent=2)+'\n')
summary=[]
for p in (28.,40.):
    for a in (.02,.01,.005):
        pair={r['space']:r for r in rows if r['p']==p and r['a']==a and r['H']==float(np.ceil(3*r['wave']['L']+2))}
        for reg in ('peak','shoulders','wave'):
            for i,t in enumerate((.05,.1,.25)):
                A=pair['integrable_moving']['observations'][i]['regions'][reg]
                B=pair['ordinary_moving']['observations'][i]['regions'][reg]
                summary.append(dict(p=p,a=a,region=reg,t=t,
                    u_ratio=A['u']/B['u'],rho_ratio=A['rho']/B['rho'],joint_ratio=A['joint']/B['joint']))
print('best control',min(summary,key=lambda r:r['joint_ratio']))
print('wins',[r for r in summary if min(r['u_ratio'],r['rho_ratio'],r['joint_ratio'])<1])
