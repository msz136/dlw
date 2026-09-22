"""Direction G, check 6a: brute-force closed form discovery for the mode-pair
eigenvalue of the DLW bilinear operator B_s = D_x^2 + D_t + 2 s D_x.

We fix the two dispersion relations  k_i^2 + w_i + 2 a k_i = 0  by substituting
w_i = -(k_i^2 + 2 a k_i), form the eigenvalue

    eigen s mu nu = K^2 + W + 2 s K ,  K = k_mu - k_nu , W = w_mu - w_nu ,

as a polynomial in k1, k2, a, delta (s = a + delta), and solve for its exact
decomposition.  We then print the coefficient of each monomial, and separately
verify the resulting formula on the 16 mode pairs at exact rationals.

Run:  python -u g6a_closed_form.py
"""
from fractions import Fraction as F
from itertools import product

import sympy as sp

k1, k2, a, delta = sp.symbols("k1 k2 a delta")
w1 = -(k1**2 + 2 * a * k1)
w2 = -(k2**2 + 2 * a * k2)

modes = list(product((0, 1), repeat=2))

print("=== eigen (a+delta) as a polynomial in k1,k2,a,delta ===")
table = {}
for mu in modes:
    for nu in modes:
        K = (mu[0] * k1 + mu[1] * k2) - (nu[0] * k1 + nu[1] * k2)
        W = (mu[0] * w1 + mu[1] * w2) - (nu[0] * w1 + nu[1] * w2)
        e = sp.expand(K**2 + W + 2 * (a + delta) * K)
        table[(mu, nu)] = sp.expand(e)
        d0, d1 = mu[0] - nu[0], mu[1] - nu[1]
        print(f"mu={mu} nu={nu} d=({d0},{d1}) eigen = {sp.factor(e)}")

print("\n=== candidate closed forms ===")
cands = {
    "K + P1 (P1=d0(d0-1)k1^2+d1(d1-1)k2^2)":
        lambda mu, nu: (1 + 2 * delta) * ((mu[0] - nu[0]) * k1 + (mu[1] - nu[1]) * k2)
        + ((mu[0] - nu[0]) * ((mu[0] - nu[0]) - 1) * k1**2
           + (mu[1] - nu[1]) * ((mu[1] - nu[1]) - 1) * k2**2),
}
for name, f in cands.items():
    bad = [key for key, val in table.items()
           if sp.simplify(sp.expand(val - f(*key))) != 0]
    print(f"  {name}: {'OK' if not bad else 'FAIL on ' + str(bad[:3])}")

# ------------------------------------------------- explicit exact-rational check
print("\n=== exact rational check, a = -2, q = 2, several p ===")
OK = True
for p1 in (F(1), F(3, 2), F(2), F(5, 2)):
    for p2 in (F(1), F(3, 2), F(2), F(5, 2)):
        q1, q2 = F(2), F(2)
        A = F(-2)
        K1, K2 = p1 + q1, p2 + q2
        W1, W2 = q1**2 - p1**2, q2**2 - p2**2
        if K1**2 + W1 + 2 * A * K1 != 0 or K2**2 + W2 + 2 * A * K2 != 0:
            continue
        for mu in modes:
            for nu in modes:
                K = (mu[0] * K1 + mu[1] * K2) - (nu[0] * K1 + nu[1] * K2)
                W = (mu[0] * W1 + mu[1] * W2) - (nu[0] * W1 + nu[1] * W2)
                for dl in (F(0), F(1, 10), F(-2, 7)):
                    lhs = K * K + W + 2 * (A + dl) * K
                    d0, d1 = mu[0] - nu[0], mu[1] - nu[1]
                    rhs = (1 + 2 * dl) * K + K1**2 * d0 * (d0 - 1) + K2**2 * d1 * (d1 - 1)
                    if lhs != rhs:
                        OK = False
                        print("   FAIL", p1, p2, mu, nu, dl, lhs, rhs)
                        break
print("   exact check:", "PASS" if OK else "FAIL")
