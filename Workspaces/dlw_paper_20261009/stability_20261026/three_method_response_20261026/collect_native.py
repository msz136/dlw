"""Assemble native-only per-method response data, with no cross-method metric."""
from pathlib import Path
import csv,hashlib,json
import numpy as np
HERE=Path(__file__).resolve().parent
NATIVE=HERE/'native'
CASES=['A','D','Gaussian','Sinusoidal']
rows=[];checks=[];records=[]
for case in CASES:
    path=NATIVE/(case+'.json')
    if not path.exists():continue
    record=json.loads(path.read_text(encoding='utf-8'))
    assert record['interpolation_used'] is False and record['method_pair_comparisons'] is False
    assert hashlib.sha256(path.with_suffix('.npz').read_bytes()).hexdigest()==record['artifact_sha256']
    data=np.load(path.with_suffix('.npz'))
    assert data['response_normalized'].shape==(101,3,2,2)
    assert record['status']=='complete' and record['reached']==.01
    records.append(record)
    for r in record['terminal']:
        rows.append(dict(case=case,method=r['method'],input=r['input'],T=record['reached'],epsilon=record['epsilon'],kappa=record['kappa'],initial_u_over_epsilon=r['initial_response_normalized'][0],initial_v_over_epsilon=r['initial_response_normalized'][1],terminal_u_over_epsilon=r['terminal_response_normalized'][0],terminal_v_over_epsilon=r['terminal_response_normalized'][1]))
    checks.append(dict(case=case,baselines=record['baseline_checks'],initial_checks=record['initial_checks'],status=record['status'],reached=record['reached']))
with (NATIVE/'terminal_rows.csv').open('w',newline='',encoding='utf-8-sig') as f:
    writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
out=dict(completed_cases=[r['case'] for r in records],complete_perturbed_trajectories=len(rows),rows=rows,checks=checks,interpolation_used=False,method_pair_comparisons=False,continuous_certificate=False)
(NATIVE/'summary.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(dict(cases=out['completed_cases'],trajectories=len(rows)),indent=2))
