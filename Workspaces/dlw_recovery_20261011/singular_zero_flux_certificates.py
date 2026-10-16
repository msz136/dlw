"""Exact local certificates for c=Gamma=0; no flow/completeness claim.

The accompanying review contains all-M arguments. These finite symbolic checks
test signs, projection, the consistency current, and the third PDO coefficient.
"""
from pathlib import Path
import hashlib
import json
import sympy as sp

h = sp.symbols("h", positive=True)
beta = h**2 / 32
records = []

for M in range(2, 7):
    Pi_mat = sp.ones(M) / M
    P0 = sp.eye(M) - Pi_mat
    Eminus = sp.zeros(M)
    for j in range(M):
        Eminus[j, (j - 1) % M] = 1
    delta = (sp.eye(M) - Eminus) / h
    average = (sp.eye(M) + Eminus) / 2
    R = (delta + Pi_mat).inv() * average * P0
    assert R + R.T == sp.zeros(M)
    jets = {}

    def field(prefix):
        rows = []
        for order in range(4):
            vals = [sp.Symbol(f"{prefix}{j}_{order}") for j in range(M - 1)]
            rows.append(sp.Matrix(vals + [-sum(vals)]))
        for order in range(3):
            jets.update({rows[order][j]: rows[order + 1][j] for j in range(M - 1)})
        return rows

    p, px, pxx, pxxx = field("p")
    s, sx, sxx, sxxx = field("s")
    b, bx, bxx = sp.symbols("b bx bxx")
    f, fx, fxx = sp.symbols("f fx fxx")
    jets.update({b: bx, bx: bxx, f: fx, fx: fxx})

    def D(expr):
        return sp.expand(sum(sp.diff(expr, v) * dv for v, dv in jets.items()))

    def mean(exprs):
        return sum(exprs) / M

    def check(expr):
        assert sp.expand(expr) == 0

    q = mean([p[j] * s[j] for j in range(M)])
    chi = mean([
        -p[j]**2 * s[j] - 2 * beta * s[j]**3 / 3
        + p[j] * sx[j] - s[j] * px[j] - s[j] * (R * sx)[j]
        for j in range(M)
    ])
    e = mean([
        p[j]**2 * s[j] / 2 + beta * s[j]**3 / 3
        + s[j] * px[j] + s[j] * (R * sx)[j] / 2
        for j in range(M)
    ])
    check(chi + 2 * e - D(q))

    gp = P0 * sp.Matrix([p[j] * s[j] - sx[j] for j in range(M)])
    gs = P0 * sp.Matrix([
        p[j]**2 / 2 + beta * s[j]**2 + px[j] + (R * sx)[j]
        for j in range(M)
    ])
    A = -sp.Matrix([D(z) for z in gs])
    S = -sp.Matrix([D(z) for z in gp])
    check(mean([s[j] * A[j] + p[j] * S[j] for j in range(M)]) - D(chi))
    evolution = {}
    gauge = {}
    for j in range(M - 1):
        evolution[p[j]] = A[j]
        evolution[s[j]] = S[j]
        evolution[px[j]] = D(A[j])
        evolution[sx[j]] = D(S[j])
        gauge[p[j]] = -D(f * p[j])
        gauge[s[j]] = -D(f * s[j])
        gauge[px[j]] = D(gauge[p[j]])
        gauge[sx[j]] = D(gauge[s[j]])

    rho = sp.expand(sum(sp.diff(chi, z) * dz for z, dz in evolution.items()))
    gauge_chi = sp.expand(sum(sp.diff(chi, z) * dz for z, dz in gauge.items()))
    check(gauge_chi + f * D(chi) + 3 * fx * chi)
    eta = 2 * mean([gp[j] * gs[j] - s[j] * A[j] for j in range(M)])
    eta -= mean([s[j] * (R * S)[j] for j in range(M)])
    eta += D(chi)
    check(rho - D(eta))

    # Ordered composition of T_j=1+A_j D^-1+B_j D^-2+C_j D^-3.
    d = h * s / 8
    v = (sp.ones(M, 1) * b + p) / 2 - d
    AA = [-2 * d[j] for j in range(M)]
    BB = [-2 * v[j] * d[j] + 2 * D(d[j]) for j in range(M)]
    CC = [
        -2 * d[j] * (v[j]**2 - D(v[j]))
        + 4 * v[j] * D(d[j]) - 2 * D(D(d[j]))
        for j in range(M)
    ]
    a2 = sum(BB) + sum(AA[i] * AA[j] for i in range(M) for j in range(i))
    a3 = sum(CC)
    a3 += sum(
        AA[i] * BB[j] + BB[i] * AA[j] - AA[i] * D(AA[j])
        for i in range(M) for j in range(i)
    )
    a3 += sum(
        AA[i] * AA[j] * AA[k]
        for i in range(M) for j in range(i) for k in range(j)
    )
    check(a2 + h * M * q / 8)
    check(a3 - h * M * chi / 16 - 3 * h * M * D(q) / 16 + h * M * b * q / 8)
    records.append({
        "M": M,
        "chi_energy_pointwise": True,
        "q_hamiltonian_flux": True,
        "chi_primary_weight_three": True,
        "rho_is_D_eta": True,
        "a2_pointwise": True,
        "a3_pointwise": True,
    })

