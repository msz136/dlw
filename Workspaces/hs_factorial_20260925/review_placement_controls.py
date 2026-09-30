"""Refine the matched-endpoint node-placement diagnostic; no production edits."""
import json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline
from run_parameter_scan import setup,CHOICES
from local_advantage_study import NonuniformMovingSystem

HERE=Path(__file__).resolve().parent
DEST=HERE/'out'/'independent_review'
audit=json.loads((DEST/'audit.json').read_text())
rows=[]
for p in (3,5,12,20):
    ref,base,z0,X,n=setup(p,'ordinary_moving')
    f0=base.fields(0,z0)
    x=np.linspace(f0['x'][0],f0['x'][-1],n+1)
    u,rho,labels=ref.continuous_x(x,0)
    sys=NonuniformMovingSystem(np.diff(labels),1,base.left_u)
    z=sys.pack(np.diff(u),np.diff(x),x[0])
    grid=np.linspace(-3*CHOICES[p]['u_fwhm'],3*CHOICES[p]['u_fwhm'],9601)
    ur,rr,_=ref.continuous_x(grid,.25)
    scans=[]
    for dt in (.00625,.003125):
        sol=solve_ivp(sys.rhs,(0,.25),z,method='DOP853',rtol=2e-12,atol=2e-14,max_step=dt)
        assert sol.success
        f=sys.fields(.25,sol.y[:,-1]);xp=f['x'];rx=(xp[1:]+xp[:-1])/2
        rpoint=f['rho']-np.diff(xp)**2*CubicSpline(rx,f['rho'])(rx,2)/24
        ue=np.max(abs(CubicSpline(xp,f['u'])(grid)-ur))
        re=np.max(abs(CubicSpline(rx,rpoint)(grid)-rr))
        # Exact field on the same evolved mesh through identical reconstruction.
        un,_,_=ref.continuous_x(xp,.25)
        rn=ref.continuous_density_cell_mean(xp[:-1],xp[1:],.25)
        rnp=rn-np.diff(xp)**2*CubicSpline(rx,rn)(rx,2)/24
        scans.append(dict(max_step=dt,u_linf=float(ue),rho_linf=float(re),
            u_reconstruction_floor=float(np.max(abs(CubicSpline(xp,un)(grid)-ur))),
            rho_reconstruction_floor=float(np.max(abs(CubicSpline(rx,rnp)(grid)-rr)))))
    natural=next(r for r in audit['rows'] if r['p']==p and r['space']=='ordinary_moving')['metrics']['9601']
    rows.append(dict(p=p,scans=scans,ratio_uniform_to_natural={k:scans[-1][k]/natural[k] for k in ('u_linf','rho_linf')}))
(DEST/'placement_controls.json').write_text(json.dumps({'scope':'same moving formula, endpoint labels, node budget and velocity law; initial placement changes','rows':rows},indent=2)+'\n')
print(json.dumps(rows,indent=2))
