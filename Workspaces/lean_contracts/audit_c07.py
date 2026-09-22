"""Exact-rational audit of frozen target C07, for N = 1,2,3,4.

All arithmetic is exact (`fractions.Fraction`); there is no floating point and no
tolerance: "vanishes" is a literal `== 0` test.

Method.  `det(I+K) = sum over principal subsets S of det(K_S)` is an identity, and with

    K^(n)_{ik} = rho_i/(p_i+q_k) * gamma_{ik}^n * chi_{ik}^j
                 * exp((p_i+q_k) x + ((q_k)^2-(p_i)^2) t),
    gamma_{ik} = u_i v_k,  u_i = p_i-s,  v_k = -1/(q_k+s),

the determinant identities det(I+XY) = det(I+YX) give the exact representation

    tau_n = sum_S c_S * (prod_{i in S} w_i^n) * E_S,
    E_S   = exp(Lambda_S x + Mu_S t),
    Lambda_S = sum_{i in S} (p_i+q_i),  Mu_S = sum_{i in S} (q_i^2-p_i^2),
    c_S   = det(M_S),  M_{ik} = rho_i * chi_{ik}^j / (p_i+q_k),
    w_i   = gamma_{ii} = -(p_i-s)/(q_i+s).

Since `bil` acts on plane waves by
    bil_a(e^{L1 x+M1 t}, e^{L2 x+M2 t}) = [(L1-L2)^2 + (M1-M2) + 2a(L1-L2)] e^{(L1+L2)x+(M1+M2)t},
target C07 (there a = s) is equivalent to: for every (Lambda, Mu), the grouped coefficient

    sum_{(S,T): Lambda_S+Lambda_T = Lambda, Mu_S+Mu_T = Mu} c_S^{(n+1)} c_T^{(n)} theta(S,T)

vanishes.  Substituting exact rationals first makes each group an exact Fraction.
"""
from fractions import Fraction as F
from itertools import combinations

import sympy as sp


def lam(z, h):
    return (z + h / 2) / (z - h / 2)


def tau_dict(N, P, Q, RHO, H, A, S, j, n):
    """{exponent key -> exact Fraction coefficient} for tau_n, parameters already numeric."""
    p = [P[i] for i in range(N)]
    q = [Q[i] for i in range(N)]
    rho = [RHO[i] for i in range(N)]
    Psum = [p[i] + q[i] for i in range(N)]
    Qsum = [q[i] ** 2 - p[i] ** 2 for i in range(N)]
    w = [-(p[i] - S) / (q[i] + S) for i in range(N)]

    def chi(i, k):
        return lam(p[i] - A, H) * lam(q[k] + A, H)

    M = sp.Matrix(N, N, lambda i, k: sp.Rational(rho[i] * chi(i, k) ** j / (p[i] + q[k])))

    out = {}
    for r in range(N + 1):
        for Sub in combinations(range(N), r):
            if not Sub:
                cS, L, Mu, wS = F(1), F(0), F(0), F(1)
            else:
                cS = F(str(M.extract(Sub, Sub).det()))
                L = sum(Psum[i] for i in Sub)
                Mu = sum(Qsum[i] for i in Sub)
                wS = F(1)
                for i in Sub:
                    wS *= w[i]
            key = (F(str(sp.Rational(L))), F(str(sp.Rational(Mu))))
            out[key] = out.get(key, F(0)) + cS * wS ** n
    return out


def check(N, j, n, params):
    P = [F(params[f'p{i}']) for i in range(N)]
    Q = [F(params[f'q{i}']) for i in range(N)]
    RHO = [F(params[f'rho{i}']) for i in range(N)]
    H, A, S = F(params['h']), F(params['a']), F(params['s'])

    A_ = tau_dict(N, P, Q, RHO, H, A, S, j, n + 1)
    B_ = tau_dict(N, P, Q, RHO, H, A, S, j, n)

    groups = {}
    for (L1, M1), c1 in A_.items():
        for (L2, M2), c2 in B_.items():
            theta = (L1 - L2) ** 2 + (M1 - M2) + 2 * S * (L1 - L2)
            key = (L1 + L2, M1 + M2)
            groups[key] = groups.get(key, F(0)) + c1 * c2 * theta
    return {k: v for k, v in groups.items() if v != 0}


PARAMS = [
    dict(p0='3', q0='5', rho0='7', p1='2', q1='11', rho1='13',
         p2='1', q2='17', rho2='19', p3='4', q3='19', rho3='23', s='6', h='1', a='8'),
    dict(p0='10', q0='3', rho0='5', p1='7', q1='2', rho1='9',
         p2='13', q2='5', rho2='11', p3='1', q3='7', rho3='3', s='2', h='1', a='20'),
    dict(p0='5', q0='5', rho0='3', p1='3', q1='7', rho1='5',
         p2='9', q2='2', rho2='7', p3='6', q3='11', rho3='2', s='9', h='1', a='15'),
]

if __name__ == '__main__':
    total_bad = 0
    for pi, params in enumerate(PARAMS):
        print(f'parameter set {pi}:', flush=True)
        for N in (1, 2, 3, 4):
            for j in (0, 1, 2):
                for n in (0, 1, 2):
                    bad = check(N, j, n, params)
                    total_bad += len(bad)
                    print(f'   N={N} j={j} n={n}: {"ok" if not bad else "NONZERO"}', flush=True)
                    for k, v in list(bad.items())[:4]:
                        print('       NONZERO group', k, v, flush=True)
    print()
    print('C07 AUDIT:', 'all grouped coefficients vanish exactly' if total_bad == 0
          else f'{total_bad} NONZERO group(s) -> C07 FALSE')
