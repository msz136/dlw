"""Linearized spectrum of the three spatial formulations about the rest state.

The rest state u=v=0 is an exact solution of all three formulations with zero
reference data.  The x direction is periodic and Fourier-differentiated, so the
linearization is block diagonal in the x wavenumber.  For each wavenumber we
build the (2*ny) x (2*ny) complex matrix by applying the production right-hand
side to cos/sin perturbations, then form M = d(cos) + i d(sin) and project.
"""
import json
import sys
from pathlib import Path

import numpy as np

SPATIAL = Path(r"C:\Users\msz\aca\Workspaces\dlw_paper_20261009\spatial_audit_20261023")
sys.path.insert(0, str(SPATIAL))
from run import Model, step  # noqa: E402

HERE = Path(__file__).resolve().parent


def rest_model(method, dx=0.1, h=0.1, case="A"):
    m = Model(case, method, dx, h)
    m.profile = lambda y, t=0.0, x=None: np.zeros((2, np.size(y), m.nx))
    m.ut = lambda y, t: np.zeros((np.size(y), m.nx))
    m.cache = {}
    return m


def modal_matrix(m, xi, eps=1e-4):
    ny, nx, n = len(m.y), m.nx, 2 * len(m.y)
    z0 = np.zeros((2, ny, nx))
    c, s = np.cos(xi * m.x), np.sin(xi * m.x)
    e = np.exp(-1j * xi * m.x) / nx
    M = np.zeros((n, n), dtype=complex)
    for j in (0, 1):
        for k in range(ny):
            col = j * ny + k
            D = np.zeros((2, ny, nx), dtype=complex)
            for f, w in ((c, 1.0), (s, 1j)):
                zp = z0.copy()
                zp[j, k] += eps * f
                zm = z0.copy()
                zm[j, k] -= eps * f
                D += w * (m.rhs(0.0, zp) - m.rhs(0.0, zm)) / (2 * eps)
            for jj in (0, 1):
                for kk in range(ny):
                    M[jj * ny + kk, col] = np.sum(D[jj, kk] * e)
    return M


def modal_growth(m, xi, eigvec, T=0.01, dt=1e-4, eps=1e-6):
    ny, nx = len(m.y), m.nx
    W = eigvec.reshape(2, ny)
    z = np.real(W[:, :, None] * np.exp(1j * xi * m.x)[None, None, :]) * eps
    n0 = np.max(np.abs(z))
    z = z.copy()
    for i in range(round(T / dt)):
        z = step(m, i * dt, z, dt)
    rate = np.log(np.max(np.abs(z)) / n0) / T
    return float(rate)


def main():
    methods = ("Endpoint-SD", "Centered-SD", "FD")
    out = {}
    for method in methods:
        m = rest_model(method)
        zero = m.rhs(0.0, np.zeros((2, len(m.y), m.nx)))
        rec = {"nx": m.nx, "ny": len(m.y), "dx": m.dx, "h": m.h,
               "rest_state_rhs_max": float(np.max(np.abs(zero))), "modes": []}
        for j in range(1, 51):
            xi = 2 * np.pi * j / (2 * m.half)
            if xi > np.pi / m.dx:
                break
            M = modal_matrix(m, xi)
            lam, vec = np.linalg.eig(M)
            i = int(np.argmax(lam.real))
            g = modal_growth(m, xi, vec[:, i])
            rec["modes"].append(dict(xi=float(xi), j=j, re_sigma=float(lam[i].real),
                                     im_sigma=float(lam[i].imag),
                                     predicted_xi2=float(xi ** 2),
                                     predicted_lattice=float(xi * np.sqrt(max(xi ** 2 - m.h ** 2, 0.0))),
                                     measured_rate=g))
        out[method] = rec
        print(method, "done", flush=True)
    (HERE / "linear_spectrum.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    for method, rec in out.items():
        print(method, "rest-rhs", rec["rest_state_rhs_max"])
        for row in rec["modes"]:
            print("  xi=%7.3f  Re sig=%9.4f  xi^2=%9.4f  meas=%9.4f" %
                  (row["xi"], row["re_sigma"], row["predicted_xi2"], row["measured_rate"]))


if __name__ == "__main__":
    main()
