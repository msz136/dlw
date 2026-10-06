"""Exact checks for the equation-to-error derivations in the DLW theory HTML.

No PDE trajectories or measured errors are used.  The checks certify algebra and
kernel moments; regularity, initial/boundary compatibility and stability remain
hypotheses of an error theorem.
"""
from pathlib import Path
import hashlib
import json
import sympy as sp

HERE = Path(__file__).resolve().parent
x, y, time, s = sp.symbols("x y time s", real=True)
h = sp.symbols("h", positive=True)
a, alpha, beta = sp.symbols("a alpha beta", real=True)
checks = []


def zero(name, expr):
    reduced = sp.simplify(sp.expand(expr))
    if reduced != 0:
        raise AssertionError(f"{name}: {reduced}")
    checks.append({"name": name, "exact_residual": "0"})


rho = sp.Function("rho")(x, y, time)
theta = sp.Function("theta")(x, y, time)
f, g = sp.exp((theta + rho) / 2), sp.exp((theta - rho) / 2)


def hirota(nx=0, ny=0, nt=0):
    result = 0
    for ix in range(nx + 1):
        for iy in range(ny + 1):
            for it in range(nt + 1):
                weight = (-1) ** (ix + iy + it)
                weight *= sp.binomial(nx, ix) * sp.binomial(ny, iy) * sp.binomial(nt, it)
                left = sp.diff(f, x, nx - ix, y, ny - iy, time, nt - it)
                right = sp.diff(g, x, ix, y, iy, time, it)
                result += weight * left * right
    return sp.simplify(result / (f * g))


rx = sp.diff(rho, x)
E = sp.diff(theta, x, 2) + rx ** 2 + sp.diff(rho, time) + 2 * a * rx
zero("Hirota Dx divided by fg", hirota(nx=1) - rx)
zero("Hirota Dx2 divided by fg", hirota(nx=2) - sp.diff(theta, x, 2) - rx ** 2)
zero("Hirota DyDx divided by fg", hirota(nx=1, ny=1)
     - sp.diff(theta, x, y) - sp.diff(rho, y) * rx)
zero("Hirota DyDt divided by fg", hirota(ny=1, nt=1)
     - sp.diff(theta, y, time) - sp.diff(rho, y) * sp.diff(rho, time))
zero("Hirota DyDx2 divided by fg", hirota(nx=2, ny=1)
     - sp.diff(rho, x, 2, y) - 2 * rx * sp.diff(theta, x, y)
     - sp.diff(rho, y) * (sp.diff(theta, x, 2) + rx ** 2))

H = (sp.diff(rho, x, 2, y) + sp.diff(theta, y, time)
     + 2 * (rx + a) * sp.diff(theta, x, y) - 4 * rx)
second_bilinear = (hirota(nx=2, ny=1) + hirota(ny=1, nt=1)
                  + 2 * a * hirota(nx=1, ny=1) - 4 * hirota(nx=1))
zero("continuous second bilinear equation equals H plus rho_y E",
     second_bilinear - H - sp.diff(rho, y) * E)
u, v = 2 * rx, 2 * sp.diff(theta, x, y)
dlw1 = sp.diff(u, y, time) + sp.diff(v, x, 2) + sp.diff((u + 2 * a) * sp.diff(u, y), x)
dlw2 = sp.diff(v, time) + sp.diff(u, x, 2, y) + sp.diff((u + 2 * a) * v - 4 * u, x)
zero("twice mixed derivative of first bilinear equation is DLW1", 2 * sp.diff(E, x, y) - dlw1)
zero("twice x derivative of reduced second bilinear equation is DLW2", 2 * sp.diff(H, x) - dlw2)

# Two staggered walls: their sum/difference precedes auxiliary-potential elimination.
lf = sp.Function("lf")(x, time)
lg0 = sp.Function("lg0")(x, time)
lg1 = sp.Function("lg1")(x, time)


def wall(left, right, parameter):
    return (sp.diff(left + right, x, 2) + sp.diff(left - right, x) ** 2
            + sp.diff(left - right, time) + 2 * parameter * sp.diff(left - right, x))


