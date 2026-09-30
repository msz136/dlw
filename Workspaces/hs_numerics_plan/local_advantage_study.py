"""Compare genuine moving-grid time integration on uniform/adapted labels.

The monitor is computed from the continuous initial profile. Each chosen label
is then evolved by the ordinary 2-HS moving-grid ODE; no exact interior values
are injected after t=0. This tests a solution-guided initial mesh, not dynamic
remeshing or preservation of the integrable semi-discrete lattice.
"""
import json
from pathlib import Path
from time import perf_counter

import numpy as np
from scipy.integrate import cumulative_trapezoid

from hs_exact import Soliton
from hs_solver import MovingSystem, solve

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'out'
OUT.mkdir(exist_ok=True)


class NonuniformMovingSystem(MovingSystem):
    def __init__(self, mass, c, left_u):
        self.mass = np.asarray(mass)
        super().__init__(float(np.mean(mass)), c, len(mass), left_u, kind='fd')

    def fields(self, t, z):
        f = super().fields(t, z)
        f['rho'] = self.mass / f['d']
        return f

    def rhs(self, t, z):
        f = self.fields(t, z)
        v, d, u, rho = f['v'], f['d'], f['u'], f['rho']
        w = v / d
        dw = .5*w*w + 2*(u[1:] + u[:-1]) + .5*self.c**2*(rho*rho - 1)
        return self.pack(d*dw-w*v, -v, -float(self.left_u(t)))


def labels(ref, n, gamma):
    Xd = np.linspace(-4, 4, 4001)
    u, x, rho = ref.continuous_X(Xd, 0)
    uxx = np.gradient(np.gradient(u, x), x)
    rxx = np.gradient(np.gradient(rho, x), x)
    monitor = 1 + gamma*(abs(uxx)/max(abs(uxx)) + abs(rxx)/max(abs(rxx)))/2
    measure = np.r_[0., cumulative_trapezoid(monitor, Xd)]
    return np.interp(np.linspace(0, measure[-1], n), measure, Xd)


def run_case(p, n, gamma, T, dt=.001):
    ref = Soliton((float(p),))
    X = labels(ref, n, gamma)
    a = np.diff(X)
    u0, x0, _ = ref.continuous_X(X, 0)
    system = NonuniformMovingSystem(a, ref.c,
                                     lambda t: float(ref.continuous_X(np.array([X[0]]), t)[0][0]))
    z0 = system.pack(np.diff(u0), np.diff(x0), x0[0])
    start = perf_counter()
    result = solve(system, z0, 0, T, dt, 'rk4', strict=False)
    f = system.fields(result.t[-1], result.states[-1])
    ue, _, _ = ref.continuous_x(f['x'], result.t[-1])
    re = ref.continuous_density_cell_mean(f['x'][:-1], f['x'][1:], result.t[-1])
    ec = .5*(f['x'][1:]+f['x'][:-1])
    node_core = abs(f['x']) <= 1
    edge_core = abs(ec) <= 1
    common_x=np.linspace(-2.5,2.5,2001)
    common_ue,common_re,_=ref.continuous_x(common_x,result.t[-1])
    common_un=np.interp(common_x,f['x'],f['u'])
    common_rn=np.interp(common_x,ec,f['rho'])
    common_core=abs(common_x)<=1
    return {'p':p, 'n':n, 'gamma':gamma, 'T':T, 'dt':dt,
            'status':result.status, 'reached':float(result.t[-1]),
            'seconds':perf_counter()-start,
            'max_initial_mass':float(max(a)), 'min_initial_mass':float(min(a)),
            'min_final_edge':float(min(f['d'])),
            'u_linf':float(max(abs(f['u']-ue))),
            'rho_linf':float(max(abs(f['rho']-re))),
            'u_core_linf':float(max(abs(f['u'][node_core]-ue[node_core]))),
            'rho_core_linf':float(max(abs(f['rho'][edge_core]-re[edge_core]))),
            'u_l2':float(np.sqrt(np.mean((f['u']-ue)**2))),
            'rho_l2':float(np.sqrt(np.mean((f['rho']-re)**2))),
            'u_common_linf':float(max(abs(common_un-common_ue))),
            'rho_common_linf':float(max(abs(common_rn-common_re))),
            'u_common_core_linf':float(max(abs(common_un[common_core]-common_ue[common_core]))),
            'rho_common_core_linf':float(max(abs(common_rn[common_core]-common_re[common_core])))}


def main():
    rows = []
    for p in (4.5, 5., 5.5):
        for n in (101, 201):
            for T in (.1, .25, .5):
                for gamma in (0., 2., 5., 10.):
                    row=run_case(p,n,gamma,T)
                    rows.append(row)
                    print(f"p={p:g} n={n} T={T:g} gamma={gamma:g} "
                          f"u={row['u_core_linf']:.3g} rho={row['rho_core_linf']:.3g}", flush=True)
    (OUT/'local_advantage.json').write_text(json.dumps({
        'experiment':'Ordinary nonuniform moving-grid time integration from exact continuous initial fields.',
        'monitor':'Initial two-field curvature monitor 1+gamma*(normalized |u_xx|+normalized |rho_xx|)/2.',
        'common_setup':'Same X endpoints, node count, initial physical solution, left boundary, RK4 dt=0.001 and final time within each pair.',
        'common_physical_metric':'Interpolate numerical node u and edge-center rho linearly to the same 2001 physical locations in [-2.5,2.5], then compare with continuous exact point fields.',
        'rows':rows},indent=2),encoding='utf-8')


if __name__=='__main__':
    main()
