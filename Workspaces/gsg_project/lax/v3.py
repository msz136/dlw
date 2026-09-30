"""v3.py -- validate tau3 (two independent paths) and recompute sigma_n."""
import sys
import mpmath as mp

sys.path.insert(0, r'C:\Users\msz\学术内容\Workspaces\gsg_project\lax')
from tau3 import Tau

mp.mp.dps = 60
H = mp.mpf(1) / 3
A = mp.mpf(17) / 5
PS = [mp.mpf(29) / 3, mp.mpf(12) / 5, mp.mpf(7), mp.mpf(31) / 4]
QS = [mp.mpf(40) / 3, mp.mpf(7) / 5, mp.mpf(9) / 2, mp.mpf(13) / 3]
CV = [mp.mpf(1), mp.mpf(3) / 2, mp.mpf(2) / 3, mp.mpf(5) / 4]
X0, Y0, T0 = mp.mpf(1) / 100, mp.mpf(-1) / 100, mp.mpf(1) / 100

print('=' * 92)
print('1.  tau (principal-minor sum)  vs  tau_raw (literal determinant)')
print('=' * 92)
ok = True
for N in (1, 2, 3, 4):
    T = Tau(N, A, H, PS[:N], QS[:N], CV[:N])
    for n in (-1, 0, 1, 2):
        a_ = T.tau(n, xv=X0, yv=Y0, tv=T0)
        b_ = T.tau_raw(n, xv=X0, yv=Y0, tv=T0)
        rel = abs(a_ - b_) / max(abs(a_), abs(b_), mp.mpf('1e-300'))
        if rel > mp.mpf('1e-40'):
            ok = False
        print('   N=%d n=%2d   subset=%-24s raw=%-24s rel=%s'
              % (N, n, mp.nstr(a_, 16), mp.nstr(b_, 16), mp.nstr(rel, 3)))
print('   ALL MATCH' if ok else '   *** MISMATCH ***')

print()
print('=' * 92)
print('2.  sigma_n = tau_{n+1} tau_{n-1} / tau_n^2')
print('=' * 92)
for N in (1, 2, 3, 4):
    T = Tau(N, A, H, PS[:N], QS[:N], CV[:N])
    for n in (0, 1, 2):
        t1 = T.tau(n + 1, xv=X0, yv=Y0, tv=T0)
        t0 = T.tau(n, xv=X0, yv=Y0, tv=T0)
        tm = T.tau(n - 1, xv=X0, yv=Y0, tv=T0)
        print('   N=%d n=%d   sigma_n = %s' % (N, n, mp.nstr(t1 * tm / t0 ** 2, 25)))
    # also n = 0 and check whether sigma depends on n
    s0 = T.tau(1, xv=X0, yv=Y0, tv=T0) * T.tau(-1, xv=X0, yv=Y0, tv=T0) / T.tau(0, xv=X0, yv=Y0, tv=T0) ** 2
    s1 = T.tau(2, xv=X0, yv=Y0, tv=T0) * T.tau(0, xv=X0, yv=Y0, tv=T0) / T.tau(1, xv=X0, yv=Y0, tv=T0) ** 2
    print('      N=%d  sigma_0 = %s   sigma_1 = %s   equal? %s'
          % (N, mp.nstr(s0, 16), mp.nstr(s1, 16),
             'yes' if abs(s0 / s1 - 1) < mp.mpf('1e-30') else 'NO'))

print()
print('=' * 92)
print('3.  ratio tau_{n+1}/tau_n  (is it n-independent?)')
print('=' * 92)
for N in (1, 2, 3, 4):
    T = Tau(N, A, H, PS[:N], QS[:N], CV[:N])
    rs = []
    for n in (-1, 0, 1, 2):
        rs.append(T.tau(n + 1, xv=X0, yv=Y0, tv=T0) / T.tau(n, xv=X0, yv=Y0, tv=T0))
    print('   N=%d  ' % N + '  '.join(mp.nstr(r, 12) for r in rs))
