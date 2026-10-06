"""Matched conservative flux identity at perturbed discrete states."""
import sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
import experiment as e


def main():
    checks = []
    for case in e.CASES:
        for model in ('SD', 'FD'):
            s = dict(case=case, model=model, mesh='minus', motion='frozen', nx=33,
                     h=.125, dt=5e-6, T=.001, variant='audit')
            p = e.Problem(s)
            state = p.initial()
            state[:p.np+p.nq] += 1e-5*np.random.default_rng(23).normal(size=p.np+p.nq)
            P, Q, u, v, du, gh = p.unpack(state, 0.)
            Pt, Qt = p.physical_rhs(P, Q, u, v, du, gh)
            bt = p.G.uv([p.y[0]], p.X.x, 0., derivative=True)[0][0]
            ut = np.vstack((bt, bt[None, :]+p.h*np.cumsum(Pt, axis=0)))
            gt = p.G.uv([p.y[0]-p.h, p.y[-1]+p.h], p.X.x, 0., derivative=True)[0]
            # Upper-ghost closure does not enter the fixed interior monitor band.
            dut = p.dy(ut, gt)
            vt = Qt+dut if model == 'SD' else Qt
            for name, sigma in (('minus', -1), ('zero', 0), ('plus', 1)):
                R, flux = p.density_flux(P, Q, u, v, du, name)
                Rt = p.monitor_weights @ (-(vt[1:-1]+sigma*dut[1:-1])/4)
                err = float(abs((Rt+p.X.d1(flux))[1:-1]).max())
                checks.append(dict(case=case, model=model, density=name,
                                   interior_semidiscrete_identity_residual=err))
    maximum = max(r['interior_semidiscrete_identity_residual'] for r in checks)
    assert maximum < 1e-10
    result = dict(source_sha256=e.sha(ROOT/'experiment.py'), checks=checks,
                  max_residual=maximum,
                  scope='Actual conservative spatial flux identity at a perturbed state, interior y monitor band and interior x nodes; no RK or moving-grid mass-conservation claim.')
    e.dump(HERE/'flux_identity_checks.json', result)
    print('flux checks', len(checks), 'max residual', maximum)


if __name__ == '__main__':
    main()
