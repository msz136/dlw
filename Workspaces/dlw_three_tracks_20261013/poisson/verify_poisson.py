"""Exact finite-dimensional DLW Poisson certificates (SymPy only).

Run: python Workspaces/dlw_three_tracks_20261013/poisson/verify_poisson.py
The analytic proof for arbitrary M,N is in report.md.  These checks independently
differentiate the explicit PHYSICAL bracket, including its mean corrections.
No numerical tolerance is used.  Data are written beside this script.
"""
from __future__ import annotations

from itertools import combinations
from pathlib import Path
import hashlib
import json
import time

import sympy as sp

HERE = Path(__file__).resolve().parent
CHECKS = []


def assert_zero(name, expression, **metadata):
    entries = list(expression) if isinstance(expression, sp.MatrixBase) else [expression]
    residuals = [sp.expand(e) for e in entries]
    ok = all(e == 0 for e in residuals)
    CHECKS.append(dict(name=name, passed=ok, **metadata))
    if not ok:
        raise AssertionError((name, [str(e) for e in residuals if e != 0][:3]))


def y_operators(m, h):
    eye = sp.eye(m)
    shift = sp.zeros(m)
    for j in range(m):
        shift[j, (j + 1) % m] = 1
    mean = sp.ones(m) / m
    proj = eye - mean
    c0 = (shift - shift.T) / (2 * h)
    inverse = sp.zeros(m)
    for ell in range(1, m):
        inverse += h * (sp.Rational(ell, m) - sp.Rational(1, 2)) * shift**ell
    return mean, proj, c0, inverse


def central_derivative(n, dx):
    d = sp.zeros(n)
    for i in range(n):
        # += and -= deliberately handle any coincident neighbors.
        d[i, (i + 1) % n] += 1 / (2 * dx)
        d[i, (i - 1) % n] -= 1 / (2 * dx)
    return d


def physical_bracket(m, n, h, dx, rho, u, v):
    """Return B in ordinary Euclidean-coordinate normalization.

    j-major ordering: u[ j*N+i ], followed by v[ j*N+i ].
    q=Pu, r=Pv.  B equals A J_red A.T/(h*dx).
    """
    _, py, _, _ = y_operators(m, h)
    proj = sp.kronecker_product(py, sp.eye(n))
    q, r = proj * u, proj * v
    d = central_derivative(n, dx)
    b = sp.zeros(2 * m * n)
    omega = h * dx
    for j in range(m):
        for i in range(n):
            ji = j * n + i
            for k in range(m):
                for ell in range(n):
                    kl = k * n + ell
                    common = -d[i, ell] / omega
                    collective = sum(r[a*n+i]*q[a*n+ell] + q[a*n+i]*r[a*n+ell]
                                     for a in range(m))
                    b[ji, kl] = sp.expand(common * (
                        rho * (q[j*n+ell] + q[k*n+i]) / m
                        + rho**2 * collective / m**2))
                    b[ji, m*n+kl] = sp.expand(common * (
                        py[j, k] + rho * r[k*n+i] / m))
                    b[m*n+ji, kl] = sp.expand(common * (
                        py[j, k] + rho * r[j*n+ell] / m))
    return b, q, r


