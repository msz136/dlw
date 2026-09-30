"""Targeted time-step and artifact checks for the route-one conclusions."""
from pathlib import Path
import sys,json,hashlib

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'lib'),str(ROOT/'experiments')]
from moving_mesh_study import ALL
from moving_mesh_route1_coupled import run


def main():
    base=ROOT/'out'/'moving_mesh'
    coupled=json.loads((base/'route1_coupled.json').read_text(encoding='utf-8'))
    result={'scope':{'cases':['P1','P7'],'T':.04,'dt_coarse':.000125,
                     'dt_fine':.0000625,'modes':['static_adaptive','moving',
                                                 'intermittent']},'rows':[]}
    for index in (0,6):
        for model in ('structure','fd'):
            for mode in ('static_adaptive','moving','intermittent'):
                fine=run(ALL[index],model,mode,.04,.0000625)
                coarse=next(x for x in coupled['runs'] if
                    x['parameter_id']==f'P{index+1}' and x['model']==model
                    and x['T']==.04 and x['mode']==mode)
                assert fine['status']=='complete' and coarse['status']=='complete'
                a=coarse['observations'][-1];b=fine['observations'][-1]
                keys=('u_error','v_error','u_common_error','v_common_error')
                result['rows'].append({'parameter_id':f'P{index+1}',
                    'model':model,'mode':mode,
                    'absolute_metric_changes':{k:abs(a[k]-b[k]) for k in keys},
                    'relative_metric_changes':{k:abs(a[k]-b[k])/max(b[k],1e-30)
                                               for k in keys}})
                print(f'P{index+1} {model} {mode} checked',flush=True)
    files=['route1_geometry.json','route1_coupled.json','route1_gradient.json',
           'route1_replay.json','route1_cost.json','route1_perturb.json',
           'route1_transport.json','route1_transport_dt.json','route1_dlw_gate.json']
    transport=json.loads((base/'route1_transport.json').read_text(encoding='utf-8'))
    transport_dt=json.loads((base/'route1_transport_dt.json').read_text(encoding='utf-8'))
    gates=json.loads((base/'route1_dlw_gate.json').read_text(encoding='utf-8'))
    assert len(transport['runs'])==48
    assert all(r['status']=='complete' for r in transport['runs'])
    runs={(r['parameter_id'],r['nx'],r['mode']):r for r in transport['runs']}
    ratio_checks=[]
    for pid in ('P1','P2','P7','P10'):
        for nx in (64,128,256):
            a=runs[pid,nx,'moving']['observations'][-1]
            b=runs[pid,nx,'static_adaptive']['observations'][-1]
            ratios={k:a[k]/b[k] for k in ('u_common_error','v_common_error',
                                          'u_node_error','v_node_error')}
            ratio_checks.append({'parameter_id':pid,'nx':nx,'ratios':ratios})
            if pid in ('P1','P2','P7'):
                assert all(value<.8 for value in ratios.values())
    max_dt=max(value['relative'] for row in transport_dt['rows']
               for value in row['error_metric_changes_at_D2'].values())
    assert max_dt<1e-7
    assert len(gates['runs'])==16
    assert all(r['last_checked'] and r['last_checked']['D']<.06
               for r in gates['runs'])
    result['long_distance_checks']={'transport_completed':48,
        'strong_gain_cases':['P1','P2','P7'],
        'ratios':ratio_checks,'max_dt_metric_relative_change':max_dt,
        'dlw_gate_failure_count':len(gates['runs']),
        'maximum_dlw_gate_failure_D':max(r['last_checked']['D']
                                         for r in gates['runs'])}
    result['artifact_sha256']={f:hashlib.sha256((base/f).read_bytes()).hexdigest()
                               for f in files}
    result['figure_sha256']={f:hashlib.sha256((ROOT/'figures'/f).read_bytes()).hexdigest()
                             for f in ('fig19_route1_mesh.png','fig20_route1_transport.png')}
    result['source_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
        for p in (Path(__file__),ROOT/'experiments/moving_mesh_route1_coupled.py',
                  ROOT/'experiments/moving_mesh_route1_geometry.py',
                  ROOT/'experiments/moving_mesh_route1_replay.py',
                  ROOT/'experiments/moving_mesh_route1_cost.py',
                  ROOT/'experiments/moving_mesh_route1_perturb.py',
                  ROOT/'experiments/moving_mesh_route1_transport.py',
                  ROOT/'experiments/moving_mesh_route1_transport_dt.py',
                  ROOT/'experiments/moving_mesh_route1_dlw_gate.py',
                  ROOT/'experiments/moving_mesh_route1_transport_figure.py',
                  ROOT/'lib/moving_mesh.py')}
    (base/'route1_validation.json').write_text(json.dumps(result,indent=2,
        allow_nan=False),encoding='utf-8')


if __name__=='__main__':main()
