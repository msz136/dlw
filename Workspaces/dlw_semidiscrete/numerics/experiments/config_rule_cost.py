"""Measure the already-locked selector's feature-evaluation overhead.

This imports the frozen feature function but never rewrites locked_rule.json.
"""
from pathlib import Path
import hashlib
import json
import sys
import time
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'lib'))
from parametric import Parameters
from config_rule_lock import features

OUT=ROOT/'out/injection_amplification'


def main():
    locked=json.loads((OUT/'locked_rule.json').read_text(encoding='utf-8'))
    held=json.loads((OUT/'holdout.json').read_text(encoding='utf-8'))
    rows=[]
    for entry in locked['held_out']:
        name=entry['case'];pars=Parameters(**entry['parameters'])
        times=[]
        for _ in range(3):
            start=time.perf_counter()
            computed=[features(pars,c['h'],c['nx']) for c in entry['candidates']]
            times.append(time.perf_counter()-start)
            for a,b in zip(computed,entry['candidates']):
                assert max(abs(np.array(a['predicted_target_ratio'])-b['predicted_target_ratio']))<1e-12
        result=next(x for x in held['results'] if x['case']==name)
        selected=next(x for x in result['runs'] if x['h']==entry['chosen']['h'] and x['nx']==entry['chosen']['nx'])
        baseline=next(x for x in result['runs'] if x['h']==.125 and x['nx']==128)
        med=float(np.median(times))
        rows.append({'case':name,'feature_seconds':times,'feature_median_seconds':med,
                     'selected_advance_median_seconds':selected['median_seconds'],
                     'baseline_advance_median_seconds':baseline['median_seconds'],
                     'selector_plus_selected_to_baseline_advance_ratio':(med+selected['median_seconds'])/baseline['median_seconds']})
        print(name,'feature',med,'all-in/base',rows[-1]['selector_plus_selected_to_baseline_advance_ratio'],flush=True)
    data={'locked_rule_sha256':hashlib.sha256((OUT/'locked_rule.json').read_bytes()).hexdigest(),
          'scope':'3 sequential repeats; six analytic/defect features per case; excludes process startup and reporting',
          'rows':rows,
          'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in [Path(__file__),ROOT/'experiments/config_rule_lock.py',
                                     ROOT/'lib/parametric.py',ROOT/'lib/parametric_open.py']}}
    (OUT/'rule_cost.json').write_text(json.dumps(data,indent=2,allow_nan=False)+'\n',encoding='utf-8')


if __name__=='__main__':main()
