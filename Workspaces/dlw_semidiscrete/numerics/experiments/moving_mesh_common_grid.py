"""Compare numerical fields on one physical x grid, not their own nodes."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'lib'))
sys.path.insert(0,str(ROOT/'experiments'))
import numpy as np
from scipy.interpolate import CubicSpline
from parametric import Exact
from moving_mesh_study import OUT,ALL,inf


def assess(row, continuous):
    pars=ALL[int(row['parameter_id'][1:])-1]
    exact=Exact(pars,.125,continuous=continuous)
    js=np.arange(-12,12)
    data=np.load(OUT/row['file'])
    x=data['x1']
    target_x=np.linspace(-9,9,1025)
    t=.01
    en_u,en_v=exact.uv(js,x,t)
    et_u,et_v=exact.uv(js,target_x,t)
    ans={}
    for field,en,et in (('u',en_u,et_u),('v',en_v,et_v)):
        numerical_nodes=en+data[f'{field}1']
        numerical_common=CubicSpline(x,numerical_nodes,axis=1,bc_type='natural')(target_x)
        difference=numerical_common-et
        ans[field+'_common_inf']=inf(difference)
        ans[field+'_common_interior']=inf(difference[abs((js+.5)*.125)<=.75])
        ans[field+'_node_inf']=row['observations'][-1][field+'_inf']
    return {'parameter_id':row['parameter_id'],'model':row['model'],'mesh':row['mesh'],
            'target':'continuous' if continuous else 'finite_h_gram',**ans}


def main():
    c=json.loads((OUT/'continuum.json').read_text(encoding='utf-8'))
    g=json.loads((OUT/'study.json').read_text(encoding='utf-8'))
    rows={'continuous':[assess(x,True) for x in c['runs']],
          'gram':[assess(x,False) for x in g['gram']]}
    rows['scope']={'x_evaluation_interval':[-9,9],'evaluation_points':1025,
                   'interpolation':'natural cubic spline of numerical u/v',
                   'same_physical_x_for_all_models_and_meshes':True,'t':.01}
    paths=[Path(__file__),ROOT/'lib/moving_mesh.py',ROOT/'lib/parametric.py']
    rows['source_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in paths}
    (OUT/'common_grid.json').write_text(json.dumps(rows,indent=2,allow_nan=False),encoding='utf-8')
    print('common physical x grid assessed:',len(rows['continuous']),len(rows['gram']))


if __name__=='__main__':main()
