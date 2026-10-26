"""Independent formulas and saved-state audit; does not import the runner."""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
H = .1


def jets(case, x, y):
    x = np.asarray(x)
    y = np.asarray(y)
    k = np.pi/4
    if case == 'Gaussian':
        amplitude = .05
        f, fx, fxx = (np.zeros_like(x) for _ in range(3))
        for j in (-1, 0, 1):
            q = x+192*j
            g = np.exp(-q*q/36)
            f += g
            fx += -q*g/18
            fxx += (q*q/324-1/18)*g
    else:
        amplitude = .03
        omega = np.pi/12
        f = np.cos(omega*x)
        fx = -omega*np.sin(omega*x)
        fxx = -omega**2*f
    s = amplitude*np.sin(k*(y+2))[:, None]
    sy = amplitude*k*np.cos(k*(y+2))[:, None]
    u, ux, uxx = s*f, s*fx, s*fxx
    uy, uxy, uxxy = sy*f, sy*fx, sy*fxx
    return dict(u=u, v=4-3*uy, uy=uy,
                ut=3*uxx-(u+4)*ux,
                vt=-uxxy+3*(ux*uy+(u+4)*uxy))


def derivative(f, order):
    omega = 2*np.pi*np.fft.rfftfreq(f.shape[-1], H)
    multiplier = (1j*omega)**order if order >= 0 else np.zeros_like(omega, dtype=complex)
    if order in (1, -1):
        if order == -1:
            multiplier = np.zeros_like(omega, dtype=complex)
            multiplier[1:-1] = 1/(1j*omega[1:-1])
        multiplier[-1] = 0
    return np.fft.irfft(np.fft.rfft(f, axis=-1)*multiplier,
                        n=f.shape[-1], axis=-1)


def physical_v(state):
    u, w = state
    nonlinear = w*w/32-w/4
    return np.diff(u, axis=0)/H+(w[1:]+w[:-1])/2+H*derivative(np.diff(nonlinear, axis=0), -1)


def rhs_initial(case, method, state, x, y):
    u, second = state
    boundary_y = np.r_[y[0]-H, y[0], y[-3:], y[-1]+H]
    initial = jets(case, x, boundary_y)
    b, bt = initial['u'], initial['ut']

    def delta0(values, background):
        right = background[-1]+3*(values[-1]-background[-2])-3*(values[-2]-background[-3])+(values[-3]-background[-4])
        extended = np.concatenate((background[:1], values, right[None]))
        return (extended[2:]-extended[:-2])/(2*H)

    if method in ('Centered-SD', 'CSD0'):
        w = second if method == 'Centered-SD' else second-delta0(u, b)
        flux = u*u/2+4*u+H*H*(w*w/32-w/4)
        coupling = np.diff(u, axis=0)/H+(w[1:]+w[:-1])/2
    else:
        flux = u*u/2+4*u
        coupling = second[1:] if method == 'Endpoint-SD' else (second[1:]+second[:-1])/2
    rate_gradient = -np.diff(derivative(flux, 1), axis=0)/H-derivative(coupling, 2)
    ut = np.concatenate((bt[1:2], bt[1:2]+H*np.cumsum(rate_gradient, axis=0)))
    if method in ('Centered-SD', 'CSD0'):
        wt = derivative(w, 2)-derivative((u+4)*w-4*u, 1)
        if method == 'CSD0':
            vt = wt+delta0(ut, bt)
        else:
            vt = np.diff(ut, axis=0)/H+(wt[1:]+wt[:-1])/2+H*derivative(np.diff((w/16-.25)*wt, axis=0), -1)
    elif method == 'FD':
        vt = -derivative((u+4)*second-4*u, 1)-derivative(delta0(u, b), 2)
    else:
        previous = np.concatenate((b[:1], u[:-1]))
        mean_u = (u+previous)/2
        jump = (u-previous)/H
        flux_v = (mean_u+4-2*H)*second+H*second*second/4-4*mean_u-H*jump*jump/4
        vt = -derivative(flux_v, 1)-derivative(jump, 2)
    return ut, vt


def max_error(value, reference, y):
    return float(np.max(abs(value-reference)[abs(y)<=1.8+1e-12]))


