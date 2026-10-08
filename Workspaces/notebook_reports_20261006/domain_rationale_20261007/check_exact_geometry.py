"""Evaluate analytic DLW wave geometry and boundary tails, without PDE integration."""
from pathlib import Path
import hashlib
import json
import sys
import mpmath as mp
import numpy as np

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
sys.path.insert(0, str(PROJECT))
from dlw_numeric_cells import CELLS
ns = {}
for name in ('imports','config','reference'):
    exec(CELLS[name], ns)
mp.mp.dps = 50

def uv(case, x, y, t):
    p, q = [[mp.mpf(str(v)) for v in values] for values in ns['CASES'][case]]
    S = [a+b for a,b in zip(p,q)]
    omega = [b*b-a*a for a,b in zip(p,q)]
    ell = [1/(a-2)+1/(b+2) for a,b in zip(p,q)]
    gamma = [-(a-2)/(b+2) for a,b in zip(p,q)]
    coeff = [mp.mpf(1), 1/S[0]]
    subsets = [(0,), (1,)]
    if len(p) == 2:
        cross = ((p[0]-p[1])*(q[0]-q[1]) /
                 ((p[0]+q[0])*(p[0]+q[1])*(p[1]+q[0])*(p[1]+q[1])))
        coeff = [mp.mpf(1), 1/S[0], 1/S[1], cross]
        subsets = [(0,0),(1,0),(0,1),(1,1)]
    fields = []
    for f in (False, True):
        rates = [(sum(S[i]*z for i,z in enumerate(sub)),
                  sum(ell[i]*z for i,z in enumerate(sub))) for sub in subsets]
        weights = [c*mp.exp(sum(z*(S[i]*x+omega[i]*t+ell[i]*y)
                                  for i,z in enumerate(sub))) *
                   (mp.fprod(gamma[i]**z for i,z in enumerate(sub)) if f else 1)
                   for c,sub in zip(coeff,subsets)]
        total = sum(weights)
        weights = [w/total for w in weights]
        mx = sum(w*r[0] for w,r in zip(weights,rates))
        my = sum(w*r[1] for w,r in zip(weights,rates))
        covariance = sum(w*r[0]*r[1] for w,r in zip(weights,rates))-mx*my
        fields.append((mx,covariance))
    return 2*(fields[1][0]-fields[0][0]), 2*(fields[1][1]+fields[0][1])

boundary = []
for case in ns['CASES']:
    max_u = max_v = mp.mpf(0)
    for x in (-20,20):
        for y in np.linspace(-1.5,1.5,25):
            for t in np.linspace(0,.01,11):
                u,v = uv(case,mp.mpf(x),mp.mpf(str(y)),mp.mpf(str(t)))
                max_u,max_v = max(max_u,abs(u)),max(max_v,abs(v))
    boundary.append(dict(case=case,max_boundary_u=float(max_u),max_boundary_v=float(max_v)))

T,Y = .01,1.5
result = dict(success=True,analysis='analytic reference only; no PDE integration',
    boundary_sampling=dict(x=[-20,20],y_points=25,time_points=11,decimal_precision=50),
    boundary_fields=boundary,
    centers=dict(A=dict(formula='.597253-t+.25y',minimum=.212253,max=.972253),
                 B=dict(formula='-.346574+7t+.5y',minimum=-1.096574,max=.473426)),
    two_mode_phase_difference='5y/12-4t',
    two_mode_exponential_ratio=[float(np.exp(-5*Y/12-4*T)),float(np.exp(5*Y/12))],
    two_mode_equal_phase_line_y=[0,9.6*T],
    largest_strip_halfwidth_for_factor_two=float(12/5*(np.log(2)-4*T)),
    largest_integer_h_below_halfwidth=float(.125*np.floor((12/5*(np.log(2)-4*T))/.125)),
    source_sha256=hashlib.sha256((PROJECT/'dlw_numeric_cells.py').read_bytes()).hexdigest())
(HERE/'exact_geometry.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
