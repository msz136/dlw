"""Finite-h SD error injection and matrix-free RK4 propagation on fixed grids.

All background states and boundary data are from the same finite-h Gram field.
The split by state row is a location diagnostic, not a pure boundary truncation
decomposition. Each linear response is propagated by the derivative of RK4.
"""
from pathlib import Path
import hashlib
import json
import sys
import time
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'lib'))
from parametric import Parameters, Exact, rk4
from parametric_open import OpenModel

OUT = ROOT / 'out' / 'injection_amplification'
OUT.mkdir(parents=True, exist_ok=True)

CASES = {
    'P1': Parameters(),
    'P5': Parameters(p=.5, q=1, rho=1.5),
    'P6': Parameters(p=1, q=3, rho=4),
    'P10': Parameters(a=2, p=1.5, q=2, rho=3.5),
}


def norm(a):
    return float(np.max(np.abs(a)))


def tangent_step(m, t, z, dt, v):
    """D RK4(t,z)[v], differentiating all four actual internal stages."""
    f1 = m.rhs(t, z)
    z2 = z + dt*f1/2
    f2 = m.rhs(t+dt/2, z2)
    z3 = z + dt*f2/2
    f3 = m.rhs(t+dt/2, z3)
    z4 = z + dt*f3
    f4 = m.rhs(t+dt, z4)
    out = []
    for vec in v:
        k1 = m.delta(t, z, vec, True)
        k2 = m.delta(t+dt/2, z2, vec+dt*k1/2, True)
        k3 = m.delta(t+dt/2, z3, vec+dt*k2/2, True)
        k4 = m.delta(t+dt, z4, vec+dt*k3, True)
        out.append(vec+dt*(k1+2*k2+2*k3+k4)/6)
    return z+dt*(f1+2*f2+2*f3+f4)/6, out


def outputs(m, state):
    return tuple(norm(x) for x in m.error_fields(state))


def split_rows(m, b):
    P, Q = m.unpack(b)
    pb = np.zeros_like(P)
    qb = np.zeros_like(Q)
    pb[[0, -1]] = P[[0, -1]]
    qb[[0, -1]] = Q[[0, -1]]
    edge = m.pack(pb, qb)
    return edge, b-edge


def run(pars, h=.125, nx=128, T=.01, dt=.00025, closure='extrapolated',
        decomposition=True):
    cls = OpenModel if closure == 'extrapolated' else __import__('parametric').Model
    m = cls(pars, h, nx, model='structure')
    n = round(T/dt)
    assert abs(n*dt-T) < 1e-12
    z = m.exact(0)
    lin = np.zeros_like(z)
    edge = np.zeros_like(z)
    core = np.zeros_like(z)
    injection = np.zeros_like(z)
    sums = np.zeros((3, 2))
    max_closure = 0.
    start = time.perf_counter()
    for k in range(n):
        t = k*dt
        bar = m.exact(t)
        nxt = m.exact(t+dt)
        if decomposition:
            step, propagated = tangent_step(m, t, bar, dt, (lin, edge, core))
            b = step-nxt
            be, bc = split_rows(m, b)
            lin, edge, core = propagated
            lin += b
            edge += be
            core += bc
            injection += b
            sums[0] += outputs(m, b)
            sums[1] += outputs(m, be)
            sums[2] += outputs(m, bc)
            max_closure = max(max_closure, norm(lin-edge-core))
        z = rk4(m.rhs, t, z, dt)
        if not np.all(np.isfinite(z)) or norm(z)>1e3:
            return {'complete': False, 'stopped_step':k+1, 'seconds':time.perf_counter()-start}
    seconds = time.perf_counter()-start
    actual = z-m.exact(T)
    finite = Exact(pars,h).uv(m.js,m.X.x,T)
    continuous = Exact(pars,h,continuous=True).uv(m.js,m.X.x,T)
    result = {'complete':True,'seconds':seconds,'steps':n,
              'solver':outputs(m,actual),
              'model':tuple(norm(f-c) for f,c in zip(finite,continuous)),
              'initial_output_defect':outputs(m,m.rhs(0,m.exact(0))-m.exact(0,True)),
              'amplitude':tuple(norm(a) for a in Exact(pars,h).uv(m.js,m.X.x,0))}
    if decomposition:
        result.update({'linear':outputs(m,lin),'nonlinear_remainder':outputs(m,actual-lin),
                       'unpropagated_sum':outputs(m,injection),
                       'edge_response':outputs(m,edge),'interior_response':outputs(m,core),
                       'absolute_injections':sums.tolist(),
                       'edge_state_row_fraction':(sums[1]/np.maximum(sums[0],1e-30)).tolist(),
                       'linear_to_raw_injection':(np.array(outputs(m,lin))/np.maximum(outputs(m,injection),1e-30)).tolist(),
                       'linear_to_absolute_injection':(np.array(outputs(m,lin))/np.maximum(sums[0],1e-30)).tolist(),
                       'split_closure_residual':max_closure,
                       'linear_prediction_relative':(np.array(outputs(m,actual-lin))/np.maximum(outputs(m,actual),1e-30)).tolist()})
    return result


def main():
    rows=[]
    configs=[]
    for case in CASES:
        for nx in (128,256):
            configs.append((case,.125,nx,.00025,'extrapolated',True))
    for case in ('P5','P6'):
        configs.append((case,.125,512,.00025,'extrapolated',True))
    for case in ('P1','P5','P6','P10'):
        configs.append((case,.125,128,.000125,'extrapolated',False))
        configs.append((case,.125,128,.00025,'original',True))
    for case,h,nx,dt,closure,decomp in configs:
        cfg={'case':case,'h':h,'nx':nx,'dt':dt,'T':.01,'closure':closure}
        row={'config':cfg, **run(CASES[case],h,nx,dt=dt,closure=closure,decomposition=decomp)}
        rows.append(row)
        print(cfg, 'solver',row.get('solver'),'linear',row.get('linear'),
              'seconds',round(row['seconds'],2), flush=True)
        (OUT/'mechanism.json').write_text(json.dumps({'runs':rows},indent=2,allow_nan=False)+'\n',encoding='utf-8')
    paths=[Path(__file__),ROOT/'lib/parametric.py',ROOT/'lib/parametric_open.py',
           ROOT/'lib/dynamics.py']
    data={'scope':'finite-h exact background, fixed periodic x, open y; T=.01',
          'runs':rows,'sources_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}
    (OUT/'mechanism.json').write_text(json.dumps(data,indent=2,allow_nan=False)+'\n',encoding='utf-8')


if __name__=='__main__': main()
