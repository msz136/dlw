"""Frozen-point quadrature validation; no evolution, scan, or fitted theory."""
from pathlib import Path
import hashlib
import json
import numpy as np
from scipy.special import expit
from scipy.optimize import least_squares
from numpy.polynomial.legendre import leggauss

HERE = Path(__file__).resolve().parent
THETA = np.array([2.0, -1.0, -np.log(2.0)/2])
A_PHYS = 0.0
T_PHYS = 0.0
HS = [1/4, 1/8, 1/16, 1/32]


def grid(n):
    nodes, weights = leggauss(n)
    x, y = np.meshgrid(8*nodes, nodes, indexing='ij')
    # Integral divided by rectangle area32: Jacobian8 /32.
    weight = weights[:, None]*weights[None, :]/4
    return x, y, weight


def jets(z):
    s = expit(z)
    d1 = s*(1-s)
    d2 = d1*(1-2*s)
    d3 = d1*(1-6*s+6*s*s)
    return s, d1, d2, d3


def constants(theta):
    p, q, phi = theta
    P, Q = p-A_PHYS, q+A_PHYS
    K, ell, g = p+q, 1/P+1/Q, np.log(-P/Q)
    return p, q, phi, P, Q, K, ell, g


def continuous(theta, x, y, with_tangent=False):
    p, q, phi, P, Q, K, ell, g = constants(theta)
    z = K*x+ell*y+(q*q-p*p)*T_PHYS+phi
    s, s1, s2, _ = jets(z)
    f, f1, f2, _ = jets(z+g)
    U = np.stack([2*K*(f-s), 2*K*ell*(f1+s1)], axis=-1)
    if not with_tangent:
        return U
    zp, zq = x-y/P**2-2*p*T_PHYS, x-y/Q**2+2*q*T_PHYS
    ds, cs2 = f1-s1, f2+s2
    up = 2*(f-s)+2*K*(ds*zp+f1/P)
    uq = 2*(f-s)+2*K*(ds*zq-f1/Q)
    uf = 2*K*ds
    vp = 2*(ell-K/P**2)*(f1+s1)+2*K*ell*(cs2*zp+f2/P)
    vq = 2*(ell-K/Q**2)*(f1+s1)+2*K*ell*(cs2*zq-f2/Q)
    vf = 2*K*ell*cs2
    tangent = np.stack([np.stack([up, vp], -1),
                        np.stack([uq, vq], -1),
                        np.stack([uf, vf], -1)], axis=-1)
    return U, tangent


def correction(theta, x, y):
    p, q, phi, P, Q, K, ell, g = constants(theta)
    z = K*x+ell*y+(q*q-p*p)*T_PHYS+phi
    _, s1, s2, s3 = jets(z)
    _, f1, f2, f3 = jets(z+g)
    c3, gamma2 = (P**-3+Q**-3)/12, (Q**-2-P**-2)/8
    Bu = 2*K*y*c3*(f1-s1)+2*K*gamma2*f1-K*ell**2*s2/4
    Bv = (2*K*c3*(f1+s1)+2*K*ell*y*c3*(f2+s2)
          +2*K*ell*gamma2*f2+K*ell**3*(4*f3-5*s3)/12)
    return np.stack([Bu, Bv], axis=-1)


def finite_h(theta, x, y, h):
    p, q, phi, P, Q, K, _, g = constants(theta)
    # log1p formulas avoid avoidable loss for smallh.
    logchi = (np.log1p(h/(2*P))-np.log1p(-h/(2*P))
              +np.log1p(h/(2*Q))-np.log1p(-h/(2*Q)))
    lam, delta = logchi/h, logchi/2
    eps = (np.log1p(-h*h/(4*P*P))-np.log1p(-h*h/(4*Q*Q)))/2
    z = K*x+lam*y+(q*q-p*p)*T_PHYS+phi

    def uh(zz):
        return K*(2*expit(zz+g+eps)-expit(zz-delta)-expit(zz+delta))

    u = uh(z)
    v = 4*K/h*(expit(z+delta)-expit(z-delta))+(uh(z+lam*h)-uh(z-lam*h))/(2*h)
    return np.stack([u, v], axis=-1)


def norm(a, weight):
    return float(np.sqrt(np.sum(weight[..., None]*a*a)))


def projection(T, B, weight):
    G = np.einsum('ij,ijak,ijal->kl', weight, T, T)
    b = np.einsum('ij,ijak,ija->k', weight, T, B)
    coeff = np.linalg.solve(G, b)
    normal = B-np.einsum('ijak,k->ija', T, coeff)
    return {'d': norm(normal, weight), 'normB': norm(B, weight),
            'c': coeff.tolist(), 'G': G.tolist(), 'b': b.tolist(),
            'conditionG': float(np.linalg.cond(G)),
            'gram_residual_squared': float(np.sum(weight[..., None]*B*B)-b@coeff)}