Em = wall(lf, lg0, a - h / 2)
Ep = wall(lf, lg1, a + h / 2)
uj = sp.diff(2 * lf - lg0 - lg1, x)
omega = sp.diff(lg1 - lg0, x)
Z = sp.diff(2 * lf + lg0 + lg1, x)
zero("staggered wall sum gives u and Z equation", sp.diff(Em + Ep, x)
     - sp.diff(uj, time) - sp.diff((uj ** 2 + omega ** 2) / 2 + 2 * a * uj - h * omega, x)
     - sp.diff(Z, x, 2))
zero("staggered wall difference gives omega equation", sp.diff(Em - Ep, x)
     - sp.diff(omega, time) - sp.diff((uj + 2 * a) * omega - h * uj, x)
     + sp.diff(omega, x, 2))

lfm, bminus, bzero, bplus = sp.symbols("lfm bminus bzero bplus")
lfzero = sp.symbols("lfzero")
Zzero, Zminus = 2 * lfzero + bzero + bplus, 2 * lfm + bminus + bzero
uzero, uminus = 2 * lfzero - bzero - bplus, 2 * lfm - bminus - bzero
omegazero, omegaminus = bplus - bzero, bzero - bminus
zero("auxiliary-potential difference identity",
     (Zzero - Zminus) / h - (uzero - uminus) / h
     - (4 / h) * (omegazero + omegaminus) / 2)

grid = {j: sp.symbols(f"u{j:+d}") for j in range(-2, 3)}


def delta0(j):
    return (grid[j + 1] - grid[j - 1]) / (2 * h)


def deltaminus(j):
    return (grid[j] - grid[j - 1]) / h


def laplacian(j):
    return (grid[j + 1] - 2 * grid[j] + grid[j - 1]) / h ** 2


lap_dminus = (deltaminus(1) - 2 * deltaminus(0) + deltaminus(-1)) / h ** 2
zero("Mminus delta0 equals deltaminus plus h2 Delta deltaminus over four",
     (delta0(0) + delta0(-1)) / 2 - deltaminus(0) - h ** 2 * lap_dminus / 4)
lap2 = (laplacian(1) - 2 * laplacian(0) + laplacian(-1)) / h ** 2
zero("delta0 squared equals Delta plus h2 Delta squared over four",
     (delta0(1) - delta0(-1)) / (2 * h) - laplacian(0) - h ** 2 * lap2 / 4)


def A(q):
    return q ** 2 / 2 + 2 * a * q


zero("quadratic flux discrete product identity",
     (A(grid[1]) - A(grid[-1])) / (2 * h) - (grid[0] + 2 * a) * delta0(0)
     - h ** 2 * laplacian(0) * delta0(0) / 2)

# FD first residual equals trapezoid average minus interval average of v_xx.
# Two integrations by parts identify its nonnegative Peano kernel.
kernel = ((h / 2) ** 2 - s ** 2) / (2 * h)
zero("first-residual Peano kernel left endpoint", kernel.subs(s, -h / 2))
zero("first-residual Peano kernel right endpoint", kernel.subs(s, h / 2))
zero("first-residual Peano kernel second derivative", sp.diff(kernel, s, 2) + 1 / h)
zero("first-residual Peano kernel endpoint slope left", sp.diff(kernel, s).subs(s, -h / 2) - sp.Rational(1, 2))
zero("first-residual Peano kernel endpoint slope right", sp.diff(kernel, s).subs(s, h / 2) + sp.Rational(1, 2))
zero("first-residual leading kernel mass h2 over twelve", sp.integrate(kernel, (s, -h / 2, h / 2)) - h ** 2 / 12)
zero("first-residual odd kernel moment zero", sp.integrate(s * kernel, (s, -h / 2, h / 2)))
zero("first-residual fourth-order remainder constant h4 over 480",
     sp.integrate(s ** 2 * kernel / 2, (s, -h / 2, h / 2)) - h ** 4 / 480)
