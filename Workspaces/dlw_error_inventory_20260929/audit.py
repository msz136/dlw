"""Read-only audit of existing DLW trajectories; no new PDE evolution."""
from pathlib import Path
import csv
import hashlib
import json
import sys
import numpy as np
from scipy.interpolate import CubicSpline

HERE = Path(__file__).resolve().parent
WS = HERE.parent
sys.path.insert(0, str(WS / 'dlw_paper_cases_20260927'))
import run as paper

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

checks, tables, pairs = [], [], []
for name in ('dlw_paper_cases_20260927', 'dlw_time_curves_20260928'):
    source = WS / name / 'out/results.json'
    data = json.loads(source.read_text(encoding='utf-8'))
    readback = 0.0
    count = 0
    for run in data['runs']:
        assert sha(run['profile']) == run['profile_sha256']
        s = run['spec']
        ref = paper.PaperExact(paper.CASES[s['case']], s['h'], True)
        with np.load(run['profile']) as fields:
            js = np.rint(fields['y'] / s['h'] - .5).astype(int)
            for row in run['history']:
                t = row['t']
                if name == 'dlw_paper_cases_20260927':
                    x = fields['x']
                    approx = [fields[f't{t:g}_{f}'] for f in ('u', 'v')]
                    stored = [row[f'{f}_error'] for f in ('u', 'v')]
                else:
                    x = np.linspace(-10, 10, 4001)
                    approx = [CubicSpline(fields[f't{t:g}_x'], fields[f't{t:g}_{f}'], axis=-1)(x) for f in ('u', 'v')]
                    stored = [row['errors'][f] for f in ('u', 'v')]
                errors = [float(np.max(np.abs(a-b))) for a,b in zip(approx, ref.uv(js,x,t))]
                readback = max(readback, *(abs(a-b) for a,b in zip(errors, stored)))
                count += 2
                if name == 'dlw_paper_cases_20260927' and s['method'] == 'euler' and t in (.005, .01, .02):
                    tables.append({**s, 't':t, 'u_error':errors[0], 'v_error':errors[1], 'reached':run['reached']})
    assert readback < 1e-11
    checks.append({'source':str(source), 'sha256':sha(source), 'runs':len(data['runs']),
                   'scalar_errors_checked':count, 'max_readback_difference':readback,
                   'current_source_hash_matches':{p:Path(p).exists() and sha(p)==h for p,h in data['sources'].items()}})
    if name == 'dlw_paper_cases_20260927':
        for case in paper.CASES:
            for model in ('structure','fd'):
                matched = [next(r for r in data['runs'] if r['spec']['case']==case and r['spec']['model']==model and r['spec']['method']=='euler' and r['spec']['purpose']==v) for v in ('main','time_half')]
                with np.load(matched[0]['profile']) as a, np.load(matched[1]['profile']) as b:
                    for f in ('u','v'):
                        diff = float(np.max(abs(a[f't0.01_{f}']-b[f't0.01_{f}'])))
                        base = next(r for r in tables if r['case']==case and r['model']==model and r['purpose']=='main' and r['t']==.01)[f'{f}_error']
                        pairs.append({'case':case,'model':model,'field':f,'t':.01,'dt_half_field_difference':diff,'difference_over_total_error':diff/base})

for filename, rows in (('euler_existing.csv',tables),('time_half_field_differences.csv',pairs)):
    with (HERE/filename).open('w',encoding='utf-8-sig',newline='') as out:
        writer=csv.DictWriter(out,fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)
(HERE/'audit.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'checks':checks,'time_half':pairs},ensure_ascii=False,indent=2))
