"""Audit the frozen CN revision; original evidence and notebooks remain untouched."""
import ast
import hashlib
import json
import pathlib
import re
import time

import numpy as np

BASE=pathlib.Path(__file__).resolve().parent
SNAPSHOT=BASE/'DLW数值分析report.ipynb'
nb=json.loads(SNAPSHOT.read_text(encoding='utf-8'))
hash_value=hashlib.sha256(SNAPSHOT.read_bytes()).hexdigest()
assert hash_value=='1061f774c69dc1e3dfc1dd0f1bd6f9510f66760fda635a02fd342746db508635'
ns={'display':lambda *args,**kwargs:None}
for number in (2,4,6,8,9,11,13,14,16,18,20):
    source=''.join(nb['cells'][number-1]['source']).replace('from IPython.display import display','# display shim')
    exec(compile(source,f'CN snapshot cell {number}','exec'),ns)

prior_numbered=(BASE.parent/'notebook_source_numbered.txt').read_text(encoding='utf-8')
prior_sources={}
chunks=re.split(r'(?m)^CELL (\d+) (markdown|code)\n',prior_numbered)
for i in range(1,len(chunks),3):
    prior_sources[int(chunks[i])]=re.sub(r'(?m)^\d{4} ','',chunks[i+2]).rstrip()
changes=[i+1 for i,c in enumerate(nb['cells']) if ''.join(c['source']).rstrip()!=prior_sources[i+1]]
old_step=ast.parse(prior_sources[20]).body[0]
new_step=ast.parse(''.join(nb['cells'][19]['source'])).body[0]
baseline_same=(ast.dump(old_step.body[0])==ast.dump(new_step.body[0]) and
    [ast.dump(s) for s in old_step.body[1:]]==[ast.dump(s) for s in new_step.body[3:]])
evidence=dict(sha256=hash_value,source_changed_cells=changes,
    euler_rk4_step_bodies_unchanged=baseline_same,
    prior_evidence_reused='../numerical_checks.json: default 27 Euler/RK4 runs and 108 table values')

started=time.perf_counter()
records={}
main=[]
for case in ns['CASES']:
    for model in ns['MODELS']:
        result=ns['solve'](case,model,'CN','fixed',ns['CONFIG'])
        records[case,model]=result
        diagnostics=result['cn_diagnostics']
        main.append(dict(case=case,model=model,method='CN',mesh='fixed',
            completed=bool(result['completed']),reached=result['reached'],reason=result['reason'],
            initial_error=result['initial_error'],max_errors=result['max_errors'],min_J=result['min_J'],
            step_count=len(diagnostics),max_iterations=max(d['iterations'] for d in diagnostics),
            max_residual=max(d['residual'] for d in diagnostics),
            max_tolerance=max(d['tolerance'] for d in diagnostics),
            max_residual_to_tolerance=max(d['residual']/d['tolerance'] for d in diagnostics),
            all_diagnostics=diagnostics))
evidence['cn_default_9_runs']=main

prior=json.loads((BASE.parent/'numerical_checks.json').read_text(encoding='utf-8'))
prior_records={(r['case'],r['model'],r['method'],r['mesh']):r for r in prior['main_27_runs']}
html=next(''.join(o['data']['text/html']) for o in nb['cells'][23]['outputs'] if 'text/html' in o.get('data',{}))
stored={(int(row),int(col)):value.strip() for row,col,value in re.findall(r'<td\s+id="[^"]*_row(\d+)_col(\d+)"[^>]*>([^<]+)</td>',html)}
actual={}
for row,(case,model,field) in enumerate((case,model,field) for case in ns['CASES'] for model in ns['MODELS'] for field in ('u','v')):
    for col,method in enumerate(('Euler','RK4','CN')):
        result=records[case,model] if method=='CN' else prior_records[case,model,method,'fixed']
        actual[row,col]=f"{result['max_errors'][field]:.3e}"
evidence['saved_new_time_table']=dict(numeric_entries=len(stored),
    mismatches=[dict(row=key[0],column=key[1],saved=value,recomputed=actual.get(key)) for key,value in stored.items() if actual.get(key)!=value])
