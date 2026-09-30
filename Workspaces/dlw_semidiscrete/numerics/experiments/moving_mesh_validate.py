"""Focused identities and generated-artifact checks for the moving mesh."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'lib'))
import numpy as np
from moving_mesh import MovingGrid,MovingProblem,gram_mesh,gram_phi
from parametric import Parameters

OUT=ROOT/'out'/'moving_mesh'


def inf(a):return float(np.max(np.abs(a)))


def main():
    checks={}
    p=Parameters()
    m=MovingProblem(p,nx=128)
    state,s=m.initial('moving',balanced=True)
    assert np.min(m.X.spacing())>0 and np.min(m.X.J)>0
    assert inf(state)==0
    x=np.r_[m.X.x,m.X.x[0]+m.X.L]
    phi=m.weights@gram_phi(p,.125,m.m.js,x,0.)
    mass=np.diff(x-phi)
    checks['initial_equal_gram_mass_spread']=float(np.ptp(mass))
    assert checks['initial_equal_gram_mass_spread']<2e-11

    r,q=m.mesh_density_flux(0.,m.m.exact(0.))
    z=m.m.exact(0.)
    P,W=m.m.unpack(z)
    checks['rho_W_identity']=inf(r-(1-m.weights@W/4))
    assert checks['rho_W_identity']<1e-13

    # The nonuniform physical derivative converges on a smooth periodic map.
    errors=[]
    for n in (64,128,256):
        g=MovingGrid(n,20.)
        g.set_s(.15*np.sin(2*np.pi*g.xi/20))
        f=np.sin(4*np.pi*g.x/20)
        truth=(4*np.pi/20)*np.cos(4*np.pi*g.x/20)
        errors.append(inf(g.d1(f)-truth))
    checks['x_derivative_errors']=errors
    checks['x_derivative_order']=[float(np.log2(errors[i]/errors[i+1])) for i in (0,1)]
    assert min(checks['x_derivative_order'])>3.7

    # A balanced exact background is invariant while its shared grid moves.
    rows,status=m.evolve(.005,.000125,mesh_mode='moving',balanced=True,
                         observations=(.005,))
    assert status['complete'] and inf(rows[-1]['u_response'])<1e-13
    assert inf(rows[-1]['v_response'])<1e-13
    checks['zero_perturbation_mesh_error']=inf(m.X.x-gram_mesh(p,.125,m.m.js,m.X.xi,.005))
    assert checks['zero_perturbation_mesh_error']<1e-4

    study=json.loads((OUT/'study.json').read_text(encoding='utf-8'))
    controls=json.loads((OUT/'controls.json').read_text(encoding='utf-8'))
    continuum=json.loads((OUT/'continuum.json').read_text(encoding='utf-8'))
    common=json.loads((OUT/'common_grid.json').read_text(encoding='utf-8'))
    checks['study_counts']={k:len(study[k]) for k in ('geometry','gram','perturbation','references')}
    assert checks['study_counts']=={'geometry':16,'gram':96,'perturbation':96,'references':32}
    assert all(x['complete'] for k in ('geometry','gram','perturbation','references') for x in study[k])
    assert all(x['min_spacing']>0 and x['min_J']>0 for x in study['geometry'])
    assert all(r['min_dx']>0 and r['min_J']>0 for k in ('gram','perturbation')
               for x in study[k] for r in x['observations'])
    checks['all_primary_runs_complete_and_positive']=True
    checks['control_counts']={k:len(controls[k]) for k in
                              ('high_vonly','x_dt_controls','long_geometry')}
    assert checks['control_counts']=={'high_vonly':12,'x_dt_controls':8,'long_geometry':3}
    checks['continuous_runs']=len(continuum['runs'])
    assert checks['continuous_runs']==96
    assert len(common['continuous'])==96 and len(common['gram'])==96
    checks['common_grid_assessments']=192
    assert all(x['complete'] for x in continuum['runs'])
    assert all(o['min_dx']>0 and o['min_J']>0 for x in continuum['runs']
               for o in x['observations'])
    assert all(x['complete'] for x in controls['long_geometry'])
    assert all(x['complete'] for group in controls['high_vonly']
               for x in [group['reference'],*group['variants']])
    assert all(x['complete'] for group in controls['x_dt_controls']
               for x in group['runs'])

    sources=[ROOT/'lib/moving_mesh.py',ROOT/'experiments/moving_mesh_study.py',
             ROOT/'experiments/moving_mesh_controls.py',
             ROOT/'experiments/moving_mesh_continuum.py',
             ROOT/'experiments/moving_mesh_common_grid.py',
             ROOT/'experiments/moving_mesh_report.py',Path(__file__)]
    artifacts=[OUT/'study.json',OUT/'controls.json',OUT/'continuum.json',
               OUT/'common_grid.json',
               ROOT/'MOVING_MESH_REPORT.md',
               ROOT/'figures/fig16_moving_mesh_comparison.png']
    checks['source_sha256']={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest()
                             for f in sources}
    checks['artifact_sha256']={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest()
                               for f in artifacts}
    arrays=sorted(OUT.glob('*.npz'))
    checks['raw_array_count']=len(arrays)
    checks['raw_array_sha256']={f.name:hashlib.sha256(f.read_bytes()).hexdigest()
                                for f in arrays}
    (OUT/'validation.json').write_text(json.dumps(checks,indent=2,allow_nan=False),encoding='utf-8')
    print(json.dumps({k:v for k,v in checks.items() if 'sha256' not in k},indent=2))


if __name__=='__main__':main()
