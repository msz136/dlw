"""Time-step check for controlled long-distance field transport."""
from pathlib import Path
import sys,json,hashlib

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'lib'),str(ROOT/'experiments')]
from moving_mesh_study import ALL
from moving_mesh_route1_transport import run


def main():
    base=ROOT/'out/moving_mesh'
    earlier=json.loads((base/'route1_transport.json').read_text(encoding='utf-8'))
    geom=json.loads((base/'route1_geometry.json').read_text(encoding='utf-8'))
    width={x['parameter_id']:x['width'] for x in geom['cases']}
    result={'scope':{'nx':128,'D':2,'dt_coarse':.001,'dt_fine':.0005,
                     'modes':['static_adaptive','moving']},'rows':[]}
    for index in (0,1,6,9):
        pid=f'P{index+1}'
        for mode in ('static_adaptive','moving'):
            a=next(r for r in earlier['runs'] if r['parameter_id']==pid
                   and r['nx']==128 and r['mode']==mode)
            b=run(ALL[index],width[pid],[.5,1,2],nx=128,dt=.0005,mode=mode)
            assert a['status']==b['status']=='complete'
            diffs={}
            for field in ('u_common_error','v_common_error',
                          'u_node_error','v_node_error'):
                old=a['observations'][-1][field]
                new=b['observations'][-1][field]
                diffs[field]={'absolute':abs(old-new),
                              'relative':abs(old-new)/max(new,1e-30)}
            result['rows'].append({'parameter_id':pid,'mode':mode,
                                   'error_metric_changes_at_D2':diffs})
            print(pid,mode,diffs,flush=True)
    paths=[Path(__file__),ROOT/'experiments/moving_mesh_route1_transport.py']
    result['source_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in paths}
    (base/'route1_transport_dt.json').write_text(json.dumps(result,indent=2,
        allow_nan=False),encoding='utf-8')


if __name__=='__main__':main()
