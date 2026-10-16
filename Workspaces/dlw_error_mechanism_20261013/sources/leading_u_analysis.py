"""Analytic leading source coefficients for the reconstructed physical u.

No PDE evolution or fitted coefficients. Log-tau derivatives are cumulants
of the exact finite exponential sum. Compare to the existing exact residual.
"""
from pathlib import Path
import csv
import json
from math import comb
import numpy as np
from common_sources import load_solver, source_parts, exact_jets

HERE = Path(__file__).resolve().parent


def log_jets(obj, js, x, t, is_f, order=5):
    _, weights = obj.G.tau(js, x, t, is_f)
    rates = obj.G.rates[:, (0, 2)]
    means = [np.einsum('a,ajk->jk', rates[:, k], weights) for k in (0, 1)]
    centered = [rates[:, k, None, None] - means[k] for k in (0, 1)]
    powers = [[np.ones_like(weights)] for _ in range(2)]
    for k in (0, 1):
        for n in range(1, order + 1):
            powers[k].append(powers[k][-1] * centered[k])
    moments, cumulants = {(0, 0): np.ones(weights.shape[1:])}, {}
    for n in range(1, order + 1):
        for a in range(n + 1):
            b = n - a
            moments[a, b] = np.sum(weights * powers[0][a] * powers[1][b], axis=0)
            value = moments[a, b].copy()
            if a:
                for i in range(1, a + 1):
                    for j in range(b + 1):
                        if (i, j) == (a, b):
                            continue
                        value -= comb(a - 1, i - 1) * comb(b, j) * cumulants[i, j] * moments[a - i, b - j]
            else:
                for j in range(1, b):
                    value -= comb(b - 1, j - 1) * cumulants[0, j] * moments[0, b - j]
            cumulants[a, b] = value
    cumulants[1, 0] = means[0]
    cumulants[0, 1] = means[1]
    return cumulants


def coefficients(obj, js, x, t):
    f, g = [log_jets(obj, js, x, t, is_f) for is_f in (True, False)]
    u, ux, uxx, uxxx = [2 * (f[n, 0] - g[n, 0]) for n in (1, 2, 3, 4)]
    v_xxy = 2 * (f[3, 2] + g[3, 2])
    u_xxyy = 2 * (f[3, 2] - g[3, 2])
    W, Wx = 4 * g[1, 1], 4 * g[2, 1]
    Kx = (W / 16 - 1 / 4) * Wx
    delta = lambda a: a[1:] - a[0]
    Ay_fd = delta(-v_xxy / 12)
    reconstruct = delta(u_xxyy / 4)
    flux = -delta(Kx)
    Ay_pe = Ay_fd + reconstruct + flux
    Hxxx = 3 * ux * uxx + (u + 2 * obj.a) * uxxx
    Bx = -delta(Hxxx + f[5, 0] + g[5, 0]) / 6
    # Existing analytic first/second x derivatives independently check conventions.
    old = exact_jets(obj, t, x=x, js=js)
    convention = max(float(np.max(np.abs(old[k] - value))) for k, value in
                     [('u', u), ('ux', ux), ('uxx', uxx)])
    return {'FD': Ay_fd, 'SD': Ay_pe, 'x': Bx, 'flux': flux,
            'reconstruction': reconstruct, 'convention_linf': convention}


def rms(a):
    return float(np.sqrt(np.mean(a * a)))


def cosine(a, b):
    return float(np.mean(a * b) / (rms(a) * rms(b)))


def main():
    ns, _ = load_solver()
    rows, comparisons, derivatives = [], [], []
    for case in ('A', 'C'):
        cfg = ns['case_config'](case)
        obj = ns['SDModel'](case, 'FD', cfg)
        iy = np.flatnonzero(np.abs(obj.y) < cfg['eval_yhalf'])
        ix = np.flatnonzero(np.abs(obj.X.x) <= cfg['eval_half'] + 1e-10)
        js, x = np.r_[obj.js[0], obj.js[iy]], obj.X.x[ix]
        coef = coefficients(obj, js, x, 0.)
        derivatives.append({'case': case, 'convention_linf': coef['convention_linf']})
        # Check the fifth x / third x second y cumulants as x derivatives of fourth jets,
        # on a fixed small set of physical nodes, using two independent centered steps.
        sample_js, sample_x = js[[0, len(js)//2, -1]], x[[len(x)//3, len(x)//2, 2*len(x)//3]]
        for is_f in (True, False):
            exact = log_jets(obj, sample_js, sample_x, 0., is_f)
            for step in (.001, .0005):
                plus = log_jets(obj, sample_js, sample_x + step, 0., is_f, order=4)
                minus = log_jets(obj, sample_js, sample_x - step, 0., is_f, order=4)
                for target, lower in [((5, 0), (4, 0)), ((3, 2), (2, 2))]:
                    est = (plus[lower] - minus[lower]) / (2 * step)
                    derivatives.append({'case': case, 'tau': 'f' if is_f else 'g',
                                        'derivative': str(target), 'step': step,
                                        'relative_error': rms(est - exact[target]) / max(rms(exact[target]), 1e-30)})
        for kind in ('SD', 'FD'):
            model = ns['SDModel'](case, kind, cfg)
            exact = source_parts(model, 0., details=True)['fields']
            sy, sx = cfg['h']**2 * coef[kind], obj.X.dx**2 * coef['x']
            exact_y, exact_x, exact_total = [exact[s]['u'][np.ix_(iy, ix)] for s in ('y_model', 'x_stencil', 'total')]
            rows.append({'case': case, 'method': kind, 'field': 'u', 't': 0.,
                         'rms_y_leading': rms(sy), 'rms_x_leading': rms(sx),
                         'cosine_leading': cosine(sy, sx), 'rms_total_leading': rms(sy + sx),
                         'rms_total_exact': rms(exact_total), 'cross_energy_leading': float(2 * np.mean(sy * sx)),
                         'rms_PE_flux_correction': rms(cfg['h']**2 * coef['flux']),
                         'rms_PE_reconstruction_correction': rms(cfg['h']**2 * coef['reconstruction'])})
            for source, leading, truth in [('y', sy, exact_y), ('x', sx, exact_x), ('total', sy + sx, exact_total)]:
                comparisons.append({'case': case, 'method': kind, 'source': source,
                                    'relative_field_difference': rms(leading - truth) / rms(truth),
                                    'cosine': cosine(leading, truth)})
        np.savez_compressed(HERE / f'leading_u_{case}.npz', x=x, y=obj.y[iy],
                            y_FD=cfg['h']**2 * coef['FD'], y_PE=cfg['h']**2 * coef['SD'],
                            x_common=obj.X.dx**2 * coef['x'])
        print('completed', case, flush=True)
    for filename, data in [('leading_u_budget.csv', rows), ('leading_u_comparison.csv', comparisons)]:
        with (HERE / filename).open('w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=list(data[0])); w.writeheader(); w.writerows(data)
    result = {'scope': 'Leading joint h/k expansion of instantaneous u source at t=0; not terminal error.',
              'derivative_checks': derivatives, 'field_comparisons': comparisons,
              'passed': max(x['relative_field_difference'] for x in comparisons) < .05
                        and max(x.get('relative_error', 0) for x in derivatives) < .001}
    (HERE / 'leading_u_validation.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
