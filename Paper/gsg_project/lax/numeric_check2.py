"""numeric_check2.py -- high precision, no sympy."""
import mpmath as mp

mp.mp.dps = 50
a = mp.mpf(17) / 5
h = mp.mpf(1) / 3
p = [mp.mpf(29) / 3, mp.mpf(12) / 5]
q = [mp.mpf(40) / 3, mp.mpf(7) / 5]


def entry(n, i, k, s, X, Y, T, j=0):
    P = p[i] - s
    Q = q[k] + s
    coef = (-P / Q) ** n / (p[i] + q[k])
    if j:
        lam = lambda v: (v + h / 2) / (v - h / 2)
        coef *= (lam(p[i] - a) * lam(q[k] + a)) ** j
    xi = p[i] * X - p[i] ** 2 * T + Y / P
    eta = q[k] * X + q[k] ** 2 * T + Y / Q
    return coef * mp.e ** (xi + eta)


X, Y, T = mp.mpf(1) / 3, mp.mpf(-2) / 5, mp.mpf(3) / 7
print('a =', a, 'p =', p, 'q =', q)
print()
print('entry values and their exact log-rates (d/dx, d/dt, d/dy of log entry):')
rates = {}
for i in range(2):
    for k in range(2):
        e = entry(0, i, k, a, X, Y, T)
        r = (p[i] + q[k], q[k] ** 2 - p[i] ** 2, 1 / (p[i] - a) + 1 / (q[k] + a))
        rates[(i, k)] = r
        print('  M[%d,%d] = %s   rate=(%s,%s,%s)' % (i, k, mp.nstr(e, 12), *[mp.nstr(v, 12) for v in r]))
print()
print('PRODUCT rate comparisons:')
print('  diag  (0,0)+(1,1) :', [mp.nstr(x, 20) for x in
                               [rates[(0, 0)][t] + rates[(1, 1)][t] for t in range(3)]])
print('  offd  (0,1)+(1,0) :', [mp.nstr(x, 20) for x in
                               [rates[(0, 1)][t] + rates[(1, 0)][t] for t in range(3)]])
print('  difference        :', [mp.nstr(rates[(0, 0)][t] + rates[(1, 1)][t]
                                        - rates[(0, 1)][t] - rates[(1, 0)][t], 20) for t in range(3)])
print()
# the determinant
M = mp.matrix(2, 2)
for i in range(2):
    for k in range(2):
        M[i, k] = entry(0, i, k, a, X, Y, T)
        if i == k:
            M[i, k] += 1
print('det M =', mp.nstr(mp.det(M), 20))
print()
print('a00*a11 =', mp.nstr(M[0, 0] * M[1, 1], 20))
print('a01*a10 =', mp.nstr(M[0, 1] * M[1, 0], 20))
print('ratio   =', mp.nstr((M[0, 0] * M[1, 1]) / (M[0, 1] * M[1, 0]), 20))
print()
# recompute the coefficient-only determinant
c = mp.matrix(2, 2)
for i in range(2):
    for k in range(2):
        c[i, k] = entry(0, i, k, a, X, Y, T) / mp.e ** (rates[(i, k)][0] * X
                                                        + rates[(i, k)][1] * T
                                                        + rates[(i, k)][2] * Y)
print('coefficient matrix (should be A_ik = 1/(p_i+q_k)):')
print('  ', mp.nstr(c[0, 0], 20), mp.nstr(c[0, 1], 20))
print('  ', mp.nstr(c[1, 0], 20), mp.nstr(c[1, 1], 20))
print('1/(p_i+q_k):')
print('  ', mp.nstr(1 / (p[0] + q[0]), 20), mp.nstr(1 / (p[0] + q[1]), 20))
print('  ', mp.nstr(1 / (p[1] + q[0]), 20), mp.nstr(1 / (p[1] + q[1]), 20))
