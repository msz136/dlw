"""Direction G, check 6b: solve for the exact closed form of the mode-pair
eigenvalue symbolically (no guessing).

Run:  python -u g6b_solve.py
"""
from itertools import product

import sympy as sp

k1, k2, a, delta = sp.symbols("k1 k2 a delta")
w1 = -(k1**2 + 2 * a * k1)
w2 = -(k2**2 + 2 * a * k2)
modes = list(product((0, 1), repeat=2))


def eig(mu, nu, s):
    K = (mu[0] * k1 + mu[1] * k2) - (nu[0] * k1 + nu[1] * k2)
    W = (mu[0] * w1 + mu[1] * w2) - (nu[0] * w1 + nu[1] * w2)
    return sp.expand(K**2 + W + 2 * s * K), sp.expand(K)


print("=== delta = 0 : eigen(a) for every pair, factored ===")
for mu in modes:
    for nu in modes:
        e, K = eig(mu, nu, a)
        print(f"mu={mu} nu={nu} K={K}  eigen(a)={sp.factor(e)}")

print("\n=== delta coefficient: eigen(a+delta) - eigen(a) - c*K, solve for c ===")
c = sp.symbols("c")
for mu in modes:
    for nu in modes:
        e1, K = eig(mu, nu, a + delta)
        e0, _ = eig(mu, nu, a)
        resid = sp.expand(e1 - e0 - c * K)
        sol = sp.solve(sp.Eq(resid, 0), c)
        print(f"mu={mu} nu={nu}  c = {sol}")

print("\n=== full closed form: eigen(a+delta) vs (1+2 delta)K + P, P solved ===")
P = sp.symbols("P")
for mu in modes:
    for nu in modes:
        e, K = eig(mu, nu, a + delta)
        resid = sp.expand(e - (1 + 2 * delta) * K)
        print(f"mu={mu} nu={nu}  remainder = {sp.factor(resid)}")
