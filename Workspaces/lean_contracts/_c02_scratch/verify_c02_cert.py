"""Honest verification of the C02 certificate.

Jet ring: symbols A(i,j,k), B(i,j,k) = d_x^i d_y^j d_t^k A/B, Clairaut built in
by construction (multi-index).  Everything is exact sympy (no floats).

Checks
  (1) c1 == 2*Dx(Dy(R))
  (2) c2 == 2*Dx(Dy(R)) - 2*Dx(S)
  (3) bridge: cbil a f (sy g)/(f g) == (sy q)*R + E   (via C13 + log-derivative trick)
  (4) 2*E + 4*sx B == S (A,B form)  and  S == -(syA-syB)*R  on the hypotheses
"""
import sympy as sp
from sympy import symbols, expand, simplify, cancel, Rational

M = 8
A = {}
B = {}
for i in range(M + 1):
    for j in range(M + 1):
        for k in range(M + 1):
            if i + j + k <= M:
                A[(i, j, k)] = sp.Symbol('A_%d_%d_%d' % (i, j, k))
                B[(i, j, k)] = sp.Symbol('B_%d_%d_%d' % (i, j, k))

a = sp.Symbol('a')


def D(expr, v):
    """total derivative w.r.t. variable v (0=x,1=y,2=t) of a jet polynomial"""
    sub = {}
    for idx, s in A.items():
        t = list(idx)
        t[v] += 1
        if sum(t) <= M:
            sub[s] = A[tuple(t)]
    for idx, s in B.items():
        t = list(idx)
        t[v] += 1
        if sum(t) <= M:
            sub[s] = B[tuple(t)]
    return sp.expand(expr.subs(sub, simultaneous=True))


Dx = lambda e: D(e, 0)
Dy = lambda e: D(e, 1)
Dt = lambda e: D(e, 2)

# ---------------------------------------------------------------- A,B objects
R = A[(2, 0, 0)] + B[(1, 0, 0)]**2 + B[(0, 0, 1)] + 2 * a * B[(1, 0, 0)]

S = (A[(2, 1, 0)] - B[(2, 1, 0)] - A[(0, 1, 1)] + B[(0, 1, 1)]
     - 2 * B[(1, 0, 0)] * (A[(1, 1, 0)] - B[(1, 1, 0)])
     - 2 * a * (A[(1, 1, 0)] - B[(1, 1, 0)])
     + 4 * B[(1, 0, 0)])

c1 = (2 * B[(1, 1, 1)] + 2 * A[(3, 1, 0)] + 4 * B[(2, 0, 0)] * B[(1, 1, 0)]
      + 4 * B[(1, 0, 0)] * B[(2, 1, 0)] + 4 * a * B[(2, 1, 0)])
c2 = (2 * A[(1, 1, 1)] + 4 * B[(2, 0, 0)] * A[(1, 1, 0)]
      + 4 * B[(1, 0, 0)] * A[(2, 1, 0)] + 2 * B[(3, 1, 0)]
      + 4 * a * A[(2, 1, 0)] - 8 * B[(2, 0, 0)])

print('(1) c1 - 2 DxDy R  =', expand(c1 - 2 * Dx(Dy(R))))
print('(2) c2 - (2 DxDy R - 2 Dx S) =', expand(c2 - (2 * Dx(Dy(R)) - 2 * Dx(S))))

# also in canonical "syntactic" form used in Lean: c2 = 2*sx(sy R) - 2*sx S
print('(2b) c2 - (2 Dx(Dy(R)) - 2 Dx(S)) with S = 2E+4sxB:', end=' ')
E_AB = (S - 4 * B[(1, 0, 0)]) / 2
print(expand(E_AB * 2 + 4 * B[(1, 0, 0)] - S))

# ------------------------------------------------------------- bridge identity
# p = log f, q = log g ;  A = p+q, B = p-q
# C13: bil a f g /(f g) = (p+q)_xx + ((p-q)_x)^2 + (p-q)_t + 2a (p-q)_x  =  R
print('(3a) C13 quotient == R:',
      expand((A[(2, 0, 0)]) + B[(1, 0, 0)]**2 + B[(0, 0, 1)]
             + 2 * a * B[(1, 0, 0)] - R))

# For the pair (f, sy g):  log(sy g) = q + L,  L = log(q_y)
# q_y = (A_y-B_y)/2 ; q_xy = (A_xy-B_xy)/2 ; q_xxy = (A_xxy-B_xxy)/2 ; q_yt = (A_yt-B_yt)/2
qy = (A[(0, 1, 0)] - B[(0, 1, 0)]) / 2
qxy = (A[(1, 1, 0)] - B[(1, 1, 0)]) / 2
qxxy = (A[(2, 1, 0)] - B[(2, 1, 0)]) / 2
qyt = (A[(0, 1, 1)] - B[(0, 1, 1)]) / 2
Lx = qxy / qy
Lxx = qxxy / qy - (qxy / qy)**2
Lt = qyt / qy

# bracket for the pair (f, sy g) :  log f = p, log(sy g) = q + L
# (p + q + L)_xx + ((p - q - L)_x)^2 + (p - q - L)_t + 2a (p - q - L)_x
brack = ((A[(2, 0, 0)] + Lxx)
         + (B[(1, 0, 0)] - Lx)**2
         + (B[(0, 0, 1)] - Lt)
         + 2 * a * (B[(1, 0, 0)] - Lx))
E = qxxy - 2 * B[(1, 0, 0)] * qxy - qyt - 2 * a * qxy
diff = cancel(sp.together(qy * brack - (qy * R + E)))
print('(3b) [cbil a f (sy g)]/(fg) - (q_y R + E) =', diff)

# (4) E relation:  2E + 4 sxB == S ?
twoE_plus = expand(2 * E + 4 * B[(1, 0, 0)] - S)
print('(4a) 2E + 4 sxB - S =', twoE_plus)

# H2 : (sy q) R + E + 2 sx B = 0  ==>  S = -2 (sy q) R  (using R = 0)
lhs = qy * R + E + 2 * B[(1, 0, 0)]
print('(4b) S + 2 (sy q) R - 2*(sy q R + E + 2 sxB) =',
      expand(S + 2 * qy * R - 2 * lhs))

# final sanity: c2 == 2 DxDy R - 2 Dx S exactly (already (2)), now confirm
# with S written as 2E+4sxB and E as above
S2 = expand(2 * E + 4 * B[(1, 0, 0)])
print('(5) S == 2E+4sxB :', expand(S2 - S))
print('(6) c2 - (2 DxDyR - 2 Dx S2) :', expand(c2 - (2 * Dx(Dy(R)) - 2 * Dx(S2))))
