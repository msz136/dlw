"""Separate accepted residual size from observed CN time order."""
from collections import Counter
import json
import pathlib

import numpy as np

base=pathlib.Path(__file__).resolve().parent
nb=json.loads((base/'DLW数值分析report.ipynb').read_text(encoding='utf-8'))
ns={'display':lambda *args,**kwargs:None}
for number in (2,4,6,8,9,11,13,14,16,18,20):
    source=''.join(nb['cells'][number-1]['source']).replace('from IPython.display import display','# display shim')
    exec(compile(source,f'cell {number}','exec'),ns)
actual_step=ns['step']

def strict_step(fun,t,state,dt,method):
    if method!='CN':
        return actual_step(fun,t,state,dt,method)
    f0=fun(t,state)
    candidate=state+dt*f0
    tolerance=1e-15+1e-14*max(1.,float(abs(state).max()))
    for iteration in range(1,81):
        residual=candidate-state-dt*(f0+fun(t+dt,candidate))/2
        size=float(abs(residual).max())
        # Three evaluations include two Picard corrections of the Euler predictor.
        if iteration>=3 and size<=tolerance:
            strict_step.cn_last=dict(iterations=iteration,residual=size,tolerance=tolerance)
            return candidate
        candidate-=residual
    raise ValueError('strict tolerance did not converge')

results=[]
for mode in ('actual','tight_tol_min3'):
    ns['step']=actual_step if mode=='actual' else strict_step
    for model in ('SD','SD2','FD'):
        records=[]
        summary=[]
        for divisor in (1,2,4):
            cfg=dict(ns['CONFIG'],dt=ns['CONFIG']['dt']/divisor)
            record=ns['solve']('C',model,'CN','fixed',cfg)
            records.append(record)
            hist=Counter(d['iterations'] for d in record['cn_diagnostics'])
            summary.append(dict(divisor=divisor,dt=cfg['dt'],steps=len(record['cn_diagnostics']),iteration_histogram=dict(hist),
                max_residual=max(d['residual'] for d in record['cn_diagnostics']),
                max_tolerance=max(d['tolerance'] for d in record['cn_diagnostics'])))
        field_orders=[]
        for fi,name in enumerate(('u','v')):
            d1=float(abs(records[0]['fields'][fi]-records[1]['fields'][fi]).max())
            d2=float(abs(records[1]['fields'][fi]-records[2]['fields'][fi]).max())
            field_orders.append(dict(field=name,d1=d1,d2=d2,order=float(np.log2(d1/d2))))
        out=dict(mode=mode,model=model,refinement_diagnostics=summary,field_orders=field_orders)
        if mode=='actual':
            cfg=dict(ns['CONFIG'],dt=ns['CONFIG']['dt']/4)
            euler=ns['solve']('C',model,'Euler','fixed',cfg)
            out['quarter_dt_difference_from_euler']={field:float(abs(records[-1]['fields'][i]-euler['fields'][i]).max()) for i,field in enumerate(('u','v'))}
            p=ns['Problem']('C',model,'fixed',cfg)
            state=p.initial()
            c=actual_step(p.stage,0.,state,cfg['dt'],'CN')
            e=actual_step(p.stage,0.,state,cfg['dt'],'Euler')
            out['first_quarter_step_difference_from_euler']=float(abs(c-e).max())
            out['first_quarter_step_cn_diagnostic']=dict(actual_step.cn_last)
        results.append(out)
(base/'cn_tolerance_evidence.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(results,ensure_ascii=False,indent=2))
