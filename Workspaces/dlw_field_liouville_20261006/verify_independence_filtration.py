"""Finite exact checks supporting the separate all-order filtration proof.

The proof is in INDEPENDENCE.md. This script is not the induction proof.
No Fourier truncation of the dynamics is made: Fourier polynomials only
specify one field and six admissible tangent vectors on its Casimir leaf.
"""
import importlib.util
import json
from pathlib import Path

import sympy as s

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "dlw_conservation_hierarchy_20261004/lax/verify_fixed_leaf_independence.py"
spec = importlib.util.spec_from_file_location("fourier_dual", SOURCE)
fd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fd)
fd.NDUAL = 7
def dual7(value, derivative=None):
    result = [s.sympify(value)] + [s.Integer(0)] * 6
    if derivative is not None:
        result[derivative + 1] = s.Integer(1)
    return tuple(result)

fd.dual = dual7
fd.ZERO = fd.dual(0)
fd.ONE = fd.dual(1)


def mode(k, value=0, derivative=None):
    coefficient = fd.scale(fd.dual(value, derivative), s.Rational(1, 2))
    return {k: coefficient, -k: coefficient}


def main():
    z, g, f, e, mu = s.symbols("z g f e mu", nonzero=True)
    mean_u = mu - f * e / g
    us = [mean_u + f, mean_u - f]
    gs = [g + e, g - e]
    pp = s.prod((z - (u + w) / 2) / (z - (u - w) / 2) for u, w in zip(us, gs))
    ll = s.factor(-2 * g / (pp - 1) - g + mu / 2)
    q = (g**2 - e**2) * (g**2 - f**2) / (4 * g**2)
    b = mu / 2 - f * e / g
    assert s.factor(ll - z - q / (z - b)) == 0
    for k in range(1, 13):
        odd_n, even_n = 2 * k - 1, 2 * k
        def residue(n):
            return s.expand(sum(s.binomial(n, t) * s.binomial(n - t, n + 1 - 2 * t)
                                * q**t * b**(n + 1 - 2 * t)
                                for t in range(1, (n + 1) // 2 + 1)))
        odd, even = residue(odd_n), residue(even_n)
        ck = (-s.Rational(1, 4))**k * s.binomial(2 * k - 1, k)
        dk = -k * s.binomial(2 * k, k) * (-s.Rational(1, 4))**k / g
        assert s.expand(odd.subs(e, 0)).coeff(f, 2 * k) == ck
        assert s.expand(s.diff(odd, e).subs(e, 0)).coeff(f, 2 * k) == 0
        assert s.expand(even.subs(e, 0)).coeff(f, 2 * k + 1) == 0
        assert s.factor(s.expand(s.diff(even, e).subs(e, 0)).coeff(f, 2 * k + 1) - dk) == 0

    # Columns: e*cos(x), f*cos(x), e*cos(3x), f*cos(3x), e*cos(5x), f*cos(5x).
    ff = fd.fsum([mode(1, s.Rational(2, 5), 1), mode(3, 0, 3), mode(5, 0, 5)])
    ee = fd.fsum([mode(1, 0, 0), mode(3, 0, 2), mode(5, 0, 4)])
    const_g, const_mu = s.Integer(3), s.Integer(2)
    mm = fd.fa(fd.fc(const_mu), fd.fs(fd.fm(ff, ee), -1 / const_g))
    uu = [fd.fa(mm, ff), fd.fa(mm, fd.fs(ff, -1))]
    gg = [fd.fa(fd.fc(const_g), ee), fd.fa(fd.fc(const_g), fd.fs(ee, -1))]
    order = 5
    pdo = {0: fd.fc(1)}
    for u, w in zip(uu, gg):
        bb = fd.fs(fd.fa(u, fd.fs(w, -1)), s.Rational(1, 2))
        factor = {0: fd.fc(1), -1: fd.fs(w, -1)}
        for n in range(1, order + 2):
            factor[-n - 1] = fd.fa(fd.fm(bb, factor[-n]), fd.fs(fd.fd(factor[-n]), -1))
        pdo = fd.pmul(factor, pdo, lo=-order - 2)
    aa, bb = s.Integer(-6), s.Integer(12)
    assert pdo[-1] == fd.fc(aa)
    assert pdo[-2] == fd.fc(bb)
    ell = {}
    for n in range(1, order + 1):
        value = fd.fa(fd.fs(pdo[-n - 1], bb / aa**2), fd.fs(pdo[-n - 2], -1 / aa))
        for k in range(1, n):
            for j in range(1, n + 2 - k):
                r = n + 1 - j - k
                value = fd.fa(value, fd.fs(fd.fm(pdo[-j], fd.fd(ell[k], r)),
                                          -s.binomial(-j, r) / aa))
        ell[n] = value
    lop = {1: fd.fc(1), **{-k: value for k, value in ell.items()}}
    lp = {0: fd.fc(1)}
    charges = [fd.fs(fd.fm(ff, ee), 8)]
    for n in range(1, order + 1):
        lp = fd.pmul(lp, lop, lo=-order)
        charges.append(lp[-1])
    jac = s.Matrix([list(value.get(0, fd.ZERO)[1:]) for value in charges])
    assert all(jac[i, j] == 0 for i in range(6) for j in range(i + 1, 6))
    amplitude = s.Rational(2, 5)
    expected = [4 * amplitude, -amplitude / 4]
    for k in range(1, 3):
        ck_next = (-s.Rational(1, 4))**(k + 1) * s.binomial(2 * k + 1, k + 1)
        dk = -k * s.binomial(2 * k, k) * (-s.Rational(1, 4))**k / const_g
        expected += [dk * amplitude**(2 * k + 1) / 2**(2 * k + 1),
                     (2 * k + 2) * ck_next * amplitude**(2 * k + 1) / 2**(2 * k + 1)]
    assert [jac[k, k] for k in range(6)] == expected
    assert jac.det() != 0
    result = {
        "passed": True,
        "commutative_normalization": str(ll),
        "symbolic_top_coefficient_checks": "odd/even pairs k=1,...,12",
        "exact_PDO_check": "Pmom,H1,...,H5 on N=2,G=6,T=12,A=2/5",
        "pairing": "x mean, i.e. integral divided by 2*pi",
        "Jacobian_columns": ["e cos x", "f cos x", "e cos 3x", "f cos 3x", "e cos 5x", "f cos 5x"],
        "Jacobian": str(jac),
        "diagonal": list(map(str, expected)),
        "determinant": str(jac.det()),
        "scope": "All-order independence is established by the filtration and Fourier proof in INDEPENDENCE.md; this is only a finite exact consistency check.",
    }
    (HERE / "independence_filtration_checks.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
