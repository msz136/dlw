"""Register planned pilot/time-factor runs; never execute a PDE solver."""
import hashlib
import itertools
import json
from pathlib import Path

root = Path(__file__).resolve().parent
cases = []
for k,p in enumerate((3,4,5,6,8,12),1):
    cases.append(dict(id=f'HS_DEV_{k:02d}', system='2HS', c=1, p=p,
                      times=[.1,.25,.5], resolutions=[100,200,400],
                      resolution_unit='physical_cells'))
for k,(a,p,q) in enumerate(((4,1,2),(4,2,3),(6,1,3),(4,2,1),(2,1.5,2),(3.5,.75,1.5)),1):
    cases.append(dict(id=f'DLW_DEV_{k:02d}',system='DLW',a=a,p=p,q=q,
                      h=.125,x_c=0,gram_amplitude=p+q,
                      times=[.005,.01,.02,.04], resolutions=[64,128,256],
                      resolution_unit='physical_x_points'))
runs=[]
for case in cases:
    for monitor,n in itertools.product(range(5),case['resolutions']):
        runs.append(dict(id=f"E2_{case['id']}_M{monitor}_N{n}",stage='E2',
                         case=case['id'],monitor=f'M{monitor}',resolution=n,
                         method='rk4',mesh_policy='common_rezone',status='planned',
                         dt=None, spatial_model='common_model_pending_E0',
                         times=case['times']))
    for monitor in range(5):
        runs.append(dict(id=f"E2control_{case['id']}_M{monitor}",stage='E2_dt_control',
                         case=case['id'],monitor=f'M{monitor}',resolution=case['resolutions'][1],
                         method='rk4',dt='half_of_matched_E2',status='planned'))

# Symbolic finalist slots are deliberately not assigned before screening.
for case in [c for c in cases if c['id'].endswith(('01','03','05'))]:
    for slot,method,level in itertools.product(('baseline','finalist_1','finalist_2'),
                                               ('euler','heun','rk4','rk8'),range(3)):
        runs.append(dict(id=f"E3_{case['id']}_{slot}_{method}_L{level}",stage='E3',
                         case=case['id'],candidate_slot=slot,method=method,
                         dt_level=level,resolution=case['resolutions'][1],status='planned'))
assert len({r['id'] for r in runs}) == len(runs)
counts={stage:sum(r['stage']==stage for r in runs)
        for stage in ('E2','E2_dt_control','E3')}
assert counts == {'E2':180,'E2_dt_control':60,'E3':216}
protocol=root/'EXPERIMENT_PROTOCOL.md'
manifest=dict(protocol='EXPERIMENT_PROTOCOL.md',
              protocol_sha256=hashlib.sha256(protocol.read_bytes()).hexdigest(),
              status='design_only_not_solver_ready',executed_runs=0,
              blocking_setup=['E0 common spatial model and boundary implementation',
                              'monitor strengths and event schedule from development',
                              'reference controls and timestep calibration'],
              counts=counts,cases=cases,runs=runs,
              confirmation=dict(status='not_generated_not_evaluated',
                                cases_per_system=30,phase_offsets_per_case=3,
                                seed=2026092502,
                                requires='freeze algorithm and protocol before generation'))
out=root/'planned_matrix.json'
out.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(counts=counts,total=len(runs),executed=0,
                     status=manifest['status']),ensure_ascii=False))
