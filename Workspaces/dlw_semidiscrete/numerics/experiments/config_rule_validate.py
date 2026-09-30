"""Advance all pre-registered held-out configurations after rule lock."""
from pathlib import Path
import hashlib
import json
import sys
import time
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'lib'))
from parametric import Parameters, Exact, rk4
from parametric_open import OpenModel

OUT=ROOT/'out/injection_amplification'


def inf(x):return float(np.max(np.abs(x)))


def advance(pars,h,nx,T,dt):
    m=OpenModel(pars,h,nx)
    z=m.exact(0)
    n=round(T/dt)
    assert abs(T-n*dt)<1e-12
    start=time.perf_counter()
    for k in range(n):
        z=rk4(m.rhs,k*dt,z,dt)
        if not np.all(np.isfinite(z)) or inf(z)>1e3:
            return {'complete':False,'stopped_step':k+1,'seconds':time.perf_counter()-start}
    seconds=time.perf_counter()-start
    numerical=m.fields(z,T)
    finite=Exact(pars,h).uv(m.js,m.X.x,T)
    continuous=Exact(pars,h,continuous=True).uv(m.js,m.X.x,T)
    solver=[inf(a-b) for a,b in zip(numerical,finite)]
    total=[inf(a-b) for a,b in zip(numerical,continuous)]
    return {'complete':True,'seconds':seconds,'solver':solver,'total':total,
            'model':[inf(a-b) for a,b in zip(finite,continuous)],
            'decomposition_residual':max(inf((a-c)-(a-b)-(b-c))
                                         for a,b,c in zip(numerical,finite,continuous))}


def main():
    raw=(OUT/'locked_rule.json').read_bytes()
    locked=json.loads(raw)
    lock_hash=hashlib.sha256(raw).hexdigest()
    rows=[]
    for case in locked['held_out']:
        pars=Parameters(**case['parameters'])
        chosen=case['chosen']
        trials=[]
        for candidate in case['candidates']:
            h,nx=candidate['h'],candidate['nx']
            actual=advance(pars,h,nx,locked['target_T'],locked['dt'])
            if actual['complete']:
                ratios=[actual['total'][i]/(locked['target_relative_per_field']*candidate['amplitude'][i])
                        for i in range(2)]
                actual['observed_target_ratio']=ratios
                actual['observed_pass']=max(ratios)<=1
                actual['predicted_upper_violations']=[actual['total'][i]>candidate['predicted_conservative_error'][i]
                                                      for i in range(2)]
            trials.append({'h':h,'nx':nx,'predicted_pass':candidate['pass'],**actual})
            print(case['case'],h,nx,'pred',candidate['pass'],'actual',actual.get('observed_target_ratio'),flush=True)
        selected=next(r for r in trials if r['h']==chosen['h'] and r['nx']==chosen['nx'])
        baseline=next(r for r in trials if r['h']==.125 and r['nx']==128)
        # Two further independent wall-clock measurements, with the first run above.
        for target in (selected,baseline):
            target['timing_repeats']=[target['seconds']]
            for _ in range(2):
                again=advance(pars,target['h'],target['nx'],locked['target_T'],locked['dt'])
                assert again['complete'] and max(abs(np.array(again['total'])-target['total']))<1e-12
                target['timing_repeats'].append(again['seconds'])
            target['median_seconds']=float(np.median(target['timing_repeats']))
        rows.append({'case':case['case'],'chosen':chosen,'runs':trials,
                     'selected_to_baseline_work_ratio':next(c['work_units'] for c in case['candidates'] if c['h']==chosen['h'] and c['nx']==chosen['nx'])/case['candidates'][0]['work_units'],
                     'selected_to_baseline_median_seconds':selected['median_seconds']/baseline['median_seconds']})
        (OUT/'holdout.json').write_text(json.dumps({'locked_rule_sha256':lock_hash,'results':rows},indent=2,allow_nan=False)+'\n',encoding='utf-8')
    data={'locked_rule_sha256':lock_hash,'results':rows,
          'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in [Path(__file__),ROOT/'lib/parametric.py',ROOT/'lib/parametric_open.py']}}
    (OUT/'holdout.json').write_text(json.dumps(data,indent=2,allow_nan=False)+'\n',encoding='utf-8')


if __name__=='__main__':main()
