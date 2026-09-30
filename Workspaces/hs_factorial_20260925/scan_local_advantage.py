"""Exploratory p scan on predeclared physical regions. Original c=1 schemes.
No parameter calibration, no density replacement, no best-point selection.
"""
import json,hashlib
from pathlib import Path
import numpy as np
from scipy.interpolate import CubicSpline
from run_parameter_scan import RobustSoliton
from hs_solver import MovingSystem,solve
from hs_fixed import FixedSystem

HERE=Path(__file__).resolve().parent
OUT=HERE/'out'/'local_p_search'
OUT.mkdir(parents=True,exist_ok=True)
PS=(2.5,3.,4.,5.,7.,10.,12.,16.,20.,28.,40.)
SPACES=('integrable_moving','ordinary_moving','fixed_difference')
TIMES=(.05,.1,.25)

class LocalReference(RobustSoliton):
    """Safeguarded monotone inverse for the centered c=1 single wave, all p>2."""
    def continuous_x(self,x,t,iterations=12):
        p=self.p[0];s=1-2/p;beta=p-p/(p-1);speed=(1-s*s)/4
        y=np.asarray(x)-speed*t
        lo=beta*(y-s/2)-1e-12;hi=beta*(y+s/2)+1e-12
        for _ in range(60):
            th=(lo+hi)/2
            error=th/beta+s*np.tanh(th/2)/2-y
            lo=np.where(error<0,th,lo)
            hi=np.where(error>=0,th,hi)
        th=(lo+hi)/2
        z=np.tanh(th/2);error=th/beta+s*z/2-y
        if np.max(abs(error))>1e-11:raise RuntimeError('Safeguarded reference inverse failed')
        sech2=1/np.cosh(th/2)**2
        return s*s*sech2/4,1/(1+s*s/(1-s*s)*sech2),(th+s*t)/beta

def wave(p):
    s=1-2/p;beta=p-p/(p-1)
    L=4*np.arccosh(np.sqrt(2))/beta+s/np.sqrt(2)
    return dict(s=s,L=L,V=(1-s*s)/4,Au=s*s/4,Ar=s*s,
                half=float(np.ceil(3*L+2)))

def run(p,space,a=.02,dt=.00625,half_extra=0):
    w=wave(p);ref=LocalReference((p,),shift=-w['s']/2)
    H=w['half']+half_extra;n=round(2*H/a);X=np.linspace(-H,H,n+1)
    if space=='fixed_difference':
        sys=FixedSystem(X,1,ref);state=sys.initial(0)
    else:
        u,x,rho=ref.continuous_X(X,0)
        b=lambda t:float(ref.continuous_X(np.array([-H]),t)[0][0])
        sys=MovingSystem(a,1,n,b,'sd' if space=='integrable_moving' else 'fd')
        state=sys.pack(np.diff(u),np.diff(x),x[0])
    result=solve(sys,state,0,.25,dt,'rk4',outputs=TIMES,strict=False)
    row=dict(p=p,space=space,a=a,dt=dt,H=H,wave=w,status=result.status,
             reached=float(result.t[-1]),rejected=result.rejected,
             failure=result.failure_reason,observations=[])
    for t,z in zip(result.t[1:],result.states[1:]):
        if not any(abs(t-tt)<1e-10 for tt in TIMES):continue
        f=sys.fields(t,z);x=f['x'];u=f['u'];rho=f['rho']
        rx=x if space=='fixed_difference' else (x[1:]+x[:-1])/2
        ur,rr,_=ref.continuous_x(x,t)
        if space=='fixed_difference':rp=rho;rn=rr;rpn=rr
        else:
            rn=ref.continuous_density_cell_mean(x[:-1],x[1:],t)
            rp=rho-f['d']**2*CubicSpline(rx,rho)(rx,2)/24
            rpn=rn-f['d']**2*CubicSpline(rx,rn)(rx,2)/24
        eta=np.linspace(-3,3,4801);grid=eta*w['L']+w['V']*t
        if grid[0]<rx[0] or grid[-1]>rx[-1]:raise ValueError('evaluation outside grid')
        ut,rt,_=ref.continuous_x(grid,t)
        ue=abs(CubicSpline(x,u)(grid)-ut);re=abs(CubicSpline(rx,rp)(grid)-rt)
        uf=abs(CubicSpline(x,ur)(grid)-ut);rf=abs(CubicSpline(rx,rpn)(grid)-rt)
        masks={'peak':abs(eta)<=.5,'shoulders':(abs(eta)>.5)&(abs(eta)<=1.5),
               'wave':np.ones(eta.shape,dtype=bool)}
        obs=dict(t=float(t),regions={})
        for label,mask in masks.items():
            eu=float(max(ue[mask]));er=float(max(re[mask]))
            obs['regions'][label]=dict(u=eu,rho=er,joint=max(eu/w['Au'],er/w['Ar']),
                u_floor=float(max(uf[mask])),rho_floor=float(max(rf[mask])))
        row['observations'].append(obs)
    return row

def main():
    data=dict(scope='exploratory fixed original c=1 p scan; regions declared before results',
              ps=PS,regions={'peak':'|x-Vt|<=L/2','shoulders':'L/2<|x-Vt|<=1.5L',
                             'wave':'|x-Vt|<=3L'},rows=[],status='running')
    for p in PS:
        for space in SPACES:
            print('scan',p,space,flush=True)
            try:data['rows'].append(run(p,space))
            except Exception as ex:data['rows'].append(dict(p=p,space=space,status='exception',failure=str(ex)))
            (OUT/'scan.json').write_text(json.dumps(data,indent=2)+'\n')
    comparisons=[]
    for p in PS:
        rows={r['space']:r for r in data['rows'] if r['p']==p}
        if any(r['status']!='completed' for r in rows.values()):continue
        for i,t in enumerate(TIMES):
            for region in data['regions']:
                aa=rows['integrable_moving']['observations'][i]['regions'][region]
                for target in SPACES[1:]:
                    bb=rows[target]['observations'][i]['regions'][region]
                    ratios={k:aa[k]/bb[k] for k in ('u','rho','joint')}
                    comparisons.append(dict(p=p,t=t,region=region,against=target,
                        ratios=ratios,both_fields_better=ratios['u']<1 and ratios['rho']<1,
                        reconstruction_resolved=all(v[k+'_floor']<.1*v[k] for v in (aa,bb) for k in ('u','rho'))))
    data.update(status='completed',comparisons=comparisons,
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (OUT/'scan.json').write_text(json.dumps(data,indent=2)+'\n')
    print('wins',json.dumps([r for r in comparisons if min(r['ratios'].values())<1],indent=2))
if __name__=='__main__':main()
