"""Independent consistency and scope checks for the route-3 evidence."""
from pathlib import Path
import hashlib, json, math

ROOT=Path(__file__).resolve().parents[1]
d=json.loads((ROOT/'out/manifold_scattering.json').read_text(encoding='utf-8'))
assert len(d['validation'])==6
assert len(d['n2'])==22 and len(d['matched_singles'])==8 and len(d['n3_local'])==8
assert d['n3_factorization']['triple_coefficient']=='1/100'
assert d['n3_factorization']['pair_factors']=={'12':'3/10','13':'1/2','23':'1/15'}
for row in d['n2']+d['matched_singles']+d['n3_local']:
    p=row['defect']
    assert p['identifiable'] and p['core_projection']['identifiable']
    assert p['condition']<10 and p['orthogonality_inf']<1e-9
    total=p['total_weighted_l2'];tangent=p['tangent_weighted_l2'];normal=p['normal_weighted_l2']
    assert abs(total**2-tangent**2-normal**2)<1e-10*max(1,total**2)
    assert 0<=p['normal_fraction']<=1+1e-12
    if 'burst' in row:
        b=row['burst']
        assert b['complete'] and b['u_inf']>=0 and b['v_inf']>=0
        fit=b['phase_fit']
        assert fit['success'] and fit['weighted_residual']<=fit['weighted_initial_error']+1e-12
for model in ('structure','fd'):
    coarse=next(r for r in d['n2'] if r['h']==.25 and r['nx']==256 and r['t']==0 and r['model']==model)
    fine=next(r for r in d['n2'] if r['h']==.25 and r['nx']==512 and r['t']==0 and r['model']==model)
    assert fine['defect']['normal_weighted_l2']<coarse['defect']['normal_weighted_l2']
    assert fine['burst']['u_inf']<coarse['burst']['u_inf']
    half=coarse['burst_half_dt']
    assert max(abs(coarse['burst'][k]-half[k]) for k in ('u_inf','v_inf'))<1e-10
assert all(g['failure'] and g['last_t'] < -3.5 for g in d['continuous_gate'])
paths=['MANIFOLD_SCATTERING_REPORT.md','out/manifold_scattering.json',
       'figures/fig17_manifold_scattering.png','experiments/manifold_scattering.py',
       'experiments/manifold_scattering_figure.py','lib/soliton_expansion.py']
manifest={'checks':'passed','n2_rows':len(d['n2']),'n3_rows':len(d['n3_local']),
          'scope':'local dynamics and analytic factorization; no numerical full scattering',
          'sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}}
out=ROOT/'out/manifold_scattering_validation.json'
out.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print('route-3 validation passed',out)
