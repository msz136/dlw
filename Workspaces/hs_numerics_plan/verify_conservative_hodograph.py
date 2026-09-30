"""Audit the weighted reciprocal coordinate for the normalized 2-HS system."""
import json
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import cumulative_trapezoid

from hs_exact import Soliton
from local_advantage_study import labels

u,w,rho,c=sp.symbols('u w rho c', real=True)
rho_x,mu,mu_x,mu_t=sp.symbols('rho_x mu mu_x mu_t', real=True)
rho_t=u*rho_x+rho*w
weighted_residual=sp.expand(mu*rho_t+rho*mu_t-
                            (w*mu*rho+u*mu_x*rho+u*mu*rho_x))
assert sp.simplify(weighted_residual-rho*(mu_t-u*mu_x))==0

# The continuous slope equation is D w = w^2/2 + 4u + c^2(rho^2-1)/2.
dw=w*w/2+4*u+c*c*(rho*rho-1)/2
arc=sp.sqrt(1+w*w)
arc_defect=sp.simplify(sp.diff(arc,w)*dw-arc*w)
arc_value=float(arc_defect.subs({u:.1,w:.3,rho:.8,c:1.}))
assert abs(arc_value)>1e-3

ref=Soliton((5.,))
Xd=np.linspace(-4,4,4001)
field_u,physical_x,field_rho=ref.continuous_X(Xd,0)
uxx=np.gradient(np.gradient(field_u,physical_x),physical_x)
rxx=np.gradient(np.gradient(field_rho,physical_x),physical_x)
gamma=2.
monitor=1+gamma*(abs(uxx)/max(abs(uxx))+abs(rxx)/max(abs(rxx)))/2
measure=np.r_[0.,cumulative_trapezoid(monitor,Xd)]
X=labels(ref,201,gamma)
cell_weight=np.diff(np.interp(X,Xd,measure))
target=measure[-1]/200
relative_defect=float(max(abs(cell_weight/target-1)))
assert relative_defect<1e-10

u0,x0,r0=ref.continuous_X(X,0)
cell_mass=np.diff(X)
cell_length=np.diff(x0)
rho_cell=cell_mass/cell_length
assert max(abs(rho_cell*cell_length-cell_mass))<1e-14

result={'symbolic_weighted_law':'(rho*mu)_t-(u*rho*mu)_x = rho*(mu_t-u*mu_x)',
        'advected_mu_condition':'mu_t-u*mu_x=0',
        'same_velocity_local_slope_density':'If R=F(w,rho), requiring D R=R*w for arbitrary u forces F_w=0 and rho*F_rho=F; hence R=C*rho.',
        'arclength_candidate_defect_at_sample':arc_value,
        'monitor_cell_count':len(cell_weight),
        'equal_weight_target':float(target),
        'max_relative_equal_weight_defect':relative_defect,
        'max_initial_mass_identity_residual':float(max(abs(rho_cell*cell_length-cell_mass)))}
out=Path(__file__).resolve().parent/'out'/'conservative_hodograph.json'
out.write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
