"""Independent saved-array audit; no evolution or report generation."""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
ROOT = PROJECT.parents[1]
SPATIAL = PROJECT / 'spatial_audit_20261023'
sys.path.insert(0, str(SPATIAL))
from run import Model, HALF_WIDTHS


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def exact_rate(m):
    pieces = []
    for isf in (True, False):
        _, weights = m.G.tau(m.y/m.h-.5, m.x, 0., isf)
        sx, st, sy = [m.G.rates[:, j, None, None] for j in range(3)]
        avg = lambda z: np.sum(weights*z, axis=0)
        ut = avg(sx*st)-avg(sx)*avg(st)
        vt = (avg(sx*sy*st)-avg(sx*sy)*avg(st)-avg(sx*st)*avg(sy)
              -avg(sy*st)*avg(sx)+2*avg(sx)*avg(sy)*avg(st))
        pieces.append((ut, vt))
    return np.array([2*(pieces[0][0]-pieces[1][0]),
                     2*(pieces[0][1]+pieces[1][1])])


def initial_rhs(m, z):
    # Assemble the documented CSD0 equations without calling Model.rhs.
    u, v = z
    h, a = m.h, m.a
    freq = 2*np.pi*np.fft.rfftfreq(m.nx, m.dx)
    p1 = 1j*freq
    p1[-1] = 0
    d1 = lambda q: np.fft.irfft(np.fft.rfft(q, axis=-1)*p1, n=m.nx, axis=-1)
    d2 = lambda q: np.fft.irfft(np.fft.rfft(q, axis=-1)*(-freq**2), n=m.nx, axis=-1)
    sites = np.r_[m.y[0]-h, m.y[0], m.y[-3:], m.y[-1]+h]
    b = m.profile(sites, 0.)[0]
    bt = m.ut(sites, 0.)

    def delta0(q, background):
        e = q[-3:]-background[-4:-1]
        right = background[-1]+3*e[-1]-3*e[-2]+e[-3]
        ext = np.concatenate((background[:1], q, right[None]))
        return (ext[2:]-ext[:-2])/(2*h)

    w = v-delta0(u, b)
    H = u*u/2+2*a*u+h*h*(w*w/32-w/4)
    derivative_difference = -np.diff(d1(H), axis=0)/h-d2(np.diff(u, axis=0)/h+(w[1:]+w[:-1])/2)
    ut = np.concatenate((bt[1:2], bt[1:2]+h*np.cumsum(derivative_difference, axis=0)))
    vt = delta0(ut, bt)-d1((u+2*a)*w-4*u)+d2(w)
    return np.array([ut, vt])


def norm(m, difference):
    mx = np.abs(m.x) <= HALF_WIDTHS[m.case]
    my = np.abs(m.y) < HALF_WIDTHS[m.case]
    return [float(np.max(np.abs(q[my][:, mx]))) for q in difference]


def maxdiff(a, b):
    return float(np.max(np.abs(np.asarray(a)-np.asarray(b))))


def audit(case):
    path = HERE/f'{case}_CSD0_RK4.json'
    record = json.loads(path.read_text())
    initial_record = json.loads((HERE/f'{case}_CSD0_initial.json').read_text())
    m = Model(case, 'Centered-SD', .1, .1)
    with np.load(path.with_suffix('.npz')) as data:
        assert record['status'] == 'complete'
        assert (record['h'], record['dx'], record['dt'], record['T'], record['reached']) == (.1, .1, 1e-4, .01, .01)
        assert record['method'] == 'CSD0' and record['integrator'] == 'RK4'
        assert record['artifact_sha256'] == sha(path.with_suffix('.npz'))
        assert initial_record['artifact_sha256'] == record['artifact_sha256']
        for source in record['sources']:
            assert sha(ROOT/source['path']) == source['sha256'], source['path']
        for name, expected in (('x', m.x), ('y', m.y), ('yv', m.y)):
            assert np.array_equal(data[name], expected), name
        assert np.array_equal(data['z'], np.array([data['u'], data['v']]))
        assert np.array_equal(data['z0'], np.array([data['u0'], data['v0']]))
        assert np.isfinite(data['z']).all()

        reference0 = m.profile(m.y, 0.)
        reference = m.profile(m.y, .01)
        rate_reference = exact_rate(m)
        rate = initial_rhs(m, data['z0'])
        initial_error = norm(m, data['z0']-reference0)
        initial_derivative_error = norm(m, data['initial_rate']-rate_reference)
        final_error = norm(m, data['z']-reference)
        out = dict(case=case, initial_physical_error=initial_error,
                   initial_derivative_error=initial_derivative_error, final_error=final_error,
                   initial_record_difference=maxdiff(initial_derivative_error, initial_record['total']),
                   final_record_difference=maxdiff(final_error, record['error']),
                   initial_rhs_independent_assembly_difference=maxdiff(rate, data['initial_rate']),
                   initial_reference_difference=maxdiff(reference0, data['reference0']),
                   initial_derivative_reference_difference=maxdiff(rate_reference, data['reference_rate']),
                   final_reference_difference=maxdiff(reference, data['reference']),
                   shape=list(data['z'].shape), artifact_sha256=sha(path.with_suffix('.npz')))
        assert max(initial_error) == 0.
        assert out['initial_record_difference'] < 1e-12
        assert out['final_record_difference'] == 0.
        assert out['initial_rhs_independent_assembly_difference'] < 1e-11
        assert out['initial_reference_difference'] == 0.
        assert out['initial_derivative_reference_difference'] < 1e-12
        assert out['final_reference_difference'] == 0.
        return out


if __name__ == '__main__':
    audits = [audit(case) for case in 'ABCD']
    result = dict(status='passed', records=4, audits=audits,
                  max_initial_record_difference=max(a['initial_record_difference'] for a in audits),
                  max_final_record_difference=max(a['final_record_difference'] for a in audits),
                  max_initial_rhs_assembly_difference=max(a['initial_rhs_independent_assembly_difference'] for a in audits),
                  scope='Independent saved-array, reference and initial-RHS assembly checks; native-grid sampled maxima.')
    (HERE/'independent_saved_audit.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k != 'audits'}))
