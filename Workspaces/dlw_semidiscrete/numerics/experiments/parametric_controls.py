"""Finite-h exact-family evolution, time-step control, and boundary-domain control."""
from parametric_study import PARAMS,save,diagnostics,inf
from parametric import Model,rk4
from dataclasses import asdict
import numpy as np


def run(pars,h=.25,nx=256,dt=.000125,continuous=False,model='structure',closure='original',yhalf=1.5,T=.005):
    m=Model(pars,h,nx,model=model,closure=closure,continuous=continuous,yhalf=yhalf)
    z=m.exact(0);lin=np.zeros_like(z)
    for i in range(round(T/dt)):
        def forced(t,e):
            bg=m.exact(t)
            return m.delta(t,bg,e,True)+m.rhs(t,bg)-m.exact(t,True)
        z=rk4(m.rhs,i*dt,z,dt);lin=rk4(forced,i*dt,lin,dt)
    assert np.all(np.isfinite(z))
    return {'pars':asdict(pars),'h':h,'nx':nx,'dt':dt,'continuous':continuous,'model':model,'closure':closure,'yhalf':yhalf,
            'result':diagnostics(m,T,z,lin)}


def main():
    rows=[run(p,h) for p in PARAMS for h in (.25,.125,.0625)]
    save('parametric_finite_h',rows)
    controls=[]
    for pars in (PARAMS[0],PARAMS[1],PARAMS[-1]):
        for model in ('structure','fd'):
            for dt in (.000125,.0000625):
                controls.append(run(pars,dt=dt,continuous=True,model=model))
            controls.append(run(pars,continuous=True,model=model,yhalf=2.5))
    save('parametric_time_domain_controls',controls)
    print('finite-h',len(rows),'time/domain',len(controls),flush=True)

if __name__=='__main__':main()