def run():
    theory_hash = hashlib.sha256((HERE/'THEORY.md').read_bytes()).hexdigest()
    evaluations = []
    for n in [80, 120, 180]:
        x, y, w = grid(n)
        U0, tangent = continuous(THETA, x, y, True)
        B = correction(THETA, x, y)
        evaluations.append({'order': n, 'pair': projection(tangent, B, w),
                            'u': projection(tangent[..., 0:1, :], B[..., 0:1], w),
                            'v': projection(tangent[..., 1:2, :], B[..., 1:2], w),
                            'normU0': norm(U0, w)})
    x, y, w = grid(120)
    U0 = continuous(THETA, x, y)
    B = correction(THETA, x, y)
    sqrt_weight = np.sqrt(w)[..., None]
    c_star = np.array(evaluations[1]['pair']['c'])
    rows = []
    for h in HS:
        target = finite_h(THETA, x, y, h)

        def objective(theta):
            return ((continuous(theta, x, y)-target)*sqrt_weight).ravel()

        def jac(theta):
            _, tangent = continuous(theta, x, y, True)
            return (tangent*sqrt_weight[..., None]).reshape(-1, 3)

        sol = least_squares(objective, THETA+h*h*c_star, jac=jac,
                            bounds=(THETA-0.1, THETA+0.1),
                            xtol=1e-14, ftol=1e-14, gtol=1e-14,
                            max_nfev=60)
        xf, yf, wf = grid(180)
        fine_target = finite_h(THETA, xf, yf, h)
        fine_distance = norm(fine_target-continuous(sol.x, xf, yf), wf)
        distance = norm(target-continuous(sol.x, x, y), w)
        remainder = norm(target-U0-h*h*B, w)
        rows.append({'h': h, 'D': distance, 'D_over_h2': distance/h**2,
                     'quadrature_distance180': fine_distance,
                     'quadrature_distance_difference': abs(distance-fine_distance),
                     'delta_over_h2': ((sol.x-THETA)/h**2).tolist(),
                     'remainder': remainder, 'remainder_over_h4': remainder/h**4,
                     'optimality': float(sol.optimality), 'success': bool(sol.success),
                     'nfev': int(sol.nfev),
                     'interior_margin': float(np.min(0.1-np.abs(sol.x-THETA)))})
    d = evaluations[-1]['pair']['d']
    coeff_convergence = [float(np.linalg.norm(np.array(r['delta_over_h2'])-c_star)) for r in rows]
    checks = {
        'quadrature_d_agreement': abs(evaluations[-1]['pair']['d']-evaluations[0]['pair']['d']) < 1e-11,
        'nonlinear_stationary_points_interior': all(r['success'] and r['interior_margin'] > .08 for r in rows),
        'quadrature_fitted_distance_agreement': all(r['quadrature_distance_difference'] < 1e-11 for r in rows),
        'normal_coefficient_converges': all(abs(rows[i+1]['D_over_h2']-d) < abs(rows[i]['D_over_h2']-d) for i in range(3)),
        'remainder_h4_normalization_bounded': max(r['remainder_over_h4'] for r in rows) / min(r['remainder_over_h4'] for r in rows) < 1.05,
        'relabel_coefficient_converges': all(coeff_convergence[i+1] < coeff_convergence[i] for i in range(3)),
    }
    result = {'status': 'passed' if all(checks.values()) else 'failed',
              'theory_sha256_before_verification': theory_hash,
              'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'comparison': {'a': 0, 'theta': THETA.tolist(), 't': 0,
                             'window': [[-8, 8], [-1, 1]],
                             'norm': 'sqrt(integral(u^2+v^2)/32)',
                             'h': HS, 'quadrature_orders': [80, 120, 180]},
              'projection_integrals': evaluations, 'finite_h_validation': rows,
              'checks': checks, 'new_pde_runs': 0, 'parameter_scan': False,
              'interpretation': 'quadrature and local stationary-fit support only; function identity and positivity proven analytically in THEORY.md; integral floats not certified intervals'}
    (HERE/'geometry_validation.json').write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps({'status': result['status'], 'projection': evaluations[-1], 'rows': rows, 'checks': checks}, indent=2))
    if result['status'] != 'passed':
        raise SystemExit(1)


if __name__ == '__main__':
    run()
