"""Reproduce an SD2 final-step positivity omission without changing the notebook."""
import json
import pathlib

import numpy as np

root=pathlib.Path(__file__).resolve().parent
notebook=json.loads(pathlib.Path(r'C:\Users\msz\aca\notebook\DLW数值分析report.ipynb').read_text(encoding='utf-8'))
ns={'display':lambda *args,**kwargs:None}
for number in (2,4,6,8,9,11,13,14,16,18,20):
    source=''.join(notebook['cells'][number-1]['source']).replace('from IPython.display import display','# display shim')
    exec(compile(source,f'cell {number}','exec'),ns)

results=[]
for dt in (.01,.1,.5,1.,2.):
    cfg=dict(ns['CONFIG'],dt=dt,T=dt)
    p=ns['Problem']('A','SD2','fixed',cfg)
    state=p.initial()
    candidate=ns['step'](p.stage,0.,state,dt,'Euler')
    q,r=p.m.unpack(candidate[:-p.X.n],dt)
    record=ns['solve']('A','SD2','Euler','fixed',cfg)
    results.append(dict(dt=dt,min_final_q=float(q.min()),max_abs_final_state=float(abs(candidate).max()),
        completed=bool(record['completed']),reached=record['reached'],reason=record['reason'],max_errors=record['max_errors'],
        min_J=record['min_J']))
out=root/'final_state_guard.json'
out.write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(out.read_text(encoding='utf-8'))
