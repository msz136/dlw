"""Compare equal-node representation on natural, uniform, and monitor meshes.

This isolates spatial sampling error. The monitor grid is not a new integrable
time-evolution scheme and is never substituted into the semi-discrete 2-HS ODE.
"""
import json
from pathlib import Path
import numpy as np
from scipy.integrate import cumulative_trapezoid
from hs_exact import Soliton

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'out';OUT.mkdir(exist_ok=True)
ref=Soliton((5.,));c=1.;p=5.;N=401;X=np.linspace(-4,4,N)
records=[];curves={}
for t in (0.,.5,1.):
    _,natural_x,_=ref.continuous_X(X,t)
    left,right=natural_x[[0,-1]]
    dense_x=np.linspace(left,right,12001)
    dense_u,dense_rho,_=ref.continuous_x(dense_x,t)
    dx=dense_x[1]-dense_x[0]
    second=np.gradient(np.gradient(dense_u,dx),dx)
    rho_second=np.gradient(np.gradient(dense_rho,dx),dx)
    u_curv=abs(second)/max(abs(second))
    rho_curv=abs(rho_second)/max(abs(rho_second))
    monitors={'u_curvature':1+10*u_curv,
              'two_field_curvature':1+10*(u_curv+rho_curv)/2}
    grids={'natural':natural_x,'uniform':np.linspace(left,right,N)}
    for name,monitor in monitors.items():
        integrated=np.r_[0.,cumulative_trapezoid(monitor,dense_x)]
        grids[name]=np.interp(np.linspace(0,integrated[-1],N),integrated,dense_x)
    for name,x in grids.items():
        sampled_u,sampled_rho,_=ref.continuous_x(x,t)
        interp_u=np.interp(dense_x,x,sampled_u)
        interp_rho=np.interp(dense_x,x,sampled_rho)
        e_u=interp_u-dense_u;e_rho=interp_rho-dense_rho
        gap=np.diff(x)
        core=(dense_x>=-1)&(dense_x<=1)
        records.append({'t':t,'mesh':name,'nodes':N,
                        'min_dx':float(gap.min()),'max_dx':float(gap.max()),
                        'peak_region_mean_dx':float(np.mean(gap[np.abs((x[1:]+x[:-1])/2)<.5])),
                        'u_linf':float(np.max(abs(e_u))),
                        'u_core_linf':float(np.max(abs(e_u[core]))),
                        'u_l2':float(np.sqrt(np.mean(e_u**2))),
                        'rho_linf':float(np.max(abs(e_rho))),
                        'rho_l2':float(np.sqrt(np.mean(e_rho**2)))})
        if t==.5:
            curves[f'{name}_x']=x
            curves[f'{name}_interpolated_u']=interp_u
    if t==.5:
        curves['dense_x']=dense_x;curves['exact_u']=dense_u
(OUT/'mesh_representation.json').write_text(json.dumps({
    'experiment':'Equal node count and common physical endpoints; piecewise linear interpolation of exact continuous solution.',
    'monitor':'u_curvature = 1+10 normalized |u_xx|; two_field_curvature = 1+5(normalized |u_xx|+normalized |rho_xx|), each equidistributed using a dense exact reference grid.',
    'warning':'Interpolation-only comparison. Curvature monitor is not a time-dependent integrable 2-HS scheme.',
    'rows':records},indent=2),encoding='utf-8')
np.savez_compressed(OUT/'mesh_representation.npz',**curves)
print('Wrote',OUT/'mesh_representation.json')