def initial_only():
    audits = []
    for case in ('Gaussian', 'Sinusoidal'):
        for method in ('Endpoint-SD', 'CSD0', 'Centered-SD', 'FD'):
            with np.load(HERE/f'initial_{case}_{method}.npz') as g:
                ut, vt = rhs_initial(case, method, g['z0'], g['x'], g['y'])
                difference = max(float(np.max(abs(ut-g['ut']))), float(np.max(abs(vt-g['vt']))))
                ur, vr = jets(case, g['x'], g['y']), jets(case, g['x'], g['yv'])
                rdifference = max(float(np.max(abs(ur['ut']-g['ut_ref']))), float(np.max(abs(vr['vt']-g['vt_ref']))))
                assert difference < 2e-10 and rdifference < 1e-13
                audits.append(dict(case=case, method=method, rhs_difference=difference,
                                   initial_reference_difference=rdifference))
    out = dict(status='passed', records=len(audits), audits=audits,
               max_rhs_difference=max(a['rhs_difference'] for a in audits),
               max_reference_difference=max(a['initial_reference_difference'] for a in audits))
    (HERE/'independent_initial_audit.json').write_text(json.dumps(out, indent=2), encoding='utf8')
    print(json.dumps(out, indent=2))


def main():
    rows = json.loads((HERE/'results.json').read_text(encoding='utf8'))
    initial = json.loads((HERE/'initial_results.json').read_text(encoding='utf8'))
    irecords = {(r['case'], r['method']): r for r in initial}
    audits = []
    assert len(rows) == 8
    for record in rows:
        case, method = record['case'], record['method']
        path = HERE/f'{case}_{method}_RK4.npz'
        with np.load(path) as f, np.load(HERE/f'initial_{case}_{method}.npz') as g:
            assert record['status'] == 'complete' and float(f['reached']) == .01
            assert (record['h'], record['dx'], record['dt'], record['a']) == (.1, .1, .0001, 2.)
            assert hashlib.sha256(path.read_bytes()).hexdigest() == record['artifact_sha256']
            for source in record['sources']:
                assert hashlib.sha256((ROOT/source['path']).read_bytes()).hexdigest() == source['sha256']
            for name in ('x', 'y', 'yv'):
                assert np.array_equal(f[name], g[name])
            for name in ('z', 'u', 'v', 'u_ref', 'v_ref'):
                assert np.isfinite(f[name]).all()
            reconstructed = physical_v(f['z']) if method == 'Centered-SD' else f['z'][1]
            map_difference = float(np.max(abs(reconstructed-f['v'])))
            assert map_difference < 1e-13
            end = [max_error(f['u'], f['u_ref'], f['y']), max_error(f['v'], f['v_ref'], f['yv'])]
            start = [max_error(g['ut'], g['ut_ref'], g['y']), max_error(g['vt'], g['vt_ref'], g['yv'])]
            end_difference = float(np.max(abs(np.array(end)-record['error'])))
            initial_difference = float(np.max(abs(np.array(start)-irecords[case, method]['total'])))
            assert end_difference == 0 and initial_difference == 0
            ur, vr = jets(case, f['x'], f['y']), jets(case, f['x'], f['yv'])
            initial_reference_difference = max(float(np.max(abs(ur['ut']-g['ut_ref']))), float(np.max(abs(vr['vt']-g['vt_ref']))))
            assert initial_reference_difference < 1e-13
            independent_ut, independent_vt = rhs_initial(case, method, g['z0'], g['x'], g['y'])
            rhs_difference = max(float(np.max(abs(independent_ut-g['ut']))), float(np.max(abs(independent_vt-g['vt']))))
            assert rhs_difference < 2e-10
            if method == 'Centered-SD':
                trace_difference = float(np.max(abs(g['z0'][1, 0]-(4-4*jets(case, f['x'], f['y'][:1])['uy'][0]))))
                assert trace_difference < 1e-13
            else:
                trace_difference = None
            audits.append(dict(case=case, method=method, recomputed_final_errors=end,
                               recomputed_initial_errors=start, final_record_difference=end_difference,
                               initial_record_difference=initial_difference,
                               independently_reconstructed_v_difference=map_difference,
                               independently_evaluated_initial_reference_difference=initial_reference_difference,
                               independently_implemented_initial_rhs_difference=rhs_difference,
                               centered_initial_lower_w_trace_difference=trace_difference))
    out = dict(status='passed', records=len(audits), audits=audits,
               max_final_record_difference=max(a['final_record_difference'] for a in audits),
               max_initial_record_difference=max(a['initial_record_difference'] for a in audits),
               max_initial_rhs_difference=max(a['independently_implemented_initial_rhs_difference'] for a in audits),
               scope='Independent initial analytic formulas and four spatial RHS implementations; saved physical-field reconstruction, common parameters, completion, state hashes, and table maxima. Full-time reference certification is separate.')
    (HERE/'independent_saved_audit.json').write_text(json.dumps(out, indent=2), encoding='utf8')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    initial_only() if '--initial' in sys.argv else main()
