"""Independent readback of frozen outputs, without rerunning evolution."""
from pathlib import Path
import sys, json, hashlib, csv
import numpy as np
from scipy.interpolate import CubicSpline

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
sys.path.insert(0,str(ROOT))
from reference import TwoExact,CASES

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
datasets=[json.loads((ROOT/'out'/n).read_text(encoding='utf-8')) for n in ('results.json','fine_time.json')]
runs=[r for d in datasets for r in d['runs']]
checks={'runs':len(runs),'source_hashes_match':True,'profile_hashes_match':True,'completed':0,'error_values':0,'max_error_readback_difference':0.,'main_initial_end_ratios':[]}
for d in datasets:
    for p,h in d['sources'].items():assert sha(p)==h,p
for r in runs:
    assert sha(r['profile'])==r['profile_sha256']
    checks['completed']+=int(r['status']=='completed' and r['reached']==.02)
    s=r['spec'];g=TwoExact(CASES[s['case']],s['h'])
    with np.load(r['profile']) as z:
        js=z['y']/s['h']-.5
        xx=np.linspace(-s['eval_half'],s['eval_half'],8001 if s['case']=='fig5' else 4001)
        for row in r['history']:
            t=row['t'];uv=g.uv(js,xx,t)
            for f,target in zip(('u','v'),uv):
                er=float(abs(CubicSpline(z[f't{t:g}_x'],z[f't{t:g}_{f}'],axis=-1)(xx)-target).max())
                checks['max_error_readback_difference']=max(checks['max_error_readback_difference'],abs(er-row['errors'][f]))
                checks['error_values']+=1
    if s['variant']=='main':
        checks['main_initial_end_ratios'].append(dict(case=s['case'],model=s['model'],mesh=s['mesh'],**{f:r['history'][0]['errors'][f]/r['history'][-1]['errors'][f] for f in ('u','v')}))
assert checks['max_error_readback_difference']<1e-12
controls=list(csv.DictReader((ROOT/'out/control_comparisons.csv').open(encoding='utf-8-sig')))
checks['fig4_x_refinement']=[dict(model=r['model'],mesh=r['mesh'],field=r['field'],factor=float(r['control_error'])/float(r['base_error']),control_error=float(r['control_error']),relative_control_error=float(r['control_error'])/float(r['initial_peak']),relative_field_difference=float(r['relative_field_difference']),passed=r['pass_old_threshold']) for r in controls if r['case']=='fig4' and r['variant']=='x_half' and float(r['t'])==.02]
checks['common_passing_anchors']={c:[t for t in (.001,.005,.01,.02) if all(r['pass_old_threshold']=='True' for r in controls if r['case']==c and float(r['t'])==t)] for c in CASES}
claimed=json.loads((ROOT/'out/validation.json').read_text())
assert checks['common_passing_anchors']==claimed['common_passing_anchors_by_case']
assert checks['error_values']==claimed['error_values_readback']
(HERE/'audit.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(checks,ensure_ascii=False,indent=2))