cs = sp.symbols("c0:7")
poly = sum(cs[n] * s ** n for n in range(len(cs)))
trap_minus_integral = (poly.subs(s, -h / 2) + poly.subs(s, h / 2)) / 2 - sp.integrate(poly, (s, -h / 2, h / 2)) / h
zero("Peano kernel representation verified for generic degree-six polynomial",
     trap_minus_integral - sp.integrate(kernel * sp.diff(poly, s, 2), (s, -h / 2, h / 2)))

# FD second residual is a symmetric integral average of u_xxy minus its value.
zero("second-residual symmetric averaging second moment h2 over six",
     sp.integrate(s ** 2 / 2, (s, -h, h)) / (2 * h) - h ** 2 / 6)
zero("second-residual symmetric averaging odd third moment zero",
     sp.integrate(s ** 3 / 6, (s, -h, h)) / (2 * h))
zero("second-residual fourth-order remainder constant h4 over 120",
     sp.integrate(s ** 4 / 24, (s, -h, h)) / (2 * h) - h ** 4 / 120)

# Tuning wall mean and half-separation while retaining the same physical mesh h.
W, delta_u, delta_W, dminus_u, dminus_W = sp.symbols("W delta_u delta_W dminus_u dminus_W")
uu = sp.symbols("uu")
omegaphys = h * W / 4
tunedH = (uu ** 2 + omegaphys ** 2) / 2 + 2 * (a + alpha * h ** 2) * uu - (h + beta * h ** 3) * omegaphys
baseH = A(uu) + h ** 2 * (W ** 2 / 32 - W / 4)
zero("two-parameter exact physical SD flux",
     tunedH - baseH - 2 * alpha * h ** 2 * uu + beta * h ** 4 * W / 4)
tunedWflux = 4 / h * ((uu + 2 * a + 2 * alpha * h ** 2) * omegaphys - (h + beta * h ** 3) * uu)
baseWflux = (uu + 2 * a) * W - 4 * uu
zero("two-parameter exact W flux",
     tunedWflux - baseWflux - h ** 2 * (2 * alpha * W - 4 * beta * uu))
vphysical = W + delta_u
delta_tunedH_minus_baseH = 2 * alpha * h ** 2 * delta_u - beta * h ** 4 * delta_W / 4
zero("two-parameter exact reconstructed second physical flux change",
     delta_tunedH_minus_baseH + tunedWflux - baseWflux
     - h ** 2 * (2 * alpha * vphysical - 4 * beta * uu) + beta * h ** 4 * delta_W / 4)
zero("two-parameter first leading coefficient", sp.limit(
     (2 * alpha * h ** 2 * dminus_u - beta * h ** 4 * dminus_W / 4) / h ** 2,
     h, 0) - 2 * alpha * dminus_u)

output = {
    "status": "passed",
    "method": "exact SymPy algebra, Hirota binomial identities, stencil identities and kernel moments",
    "checks": checks,
    "number_of_checks": len(checks),
    "uses_observed_error_data": False,
    "PDE_simulations": 0,
    "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "remainder_bounds": {
        "FD1": "h^4/480 times sup |v_xxyyyy| on the staggered cell",
        "FD2": "h^4/120 times sup |u_xxyyyyy| on the centered two-step cell",
        "assumptions": "h>0; enough continuous derivatives on each indicated cell; continuous DLW solution substituted",
    },
    "limitations": [
        "Logarithmic nonlinearization is local where the tau functions are nonzero and a log branch exists.",
        "Bilinear equations imply DLW; the reverse implication can require fixing integration constants and gauges.",
        "The Peano representation is universal by two integrations by parts; its polynomial check supplements the proof.",
        "The two-parameter coefficient formula keeps the same mesh h and the physical omega-to-v normalization 4/h.",
        "No stability, well-posedness or finite-time solution-error theorem is certified by these algebra checks.",
    ],
}
(HERE / "derivation_validation.json").write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({"status": output["status"], "checks": len(checks), "PDE_simulations": 0}, ensure_ascii=False))
