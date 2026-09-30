"""Pointwise additive error budget on moving coordinates for the reported case."""
import json
from pathlib import Path
import numpy as np
from hs_exact import Soliton
from hs_solver import MovingSystem,solve

ref=Soliton((5.,));a=.02;k0=-200;m=400;t=.5;dt=.002
k=np.arange(k0,k0+m+1)
system=MovingSystem(a,1,m,lambda time:float(ref.lattice(np.array([k0]),a,time)[0][0]))
z0=system.exact_initial(ref,k0,0)
result=solve(system,z0,0,t,dt,'rk4')
numerical=system.fields(t,result.states[-1]); exact=ref.lattice_state(k,a,t)
u_cont_exact=ref.continuous_x(exact['x'],t)[0]
u_cont_num=ref.continuous_x(numerical['x'],t)[0]
rho_cont_exact=ref.continuous_density_cell_mean(exact['x'][:-1],exact['x'][1:],t)
rho_cont_num=ref.continuous_density_cell_mean(numerical['x'][:-1],numerical['x'][1:],t)

def decompose(numeric,semidiscrete,continuous_exact,continuous_numeric):
    solver=numeric-semidiscrete
    model=semidiscrete-continuous_exact
    coordinate=continuous_exact-continuous_numeric
    total=numeric-continuous_numeric
    i=int(np.argmax(abs(total)))
    return {'solver_linf':float(np.max(abs(solver))),
            'model_linf':float(np.max(abs(model))),
            'coordinate_linf':float(np.max(abs(coordinate))),
            'total_linf':float(np.max(abs(total))),
            'additive_residual_linf':float(np.max(abs(total-solver-model-coordinate))),
            'at_total_max':{'index':i,'solver':float(solver[i]),
                            'model':float(model[i]),'coordinate':float(coordinate[i]),
                            'total':float(total[i])}}

out={'c':1,'p':5,'a':a,'X_range':[-4,4],'T':t,'dt':dt,
     'u_node':decompose(numerical['u'],exact['u'],u_cont_exact,u_cont_num),
     'rho_edge_cell_mean':decompose(numerical['rho'],exact['rho'],rho_cont_exact,rho_cont_num),
     'x_solver_linf':float(np.max(abs(numerical['x']-exact['x']))),
     'meaning':'Pointwise signed identity: total = solver + model + coordinate. Linf norms do not add.'}
path=Path(__file__).resolve().parent/'out'/'error_budget.json'
path.write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
