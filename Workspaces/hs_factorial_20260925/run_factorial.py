"""Run the 2HS 3-space x 4-time comparison with common continuous initial data."""
from __future__ import annotations

import hashlib
import json
import platform
import sys
from pathlib import Path
from time import perf_counter

import numpy as np
import scipy
from scipy.interpolate import CubicSpline

HERE = Path(__file__).resolve().parent
HS = HERE.parent / 'hs_numerics_plan'
sys.path.insert(0, str(HS))
from hs_exact import Soliton
from hs_fixed import FixedSystem
from hs_solver import MovingSystem, solve

OUT = HERE / 'out'
OUT.mkdir(exist_ok=True)
METHODS = ('euler', 'heun', 'rk4', 'rk8')
SPACES = ('integrable_moving', 'ordinary_moving', 'fixed_difference')
DTS = (.05, .025, .0125, .00625)
REF_DT = .000390625
TIMES = (.05, .10, .25)
MAIN_DT = .00625
CORE = np.linspace(-2., 2., 801)
FULL = np.linspace(-3.5, 3.5, 1401)


def make_system(space: str, ref: Soliton):
    a, edges, first = .02, 400, -200
    if space == 'fixed_difference':
        x = np.linspace(-4., 4., edges + 1)
        system = FixedSystem(x, ref.c, ref)
        return system, system.initial(0.)
    X = a * np.arange(first, first + edges + 1)
    u, x, _ = ref.continuous_X(X, 0.)
    b = lambda t: float(ref.continuous_X(np.array([X[0]]), t)[0][0])
    system = MovingSystem(a, ref.c, edges, b,
                          'sd' if space == 'integrable_moving' else 'fd')
    z0 = system.pack(np.diff(u), np.diff(x), float(x[0]))
    return system, z0


def evaluate(ref: Soliton, system, t: float, z: np.ndarray, space: str):
    f = system.fields(t, z)
    x, u, rho = f['x'], f['u'], f['rho']
    ue, re, _ = ref.continuous_x(x, t)
    if space == 'fixed_difference':
        rn, rho_x = re, x
        rho_point = rho
        rho_native_ref = re
        rho_reconstruction_ref = re
        rho_native_location = 'nodes, point values'
        spacing = np.diff(x)
    else:
        rho_x = (x[1:] + x[:-1]) / 2
        rho_native_ref = ref.continuous_density_cell_mean(x[:-1], x[1:], t)
        # A cell average differs from the midpoint value by d^2 rho_xx/24.
        # Use the same fourth-order reconstruction on numerical and exact averages.
        rho_point = rho - f['d']**2*CubicSpline(rho_x, rho)(rho_x, 2)/24
        rho_reconstruction_ref = (rho_native_ref
            - f['d']**2*CubicSpline(rho_x, rho_native_ref)(rho_x, 2)/24)
        rho_native_location = 'edges, exact cell averages'
        spacing = f['d']
    u_spline = CubicSpline(x, u)
    u_ref_spline = CubicSpline(x, ue)
    rho_spline = CubicSpline(rho_x, rho_point)
    rho_ref_spline = CubicSpline(rho_x, rho_reconstruction_ref)
    native = {
        'u_linf': float(np.max(np.abs(u - ue))),
        'rho_linf': float(np.max(np.abs(rho - rho_native_ref))),
        'rho_location': rho_native_location,
    }
    windows = {}
    for name, grid in (('core', CORE), ('full', FULL)):
        if x[0] > grid[0] or x[-1] < grid[-1] or rho_x[0] > grid[0] or rho_x[-1] < grid[-1]:
            windows[name] = {'status': 'outside grid coverage'}
            continue
        uval = u_spline(grid)
        rval = rho_spline(grid)
        ustar, rstar, _ = ref.continuous_x(grid, t)
        eu, er = uval - ustar, rval - rstar
        windows[name] = {
            'u_linf': float(np.max(np.abs(eu))),
            'rho_linf': float(np.max(np.abs(er))),
            'u_l2': float(np.sqrt(np.trapezoid(eu**2, grid)/(grid[-1]-grid[0]))),
            'rho_l2': float(np.sqrt(np.trapezoid(er**2, grid)/(grid[-1]-grid[0]))),
            'u_reconstruction_floor': float(np.max(np.abs(u_ref_spline(grid)-ustar))),
            'rho_reconstruction_floor': float(np.max(np.abs(rho_ref_spline(grid)-rstar))),
        }
    return {'native': native, 'common': windows,
            'mesh': {'x_left': float(x[0]), 'x_right': float(x[-1]),
                     'min_spacing': float(np.min(spacing)),
                     'max_spacing': float(np.max(spacing)),
                     'min_rho': float(np.min(rho)),
                     'max_rho': float(np.max(rho))}}


