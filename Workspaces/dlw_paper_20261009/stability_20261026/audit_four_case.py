"""Independent read-only audit of stored perturbations and constant-state controls.

Outputs are audit evidence, not certificates for nonlinear continuum solutions.
The exact constant-background formulas are sampled at the numerical native sites.
"""
from pathlib import Path
import hashlib
import json
import numpy as np
from scipy.signal import resample

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
DATA = HERE / 'perturbation_pilot/four_case_kappa_pi_over_2'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    reported_norms = json.loads((DATA / 'endpoint_norms.json').read_text())['records']
    records = []
    for case in ['A', 'D', 'Gaussian', 'Sinusoidal']:
        meta = json.loads((DATA / (case + '.json')).read_text())
        artifact = DATA / (case + '.npz')
        assert digest(artifact) == meta['artifact_sha256']
        a = np.load(artifact)
        x, y, yv = a['x'], a['y'], a['yv']
        h, dx, eps, k, T, dt = [meta[q] for q in ['h', 'dx', 'epsilon', 'kappa', 'T', 'dt']]
        L = y[-1] - y[0]
        if case in ['A', 'D']:
            R = 5 if case == 'A' else 30
            mx, my, mv = abs(x) <= R, abs(y) < R, abs(yv) < R
        else:
            mx, my, mv = np.ones(len(x), dtype=bool), abs(y) <= 1.8 + 1e-12, abs(yv) <= 1.8 + 1e-12

        def phys(state):
            u, w = state
            return u, np.diff(u, axis=0) / h + (w[1:] + w[:-1]) / 2

        def norm(q):
            return np.array([np.max(abs(q[0][my][:, mx])), np.max(abs(q[1][mv][:, mx]))])

        def phi(yy):
            return np.sin(np.pi * (yy-y[0])/L)**2

        def phi_prime(yy):
            return np.pi/L*np.sin(2*np.pi*(yy-y[0])/L)

        def primitive(yy):
            z = yy-y[0]
            return z/2-L/(4*np.pi)*np.sin(2*np.pi*z/L)

        carrier = np.cos(k*x)[None, :]
        initial_u = eps*phi(y)[:, None]*carrier
        initial_u[[0, -1]] = 0.
        initial_v = eps*phi(yv)[:, None]*carrier
        n = round(T/dt)
        rk = lambda z: 1+z+z*z/2+z**3/6+z**4/24
        rp, rm = rk(dt*(k*k-4j*k))**n, rk(dt*(-k*k-4j*k))**n
        crk, srk = (rp+rm)/2, (rp-rm)/2
        cex, sex = np.exp(-4j*k*T)*np.cosh(k*k*T), np.exp(-4j*k*T)*np.sinh(k*k*T)
        expx = np.exp(1j*k*x)[None, :]
        cc, ss = np.real(cex*expx), np.real(sex*expx)
        crc, src = np.real(crk*expx), np.real(srk*expx)
        J_h = h*np.r_[0., np.cumsum(phi(yv))]
        fdphi = np.diff(phi(y))/h
        modes = []
        for idx, component in enumerate(['u', 'v'], start=1):
            p0, pt = phys(a['z0'][idx]), phys(a['final_state'][idx])
            desired = (initial_u, np.zeros_like(initial_v)) if component == 'u' else (np.zeros_like(initial_u), initial_v)
            initial_map = [float(np.max(abs(q-r))) for q, r in zip(p0, desired)]
            m0, mt = norm(p0), norm(pt)
            assert np.max(abs(m0-a['delta_max'][0, idx-1])) < 1e-20
            assert np.max(abs(mt-a['delta_max'][-1, idx-1])) < 1e-20
            assert np.max(abs(mt-meta['final_delta_max'][idx-1])) < 1e-20
            assert np.max(abs(pt[0]-a['delta_u_from_'+component])) == 0
            assert np.max(abs(pt[1]-a['delta_v_from_'+component])) == 0
            if component == 'u':
                cont = (eps*phi(y)[:, None]*cc, eps*phi_prime(yv)[:, None]*ss)
                disc = (eps*phi(y)[:, None]*cc, eps*fdphi[:, None]*ss)
                drk = (eps*phi(y)[:, None]*crc, eps*fdphi[:, None]*src)
            else:
                cont = (eps*primitive(y)[:, None]*ss, eps*phi(yv)[:, None]*cc)
                disc = (eps*J_h[:, None]*ss, eps*phi(yv)[:, None]*cc)
                drk = (eps*J_h[:, None]*src, eps*phi(yv)[:, None]*crc)
            L0 = np.array([np.sqrt(h*dx*np.sum(p0[0][my]**2)), np.sqrt(h*dx*np.sum(p0[1][mv]**2))])
            Lt = np.array([np.sqrt(h*dx*np.sum(pt[0][my]**2)), np.sqrt(h*dx*np.sum(pt[1][mv]**2))])
            l2gain = float(np.linalg.norm(Lt)/np.linalg.norm(L0))
            at8 = [float(np.max(abs(resample(q[mask], len(x)*8, axis=-1)))) for q, mask in zip(pt, [my, mv])]
            prior = next(r for r in reported_norms if r['case']==case and r['perturbed_field']==component)
            assert abs(l2gain-prior['L2_pair_gain']) < 1e-14
            assert max(abs(v-w) for v, w in zip(at8, prior['fourier_interpolant_max']['8']['final'])) < 1e-20
            modes.append(dict(perturbed_field=component, initial_physical_mapping_max=initial_map,
                initial_native_max=m0.tolist(), numerical_final_native_max=mt.tolist(), numerical_gain=(mt/max(m0)).tolist(),
                constant_continuum_native_max=norm(cont).tolist(), constant_continuum_gain=(norm(cont)/max(m0)).tolist(),
                constant_semidiscrete_native_max=norm(disc).tolist(), constant_semidiscrete_gain=(norm(disc)/max(m0)).tolist(),
                constant_RK4_native_max=norm(drk).tolist(), constant_RK4_gain=(norm(drk)/max(m0)).tolist(),
                numerical_to_constant_semidiscrete=(mt/norm(disc)).tolist(),
                constant_semidiscrete_RK4_maxdiff=norm(tuple(q-r for q,r in zip(disc,drk))).tolist(),
                L2_pair_gain=l2gain, x8_terminal_peaks=at8))
        source_paths = [HERE/'perturbation_pilot/run_suite.py', HERE/'perturbation_pilot/run_pilot.py', PROJECT/'time_samm_20261025/time/run_time.py']
        source_match = {p.name: digest(p)==meta['source_sha256'][p.name] for p in source_paths}
        prior=np.load(PROJECT/'report_refresh_20261024/natural_edge_rk4_20261024'/(case+'.npz'))
        baseline_difference=float(np.max(abs(a['final_state'][0]-prior['z'])))
        assert baseline_difference == 0
        records.append(dict(case=case, artifact_sha256=digest(artifact), source_hashes_match=source_match,
            baseline_saved_RK4_difference=baseline_difference, y_interval=y[[0,-1]].tolist(),
            native_evaluation_y_max=float(y[my].max()), native_evaluation_yv_max=float(yv[mv].max()),
            continuous_primitive_max=float(primitive(y[my]).max()), discrete_primitive_max=float(J_h[my].max()),
            x_advection_sample_factor=float(np.max(abs(np.cos(k*(x[mx]-4*T))))), modes=modes))
    out=dict(records=records, all_array_claims_checked=True, continuous_nonlinear_certificate=False,
        exact_linear_control='u=0,v=4, lower delta u=0, same sinusoidal x carrier, same y envelopes and observation regions',
        scope='Analytic formulas evaluated in ordinary floating point; controls identify geometry and sampling, not a nonlinear perturbed PDE error enclosure.')
    (HERE/'audit_four_case.json').write_text(json.dumps(out,indent=2),encoding='utf8')
    for r in records:
        print(r['case'],'ymax',r['native_evaluation_y_max'],'J',r['continuous_primitive_max'])
        for m in r['modes']:
            print(m['perturbed_field'],'observed',m['numerical_gain'],'continuum linear',m['constant_continuum_gain'],'finite-h linear',m['constant_semidiscrete_gain'],'ratios',m['numerical_to_constant_semidiscrete'])


if __name__=='__main__':
    run()
