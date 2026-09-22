"""final_check.py -- pure mpmath, no sympy.  Decides the rank-one question."""
import mpmath as mp

mp.mp.dps = 60
a = mp.mpf(17) / 5
p = [mp.mpf(29) / 3, mp.mpf(12) / 5]
q = [mp.mpf(40) / 3, mp.mpf(7) / 5]

X, Y, T = mp.mpf(1) / 3, mp.mpf(-2) / 5, mp.mpf(3) / 7


def logentry(n, i, k, s, X, Y, T):
    """log of the (i,k) Gram entry (coefficient + exponent), exactly."""
    P = p[i] - s
    Q = q[k] + s
    coef = mp.log(abs((-P / Q) ** n / (p[i] + q[k])))
    xi = p[i] * X - p[i] ** 2 * T + Y / P
    eta = q[k] * X + q[k] ** 2 * T + Y / Q
    return coef + xi + eta


def entry(n, i, k, s, X, Y, T):
    v = logentry(n, i, k, s, X, Y, T)
    sgn = 1
    if ((-p[i] + s) / (q[k] + s)) ** n / (p[i] + q[k]) < 0:
        sgn = -1
    return sgn * mp.e ** v


print('log of each entry (n=0, s=a):')
for i in range(2):
    for k in range(2):
        print('   (%d,%d) log = %s' % (i, k, mp.nstr(logentry(0, i, k, a, X, Y, T), 30)))
print()
print('sum of logs along the two perfect matchings:')
d1 = logentry(0, 0, 0, a, X, Y, T) + logentry(0, 1, 1, a, X, Y, T)
d2 = logentry(0, 0, 1, a, X, Y, T) + logentry(0, 1, 0, a, X, Y, T)
print('   (0,0)+(1,1) : %s' % mp.nstr(d1, 30))
print('   (0,1)+(1,0) : %s' % mp.nstr(d2, 30))
print('   difference  : %s' % mp.nstr(d1 - d2, 30))
print()
print('=> the two products differ by the constant factor  exp(%s) = %s'
      % (mp.nstr(d1 - d2, 12), mp.nstr(mp.e ** (d1 - d2), 20)))
print()
M = mp.matrix(2, 2)
for i in range(2):
    for k in range(2):
        M[i, k] = entry(0, i, k, a, X, Y, T)
        if i == k:
            M[i, k] += 1
print('det   =', mp.nstr(mp.det(M), 25))
print('a00a11=', mp.nstr(M[0, 0] * M[1, 1], 25))
print('a01a10=', mp.nstr(M[0, 1] * M[1, 0], 25))
print('1 term =', mp.nstr(1 + M[0, 0] + M[1, 1], 25))
print()
print('a00 =', mp.nstr(M[0, 0], 25))
print('a11 =', mp.nstr(M[1, 1], 25))
print('a01 =', mp.nstr(M[0, 1], 25))
print('a10 =', mp.nstr(M[1, 0], 25))
