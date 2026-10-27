"""High-order lower bounds for independent DLW perturbations.

No grid evolution. Derivation is in series_highest_harmonic.md.
Arb encloses the logarithms of analytic lower bounds; mpmath independently
evaluates a finite exact divided-difference formula for the u-input chain.
"""
from pathlib import Path
import json
import mpmath as mp
from flint import arb, ctx
import sympy as sp

HERE = Path(__file__).resolve().parent
ctx.prec = 600
mp.mp.dps = 180
ORDERS = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 768, 1024, 1536, 2048, 3072, 4096]

def constants(kind, backend):
    """Amplitude coefficient at z=L/4, or leading-z jet coefficient."""
    if backend == "arb":
        R = arb
        pi = R.pi()
    else:
        R = mp.mpf
        pi = mp.pi
    k = pi / 2
    lam = k * k
    T = R(1) / 100
    eps = R(1) / 1000000
    L = R(4)
    alpha = pi / L
    phi = R(1) / 2
    Jphi = L / 8 - L / (4 * pi)
    if kind == "amplitude_u":
        a0, c, power = pi / (2 * L), phi / 2, 1
    elif kind == "amplitude_v":
        a0, c, power = phi / 2, lam * Jphi / 4, 2
    elif kind == "jet_u":
        a0, c, power = alpha ** 2, alpha ** 2 / 2, 1
    elif kind == "jet_v":
        a0, c, power = alpha ** 2 / 2, alpha ** 2 * lam / 12, 2
    else:
        raise ValueError(kind)
    return k, lam, T, eps, a0, c, power

def log_lower(n, kind, backend="arb"):
    k, lam, T, eps, a0, c, power = constants(kind, backend)
    ln = (lambda x: x.log()) if backend == "arb" else mp.log
    if n == 1:
        return (ln(eps) + ln(a0) + lam*T) / ln(type(eps)(10))
    s0 = power*(n-1)/(n*n*lam)
    s = s0 if s0 < T else T
    result = n*ln(eps)+(n-1)*ln(k)+ln(a0*n)
    result += (n-1)*(ln(c)+power*ln(s))+n*n*lam*(T-s)
    return result / ln(type(eps)(10))

def exact_u_chain(n):
    """Exact scalar positive chain, a_n'=n²lam*a_n+n*c*a_(n-1)."""
    k, lam, T, eps, a0, c, _ = constants("amplitude_u", "mp")
    # Product_{l != j}(j²-l²) = (-1)^(n-j) (n-j)!(n+j)!/(2j²).
    terms = [(-1)**(n-j)*2*j*j*mp.exp(lam*j*j*T)/
             (mp.factorial(n-j)*mp.factorial(n+j)) for j in range(1, n+1)]
    value = a0*mp.factorial(n)*(c/lam)**(n-1)*mp.fsum(terms)
    value *= eps**n*k**(n-1)
    assert value > 0
    lower = log_lower(n, "amplitude_u", "mp")
    lv = mp.log10(value)
    assert lv >= lower-mp.mpf("1e-140")
    return mp.nstr(lv, 55)

def symbolic_low_order_checks():
    t, lam, alpha = sp.symbols("t lam alpha", positive=True)
    E = sp.exp(lam*t)
    uc1, ud1 = alpha**2*E, -alpha**2/E
    uc2 = alpha**4*(3*E**4-2*E**2-1)/(8*lam)
    ud2 = alpha**4*(3/E**4-2/E**2-1)/(8*lam)
    vc1, vd1 = alpha**2*E/2, alpha**2/(2*E)
    vc2 = alpha**4*(E**2-1)**2/(48*lam)
    vd2 = alpha**4*(1-1/E**2)**2/(48*lam)
    residuals = []
    for c1,d1,c2,d2,denominator in [(uc1,ud1,uc2,ud2,4),(vc1,vd1,vc2,vd2,6)]:
        U1=(c1-d1)/denominator
        residuals.extend([sp.simplify(sp.diff(c2,t)-4*lam*c2-2*U1*c1),
                          sp.simplify(sp.diff(d2,t)+4*lam*d2-2*U1*d1)])
    assert residuals == [0,0,0,0]
    return [str(r) for r in residuals]

def main():
    rows=[]
    crossings={}
    for kind in ("amplitude_u", "amplitude_v", "jet_u", "jet_v"):
        for n in ORDERS:
            enclosure=log_lower(n,kind)
            rows.append({"kind":kind,"order":n,"log10_lower_bound_arb":str(enclosure),
                         "log10_lower_bound_decimal":mp.nstr(log_lower(n,kind,"mp"),45)})
        candidate=next(n for n in range(2,5000) if log_lower(n,kind,"mp")>0)
        assert log_lower(candidate,kind)>0 and log_lower(candidate-1,kind)<0
        crossings[kind]={"first_computed_order_with_lower_bound_exceeding_one":candidate,
                         "previous_log10_enclosure":str(log_lower(candidate-1,kind)),
                         "crossing_log10_enclosure":str(log_lower(candidate,kind))}
    chains=[{"order":n,"log10_exact_u_chain_180_decimal_digits":exact_u_chain(n)}
            for n in [1,2,4,8,16,32,64,128,256,512,1024,2048]]
    result={
        "scope":"Analytic lower bounds for highest-harmonic formal amplitude coefficients and leading-z jet coefficients; not a PDE reference solution",
        "parameters":{"L":"4","z":"L/4 for amplitude coefficients","kappa":"pi/2","epsilon":"1e-6","T":"0.01"},
        "precision":{"arb_bits":600,"mpmath_decimal_digits":180},
        "normalization":"epsilon^n*kappa^(n-1) included; jet outputs are Taylor coefficients (jet/j!), not derivative values",
        "proven_implication":"Zero radius of the independent-perturbation amplitude series around the constant background, for any t>0",
        "jet_implication_condition":"Actual sine-background highest-frequency isolation must be supplied separately before applying the jet result to that initial datum",
        "does_not_establish":"Nonexistence for a fixed nonzero perturbation in an arbitrary smooth solution class",
        "continuous_reference_error_bound":None,
        "symbolic_second_order_residuals":symbolic_low_order_checks(),
        "bounds":rows,"crossings":crossings,"exact_scalar_chain":chains,
    }
    (HERE/"series_highest_harmonic.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps({"crossings":crossings,"symbolic_residuals":result["symbolic_second_order_residuals"],
                      "output":str(HERE/"series_highest_harmonic.json")},indent=2))

if __name__=="__main__":
    main()
