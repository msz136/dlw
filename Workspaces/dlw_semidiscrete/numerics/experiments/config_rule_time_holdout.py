"""Second, independently locked target-time challenge for the same rule.

Run with 'lock' before 'verify'. The verify mode never rewrites the lock.
"""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'lib'))
from parametric import Parameters
import config_rule_lock as rule
from config_rule_validate import advance

OUT=ROOT/'out/injection_amplification'
PARS={
 'H5':Parameters(a=3.7,p=.85,q=2.35,rho=3.),
 'H6':Parameters(a=2.7,p=1.35,q=2.55,rho=3.3),
}
TARGET_T=.02


def lock():
    rule.T=TARGET_T
    rows=[]
    for name,pars in PARS.items():
        candidates=[rule.features(pars,h,nx) for h in rule.H_GRID for nx in rule.NX_GRID]
        feasible=[c for c in candidates if c['pass']]
        choice=min(feasible,key=lambda c:(c['work_units'],c['h']!=.125,c['nx'])) if feasible else None
        rows.append({'case':name,'parameters':vars(pars),'candidates':candidates,
                     'chosen':{'h':choice['h'],'nx':choice['nx']} if choice else None})
    data={'base_rule_sha256':hashlib.sha256((OUT/'locked_rule.json').read_bytes()).hexdigest(),
          'T':TARGET_T,'relative_target':rule.TARGET_REL,'dt':rule.DT,
          'factor':rule.FACTOR,'same_rule':'analytic model difference + 1.5*T*initial output defect; least work passing both fields',
          'cases':rows,'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
               for p in [Path(__file__),ROOT/'experiments/config_rule_lock.py',
                         ROOT/'lib/parametric.py',ROOT/'lib/parametric_open.py']}}
    path=OUT/'locked_time_rule.json'
    path.write_text(json.dumps(data,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print('TIME LOCKED',hashlib.sha256(path.read_bytes()).hexdigest(),flush=True)
    for x in rows:print(x['case'],x['chosen'],flush=True)


def verify():
    path=OUT/'locked_time_rule.json'
    data=json.loads(path.read_text(encoding='utf-8'))
    assert data['base_rule_sha256']==hashlib.sha256((OUT/'locked_rule.json').read_bytes()).hexdigest()
    rows=[]
    for case in data['cases']:
        pars=Parameters(**case['parameters'])
        trials=[]
        for candidate in case['candidates']:
            h,nx=candidate['h'],candidate['nx']
            actual=advance(pars,h,nx,data['T'],data['dt'])
            if actual['complete']:
                ratio=[actual['total'][i]/(data['relative_target']*candidate['amplitude'][i]) for i in range(2)]
                actual['observed_target_ratio']=ratio
                actual['observed_pass']=max(ratio)<=1
                actual['predicted_upper_violations']=[actual['total'][i]>candidate['predicted_conservative_error'][i] for i in range(2)]
            trials.append({'h':h,'nx':nx,'predicted_pass':candidate['pass'],**actual})
            print(case['case'],h,nx,'pred',candidate['pass'],'actual',actual.get('observed_target_ratio'),flush=True)
        rows.append({'case':case['case'],'chosen':case['chosen'],'runs':trials})
        (OUT/'time_holdout.json').write_text(json.dumps({'locked_time_rule_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                                                          'results':rows},indent=2,allow_nan=False)+'\n',encoding='utf-8')
    data={'locked_time_rule_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
          'results':rows,'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in [Path(__file__),ROOT/'experiments/config_rule_validate.py',
                      ROOT/'lib/parametric.py',ROOT/'lib/parametric_open.py']}}
    (OUT/'time_holdout.json').write_text(json.dumps(data,indent=2,allow_nan=False)+'\n',encoding='utf-8')


if __name__=='__main__':
    if len(sys.argv)!=2 or sys.argv[1] not in ('lock','verify'):
        raise SystemExit('usage: config_rule_time_holdout.py lock|verify')
    {'lock':lock,'verify':verify}[sys.argv[1]]()
