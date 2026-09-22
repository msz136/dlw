"""
curve.py -- DECISIVE: is tr T(z) genuinely nonconstant, or is it an artefact of
finite z (i.e. does it converge to a constant as z -> infinity)?

If  tr T(z) -> const  and all 1/z-corrections vanish, the curve is trivial.
If  tr T(z) = c0 + c1/z + c2/z^2 + ...  with c1, c2, ... not all zero, the curve
is genuinely nontrivial and generates an infinite family of conserved densities.
"""
import sys
import mpmath as mp

sys.path.insert(0, r'C:\Users\msz\学术内容\Paper\gsg_project\lax')
from tau4 import Tau

mp.mp.dps = 80
H = mp.mpf(1) / 3
A = mp.mpf(17) / 5
PS = [mp.mpf(29) / 3, mp.mpf(12) / 5, mp.mpf(7)]
QS = [mp.mpf(40) / 3, mp.mpf(7) / 5, mp.mpf(9) / 2]
X0, Y0, T0 = mp.mpf(1) / 100, mp.mpf(-1) / 100, mp.mpf(1) / 100
N = 3
T = Tau(N, A, H, PS, QS)
TAU = {n: T.tau(n, xv=X0, yv=Y0, tv=T0) for n in range(-4, 8)}


def psi(n, z):
    z = mp.mpf(z)
    return T.tau(n, xv=X0 - 1 / z, yv=Y0, tv=T0 - mp.mpf(1) / 2 / z ** 2) / TAU[n]


def AB(n, z):
    p1, p0, pm, p2 = psi(n + 1, z), psi(n, z), psi(n - 1, z), psi(n + 2, z)
    dd = p1 * pm - p0 * p0
    return ((-p2 * pm + p1 * p0) / dd, (p1 * (-p1) - p0 * (-p2)) / dd)


def trdet(z):
    prod = mp.eye(2)
    for n in (-1, 0, 1):
        An, Bn = AB(n, z)
        prod = mp.matrix([[-An, -Bn], [1, 0]]) * prod
    return prod[0, 0] + prod[1, 1], prod[0, 0] * prod[1, 1] - prod[0, 1] * prod[1, 0]


print('=' * 94)
print('tr T(z) and det T(z) at large z  (does it settle to a constant?)')
print('=' * 94)
zs = [10 ** 2, 10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6, 10 ** 7]
vals = []
for z in zs:
    t, d = trdet(mp.mpf(z))
    vals.append((mp.mpf(z), t, d))
    print('   z=1e%-3d  tr T = %-26s  det T = %s'
          % (int(mp.log10(z)), mp.nstr(t, 22), mp.nstr(d, 22)))

print()
print('=' * 94)
print('fit  tr T(z) = c0 + c1/z + c2/z^2 + c3/z^3  (using the largest z values)')
print('=' * 94)
zs2 = [mp.mpf(10 ** 4), mp.mpf(10 ** 5), mp.mpf(10 ** 6), mp.mpf(10 ** 7)]
Mx = mp.matrix(4, 4)
rhs = mp.matrix(4, 1)
for r, zz in enumerate(zs2):
    for c in range(4):
        Mx[r, c] = 1 / zz ** c
    rhs[r] = trdet(zz)[0]
sol = mp.lu_solve(Mx, rhs)
names = ['c0', 'c1', 'c2', 'c3']
for i, nm in enumerate(names):
    print('   %s = %s' % (nm, mp.nstr(sol[i], 24)))
print()
print('   => tr T(z) is %s'
      % ('NONCONSTANT (nontrivial spectral curve!)'
         if any(abs(sol[i]) > mp.mpf('1e-30') for i in (1, 2, 3))
         else 'CONSTANT (trivial curve)'))

print()
print('=' * 94)
print('det T(z) at large z')
print('=' * 94)
Mx = mp.matrix(4, 4)
rhs = mp.matrix(4, 1)
for r, zz in enumerate(zs2):
    for c in range(4):
        Mx[r, c] = 1 / zz ** c
    rhs[r] = trdet(zz)[1]
sol = mp.lu_solve(Mx, rhs)
for i, nm in enumerate(['d0', 'd1', 'd2', 'd3']):
    print('   %s = %s' % (nm, mp.nstr(sol[i], 24)))
