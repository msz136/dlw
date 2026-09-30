"""Observed 1% finite-h field-accuracy window on the original DLW RHS."""
from pathlib import Path
import sys,json,hashlib

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'lib'),str(ROOT/'experiments')]
import numpy as np
from moving_mesh import MovingProblem
from moving_mesh_study import ALL
from moving_mesh_route1_coupled import norm


def run(pars,width,model,mode,dt=.000125,nx=128):
    p=MovingProblem(pars,h=.125,nx=nx,model=model)
    z,s=p.initial('static_adaptive')
    peak=p.m.G.uv(p.m.js,p.X.x,0.)
    scale=(norm(peak[0]),norm(peak[1]))
    T=width/abs(pars.p-pars.q)
    steps=round(T/dt)
    observations=[];reason=None
    for i in range(steps):
        t=i*dt
        try:
            if mode=='moving':
                state=np.r_[z,s];nz=z.size
                def fun(tt,zz):
                    dz,ds=p.rhs(tt,(zz[:nz],zz[nz:]),balanced=False,
                                 mesh_mode='moving')
                    return np.r_[dz,ds]
                k1=fun(t,state);k2=fun(t+dt/2,state+dt*k1/2)
                k3=fun(t+dt/2,state+dt*k2/2);k4=fun(t+dt,state+dt*k3)
                state=state+dt*(k1+2*k2+2*k3+k4)/6
                z,s=state[:nz],state[nz:]
                p.set_s(s)
            else:
                def fun(tt,zz):return p.m.rhs(tt,zz)
                k1=fun(t,z);k2=fun(t+dt/2,z+dt*k1/2)
                k3=fun(t+dt/2,z+dt*k2/2);k4=fun(t+dt,z+dt*k3)
                z=z+dt*(k1+2*k2+2*k3+k4)/6
            if not np.all(np.isfinite(z)) or norm(z)>1e3:
                raise ValueError('state diverged')
            if (i+1)%round(.005/dt)==0:
                now=(i+1)*dt
                u,v=p.m.fields(z,now)
                ue,ve=p.m.G.uv(p.m.js,p.X.x,now)
                eu,ev=norm(u-ue)/scale[0],norm(v-ve)/scale[1]
                observations.append({'t':now,'D':abs(pars.p-pars.q)*now/width,
                                     'relative_u':eu,'relative_v':ev,
                                     'min_dx':float(min(p.X.spacing())),
                                     'min_J':float(min(p.X.J))})
                if max(eu,ev)>.01:
                    reason='1% field gate failed at observed time'
                    break
        except ValueError as exc:
            reason=str(exc);break
    return {'model':model,'mode':mode,'nx':nx,'dt':dt,
            'target_T_at_D1':T,'reason':reason,
            'last_checked':observations[-1] if observations else None,
            'last_passed':next((x for x in reversed(observations)
                              if max(x['relative_u'],x['relative_v'])<=.01),None),
            'observations':observations}


def main():
    base=ROOT/'out/moving_mesh'
    geom=json.loads((base/'route1_geometry.json').read_text())
    width={x['parameter_id']:x['width'] for x in geom['cases']}
    data={'scope':{'cases':['P1','P2','P7','P10'],'h':.125,'nx':128,
                   'dt':.000125,'observations_every':.005,
                   'gate':'both physical u/v max error <=1% of own initial peak',
                   'reference':'exact finite-h Gram field'},'runs':[]}
    for index in (0,1,6,9):
        pid=f'P{index+1}'
        for model in ('structure','fd'):
            for mode in ('static_adaptive','moving'):
                row=run(ALL[index],width[pid],model,mode)
                row['parameter_id']=pid
                data['runs'].append(row)
                print(pid,model,mode,row['reason'],row['last_checked'],flush=True)
    paths=[Path(__file__),ROOT/'lib/moving_mesh.py']
    data['source_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in paths}
    (base/'route1_dlw_gate.json').write_text(json.dumps(data,indent=2,
        allow_nan=False),encoding='utf-8')


if __name__=='__main__':main()
