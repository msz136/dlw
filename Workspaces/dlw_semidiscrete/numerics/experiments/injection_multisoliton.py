"""Transfer finite-h injection/propagation diagnostic to local N=2 windows."""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'lib'))
from parametric import rk4
from manifold_scattering import ManifoldModel
from injection_amplification import norm, outputs, tangent_step, split_rows

OUT=ROOT/'out/injection_amplification'


def run(p,q,rho,t0,nx=256,h=.25,T=.005,dt=.00025):
    m=ManifoldModel(p,q,rho,h,nx)
    z=m.exact(t0)
    lin=np.zeros_like(z)
    edge=np.zeros_like(z)
    core=np.zeros_like(z)
    raw=np.zeros_like(z)
    sums=np.zeros((3,2))
    n=round(T/dt)
    for k in range(n):
        t=t0+k*dt
        bar=m.exact(t)
        step,prop=tangent_step(m,t,bar,dt,(lin,edge,core))
        b=step-m.exact(t+dt)
        be,bc=split_rows(m,b)
        lin,edge,core=(prop[0]+b,prop[1]+be,prop[2]+bc)
        raw+=b
        for i,x in enumerate((b,be,bc)):sums[i]+=outputs(m,x)
        z=rk4(m.rhs,t,z,dt)
        if not np.all(np.isfinite(z)) or norm(z)>1e3:
            return {'complete':False,'stopped_step':k+1}
    actual=z-m.exact(t0+T)
    return {'complete':True,'u_v_error':outputs(m,actual),'linear_response':outputs(m,lin),
            'nonlinear_remainder':outputs(m,actual-lin),'raw_injection':outputs(m,raw),
            'absolute_injections':sums.tolist(),'edge_response':outputs(m,edge),
            'interior_response':outputs(m,core),
            'linear_to_raw_injection':(np.array(outputs(m,lin))/np.maximum(outputs(m,raw),1e-30)).tolist(),
            'initial_defect':outputs(m,m.rhs(t0,m.exact(t0))-m.exact(t0,True))}


def main():
    p,q,r=[1.,2.],[1.,3.],[3.,4.]
    configs=[('N2_separated_before',p,q,r,-4.,256),
             ('N2_overlap',p,q,r,0.,256),
             ('N2_separated_after',p,q,r,4.,256),
             ('N2_overlap_fine_x',p,q,r,0.,512),
             ('matched_N1_before',[2.],[3.],[4./6.],-4.,256),
             ('matched_N1_after',[2.],[3.],[4.],4.,256)]
    rows=[]
    for label,pp,qq,rr,t,nx in configs:
        row={'label':label,'p':pp,'q':qq,'rho':rr,'t0':t,'nx':nx,
             **run(pp,qq,rr,t,nx)}
        rows.append(row)
        print(label,row.get('u_v_error'),row.get('linear_to_raw_injection'),flush=True)
    data={'scope':'independent finite-h exact starts for each short local window; no full collision claim',
          'h':.25,'duration':.005,'dt':.00025,'results':rows,
          'source_sha256':{str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest()
             for x in [Path(__file__),ROOT/'experiments/manifold_scattering.py',
                       ROOT/'experiments/injection_amplification.py',
                       ROOT/'lib/soliton_expansion.py']}}
    (OUT/'multisoliton.json').write_text(json.dumps(data,indent=2,allow_nan=False)+'\n',encoding='utf-8')


if __name__=='__main__':main()
