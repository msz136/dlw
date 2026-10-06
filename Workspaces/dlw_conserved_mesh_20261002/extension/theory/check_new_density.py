"""Independent initial-field and finite-h flux checks; no PDE evolution."""
from pathlib import Path
import hashlib
import json
import sys

import numpy as np

HERE = Path(__file__).resolve().parent
EXT = HERE.parent
sys.path.insert(0, str(EXT))
import baseline
import candidates


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def one(case, model, mesh, nx, h):
    spec = dict(case=case, model=model, mesh=mesh, motion='moving',
                variant='check', nx=nx, h=h, dt=2.5e-5, T=.01)
    p = candidates.CandidateProblem(spec)
    z = p.initial()
    P, Q, u, v, du, gh = p.unpack(z, 0.)
    ue, ve = p.G.uv(p.y, p.X.x, 0.)
    Pt, Qt = p.physical_rhs(P, Q, u, v, du, gh)
    density, flux = p.density_flux(P, Q, u, v, du)

    # This direct q0 formula is independent of the candidate's call to
    # super().density_flux. It retains the exact finite-h SD correction.
    if model == 'SD':
        W = Q
        H = .5*u*u + 2*p.a*u + h*h*(W*W/32-W/4)
        dH = (H[2:]-H[:-2])/(2*h)
        lapW = (W[2:]-2*W[1:-1]+W[:-2])/(h*h)
        direct_q0 = -(dH+(u[1:-1]+2*p.a)*W[1:-1]-4*u[1:-1]
                      + p.X.d1(du[1:-1]+h*h*lapW/4))/4
        # Interior delta0 u_t is the average of the two evolved delta- u
        # variables. It requires no analytic future field or boundary u_t.
        vt = Qt[1:-1] + .5*(Pt[1:]+Pt[:-1])
    else:
        direct_q0 = -((u[1:-1]+2*p.a)*v[1:-1]-4*u[1:-1]
                      + p.X.d1(du[1:-1]))/4
        vt = Qt[1:-1]
    direct_q0 = p.monitor_weights @ direct_q0
    physical_excess = p.monitor_weights @ (-v[1:-1]/4)
    rt0 = p.monitor_weights @ (-vt/4)
    if mesh == 'mass':
        direct_density, direct_flux, density_t = physical_excess, direct_q0, rt0
    else:
        direct_density, direct_flux, density_t = 1+4*physical_excess, 4*direct_q0, 4*rt0

    errors = {
        'initial_u': float(abs(u-ue).max()),
        'initial_v': float(abs(v-ve).max()),
        'initial_P': float(abs(P-np.diff(ue, axis=0)/h).max()),
        'density_formula': float(abs(density-direct_density).max()),
        'finite_h_flux_formula': float(abs(flux-direct_flux).max()),
        'finite_h_interior_conservation': float(abs(density_t+p.X.d1(flux)).max()),
    }
    assert max(errors.values()) < 2e-10, (spec, errors)
    assert density.min() > 0 and p.X.J.min() > 0 and np.diff(p.X.x).min() > 0
    return dict(spec=spec, errors=errors, min_R=float(density.min()),
                min_J=float(p.X.J.min()), min_dx=float(np.diff(p.X.x).min()))


def main():
    before = {name: sha(EXT/name) for name in ('baseline.py', 'candidates.py')}
    rows = [one(case, model, mesh, nx, h)
            for case in baseline.CASES for model in ('SD', 'FD')
            for mesh in ('mass', 'strong') for nx, h in ((33, .125), (65, .0625))]
    after = {name: sha(EXT/name) for name in before}
    assert before == after
    record = dict(date='2026-10-02', scope='Initial and interior algebra checks; no PDE evolution',
                  source_sha256=before, checker_sha256=sha(__file__), passed=len(rows), checks=rows,
                  max_errors={key: max(r['errors'][key] for r in rows) for key in rows[0]['errors']},
                  source_unchanged=True)
    target = HERE/'new_density_validation.json'
    target.write_text(json.dumps(record, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(passed=record['passed'], max_errors=record['max_errors'],
                         saved=str(target)), ensure_ascii=False))


if __name__ == '__main__':
    main()
