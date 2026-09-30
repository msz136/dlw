"""Dense parameter-box probe around the observed moving-grid advantage."""
import json
from pathlib import Path
from local_advantage_study import run_case

ROOT=Path(__file__).resolve().parent
rows=[]
for p in (4.9,5.,5.1):
    for T in (.2,.25,.3):
        for gamma in (0.,1.5,2.,2.5):
            rows.append(run_case(p,201,gamma,T))
comparisons=[]
for r in rows:
    if r['gamma']==0: continue
    base=next(x for x in rows if x['p']==r['p'] and x['T']==r['T'] and x['gamma']==0)
    comparisons.append({'p':r['p'],'T':r['T'],'gamma':r['gamma'],
        **{f'{key}_gain':base[key]/r[key] for key in (
            'u_linf','rho_linf','u_core_linf','rho_core_linf',
            'u_common_linf','rho_common_linf','u_common_core_linf','rho_common_core_linf')}})
out={'parameter_box':{'p':[4.9,5.1],'T':[.2,.3],'gamma':[1.5,2.5],
                       'n':201,'dt':.001},
     'meaning':'36 evaluated parameter combinations, 27 adapted versus matched uniform. This is sampled box evidence, not an interval-arithmetic proof for every point.',
     'rows':rows,'comparisons':comparisons}
(ROOT/'out'/'local_neighborhood.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print('comparisons',len(comparisons))
for key in ('u_linf','rho_linf','u_core_linf','rho_core_linf'):
    print(key,'minimum gain',min(r[f'{key}_gain'] for r in comparisons))
for key in ('u_common_linf','rho_common_linf','u_common_core_linf','rho_common_core_linf'):
    print(key,'minimum gain',min(r[f'{key}_gain'] for r in comparisons))
