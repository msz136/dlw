"""validate_ref.py -- validate tau_ref against the exact N=1 formula and the
raw matrix determinant."""
import sys
import itertools
import mpmath as mp

sys.path.insert(0, r'C:\Users\msz\学术内容\Paper\gsg_project\lax')
from tau_ref import Ref

mp.mp.dps = 60
H = mp.mpf(1) / 3
A = mp.mpf(17) / 5
PS = [mp.mpf(29) / 3, mp.mpf(12) / 5, mp.mpf(7), mp.mpf(31) / 4]
QS = [mp.mpf(40) / 3, mp.mpf(7) / 5, mp.mpf(9) / 2, mp.mpf(13) / 3]
X0, Y0, T0 = mp.mpf(1) / 100, mp.mpf(-1) / 100, mp.mpf(1) / 100

print('=' * 92)
print('1.  N=1 closed form must equal  1 + A_11 E_11  exactly')
print('=' * 92)
R = Ref(1, A, H, PS[:1], QS[:1])
for (n, j, s) in [(0, 0, A), (1, 0, A), (0, 1, A), (1, 2, A), (1, 0, A - H / 2)]:
    E = mp.e ** (R.xi(0, s, X0, Y0, T0) + R.eta(0, s, X0, Y0, T0))
    exact = 1 + R.A(n, j, 0, 0, s) * E
    got_c = R.tau_closed(n, j, s, X0, Y0, T0)
    got_r = R.tau_raw(n, j, s, X0, Y0, T0)
    print('  n=%d j=%d s=%-8s  1+A*E=%-22s closed=%-22s raw=%-22s  |dc|=%-8s |dr|=%-8s'
          % (n, j, mp.nstr(s, 6), mp.nstr(exact, 16), mp.nstr(got_c, 16), mp.nstr(got_r, 16),
             mp.nstr(abs(got_c / exact - 1), 3), mp.nstr(abs(got_r / exact - 1), 3)))

print()
print('=' * 92)
print('2.  closed form vs raw determinant, N = 2,3,4   (validates the identity')
print('    det = prod(e^xi) prod(e^eta) * det(delta + A) )')
print('=' * 92)
for N in (2, 3, 4):
    R = Ref(N, A, H, PS[:N], QS[:N])
    for (n, j, s) in [(0, 0, A), (1, 0, A), (2, 1, A), (1, 3, A - H / 2)]:
        c = R.tau_closed(n, j, s, X0, Y0, T0)
        r = R.tau_raw(n, j, s, X0, Y0, T0)
        print('  N=%d n=%d j=%d  closed=%-24s raw=%-24s  rel.diff=%s'
              % (N, n, j, mp.nstr(c, 16), mp.nstr(r, 16), mp.nstr(abs(c / r - 1), 3)))
