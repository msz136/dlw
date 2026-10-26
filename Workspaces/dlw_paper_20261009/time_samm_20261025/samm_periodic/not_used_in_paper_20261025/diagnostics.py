"""Supporting measurements quoted in Section 5.4 of the manuscript.

Wave translation, band occupation of the error, displacement of the exact
equidistributed mesh, and the reductions measured in the discrete root-mean-square
norm. All values are recomputed from the recorded runs and the exact solutions.
"""
from pathlib import Path
import sys, json
import numpy as np
from scipy.integrate import cumulative_trapezoid

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'spatial_audit_20261023'))
from run import Model, HALF_WIDTHS

T = 0.01


def state_w(m, x, t):
    u = m.profile(m.y, t, x)[0]
    yv = (m.y[1:] + m.y[:-1]) / 2
    v = m.profile(yv, t, x)[1]
    _, g = m.G.tau(m.y[:1] / m.h - .5, x, t, False)
    w = np.empty_like(u)
    w[0] = 4 * m.G.cov(g, 0, 2)[0]
    r = 2 * (v - np.diff(u, axis=0) / m.h)
    for k in range(1, len(u)):
        w[k] = r[k - 1] - w[k - 1]
    return w


def equidistributed(m, t, nfine=20001):
    fine = np.linspace(-m.half, m.half, nfine)
    dens = np.empty(nfine)
    for i in range(0, nfine, 2000):
        sl = slice(i, min(i + 2000, nfine))
        dens[sl] = (1 - state_w(m, fine[sl], t) / 4).mean(axis=0)
    mass = np.r_[0, cumulative_trapezoid(dens, fine)]
    return np.interp(np.arange(m.nx) / m.nx * mass[-1], mass, fine)


out = {}
for case, band in (('A', 4.0), ('D', 22.0)):
    m = Model(case, 'Centered-SD', .1, .1)
    r = HALF_WIDTHS[case]
    fine = np.linspace(-r, r, 20001)
    j = int(np.argmin(abs(m.y)))
    pos = {}
    for t in (0., T):
        u = m.profile(m.y[j:j + 1] * 0 + m.y[j], t, fine)[0][0]
        pos[t] = float(fine[int(np.argmin(u))])
    n0, n1 = equidistributed(m, 0.), equidistributed(m, T)
    rec = dict(band_half_width=band,
               wave_x_position_at_0=pos[0.], wave_x_position_at_T=pos[T],
               wave_translation=abs(pos[0.] - pos[T]),
               exact_mesh_displacement_max=float(abs(n1 - n0).max()),
               exact_mesh_displacement_mean=float(abs(n1 - n0).mean()))
    for mode in ('uniform', 'moving'):
        d = np.load(HERE / f'{case}_{mode}_0.0001.npz')
        x = d['x']
        yv = (m.y[1:] + m.y[:-1]) / 2
        sel = abs(x) <= r
        ku, kv = abs(m.y) < r, abs(yv) < r
        eu, ev = m.profile(m.y, T, x)[0][ku][:, sel], m.profile(yv, T, x)[1][kv][:, sel]
        nu, nv = d['u'][ku][:, sel], d['v'][kv][:, sel]
        inb = abs(x) <= band
        prof = np.abs(d['u'] - m.profile(m.y, T, x)[0])[ku].max(axis=0)
        rec[mode] = dict(
            nodes_in_band=int(inb.sum()), nodes_total=int(len(x)),
            max_error_in_band=float(prof[inb].max()), max_error_outside=float(prof[~inb].max()),
            rms_u=float(np.sqrt(((nu - eu) ** 2).mean())), rms_v=float(np.sqrt(((nv - ev) ** 2).mean())))
        sp = d['spacing']
        rec[mode]['min_spacing_ratio'] = float(sp.min() / 0.1)
        rec[mode]['fraction_cells_compressed'] = float((sp < 0.1 * (1 - 1e-9)).mean())
    u, f = rec['uniform'], rec['moving']
    rec['reduction'] = dict(
        max_u=100 * (1 - f['max_error_in_band'] / u['max_error_in_band']),
        max_v=100 * (1 - np.load(HERE / f'{case}_moving_0.0001.npz')['error_history'][-1][1]
                     / np.load(HERE / f'{case}_uniform_0.0001.npz')['error_history'][-1][1]),
        rms_u=100 * (1 - f['rms_u'] / u['rms_u']), rms_v=100 * (1 - f['rms_v'] / u['rms_v']))
    out[case] = rec

(HERE / 'diagnostics.json').write_text(json.dumps(out, indent=2), encoding='utf-8')
print(json.dumps(out, indent=2))