def run(space: str, method: str, dt: float, ref: Soliton):
    system, z0 = make_system(space, ref)
    tic = perf_counter()
    result = solve(system, z0, 0., TIMES[-1], dt, method,
                   outputs=(0., *TIMES), strict=False)
    seconds = perf_counter() - tic
    row = {'space': space, 'method': method, 'dt_requested': dt,
           'status': result.status, 'reached': float(result.t[-1]),
           'seconds': seconds, 'accepted_steps': result.accepted,
           'rejected_steps': result.rejected, 'failure_reason': result.failure_reason,
           'observations': {}}
    for t, z in zip(result.t[1:], result.states[1:]):
        if any(abs(t-s)<1e-12 for s in TIMES):
            row['observations'][str(float(t))] = evaluate(ref, system, float(t), z, space)
    return row, result.states[-1].copy() if result.status == 'completed' else None


def first_checks(ref):
    rows=[]
    for space in SPACES:
        system, z0=make_system(space,ref)
        f=system.fields(0.,z0)
        x=f['x'];u=f['u'];rho=f['rho']
        ue,re,_=ref.continuous_x(x,0.)
        if space == 'fixed_difference':
            density_initial=float(np.max(np.abs(rho-re)))
            mass_residual=None
        else:
            density_initial=float(np.max(np.abs(rho-ref.continuous_density_cell_mean(x[:-1],x[1:],0.))))
            mass_residual=float(np.max(np.abs(rho*f['d']-.02)))
        rows.append({'space':space,'initial_u_linf':float(np.max(np.abs(u-ue))),
                     'initial_rho_native_linf':density_initial,
                     'initial_mass_reconstruction_residual':mass_residual,
                     'initial_left':float(x[0]),'initial_right':float(x[-1])})
    return rows


def main():
    ref=Soliton((5.,),c=1.)
    references={};reference_rows=[]
    for space in SPACES:
        print('reference',space,flush=True)
        row,z=run(space,'rk8',REF_DT,ref)
        if row['status']!='completed' or row['rejected_steps']:
            raise RuntimeError('Reference failed: '+space+' '+row['failure_reason'])
        references[space]=z
        reference_rows.append(row)
    rows=[]
    for space in SPACES:
        for method in METHODS:
            for dt in DTS:
                print(space,method,dt,flush=True)
                row,z=run(space,method,dt,ref)
                if z is not None:
                    row['temporal_state_linf']=float(np.max(np.abs(z-references[space])))
                else:
                    row['temporal_state_linf']=None
                rows.append(row)
    source_files = [HERE/'run_factorial.py', HS/'hs_exact.py',HS/'hs_fixed.py',HS/'hs_solver.py']
    report={'definition': '3 spatial models x 4 time methods; 4 requested dt each',
            'system': {'branch': '2HS negative-mu smooth one-soliton',
                       'c':1,'p':5,'q':1.25,'phase':0,'shift':0,
                       'initial_time':0,'X_range_moving':[-4,4],
                       'x_range_fixed':[-4,4], 'moving_a':.02,
                       'physical_edge_budget':400,'fixed_dx':.02,
                       'points':401,'observe_times':TIMES,
                       'main_dt':MAIN_DT,'time_steps':DTS,'reference_dt':REF_DT,
                       'reference_method':'fixed-step DOP853 8th-order main step',
                       'core_window':[-2,2],'full_window':[-3.5,3.5],
                       'fixed_boundary':'two exact time-dependent endpoint u values and rho/m ghost data',
                       'moving_boundary':'exact time-dependent left u; moving left x',
                       'initial':'same continuous soliton sampled on each method natural grid'},
            'initial_checks':first_checks(ref),
            'reference_runs':reference_rows,'rows':rows,
            'runtime':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__},
            'source_sha256':{str(p.relative_to(HERE.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in source_files}}
    out=OUT/'factorial_results.json'
    out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print('Wrote',out,'rows',len(rows),flush=True)


if __name__=='__main__':
    main()