def jacobi_certificate(m, n):
    start = time.perf_counter()
    h, dx = sp.Rational(2, 3), sp.Rational(3, 5)
    rho = sp.Symbol('rho', real=True)
    size = m*n
    z = sp.symbols(f'z0:{2*size}', real=True)
    u, v = sp.Matrix(z[:size]), sp.Matrix(z[size:])
    b, q, r = physical_bracket(m, n, h, dx, rho, u, v)
    prefix = f'physical M={m}, Nx={n}'
    assert_zero(prefix + ': skew', b+b.T)
    # Independent Frechet pushforward check of the printed matrix elements.
    mean, py, _, _ = y_operators(m, h)
    mean_all = sp.kronecker_product(mean, sp.eye(n))
    pd = sp.kronecker_product(py, central_derivative(n, dx))
    base = -(sp.BlockMatrix([[sp.zeros(size), pd],
                            [pd, sp.zeros(size)]])).as_explicit()/(h*dx)
    differential = sp.BlockMatrix([
        [sp.eye(size)+rho*mean_all*sp.diag(*r), rho*mean_all*sp.diag(*q)],
        [sp.zeros(size), sp.eye(size)]]).as_explicit()
    assert_zero(prefix + ': explicit formula equals coordinate pushforward',
                b-differential*base*differential.T)
    # Cache exact derivatives, not sampled values.
    differentiated = {}
    for a in range(2*size):
        for bb in range(a+1, 2*size):
            expr = b[a, bb]
            differentiated[a, bb] = [(ell, sp.diff(expr, z[ell]))
                                     for ell in range(2*size)
                                     if z[ell] in expr.free_symbols]

    def derivative_pairs(a, bb):
        if a < bb:
            return differentiated[a, bb]
        return [(ell, -val) for ell, val in differentiated[bb, a]]

    nonzero_count = 0
    checked = 0
    for a, bb, cc in combinations(range(2*size), 3):
        residual = 0
        for first, second, third in [(a, bb, cc), (bb, cc, a), (cc, a, bb)]:
            residual += sum(b[first, ell]*deriv
                            for ell, deriv in derivative_pairs(second, third))
        residual = sp.expand(residual)
        checked += 1
        if residual != 0:
            nonzero_count += 1
            raise AssertionError((prefix, (a, bb, cc), str(residual)))
    CHECKS.append(dict(name=prefix + ': all physical coordinate Jacobi triples',
                       passed=nonzero_count == 0, checked=checked,
                       symbolic_state_variables=2*size, symbolic_parameter='rho=-1/c',
                       seconds=round(time.perf_counter()-start, 3)))

    for i in range(n):
        mean_v = sum(v[j*n+i] for j in range(m))/m
        b_casimir = sum(u[j*n+i] for j in range(m))/m - rho*sum(
            q[j*n+i]*r[j*n+i] for j in range(m))/m
        for label, casimir in [('mean-v', mean_v), ('mean-u-correction', b_casimir)]:
            gradient = sp.Matrix([sp.diff(casimir, zz) for zz in z])
            assert_zero(prefix + f': {label} Casimir i={i}', b*gradient)
    print(json.dumps({'jacobi':prefix, 'triples':checked,
                      'seconds':round(time.perf_counter()-start, 3)}), flush=True)
    return dict(M=m, Nx=n, triples=checked,
                seconds=round(time.perf_counter()-start, 3))


def hamiltonian_and_rank_certificates():
    h, dx, c, gamma = sp.Rational(2, 3), sp.Rational(3, 5), sp.Integer(-4), sp.Rational(-3, 2)
    beta, rho = h*h/32, -1/c
    rank_table = []
    momentum_witness = None
    for m, n in [(2, 3), (3, 3), (3, 4), (4, 5), (4, 6)]:
        omega = h*dx
        mean, py, cy, ry = y_operators(m, h)
        d = central_derivative(n, dx)
        proj = sp.kronecker_product(py, sp.eye(n))
        d_all = sp.kronecker_product(sp.eye(m), d)
        r_all = sp.kronecker_product(ry, sp.eye(n))
        c_all = sp.kronecker_product(cy, sp.eye(n))
        p = proj * sp.Matrix([sp.Rational((k*k+2*k+3) % 17 - 8, 7)
                              for k in range(m*n)])
        s = proj * sp.Matrix([sp.Rational((3*k*k+k+5) % 19 - 9, 11)
                              for k in range(m*n)])
        bmean = [(gamma-sum(p[j*n+i]*s[j*n+i] for j in range(m))/m)/c
                 for i in range(n)]
        U = p + sp.Matrix(bmean*m)
        w = s+c*sp.ones(m*n, 1)
        a = sp.Rational(5, 7)
        u = U-2*a*sp.ones(m*n, 1)
        v = w+c_all*u+4*sp.ones(m*n, 1)
        bracket, q, r = physical_bracket(m, n, h, dx, rho, u, v)
        kernel_dim = 1 if n % 2 else 2
        expected_rank = 2*(m-1)*(n-kernel_dim)
        actual_rank = bracket.rank()
        assert_zero(f'M={m}, Nx={n}: rank formula', actual_rank-expected_rank)
        rank_table.append(dict(M=m, Nx=n, physical_dimension=2*m*n,
                               mean_constrained_dimension=2*(m-1)*n,
                               rank=actual_rank, x_derivative_kernel=kernel_dim,
                               ambient_casimirs=2*m*n-actual_rank))
        assert_zero(f'M={m}, Nx={n}: R skew', ry+ry.T)
        assert_zero(f'M={m}, Nx={n}: Dx skew', d+d.T)
        assert_zero(f'M={m}, Nx={n}: RD symmetric', r_all*d_all-(r_all*d_all).T)
        # Exact gradients relative to omega*sum.  No discrete product rule.
        f = U.multiply_elementwise(w)-d_all*w-gamma*sp.ones(m*n, 1)
        k = (U.multiply_elementwise(U)/2 + beta*w.multiply_elementwise(w)
             +d_all*U+r_all*d_all*w)
        pt, st = -proj*d_all*k, -proj*d_all*f
        assert_zero(f'M={m}, Nx={n}: mean U*w constraint',
                    sp.kronecker_product(mean, sp.eye(n))*U.multiply_elementwise(w)
                    -gamma*sp.ones(m*n,1))
        assert_zero(f'M={m}, Nx={n}: discrete K derivative',
                    omega*((proj*f).dot(pt)+(proj*k).dot(st)))
        momentum_rate = sp.factor(omega*(s.dot(pt)+p.dot(st)))
        formula_rate = sp.factor(omega*(f.dot(d_all*p)+k.dot(d_all*s)))
        assert_zero(f'M={m}, Nx={n}: momentum defect formula', momentum_rate-formula_rate)
        if momentum_witness is None and momentum_rate != 0:
            momentum_witness = dict(M=m, Nx=n, h=str(h), dx=str(dx), c=str(c),
                                    gamma=str(gamma), a=str(a),
                                    Dx=[[str(d[i,j]) for j in range(n)] for i in range(n)],
                                    p=[str(t) for t in p],
                                    s=[str(t) for t in s],
                                    dPdt_exact=str(momentum_rate),
                                    dPdt_float=float(momentum_rate),
                                    dKdt_exact='0')
    assert momentum_witness is not None
    return rank_table, momentum_witness


