"""Single-soliton completion using the verified common-u/v SD2 boundary.

Runtime adapters only; all imported production sources and old data stay intact.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
os.environ.setdefault('OMP_NUM_THREADS', '1')
import sys
import json
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np
from scipy.special import expit

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
sys.path.insert(0, str(BASE/'dlw_sd2_uv_init_20260929'))
import consistent_sd2 as consistent
import models
from reference import TwoExact, Case
import run_experiments as runner
from parametric import rk4
io = runner.previous
CASES = {'fig1a': Case((1.,), (2.,), c=(1.,), phases=(0.,)),
         'fig1b': Case((4.,), (-3.,), c=(1.,), phases=(0.,))}


class SingleExact(TwoExact):
    def __init__(self, case, h, continuous=True):
        self.case, self.h, self.continuous = case, h, continuous
        self.pars = io.pm.Parameters(a=case.a, p=case.p[0], q=case.q[0], rho=1.)
        self.legacy = io.PaperExact(self.pars, h, continuous)
        g = self.legacy
        self.S = np.array([g.S]); self.T = np.array([g.omega]); self.Y = np.array([g.ry])
        self.gamma = np.array([g.gamma0]); self.gammah = np.array([g.gamma]); self.chi = np.array([g.chi])
        self.rates = np.array([[0., 0., 0.], [g.S, g.omega, g.ry]])
        self.qjump, self.rjump = np.expm1(g.gamma0), np.expm1(-g.gamma0)
        self._cache_key = None; self._cache = {}

    def tau(self, js, x, t, is_f=False):
        j = np.atleast_1d(js)[:, None]; x = np.atleast_1d(x)[None, :]
        g = self.legacy
        phase = (j+.5)*self.h*g.ry if self.continuous else j*g.chi
        z = g.S*x + g.omega*t + phase - np.log(g.S)
        if is_f: z = z + (g.gamma0 if self.continuous else g.gamma)
        l = np.logaddexp(0., z)
        return l, np.stack((expit(-z), expit(z)))

    def uv(self, js, x, t, derivative=False):
        # Exact same physical input as the existing SD/FD single-soliton runs.
        return self.legacy.uv(js, x, t, derivative)


# The two-soliton implementation uses this factory only for analytic data.
models.TwoExact = SingleExact
models.CASES.update(CASES)
Problem = consistent.Problem
OUT = HERE/'out'
OUT.mkdir(exist_ok=True)


def plan():
    ans = []
    for method in ('RK4', 'Euler'):
        variants = ['main', 'time_half', 'x_half', 'y_half', 'domain_double', 'x_half_time_half']
        if method == 'Euler': variants += ['time_quarter']
        for variant in variants:
            n, L, h, dt = 256, 40., .125, .000125
            if variant == 'time_half': dt /= 2
            if variant == 'time_quarter': dt /= 4
            if variant.startswith('x_half'): n *= 2; dt /= 2
            if variant == 'x_half_time_half': dt /= 2
            if variant == 'y_half': h /= 2
            if variant == 'domain_double': n *= 2; L *= 2
            for case in CASES:
                for model in ('SD', 'SD2', 'FD'):
                    for mesh in ('fixed', 'moving'):
                        ans.append(dict(method=method, case=case, model=model, mesh=mesh,
                                        variant=variant, nx=n, L=L, h=h, dt=dt, T=.02, eval_half=10.))
    return ans


def euler(fun, t, z, dt): return z + dt*fun(t, z)


def one(s):
    runner.OUT = OUT/s['method']; runner.OUT.mkdir(exist_ok=True)
    runner.rk4 = euler if s['method'] == 'Euler' else rk4
    holder = []
    def factory(spec):
        p = Problem(spec); holder.append(p); return p
    runner.Problem = factory
    r = runner.one(s)
    if s['model'] == 'SD2':
        m = holder[0].m
        r['initialization'] = m.lift_diagnostics
        r['boundary_solve_max_residual'] = m.boundary_max_residual
        r['boundary_solves'] = m.boundary_solves
    r['origin'] = 'new'
    return r


def source_paths():
    return [Path(__file__), HERE/'verify.py', HERE/'implementation_checks.json',
            BASE/'dlw_sd2_uv_init_20260929/consistent_sd2.py',
            BASE/'dlw_two_soliton_20260929/models.py', BASE/'dlw_two_soliton_20260929/reference.py',
            BASE/'dlw_two_soliton_20260929/run_experiments.py', BASE/'dlw_sd2_20260929/sd2.py',
            BASE/'dlw_paper_cases_20260927/run.py',
            *[io.LIB/f for f in ('parametric.py','parametric_open.py','moving_mesh.py','dynamics.py','solver.py')],
            BASE/'dlw_time_curves_20260928/out/results.json']


def main():
    pp = plan()
    sources = {str(p): io.sha(p) for p in source_paths()}
    path = OUT/'results.json'
    if path.exists():
        data = json.loads(path.read_text(encoding='utf-8'))
        assert data['sources'] == sources and data['plan'] == pp
    else:
        oldpath = BASE/'dlw_time_curves_20260928/out/results.json'
        old = json.loads(oldpath.read_text(encoding='utf-8'))
        for p, digest in old['sources'].items(): assert io.sha(p) == digest, p
        runs = []
        for r in old['runs']:
            assert io.sha(r['profile']) == r['profile_sha256']
            s = dict(r['spec'], method='RK4', model={'structure':'SD','fd':'FD'}[r['spec']['model']], eval_half=10.)
            assert s in pp
            runs.append(dict(r, spec=s, origin='reused', original_manifest=str(oldpath)))
        data = dict(plan=pp, sources=sources, runs=runs,
                    parameters={k:vars(v) for k,v in CASES.items()},
                    scope='Single solitons Fig1a/b; common u/v and compatible lower u boundary; no report edits')
        io.dump(path, data)
    todo = [s for s in pp if not any(r['spec']==s for r in data['runs'])]
    with ProcessPoolExecutor(max_workers=2) as pool:
        fs = {pool.submit(one,s):s for s in todo}
        for f in as_completed(fs):
            r = f.result(); data['runs'].append(r); io.dump(path,data)
            print(len(data['runs']), '/'+str(len(pp)), r['spec'], r['status'], flush=True)
    assert len(data['runs']) == len(pp)
    print('DONE', len(pp), flush=True)


if __name__ == '__main__': main()
