"""Read-only comparison to the frozen report trajectories and analytic boundaries."""
from pathlib import Path
import json
import sys
import numpy as np

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
stored=ROOT/'Workspaces/hs_four_schemes_20260927/paper_point'
live=json.loads((HERE/'hs_live_default_fields.json').read_text(encoding='utf-8'))
differences={}
for label,scheme in [('Integrable','S1'),('FD','S4')]:
    with np.load(stored/f'{scheme}_rk4_0.003125.npz') as data:
        differences[label]={}
        for js_key,old_key in [('x','x'),('u','u'),('rhoX','rho_x'),('rho','rho')]:
            current=np.asarray(live[label][js_key]); target=data['t0.5_'+old_key]
            assert current.shape==target.shape
            maximum=float(np.max(np.abs(current-target)))
            assert maximum<1e-10,(label,js_key,maximum)
            differences[label][js_key]=maximum

sys.path.insert(0,str(ROOT/'Workspaces/hs_conserved_mesh_20260925'))
from run_mesh_comparison import reference
from hs_exact import Soliton
sol=Soliton((5.,),c=1.,phase=(0.,),shift=-.8)
max_boundary_difference=0.0
for t in [0.,.0015625,.25,.5]:
    X=np.linspace(-4,4,51)
    z=np.tanh((3.75*X-.6*t)/2); sx=1-z*z
    zx=1.875*sx; zxx=-2*zx*1.875*z
    J=1+.3*zx; Jx=.3*zxx
    u=.09*sx; uX=-.18*z*zx; uXX=-.18*(zx*zx+z*zxx)
    m=(uXX*J-uX*Jx)/J**3+2; x=X-.5+.3*z
    ur,rr,mr,_=reference(sol,x,t)
    maximum=max(float(np.max(abs(u-ur))),float(np.max(abs(1/J-rr))),float(np.max(abs(m-mr))))
    assert maximum<1e-11
    max_boundary_difference=max(max_boundary_difference,maximum)

result={'status':'passed','method':'All terminal x/u/rho positions and values compared to frozen original NumPy/SciPy RK4 trajectories; analytic boundary u/rho/m compared with independent existing reference.',
        'terminal_field_max_absolute_difference':differences,
        'analytic_boundary_max_absolute_difference':max_boundary_difference,
        'reference_trajectories':str(stored.relative_to(ROOT)),
        'floating_point_note':'FD uses the uniform central stencil and Thomas solve written in the report; frozen engine evaluates an equivalent stencil using local spacing differences. Small double-precision differences are expected.',
        'PDE_trajectories_read':2,'new_Python_PDE_runs':0}
(HERE/'hs_independent_validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
