"""Independent Arb certificate for stored nondegenerate initial fields/rates.

All binary64 coordinate values and reference values are converted exactly to Arb.
The periodic Gaussian sum includes its omitted infinite tails as ball radii.
Only stored reference evaluations, not numerical spatial RHS, are enclosed here.
"""
from pathlib import Path
import hashlib
import json
import time
import numpy as np
from flint import arb, ctx

HERE = Path(__file__).resolve().parent
METHODS = ('Endpoint-SD', 'CSD0', 'Centered-SD', 'FD')
ctx.dps = 80


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def certify(case):
    started = time.perf_counter()
    paths = [HERE / f'initial_{case}_{method}.npz' for method in METHODS]
    files = [np.load(p) for p in paths]
    xx = files[0]['x']
    assert all(np.array_equal(f['x'], xx) for f in files)
    assert np.max(abs(xx)) <= 96
    yy = np.unique(np.concatenate([f[k] for f in files for k in ('y', 'yv')]))
    pi, one = arb.pi(), arb(1)
    kappa = pi / 4
    # For |x| <= 96, omitted shifts |m| >= 2 start at |x+192m| >= 288.
    # The next Gaussian and polynomial-weighted derivative terms have ratio
    # bounded by (25/9) exp(-4096). Each positive tail is geometrically bounded.
    ratio = arb(25)/9 * (-arb(4096)).exp()
    tail0 = 2 * (-arb(2304)).exp() / (1-ratio)
    tail1 = 2 * arb(16) * (-arb(2304)).exp() / (1-ratio)
    tail2 = 2 * (arb(256)+one/18) * (-arb(2304)).exp() / (1-ratio)
    assert max(tail0, tail1, tail2) < arb('1e-990')
    xr = []
    for xd in xx:
        x = arb(float(xd))
        if case == 'Gaussian':
            ss = [x + 192*m for m in (-1, 0, 1)]
            gg = [(-(s/6)**2).exp() for s in ss]
            f = sum(gg) + arb(0, tail0)
            fx = sum(-s/18*g for s,g in zip(ss, gg)) + arb(0, tail1)
            fxx = sum((s*s/324-one/18)*g for s,g in zip(ss, gg)) + arb(0, tail2)
            amp = arb(1)/20
        else:
            k = pi/12
            f, fx, fxx = (k*x).cos(), -k*(k*x).sin(), -k*k*(k*x).cos()
            amp = arb(3)/100
        xr.append((amp*f, amp*fx, amp*fxx))

    # Gather the actually stored rows, including native positions outside the
    # reporting region. No reference-generating floating-point code is imported.
    values = {float(y): {key: [] for key in ('u','v','ut','vt')} for y in yy}
    for f in files:
        for y, row in zip(f['y'], f['u0_ref']):
            values[float(y)]['u'].append(row)
        for y, row in zip(f['yv'], f['v0_ref']):
            values[float(y)]['v'].append(row)
        for y, row in zip(f['y'], f['ut_ref']):
            values[float(y)]['ut'].append(row)
        for y, row in zip(f['yv'], f['vt_ref']):
            values[float(y)]['vt'].append(row)
    max_bound = {key: arb(0) for key in ('u','v','ut','vt')}
    count = {key: 0 for key in max_bound}
    for yd in yy:
        y = arb(float(yd))
        angle = kappa*(y+2)
        e, ey = angle.sin(), kappa*angle.cos()
        rows = values[float(yd)]
        for i, (p, px, pxx) in enumerate(xr):
            u, ux, uy = e*p, e*px, ey*p
            truth = {'u':u, 'v':4-3*uy,
                     'ut':3*e*pxx-(u+4)*ux,
                     'vt':-ey*pxx+3*(uy*ux+(u+4)*ey*px)}
            for key in ('u','v','ut','vt'):
                for row in rows[key]:
                    err = abs(truth[key]-arb(float(row[i])))
                    assert err < arb('1e-13'), (case, key, yd, xx[i], str(err))
                    if err.upper() > max_bound[key]:
                        max_bound[key] = err.upper()
                    count[key] += 1
    out = dict(case=case, precision_digits=80, nx=len(xx), distinct_y_sites=len(yy),
               certified_stored_values=count, bounds={k:v.str(16) for k,v in max_bound.items()},
               uniform_sample_bound_u='1e-13', uniform_sample_bound_v='1e-13',
               uniform_sample_bound_ut='1e-13', uniform_sample_bound_vt='1e-13',
               coordinates='Exact binary64 values of stored x, y and yv arrays.',
               conversion='Stored binary64 reference values enclosed directly, including evaluation and conversion rounding.',
               gaussian_omitted_jet_bound='1e-990' if case=='Gaussian' else '0',
               sources=[dict(path=p.name, sha256=sha(p)) for p in paths],
               seconds=time.perf_counter()-started)
    print(json.dumps(out), flush=True)
    for f in files:
        f.close()
    return out


if __name__ == '__main__':
    certificate = dict(formulas='u_t=3u_xx-(u+4)u_x; v_t=-u_xxy+3[u_y*u_x+(u+4)u_xy]',
                       data='u0=A sin(pi*(y+2)/4) F(x), v0=4-3u0_y',
                       scope='Analytic continuous initial-reference evaluation at every stored sample.',
                       script_sha256=sha(Path(__file__)),
                       cases=[certify(c) for c in ('Gaussian', 'Sinusoidal')])
    (HERE/'initial_reference_certificate.json').write_text(json.dumps(certificate, indent=2), encoding='utf8')
