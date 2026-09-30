"""Check every quantitative claim used in the local-advantage report."""
import json
from pathlib import Path

OUT=Path(__file__).resolve().parent/'out'
read=lambda name:json.loads((OUT/name).read_text())
mesh=read('local_advantage.json')['rows']
box=read('local_neighborhood.json')['comparisons']
time=read('local_time_comparison.json')['rows']
coarse=read('coarse_time_advantage.json')['rows']
rich=read('richardson_model.json')['rows']
model_data=read('model_factor.json')
factor=model_data['rows']
keys=('u_linf','rho_linf','u_core_linf','rho_core_linf',
      'u_common_linf','rho_common_linf','u_common_core_linf','rho_common_core_linf')
matched=[]
for row in mesh:
    if row['gamma']!=2: continue
    base=next(r for r in mesh if r['p']==row['p'] and r['n']==row['n']
              and r['T']==row['T'] and r['gamma']==0)
    matched.append((base,row))
assert len(matched)==18 and all(base[k]>adapt[k] for base,adapt in matched for k in keys)
assert len(box)==27 and all(row[k+'_gain']>1 for row in box for k in keys)
center=next((b,a) for b,a in matched if a['p']==5 and a['n']==201 and a['T']==.25)
assert center[0]['u_linf']/center[1]['u_linf']>8.6
assert center[0]['rho_linf']/center[1]['rho_linf']>4.7
for p in (4.5,5.,5.5):
    for a in (.01,.02,.03):
        for T in (.25,.5,1.):
            a4=next(r for r in time if (r['p'],r['a'],r['T'],r['method'])==(p,a,T,'rk4'))
            a8=next(r for r in time if (r['p'],r['a'],r['T'],r['method'])==(p,a,T,'rk8'))
            assert a8['u_solve']<a4['u_solve'] and a8['rho_solve']<a4['rho_solve']
assert len(rich)==27 and all(r['u_extrap']<r['u_fine'] and r['rho_extrap']<r['rho_fine'] for r in rich)
assert len(factor)==48 and len(model_data['c_scan'])==3
for p in (4.5,5.,5.5):
    for a in (.01,.02,.03):
        r4=next(r for r in coarse if (r['p'],r['a'],r['method'])==(p,a,'rk4'))
        r8=next(r for r in coarse if (r['p'],r['a'],r['method'])==(p,a,'rk8'))
        assert r8['u_total']<r4['u_total']
print('PASS: 18 broad mesh pairs, 27 neighborhood pairs, 27 time pairs, '
      '27 Richardson pairs, 48 model-factor cases plus 3 c cases, 9 coarse-time u pairs')