# M=3: a nonconstant exact point of the primary-secondary constraint layer.
r, ax, rx, a = sp.symbols("r ax rx a", real=True)
kappa = sp.symbols("kappa", nonzero=True)
p3 = sp.Matrix([a, -a, 0])
s3 = sp.Matrix([r, r, -2*r])
px3 = sp.Matrix([ax, -ax, 0])
sx3 = sp.Matrix([rx, rx, -2*rx])
R3 = h * sp.Matrix([[0, -1, 1], [1, 0, -1], [-1, 1, 0]]) / 6
q3 = (p3.dot(s3)) / 3
chi3 = sum([
    -p3[j]**2*s3[j] - 2*beta*s3[j]**3/3
    + p3[j]*sx3[j] - s3[j]*px3[j] - s3[j]*(R3*sx3)[j]
    for j in range(3)
]) / 3
assert sp.expand(q3) == 0
assert sp.expand(chi3 - 2*r*(-a**2+2*beta*r**2)/3) == 0
assert sp.simplify(chi3.subs(a**2, 2*beta*r**2-3*kappa/(2*r)) - kappa) == 0
rxx, b3, bx3 = sp.symbols("rxx b3 bx3")
S3 = -(ax*r+a*rx)*sp.Matrix([1,-1,0])
S3 += (rxx-bx3*r-b3*rx)*sp.Matrix([1,1,-2])
assert sp.expand(S3[0]-S3[1]+2*(ax*r+a*rx)) == 0

# Two distinct analytic original solutions with exactly the same full initial U,w.
x, t, eps, mass = sp.symbols("x t eps mass", real=True)
p2 = mass + eps*t**2*sp.cos(x)
b2 = eps*(t**2-2*t)*sp.sin(x)/p2
assert sp.simplify(sp.diff(p2,t) + sp.diff(b2*p2,x) + sp.diff(p2,x,2)) == 0
assert sp.simplify(p2.subs(t,0)-mass) == 0
assert sp.simplify(b2.subs(t,0)) == 0

out = {
    "status": "all exact checks passed",
    "sympy": sp.__version__,
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "checks": records,
    "M3_nonconstant_constraint_family": True,
    "M3_Hamiltonian_direction_has_component_outside_translation": True,
    "M2_same_full_initial_state_distinct_analytic_solutions": True,
    "scope": "Finite local symbolic certificates plus explicit exact solutions. No Sobolev flow, global Dirac quotient, or Liouville completeness claim.",
}
Path(__file__).with_suffix(".json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
print(out["status"], len(records), "lattice periods")
