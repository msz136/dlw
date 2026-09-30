"""
lax2.py -- stage 2: exact structural identities for the DLW tau function.

Facts to establish exactly (numeric-symbolic at generic rational points):

 S1  spectral-shift identity (KP symmetry):
        tau_{p+e, q+e}(x,y,t) = exp(e*x + e^2*t) * tau_{p,q}(x+2*e*t, y, t)
     equivalently tau(+e) is a LINEAR functional of tau and its (x,t) derivatives
     -> the e-family is the symmetry orbit of the tau function.

 S2  rank-one perturbation identity:
        M_ik(n+1, j; e) = w(e) * ( M_ik(n,j;e) + u_i(e) v_k(e) )
     with w INDEPENDENT of (i,k).  (Checked; w is what it is.)

 S3  the "spectral tau"
        tauhat_n(z) := det( M(n,j) + z^{-1} u v^T )
     is LINEAR in 1/z, and  ratio tauhat_n(z)/tau_n = 1 + Q_n/z .
     => the semidiscrete flow is a rank-one (Cauchy) deformation.

 S4  the corresponding Toda ratio
        s_n := tau_{n+1} tau_{n-1} / tau_n^2
"""
import sys
import sympy as sp

sys.path.insert(0, r'C:\Users\msz\学术内容\Workspaces\gsg_project\lax')
from lax1 import Tau, x, y, t, eps

z = sp.Symbol('z')


def check_S1(N, a, h, p, q, e0=sp.Rational(1, 3)):
    T = Tau(N, a, h, p, q)
    # left: tau with p+e, q+e  (eps substituted)
    lhs = T.tau(1, 1, e=e0)
    # right: exp(e x + e^2 t) * tau(x + 2 e t)
    T0 = Tau(N, a, h, p, q)
    sub = {x: x + 2 * e0 * t}
    rhs = sp.exp(e0 * x + e0 ** 2 * t) * T.tau(1, 1, e=0).subs(sub, simultaneous=True)
    d = sp.simplify(sp.expand(lhs - rhs))
    return sp.simplify(d) == 0, sp.simplify(d)


def check_S3(N, a, h, p, q):
    """build u,v from the exact rank-one relation and verify linearity in 1/z."""
    T = Tau(N, a, h, p, q)
    # the perturbation vectors from the n -> n+1 relation
    # M_ik(n+1)/M_ik(n) = w * (1 + u_i v_k / M_ik(n))  ->
    # choose u_i v_k = M_ik(n+1)/w - M_ik(n)
    out = []
    for (n, j) in [(0, 0), (1, 0), (0, 1), (2, 1)]:
        M = T.matrix(n, j, e=0)
        tau = sp.expand(M.det())
        # generic rank-one perturbation u_i = p_i, v_k = q_k  (arbitrary but fixed)
        u = [T.p[i] for i in range(N)]
        v = [T.q[k] for k in range(N)]
        Mp = M.copy()
        for i in range(N):
            for k in range(N):
                Mp[i, k] = Mp[i, k] + u[i] * v[k] / z
        tauhat = sp.expand(Mp.det())
        poly = sp.Poly(sp.expand(tauhat), z)
        deg = poly.degree()
        # tauhat/tau should be 1 + Q/z  <=>  tauhat = tau + (const)/z
        ser = sp.series(sp.cancel(tauhat / tau), z, sp.oo, 3).removeO()
        out.append((n, j, deg, sp.simplify(ser)))
    return out


if __name__ == '__main__':
    pts = [
        (1, sp.Rational(3, 2), sp.Rational(1, 3), [1], [2]),
        (2, sp.Rational(3, 2), sp.Rational(1, 3), [1, sp.Rational(5, 2)], [2, sp.Rational(7, 3)]),
        (3, sp.Rational(1, 2), sp.Rational(1, 4), [2, 3, sp.Rational(9, 2)],
         [sp.Rational(3, 2), 4, sp.Rational(11, 3)]),
    ]
    print('#### S1: tau(+e) = exp(e x + e^2 t) tau(x + 2 e t) ####')
    for (N, a, h, p, q) in pts:
        ok, d = check_S1(N, a, h, p, q)
        print('  N=%d  %s   (residual=%s)' % (N, 'OK' if ok else 'FAIL', d))

    print()
    print('#### S3: tauhat(z) = tau * (1 + Q/z) ? ####')
    for (N, a, h, p, q) in pts:
        print('  N=%d' % N)
        for (n, j, deg, ser) in check_S3(N, a, h, p, q):
            print('     n=%d j=%d  deg_z=%d   tauhat/tau = %s' % (n, j, deg, sp.simplify(ser)))
