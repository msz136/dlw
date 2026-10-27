"""Export each method's native-node response histories, verifying source hashes."""
from pathlib import Path
import json
import hashlib
import numpy as np

HERE=Path(__file__).resolve().parent
CASES=['A','D','Gaussian','Sinusoidal']
METHODS=['Endpoint-SD','Centered-SD','FD']
curves=[];sources={}
for case in CASES:
    jp=HERE.parent/'native'/(case+'.json');ap=jp.with_suffix('.npz')
    if not jp.exists():continue
    record=json.loads(jp.read_text(encoding='utf-8'))
    digest=hashlib.sha256(ap.read_bytes()).hexdigest()
    assert digest==record['artifact_sha256']
    data=np.load(ap)
    assert record['interpolation_used'] is False and record['method_pair_comparisons'] is False
    time=data['t'];maxima=data['response_normalized']
    assert maxima.shape==(len(time),3,2,2) and np.isfinite(maxima).all()
    sources[case]={'path':ap.relative_to(HERE.parent).as_posix(),'sha256':digest,
                   'status':record['status'],'reached':record['reached']}
    for mi,method in enumerate(METHODS):
        for pi,component in enumerate(['u','v']):
            curves.append({'case':case,'method':method,'input':component,
                'time':time.tolist(),'max_normalized':maxima[:,mi,pi].tolist()})
payload={'source':sources,'normalization':'Each method native-node maximum of its own perturbed trajectory minus its own baseline, divided by prescribed epsilon=1e-6.',
         'observation_grid':'Each method uses its own native u and v sites in the paper observation region. No interpolation, intermethod alignment or intermethod difference is used.',
         'curves':curves}
(HERE/'figure_curves.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
print(json.dumps({'completed_cases':list(sources),'curves':len(curves)}))