evidence['saved_cell30_stdout']=''.join(''.join(o.get('text',[])) for o in nb['cells'][29]['outputs'])
evidence['clean_execution_main_count']=len(prior_records)+len(records)

# A nonlinear equation distinguishes trapezoidal CN from implicit midpoint.
scalar=ns['step'](lambda t,y:y*y,0.,np.array([1.]),.1,'CN')
trapezoid=(1-np.sqrt(1-2*.1*(1+.1/2)))/.1
# Solve y1 = 1 + .1*((1+y1)/2)**2 via independent quadratic roots.
midpoint=np.roots([.1/4,.1/2-1,1+.1/4])
midpoint=float(min(midpoint))
evidence['nonlinear_scalar_formula']=dict(computed=float(scalar[0]),
    exact_trapezoid_root=float(trapezoid),error=float(abs(scalar[0]-trapezoid)),
    midpoint_root=midpoint,difference_from_midpoint=float(abs(scalar[0]-midpoint)),
    diagnostic=dict(ns['step'].cn_last))

# Stiff decaying test: CN is well-defined here, but unpreconditioned Picard diverges.
stiff=[]
for dt in (.0005,.01):
    try:
        value=ns['step'](lambda t,y:-1000*y,0.,np.array([1.]),dt,'CN')
        completed=True; reason=''; output=float(value[0]); diagnostic=dict(ns['step'].cn_last)
    except ValueError as exc:
        completed=False; reason=str(exc); output=None; diagnostic=None
    exact_factor=(1-1000*dt/2)/(1+1000*dt/2)
    stiff.append(dict(dt=dt,completed=completed,reason=reason,value=output,
        exact_cn_factor=exact_factor,picard_contraction_factor=abs(1000*dt/2),diagnostic=diagnostic))
evidence['fixed_point_solver_stiff_limit']=stiff

# Independent second-order self convergence at unchanged spatial resolution.
orders=[]
for model in ('SD','SD2','FD'):
    runs=[records['C',model]]
    for divisor in (2,4):
        runs.append(ns['solve']('C',model,'CN','fixed',dict(ns['CONFIG'],dt=ns['CONFIG']['dt']/divisor)))
    field_orders=[]
    for fi,name in enumerate(('u','v')):
        d1=float(abs(runs[0]['fields'][fi]-runs[1]['fields'][fi]).max())
        d2=float(abs(runs[1]['fields'][fi]-runs[2]['fields'][fi]).max())
        field_orders.append(dict(field=name,difference_dt_half=d1,difference_half_quarter=d2,order=float(np.log2(d1/d2))))
    orders.append(dict(case='C',model=model,completed=[bool(r['completed']) for r in runs],orders=field_orders))
evidence['cn_time_self_convergence']=orders

# One bounded moving solve per model exercises endpoint grid/state evaluation.
moving=[]
for model in ns['MODELS']:
    result=ns['solve']('C',model,'CN','moving',dict(ns['CONFIG'],T=ns['CONFIG']['dt']*4))
    moving.append(dict(case='C',model=model,completed=bool(result['completed']),reached=result['reached'],
        reason=result['reason'],min_J=result['min_J'],max_errors=result['max_errors'],
        diagnostics=result['cn_diagnostics']))
evidence['bounded_cn_moving_checks']=moving
evidence['elapsed_seconds']=time.perf_counter()-started
(BASE/'cn_evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf-8')
(BASE/'notebook_source_numbered.txt').write_text('\n\n'.join('CELL '+str(i+1)+' '+c['cell_type']+'\n'+''.join(f'{j+1:04d} {x}' for j,x in enumerate(''.join(c['source']).splitlines(True))) for i,c in enumerate(nb['cells'])),encoding='utf-8')
print(json.dumps({k:v for k,v in evidence.items() if k!='cn_default_9_runs'},ensure_ascii=False,indent=2))
print('CN main summaries',json.dumps([{k:v for k,v in r.items() if k!='all_diagnostics'} for r in main],ensure_ascii=False,indent=2))
