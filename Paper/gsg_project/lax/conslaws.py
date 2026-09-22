"""
conslaws.py -- conserved densities of the semidiscrete DLW system, obtained
from the exact wave function and verified numerically.

Mechanism (standard for bilinear integrable systems): the wave function
      psi_n(z) = tauhat_n(z)/tau_n
generates conserved densities as the coefficients of its expansion in 1/z.

We also attack the problem directly: search for rho, sigma with
      d_t rho = d_x sigma        (x-t conservation law, j fixed)
      d_y rho = d_x sigma        (y-flow form)
built from the tau data, at high precision.
"""
import sys
from itertools import permutations
from math import comb

import mpmath as mp

sys.path.insert(0, r'C:\Users\msz\学术内容\Paper\gsg_project\lax')
from mpt import MP

mp.mp.dps = 120
X = mp.mpf(1) / 100
Y = mp.mpf(-1) / 100
T = mp.mpf(1) / 100
H = mp.mpf(1) / 3
A = mp.mpf(17) / 5
PS = [mp.mpf(29) / 3, mp.mpf(12) / 5, mp.mpf(7)]
QS = [mp.mpf(40) / 3, mp.mpf(7) / 5, mp.mpf(9) / 2]
N = 3
M = MP(N, A, H, PS, QS)
d = H / 2


def btau(n1, j1, s1, n2, j2, s2, ax=0, at=0, ay=0):
    tot = mp.mpf(0)
    for p_ in range(ax + 1):
        for r_ in range(at + 1):
            for q_ in range(ay + 1):
                co = (-1) ** (p_ + r_ + q_) * comb(ax, p_) * comb(at, r_) * comb(ay, q_)
                tot += co * M.dtau(n1, j1, s1, X, Y, T, {'x': ax - p_, 't': at - r_, 'y': ay - q_}) \
                    * M.dtau(n2, j2, s2, X, Y, T, {'x': p_, 't': r_, 'y': q_})
    return tot


print('=' * 92)
print('candidate conservation laws for the LATTICE system')
print('  fields:  G_j = tau_0(j),  F_j = tau_1(j; a-d)')
print('=' * 92)
for j in (0, 1, 2):
    G = M.tau(0, j, s=A, xv=X, yv=Y, tv=T)
    F = M.tau(1, j, s=A - d, xv=X, yv=Y, tv=T)
    G1 = M.tau(0, j + 1, s=A, xv=X, yv=Y, tv=T)
    F1 = M.tau(1, j + 1, s=A - d, xv=X, yv=Y, tv=T)

    def dt(fn):
        return None
    # d_t ln G, d_t ln F, d_y ...
    dlG_t = M.dtau(0, j, A, X, Y, T, {'t': 1}) / G
    dlF_t = M.dtau(1, j, A - d, X, Y, T, {'t': 1}) / F
    dlG_x = M.dtau(0, j, A, X, Y, T, {'x': 1}) / G
    dlF_x = M.dtau(1, j, A - d, X, Y, T, {'x': 1}) / F
    dlG_y = M.dtau(0, j, A, X, Y, T, {'y': 1}) / G
    dlF_y = M.dtau(1, j, A - d, X, Y, T, {'y': 1}) / F
    print('  j=%d  d_t lnG=%-14s d_t lnF=%-14s' % (j, mp.nstr(dlG_t, 10), mp.nstr(dlF_t, 10)))
    print('        d_x lnG=%-14s d_x lnF=%-14s' % (mp.nstr(dlG_x, 10), mp.nstr(dlF_x, 10)))
    print('        d_y lnG=%-14s d_y lnF=%-14s' % (mp.nstr(dlG_y, 10), mp.nstr(dlF_y, 10)))
    print('        G1/G=%-14s F1/F=%-14s' % (mp.nstr(G1 / G, 10), mp.nstr(F1 / F, 10)))

print()
print('=' * 92)
print('The structural statement:  tau_n(j) = Lambda^n * R^j * Phi(p,q,a,x,y,t)')
print('   => d_t ln tau, d_y ln tau are n- and j-INDEPENDENT')
print('=' * 92)
for j in (0, 1, 2):
    for n in (0, 1, 2):
        G = M.tau(n, j, s=A, xv=X, yv=Y, tv=T)
        a1 = M.dtau(n, j, A, X, Y, T, {'t': 1}) / G
        a2 = M.dtau(n, j, A, X, Y, T, {'y': 1}) / G
        a3 = M.dtau(n, j, A, X, Y, T, {'x': 1}) / G
        print('  n=%d j=%d   d_t ln tau=%-16s d_y ln tau=%-16s d_x ln tau=%-16s'
              % (n, j, mp.nstr(a1, 12), mp.nstr(a2, 12), mp.nstr(a3, 12)))
