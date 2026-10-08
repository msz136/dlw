"""Pair the existing refinement evidence with only a 1000x tighter tolerance."""
import json
import pathlib
from collections import Counter

import numpy as np

base=pathlib.Path(__file__).resolve().parent
nb=json.loads((base/'DLW数值分析report.ipynb').read_text(encoding='utf-8'))
ns={'display':lambda *args,**kwargs:None}
for number in (2,4,6,8,9,11,13,14,16,18,20):
    source=''.join(nb['cells'][number-1]['source']).replace('from IPython.display import display','# display shim')
    exec(compile(source,f'cell {number}','exec'),ns)

# Tiny scalar step makes the premature Euler-predictor acceptance explicit.
state=np.array([1.])
dt=1e-6
value=ns['step'](lambda t,y:y,0.,state,dt,'CN')
scalar=dict(dt=dt,value=float(value[0]),euler_value=1+dt,
    exact_cn_value=(1+dt/2)/(1-dt/2),difference_from_euler=float(value[0]-(1+dt)),
    diagnostic=dict(ns['step'].cn_last))

step_source=''.join(nb['cells'][19]['source']).split('\ndef solve',1)[0]
replacement=step_source.replace('1e-12+1e-11','1e-15+1e-14')
assert replacement!=step_source
assert replacement.replace('1e-15+1e-14','1e-12+1e-11')==step_source
exec(compile(replacement,'step with tolerance literals only tightened','exec'),ns)

tight=[]
for model in ns['MODELS']:
    records=[]
    summaries=[]
    for divisor in (1,2,4):
        cfg=dict(ns['CONFIG'],dt=ns['CONFIG']['dt']/divisor)
        record=ns['solve']('C',model,'CN','fixed',cfg)
        records.append(record)
        summaries.append(dict(divisor=divisor,steps=len(record['cn_diagnostics']),
            iteration_histogram=dict(Counter(d['iterations'] for d in record['cn_diagnostics'])),
            max_residual=max(d['residual'] for d in record['cn_diagnostics'])))
    orders=[]
    for fi,name in enumerate(('u','v')):
        d1=float(abs(records[0]['fields'][fi]-records[1]['fields'][fi]).max())
        d2=float(abs(records[1]['fields'][fi]-records[2]['fields'][fi]).max())
        orders.append(dict(field=name,d1=d1,d2=d2,order=float(np.log2(d1/d2))))
    tight.append(dict(model=model,refinement_diagnostics=summaries,field_orders=orders))

old=json.loads((base/'cn_tolerance_evidence.json').read_text(encoding='utf-8'))
evidence=dict(only_tolerance_literals_changed=True,
    actual_tolerance='1e-12 + 1e-11 * max(1, max(abs(state)))',
    tightened_tolerance='1e-15 + 1e-14 * max(1, max(abs(state)))',
    actual_refinement=[r for r in old if r['mode']=='actual'],
    tightened_refinement=tight,scalar_euler_predictor_acceptance=scalar)
(base/'cn_tolerance_pure_evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(evidence,ensure_ascii=False,indent=2))