def symbolic_hamiltonian_gradient():
    m, n = 2, 3
    h, dx, c, gamma = sp.Rational(2, 3), sp.Rational(3, 5), -4, sp.Rational(-3, 2)
    _, py, _, ry = y_operators(m, h)
    proj = sp.kronecker_product(py, sp.eye(n))
    d_all = sp.kronecker_product(sp.eye(m), central_derivative(n, dx))
    r_all = sp.kronecker_product(ry, sp.eye(n))
    pp, ss = sp.symbols(f'p0:{m*n}'), sp.symbols(f's0:{m*n}')
    p, s = proj*sp.Matrix(pp), proj*sp.Matrix(ss)
    mean_u = [(gamma-sum(p[j*n+i]*s[j*n+i] for j in range(m))/m)/c
              for i in range(n)]
    U = p+sp.Matrix(mean_u*m)
    w = s+c*sp.ones(m*n, 1)
    beta, omega = h*h/32, h*dx
    K = omega*sum(U[k]**2*w[k]/2+beta*w[k]**3/3
                   +w[k]*(d_all*U)[k]+w[k]*(r_all*d_all*w)[k]/2-gamma*U[k]
                   for k in range(m*n))
    f = U.multiply_elementwise(w)-d_all*w-gamma*sp.ones(m*n, 1)
    k = U.multiply_elementwise(U)/2+beta*w.multiply_elementwise(w)+d_all*U+r_all*d_all*w
    grad_p = sp.Matrix([sp.diff(K, z)/omega for z in pp])
    grad_s = sp.Matrix([sp.diff(K, z)/omega for z in ss])
    assert_zero('M=2,Nx=3: symbolic K gradient p, no Leibniz identity', grad_p-proj*f)
    assert_zero('M=2,Nx=3: symbolic K gradient s, no Leibniz identity', grad_s-proj*k)


def main():
    started = time.perf_counter()
    jacobi_runs = [jacobi_certificate(m, n) for m, n in [(2, 3), (3, 3), (2, 4)]]
    ranks, momentum_witness = hamiltonian_and_rank_certificates()
    symbolic_hamiltonian_gradient()
    result = dict(
        title='DLW physical-coordinate finite-dimensional Poisson exact certificate',
        passed=all(item['passed'] for item in CHECKS),
        normalization='omega=h*dx; coordinate B=J_functional_gradient/omega',
        boundary='periodic x and periodic y; c != 0; gamma constant',
        derivative='centered periodic Dx; Dxx=Dx@Dx in the Hamiltonian flow',
        jacobi_identity='Every coordinate triple, generic physical u/v and symbolic rho=-1/c',
        jacobi_total_triples=sum(row['triples'] for row in jacobi_runs),
        jacobi_runs=jacobi_runs,
        general_proof='report.md: coordinate pushforward proves Jacobi for all M,N and any fixed skew Dx',
        ranks=ranks, momentum_nonconservation_witness=momentum_witness,
        checks=CHECKS, check_count=len(CHECKS),
        elapsed_seconds=round(time.perf_counter()-started,3),
        python_sympy_version=sp.__version__,
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (HERE/'exact_checks.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'passed':result['passed'], 'checks':result['check_count'],
                      'jacobi_triples':result['jacobi_total_triples'],
                      'seconds':result['elapsed_seconds']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
