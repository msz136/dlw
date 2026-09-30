"""Check saved experiment completeness and whether reported effects clear controls."""
import hashlib
import json
import math
from pathlib import Path

HERE=Path(__file__).resolve().parent
OUT=HERE/'out'
d=json.loads((OUT/'factorial_results.json').read_text(encoding='utf-8'))
sp=json.loads((OUT/'spatial_audit.json').read_text(encoding='utf-8'))
dm=json.loads((OUT/'domain_audit.json').read_text(encoding='utf-8'))
spaces=('integrable_moving','ordinary_moving','fixed_difference')
methods=('euler','heun','rk4','rk8')
dts=(.05,.025,.0125,.00625)
assert len(d['rows'])==48 and len(d['reference_runs'])==3
assert len(sp['rows'])==9 and len(dm['rows'])==6
keys={(r['space'],r['method'],r['dt_requested']) for r in d['rows']}
assert keys=={(s,m,dt) for s in spaces for m in methods for dt in dts}
for p,checksum in d['source_sha256'].items():
    path=HERE.parent/p
    assert hashlib.sha256(path.read_bytes()).hexdigest()==checksum,p
for r in d['rows']+d['reference_runs']:
    assert r['status']=='completed' and r['rejected_steps']==0 and abs(r['reached']-.25)<1e-12
    assert set(r['observations'])=={'0.05','0.1','0.25'}
    for o in r['observations'].values():
        assert o['mesh']['min_spacing']>0 and o['mesh']['min_rho']>0
        c=o['common']['core']
        assert all(math.isfinite(c[k]) and c[k]>=0 for k in ('u_linf','rho_linf','u_reconstruction_floor','rho_reconstruction_floor'))
for s in spaces:
    for m in methods:
        r=next(x for x in d['rows'] if (x['space'],x['method'],x['dt_requested'])==(s,m,.00625))
        core=r['observations']['0.25']['common']['core']
        assert core['u_reconstruction_floor']<.02*core['u_linf']
        assert core['rho_reconstruction_floor']<.02*core['rho_linf']
    rr=sorted([x for x in sp['rows'] if x['space']==s],key=lambda x:x['edges'])
    for field in ('u_linf','rho_linf'):
        vals=[x['core'][field] for x in rr]
        p=math.log2(vals[1]/vals[2])
        bounds=(.8,1.2) if s=='integrable_moving' else (1.8,2.2)
        assert bounds[0]<p<bounds[1],(s,field,p)
for name in ('REPORT.md','out/fig1_total_error.png','out/fig2_temporal_error.png','out/fig3_spatial_refinement.png'):
    assert (HERE/name).stat().st_size>1000
print('PASSED: 12 combinations, 48 time-step runs, 3 references, 9 space and 6 domain checks.')
