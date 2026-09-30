"""Freeze fixed-grid recommendations using analytic finite-h fields and t=0 defects.

No trajectory for a held-out H case is read or advanced by this script.
"""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'lib'))
from parametric import Parameters, Exact
from parametric_open import OpenModel

OUT=ROOT/'out/injection_amplification'
OUT.mkdir(parents=True,exist_ok=True)
HOLDOUT={
 'H1':Parameters(a=4.5,p=.9,q=2.6,rho=2.2),
 'H2':Parameters(a=3.2,p=1.2,q=2.2,rho=3.7),
 'H3':Parameters(a=2.3,p=1.65,q=2.4,rho=3.4),
 'H4':Parameters(a=5.2,p=.65,q=1.2,rho=2.),
}
H_GRID=(.125,.0625,.03125)
NX_GRID=(128,256)
TARGET_REL=.001
T=.01
DT=.00025
FACTOR=1.5


def inf(x):return float(np.max(np.abs(x)))


def features(pars,h,nx):
    m=OpenModel(pars,h,nx)
    ref=Exact(pars,h)
    amp=[inf(x) for x in ref.uv(m.js,m.X.x,0.)]
    finite=ref.uv(m.js,m.X.x,T)
    cont=Exact(pars,h,continuous=True).uv(m.js,m.X.x,T)
    model=[inf(a-b) for a,b in zip(finite,cont)]
    r=m.rhs(0,m.exact(0))-m.exact(0,True)
    injection=[inf(x) for x in m.error_fields(r)]
    prediction=[model[i]+FACTOR*T*injection[i] for i in range(2)]
    normalized=[prediction[i]/(TARGET_REL*amp[i]) for i in range(2)]
    return {'h':h,'nx':nx,'amplitude':amp,'model_error':model,
            'initial_output_defect':injection,'predicted_conservative_error':prediction,
            'predicted_target_ratio':normalized,
            'pass':max(normalized)<=1,
            'work_units':int(round(T/DT))*nx*(2*round(1.5/h)-1)}


def main():
    rows=[]
    for name,pars in HOLDOUT.items():
        candidates=[features(pars,h,nx) for h in H_GRID for nx in NX_GRID]
        feasible=[x for x in candidates if x['pass']]
        choice=min(feasible,key=lambda x:(x['work_units'],x['h']!=.125,x['nx'])) if feasible else None
        rows.append({'case':name,'parameters':vars(pars),'candidates':candidates,
                     'chosen':{'h':choice['h'],'nx':choice['nx']} if choice else None})
    data={'frozen_rule':'Use finite-h analytic model difference plus 1.5*T*initial physical-output defect; select least-work candidate passing both fields.',
          'scope':'SD, extrapolated open y closure, periodic x, L=20, yhalf=1.5; no nx>256 without separate growth pilot',
          'target_T':T,'target_relative_per_field':TARGET_REL,'dt':DT,
          'injection_factor':FACTOR,'factor_basis':'P1/P5/P6/P10 nx=128 and P1/P6/P10 nx=256; excludes known P5 nx=256/512 high-gain failure; 1.5 exceeds all remaining observed ratios',
          'cost_proxy':'number of RK4 steps times nx times number of state rows; excludes diagnostic and setup work',
          'held_out':rows,
          'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in [Path(__file__),ROOT/'lib/parametric.py',ROOT/'lib/parametric_open.py']}}
    path=OUT/'locked_rule.json'
    path.write_text(json.dumps(data,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print('LOCKED',hashlib.sha256(path.read_bytes()).hexdigest(),flush=True)
    for row in rows:print(row['case'],row['chosen'],flush=True)


if __name__=='__main__':main()
