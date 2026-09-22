"""
numeric_check.py -- DEFINITIVE check with pure mpmath/exact rational evaluation.

No sympy simplification is involved: we build the Gram matrix numerically at a
fixed point (x,y,t) and compare the determinant with the "rank-one" prediction.
"""
import sys
import mpmath as mp

mp.mp.dps = 60

# generic rational parameters (same as gen.generic_point(2,11))
a = mp.mpf(17) / 5
h = mp.mpf(1) / 3
p = [mp.mpf(29) / 3, mp.mpf(12) / 5]
q = [mp.mpf(40) / 3, mp.mpf(7) / 5]
cv = [mp.mpf(1), mp.mpf(1)]


def entry(n, j, i, k, s, X, Y, T):
    P = p[i] - s
    Q = q[k] + s
    coef = (-P / Q) ** n / (p[i] + q[k])
    if j:
        lam = lambda v: (v + h / 2) / (v - h / 2)
        coef *= (lam(p[i] - a) * lam(q[k] + a)) ** j
    xi = p[i] * X - p[i] ** 2 * T + Y / P
    eta = q[k] * X + q[k] ** 2 * T + Y / Q
    return coef * mp.e ** (xi + eta)


def tau(N, n, j, s, X, Y, T):
    M = mp.matrix(N, N)
    for i in range(N):
        for k in range(N):
            M[i, k] = entry(n, j, i, k, s, X, Y, T)
            if i == k:
                M[i, k] += cv[k]
    return mp.det(M)


X = mp.mpf(1) / 3
Y = mp.mpf(-2) / 5
T = mp.mpf(3) / 7
d = h / 2
s_lo = a - d
s_hi = a + d

print('#' * 90)
print('A.  tau_n for N = 1..4   (a=%s, p=%s, q=%s)' % (a, p, q))
for N in (1, 2, 3, 4):
    vals = [tau(N, n, 0, a, X, Y, T) for n in (0, 1)]
    print('   N=%d  tau_0 = %s' % (N, mp.nstr(vals[0], 20)))
    print('        tau_1 = %s' % mp.nstr(vals[1], 20))
    if abs(vals[0]) > mp.mpf('1e-40'):
        print('        tau_1/tau_0 = %s' % mp.nstr(vals[1] / vals[0], 20))

print()
print('#' * 90)
print('B.  rank-one prediction test:  tau = C * prod_i exp(xi_i) * prod_k exp(eta_k)')
print('    i.e.  log tau  minus  sum_i xi_i  minus  sum_k eta_k   should be CONSTANT')
print('    (independent of x,y,t) if the matrix is rank one.')
print('#' * 90)
for N in (2, 3):
    print('  N=%d' % N)
    for (Xv, Yv, Tv) in [(mp.mpf(1) / 3, mp.mpf(-2) / 5, mp.mpf(3) / 7),
                         (mp.mpf(1), mp.mpf(2), mp.mpf(3)),
                         (mp.mpf(10), mp.mpf(20), mp.mpf(5))]:
        t0 = tau(N, 0, 0, a, Xv, Yv, Tv)
        S = sum(p[i] * Xv - p[i] ** 2 * Tv + Yv / (p[i] - a) for i in range(N)) + \
            sum(q[k] * Xv + q[k] ** 2 * Tv + Yv / (q[k] + a) for k in range(N))
        print('     (x,y,t)=(%s,%s,%s)  log tau - sum(xi+eta) = %s'
              % (mp.nstr(Xv, 4), mp.nstr(Yv, 4), mp.nstr(Tv, 4),
                 mp.nstr(mp.log(abs(t0)) - S, 20)))

print()
print('#' * 90)
print('C.  ratio test:  tau(n=1)*tau(n=-1)/tau(n=0)^2')
print('#' * 90)
for N in (1, 2, 3, 4):
    t0 = tau(N, 0, 0, a, X, Y, T)
    t1 = tau(N, 1, 0, a, X, Y, T)
    tm = tau(N, -1, 0, a, X, Y, T)
    print('   N=%d   sigma_n = %s' % (N, mp.nstr(t1 * tm / t0 ** 2, 20)))

print()
print('#' * 90)
print('D.  staggered pair:  F_j = tau_1(j; a-d), G_j = tau_0(j), and the field')
print('    u_j = 2 d_x ln(F_j/G_j)   [numeric differentiation]')
print('#' * 90)
# use the exponential structure: d_x of entry multiplies by rate
def dx_log(expr_fn, X0, Y0, T0, eps=mp.mpf('1e-15')):
    """numerical d_x ln of a tau-like function given as a callable"""
    f1 = expr_fn(X0 + eps, Y0, T0)
    f0 = expr_fn(X0 - eps, Y0, T0)
    return (mp.log(abs(f1)) - mp.log(abs(f0))) / (2 * eps)


for N in (1, 2, 3):
    F = lambda Xv, Yv, Tv: tau(N, 1, 0, s_lo, Xv, Yv, Tv)
    G = lambda Xv, Yv, Tv: tau(N, 0, 0, a, Xv, Yv, Tv)
    H = lambda Xv, Yv, Tv: F(Xv, Yv, Tv) / G(Xv, Yv, Tv)
    # exact rate instead of numeric diff:  log H = sum over monomials; use d_x log
    def dxlog_H(X0, Y0, T0, e=mp.mpf('1e-20')):
        return (mp.log(abs(H(X0 + e, Y0, T0))) - mp.log(abs(H(X0 - e, Y0, T0)))) / (2 * e)
    u = 2 * dxlog_H(X, Y, T)
    print('   N=%d   u_0 = 2 d_x ln(F/G) = %s      (continuum N=1 value p+q = %s)'
          % (N, mp.nstr(u, 18), mp.nstr(sum(p[:N]) + sum(q[:N]), 18)))
