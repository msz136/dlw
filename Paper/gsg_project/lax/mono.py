"""
mono.py -- is the z-monodromy of the discrete Lax pair trivial?

psi_{n+1} = L_n psi_n ,  L_n(z) = (z + alpha_{n+1})/(z + alpha_n)

Composition identity:  L_{n+1} o L_n = L_{n+2}  (exact algebra), hence over any
complete cycle of the (periodic) lattice the monodromy map is the IDENTITY.

We check (a) the composition identity, (b) tr T(z) through a full period.
"""
import sys
import mpmath as mp

sys.path.insert(0, r'C:\Users\msz\学术内容\Paper\gsg_project\lax')
from tau4 import Tau, det_exact

mp.mp.dps = 80
H = mp.mpf(1) / 3
A = mp.mpf(17) / 5
PS = [mp.mpf(29) / 3, mp.mpf(12) / 5, mp.mpf(7)]
QS = [mp.mpf(40) / 3, mp.mpf(7) / 5, mp.mpf(9) / 2]
X0, Y0, T0 = mp.mpf(1) / 100, mp.mpf(-1) / 100, mp.mpf(1) / 100
T = Tau(3, A, H, PS, QS)
N = T.N
uu, vv = list(T.p), list(T.q)


def tauhat(n, zinv):
    M = T.gram(n, T.a, X0, Y0, T0).copy()
    for i in range(N):
        for k in range(N):
            M[i, k] += zinv * uu[i] * vv[k]
    return det_exact(M)


def psi(n, z):
    return tauhat(n, 1 / z) / T.tau(n, xv=X0, yv=Y0, tv=T0)


def alpha(n):
    return (psi(n, mp.mpf('1e8')) - 1) * mp.mpf('1e8')


print('=' * 90)
print('(a)  composition identity  L_{n+1}(L_n(z)) = L_{n+2}(z) ?')
print('=' * 90)
al = {n: alpha(n) for n in range(4)}
print('   alpha_0..3 =', [mp.nstr(al[n], 16) for n in range(4)])
for n in range(2):
    for z in (mp.mpf('1.5'), mp.mpf(4), mp.mpf(30)):
        Ln = (z + al[n + 1]) / (z + al[n])
        Ln1 = (Ln + al[n + 2]) / (Ln + al[n + 1])
        Ln2 = (z + al[n + 2]) / (z + al[n + 1])
        print('   n=%d z=%-6s  L_{n+1}(L_n)=%-20s  L_{n+2}=%-20s  rel=%s'
              % (n, mp.nstr(z, 4), mp.nstr(Ln1, 14), mp.nstr(Ln2, 14),
                 mp.nstr(abs(Ln1 / Ln2 - 1), 4)))

print()
print('=' * 90)
print('(b)  monodromy matrix over a full period of length 3')
print('     T(z) = [1 al_0; 1 al_-1] [1 al_1; 1 al_0] [1 al_2; 1 al_1]   (period 3)')
print('=' * 90)


def mat(z, a_hi, a_lo):
    return mp.matrix([[1, a_hi], [1, a_lo]])


# a genuine period-3 sequence: use alpha_0,1,2,0
seq_hi = [al[1], al[2], al[0]]
seq_lo = [al[0], al[1], al[2]]
for z in (mp.mpf('1.5'), mp.mpf(4), mp.mpf(30), mp.mpf(1000)):
    Mm = mp.matrix([[1, 0], [0, 1]])
    for a_hi, a_lo in zip(seq_hi, seq_lo):
        Mm = mat(z, a_hi, a_lo) * Mm
    print('   z=%-8s  tr T(z) = %-22s  det T(z) = %s'
          % (mp.nstr(z, 6), mp.nstr(Mm[0, 0] + Mm[1, 1], 18),
             mp.nstr(Mm[0, 0] * Mm[1, 1] - Mm[0, 1] * Mm[1, 0], 18)))
