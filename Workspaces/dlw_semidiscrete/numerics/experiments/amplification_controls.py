"""Focused P5 high-frequency growth and time-step controls."""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'lib'))
from parametric import Parameters, rk4
from parametric_open import OpenModel
from injection_amplification import norm, tangent_step

OUT=ROOT/'out/injection_amplification'


def run(nx,dt):
    pars=Parameters(p=.5,q=1.,rho=1.5)
    m=OpenModel(pars,.125,nx)
    z=m.exact(0)
    lin=np.zeros_like(z)
    records=[]
    n=round(.01/dt)
    for k in range(n):
        t=k*dt
        bar=m.exact(t)
        step,[prop]=tangent_step(m,t,bar,dt,(lin,))
        lin=prop+step-m.exact(t+dt)
        z=rk4(m.rhs,t,z,dt)
        if (k+1)%(n//5)==0:
            tt=(k+1)*dt
            err=z-m.exact(tt)
            u,v=m.error_fields(err)
            ul,vl=m.error_fields(lin)
            fft=np.fft.rfft(u,axis=-1)
            high=fft[:,max(1,len(fft[0])//2):]
            records.append({'t':tt,'actual':[norm(u),norm(v)],
                            'linear':[norm(ul),norm(vl)],
                            'u_high_half_fft_max':norm(high),
                            'u_full_fft_max':norm(fft)})
    # Check the full RK4 tangent separately by symmetric differences.
    z0=m.exact(0)
    rng=np.random.default_rng(230923)
    direction=rng.normal(size=z0.size)
    direction/=norm(direction)
    _,[tangent]=tangent_step(m,0,z0,dt,(direction,))
    eps=1e-5
    fd=(rk4(m.rhs,0,z0+eps*direction,dt)-rk4(m.rhs,0,z0-eps*direction,dt))/(2*eps)
    return {'nx':nx,'dt':dt,'records':records,'tangent_fd_residual':norm(fd-tangent)}


def main():
    runs=[]
    for nx,dt in ((256,.00025),(384,.00025),(512,.00025),(512,.000125)):
        row=run(nx,dt)
        runs.append(row)
        print(nx,dt,row['records'][-1],flush=True)
    data={'runs':runs,'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
          for p in [Path(__file__),ROOT/'experiments/injection_amplification.py',
                    ROOT/'lib/parametric.py',ROOT/'lib/parametric_open.py']}}
    (OUT/'p5_controls.json').write_text(json.dumps(data,indent=2,allow_nan=False)+'\n',encoding='utf-8')


if __name__=='__main__':main()
