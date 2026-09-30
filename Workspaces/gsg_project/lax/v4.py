"""v4.py -- validate tau4 and recompute the fundamental quantities."""
import sys
import mpmath as mp

sys.path.insert(0, r'C:\Users\msz\学术内容\Workspaces\gsg_project\lax')
from tau4 import Tau

mp.mp.dps = 60
H = mp.mpf(1) / 3
A = mp.mpf(17) / 5
PS = [mp.mpf(29) / 3, mp.mpf(12) / 5, mp.mpf(7), mp.mpf(31) / 4]
QS = [mp.mpf(40) / 3, mp.mpf(7) / 5, mp.mpf(9) / 2, mp.mpf(13) / 3]
CV = [mp.mpf(1)] * 4
X0, Y0, T0 = mp.mpf(1) / 100, mp.mpf(-1) / 100, mp.mpf(1) / 100

print('=' * 92)
print('1. principal-minor expansion vs literal Gram determinant')
print('=' * 92)
bad = 0
for N in (1, 2, 3, 4):
    T = Tau(N, A, H, PS[:N], QS[:N], CV[:N])
    for n in (-1, 0, 1, 2):
        a_ = T.tau(n, xv=X0, yv=Y0, tv=T0)
        b_ = T.tau_raw(n, xv=X0, yv=Y0, tv=T0)
        rel = abs(a_ - b_) / max(abs(a_), abs(b_), mp.mpf('1e-300'))
        if rel > mp.mpf('1e-45'):
            bad += 1
        print('   N=%d n=%2d  minor=%-22s raw=%-22s rel=%s'
              % (N, n, mp.nstr(a_, 16), mp.nstr(b_, 16), mp.nstr(rel, 3)))
print('   ==> %s' % ('ALL MATCH' if bad == 0 else '*** %d MISMATCHES ***' % bad))

print()
print('=' * 92)
print('2. sigma_n = tau_{n+1} tau_{n-1}/tau_n^2   (nontrivial Toda potential?)')
print('=' * 92)
for N in (1, 2, 3, 4):
    T = Tau(N, A, H, PS[:N], QS[:N], CV[:N])
    vals = []
    for n in (-1, 0, 1, 2):
        t1 = T.tau(n + 1, xv=X0, yv=Y0, tv=T0)
        t0 = T.tau(n, xv=X0, yv=Y0, tv=T0)
        tm = T.tau(n - 1, xv=X0, yv=Y0, tv=T0)
        vals.append(t1 * tm / t0 ** 2)
    print('   N=%d  sigma_n (n=-1,0,1,2): %s'
          % (N, '  '.join(mp.nstr(v, 14) for v in vals)))

print()
print('=' * 92)
print('3. ratio  tau_{n+1}/tau_n')
print('=' * 92)
for N in (1, 2, 3, 4):
    T = Tau(N, A, H, PS[:N], QS[:N], CV[:N])
    rs = [T.tau(n + 1, xv=X0, yv=Y0, tv=T0) / T.tau(n, xv=X0, yv=Y0, tv=T0)
          for n in (-1, 0, 1, 2)]
    print('   N=%d  %s' % (N, '  '.join(mp.nstr(r, 12) for r in rs)))
