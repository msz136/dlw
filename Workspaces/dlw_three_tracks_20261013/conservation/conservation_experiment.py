"""Periodic DLW: genuine inverse-monodromy I1,I2,I3 and numerical drift.

This is a numerical experiment on the periodic reduced Hamilton leaf, not
the nonperiodic line-soliton examples in the paper. No fitted/synthetic data.
Run: python conservation_experiment.py
Dependencies: numpy, matplotlib (already available); no package installation.
"""
from pathlib import Path
import csv
import json
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter

HERE = Path(__file__).resolve().parent
M, H, C, GAMMA = 3, 4.0, 2.0, 4.0
LX, FINAL = 2 * np.pi, 0.02
BETA = H * H / 32
P0 = np.eye(M) - np.ones((M, M)) / M
EMINUS = np.roll(np.eye(M), 1, axis=0)
DMINUS = (np.eye(M) - EMINUS) / H
MMINUS = (np.eye(M) + EMINUS) / 2
R = np.linalg.pinv(DMINUS) @ MMINUS @ P0


def binomial_integer(n, r):
    out = 1
    for k in range(r):
        out = out * (n - k) // (k + 1)
    return out


class Grid:
    def __init__(self, n, kind):
        self.n, self.kind = n, kind
        self.dx = LX / n
        self.x = np.arange(n) * self.dx
        k = 2 * np.pi * np.fft.fftfreq(n, d=self.dx)
        if n % 2 == 0:
            k[n // 2] = 0  # real skew first derivative, including its kernel
        if kind == "spectral":
            self.D = np.fft.ifft((1j * k)[:, None] * np.fft.fft(np.eye(n), axis=0), axis=0).real
        elif kind == "centered":
            self.D = (np.roll(np.eye(n), 1, axis=1) - np.roll(np.eye(n), -1, axis=1)) / (2 * self.dx)
        else:
            raise ValueError(kind)
        self.Dpowers = {0: np.eye(n), 1: self.D}
        for order in range(2, 5):
            self.Dpowers[order] = self.Dpowers[order - 1] @ self.D

    def derivative(self, f, order=1):
        return f @ self.Dpowers[order].T


def initial(grid):
    co = np.cos(grid.x)
    p = np.array([-3.0, 0.0, 3.0])[:, None] + np.array([1/5, -2/5, 1/5])[:, None] * co
    g = np.array([1.0, 2.0, 3.0])[:, None] + np.array([1/6, 1/7, -1/6-1/7])[:, None] * co
    return np.stack((p, 4*g/H - C))


def fields(z):
    p, s = z
    b = (GAMMA - np.mean(p*s, axis=0)) / C
    return p + b, C + s


def gradients(z, grid):
    U, w = fields(z)
    f = U*w - grid.derivative(w) - GAMMA
    k = U*U/2 + BETA*w*w + grid.derivative(U) + R @ grid.derivative(w)
    return P0 @ f, P0 @ k


def rhs(z, grid):
    f, k = gradients(z, grid)
    return -np.stack((grid.derivative(k), grid.derivative(f)))


def hamilton(z, grid):
    U, w = fields(z)
    density = U*U*w/2 + BETA*w**3/3 + w*grid.derivative(U) + w*(R @ grid.derivative(w))/2 - GAMMA*U
    return H*grid.dx*np.sum(density)


def pdo_mul(A, B, grid, lo=-5):
    """Formal PDO multiplication, with every x derivative evaluated by D_h.

    This diagnostic substitution does NOT imply a discrete PDO algebra:
    D_h is not a derivation of pointwise grid products.
    """
    out = {}
    for i, ai in A.items():
        for j, bj in B.items():
            for r in range(max(-1, i+j-lo)+1):
                coef = binomial_integer(i, r)
                if coef:
                    power = i+j-r
                    term = coef * ai * grid.derivative(bj, r)
                    out[power] = out.get(power, 0) + term
    return out


def spectral_charges(z, grid, return_coefficients=False):
    U, w = fields(z)
    g = H*w/4
    G = H*M*C/4
    T = H*M*GAMMA/4
    a, b = -G, (G*G-T)/2
    prod = {0: np.ones(grid.n)}
    for j in range(M):
        B = (U[j] - g[j])/2
        factor = {0: np.ones(grid.n), -1: -g[j]}
        for k in range(1, 5):
            factor[-k-1] = B*factor[-k] - grid.derivative(factor[-k])
        prod = pdo_mul(factor, prod, grid)
    p3, p4, p5 = prod[-3], prod[-4], prod[-5]
    rhos = np.array([
        b*b/(a*a) - p3/a,
        -2*p4/a + 4*b*p3/a**2 - 2*b**3/a**3,
        -3*p5/a + 6*b*p4/a**2 + 6*p3*p3/a**2 - 15*b*b*p3/a**3 + 6*b**4/a**4,
    ])
    vals = grid.dx*np.sum(rhos, axis=1)
    if return_coefficients:
        return vals, prod, rhos
    return vals


def observations(z, grid):
    U, w = fields(z)
    p, s = z
    I = spectral_charges(z, grid)
    return np.r_[I, hamilton(z, grid), H*grid.dx*np.sum(p*s),
                 np.max(np.abs(np.mean(w, axis=0)-C)),
                 np.max(np.abs(np.mean(U*w, axis=0)-GAMMA)),
                 np.max(np.abs(z)), np.max(np.abs(z-initial(grid))) ]


def solve(n, kind, steps, name, save_every=1):
    grid = Grid(n, kind)
    z = initial(grid)
    dt = FINAL / steps
    times, obs, states = [0.0], [observations(z, grid)], [z.copy()]
    for step in range(1, steps+1):
        k1 = rhs(z, grid)
        k2 = rhs(z + dt*k1/2, grid)
        k3 = rhs(z + dt*k2/2, grid)
        k4 = rhs(z + dt*k3, grid)
        z = z + dt*(k1+2*k2+2*k3+k4)/6
        if step % save_every == 0 or step == steps:
            times.append(step*dt)
            obs.append(observations(z, grid))
            states.append(z.copy())
    obs = np.asarray(obs)
    result = dict(name=name, kind=kind, nx=n, dt=dt, steps=steps,
                  times=np.asarray(times), values=obs, states=np.asarray(states), x=grid.x)
    np.savez_compressed(HERE / f"{name}.npz", **result)
    return result


def write_csv(path, rows):
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def verify():
    grid = Grid(48, "spectral")
    z = initial(grid)
    vals, prod, rho = spectral_charges(z, grid, True)
    exact_means = np.array([4 - (466031/3528)/48,
                            724400267/296352000,
                            98646175112939/11948912640000])
    U, w = fields(z)
    f, k = gradients(z, grid)
    rng = np.random.default_rng(1234)
    direction = np.stack([P0 @ rng.normal(size=(M, grid.n)) for _ in range(2)])
    grad_pairing = H*grid.dx*np.sum(np.stack((f, k))*direction)
    eps = 1e-5
    numerical = (hamilton(z+eps*direction, grid)-hamilton(z-eps*direction, grid))/(2*eps)
    # Cubic central-difference defect has O(eps^2), so check a safe absolute tolerance.
    continuum_witness = np.max(np.abs(vals/LX-exact_means))
    derivative = H*grid.dx*np.sum(np.stack((f, k))*rhs(z, grid))
    checks = {
        "R_skew_error": float(np.max(np.abs(R+R.T))),
        "D_skew_error": float(np.max(np.abs(grid.D+grid.D.T))),
        "monodromy_a_error": float(np.max(np.abs(prod[-1]+6))),
        "monodromy_b_error": float(np.max(np.abs(prod[-2]-12))),
        "exact_initial_I_over_Lx": exact_means.tolist(),
        "numerical_initial_I_over_Lx": (vals/LX).tolist(),
        "exact_Fourier_witness_max_error": float(continuum_witness),
        "hamilton_gradient_directional_absolute_error": float(abs(numerical-grad_pairing)),
        "hamilton_semidiscrete_time_derivative": float(derivative),
        "notes": "Exact witness values come from the existing rational Fourier certificate; numerical checks do not prove Jacobi or Liouville integrability."
    }
    assert checks["R_skew_error"] < 1e-12
    assert checks["D_skew_error"] < 1e-12
    assert checks["monodromy_b_error"] < 1e-11
    assert continuum_witness < 1e-9
    assert abs(numerical-grad_pairing) < 2e-7
    assert abs(derivative) < 1e-9
    checks["passed"] = True
    return checks


def plot_results(runs, time_rows):
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "axes.linewidth": .7, "savefig.bbox": "tight"})
    colors = {"centered_n24": "#643c33", "centered_n48": "#df5252",
              "centered_n96": "#c6a5c1", "spectral_n24": "#266f9f",
              "spectral_n48": "#2d927f"}
    for relative, basename in [(True,"invariant_drift"),(False,"invariant_drift_absolute")]:
        fig, axes = plt.subplots(1, 3, figsize=(10.7, 3.3))
        for j, ax in enumerate(axes):
            ax.axhline(0, color="0.8", lw=.65)
            for run in runs:
                name = run["name"]
                label = ("Centered" if run["kind"] == "centered" else "Fourier") + f", Nx={run['nx']}"
                vals = run["values"][:, j]
                denominator = abs(vals[0]) if relative else 1
                ax.plot(run["times"], (vals-vals[0])/denominator, color=colors[name],
                        lw=1.6, label=label, ls="--" if run["kind"] == "spectral" else "-")
            title=rf"({chr(97+j)}) $\Delta I_{j+1}"
            title+=rf"/|I_{j+1}(0)|$" if relative else "$"
            ax.set_title(title, loc="left", fontsize=11)
            ax.set_xlabel("Time $t$")
            ax.ticklabel_format(axis="y", style="sci", scilimits=(0,0), useMathText=True)
        axes[0].set_ylabel("Signed relative drift" if relative else "Signed drift")
        handles, labels = axes[0].get_legend_handles_labels()
        fig.legend(handles, labels, loc="lower center", ncol=5, bbox_to_anchor=(.5, -.035), frameon=False, fontsize=8)
        fig.suptitle("Periodic DLW trace invariants: spatial discretization controls drift", fontsize=12)
        fig.tight_layout(rect=(0,.07,1,.91))
        for suffix in ("png", "pdf"):
            fig.savefig(HERE / f"{basename}.{suffix}", dpi=300)
        plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(8, 3.4))
    for kind, marker, ls, color in [("centered", "o", "-", "#643c33"), ("spectral", "s", "--", "#266f9f")]:
        rows = [r for r in time_rows if r["kind"] == kind]
        axes[0].loglog([r["dt"] for r in rows], [r["field_time_error_linf"] for r in rows],
                       marker+ls, color=color, ms=4, lw=1.2, label=kind.title())
    refx=np.array([FINAL/8, FINAL])
    axes[0].loglog(refx, 5e-8*(refx/refx[-1])**4, ":", color=".35", lw=1, label=r"$O(\Delta t^4)$ guide")
    axes[0].set(xlabel=r"Time step $\Delta t$", ylabel=r"Field error $\|z_{dt}-z_{ref}\|_\infty$", title="(a) Time error at fixed Nx=24")
    axes[0].set_xticks([.0025,.005,.01,.02], labels=["0.0025","0.005","0.01","0.02"])
    axes[0].xaxis.set_minor_formatter(NullFormatter())
    axes[0].legend(fontsize=8, frameon=False)
    for j, color in enumerate(["#266f9f", "#df5252", "#643c33"]):
        rows = [r for r in runs if r["kind"] == "centered"]
        dx = np.array([LX/r["nx"] for r in rows])
        err = [abs(r["values"][-1,j]-r["values"][0,j]) for r in rows]
        axes[1].loglog(dx, err, "o-", color=color, ms=4, lw=1.2, label=rf"$I_{j+1}$")
    axes[1].loglog(dx, err[0]*(dx/dx[0])**2, ":", color=".35", lw=1, label=r"$O(\Delta x^2)$")
    axes[1].set(xlabel=r"Grid spacing $\Delta x$", ylabel=r"$|I_n(T)-I_n(0)|$", title="(b) Spatial drift at fixed dt=0.00025")
    axes[1].legend(frameon=False, fontsize=8)
    fig.tight_layout()
    for suffix in ("png", "pdf"):
        fig.savefig(HERE / f"error_separation.{suffix}", dpi=300)
    plt.close(fig)


def main():
    checks = verify()
    runs = [solve(n, "centered", 80, f"centered_n{n}") for n in [24,48,96]]
    runs += [solve(n, "spectral", 80, f"spectral_n{n}") for n in [24,48]]
    rows, summaries = [], []
    for run in runs:
        initial_vals = run["values"][0,:3]
        delta = run["values"][:,:3]-initial_vals
        grid=Grid(run["nx"],run["kind"])
        eps=1e-20
        rates=np.array([np.imag(spectral_charges(z+1j*eps*rhs(z,grid),grid))/eps for z in run["states"]])
        integrated_rates=run["dt"]/3*(rates[0]+rates[-1]+4*np.sum(rates[1:-1:2],axis=0)+2*np.sum(rates[2:-1:2],axis=0))
        for t, v, d, rate in zip(run["times"], run["values"], delta, rates):
            row = dict(run=run["name"], kind=run["kind"], nx=run["nx"], dt=run["dt"], t=t)
            for j in range(3):
                row.update({f"I{j+1}":v[j],f"delta_I{j+1}":d[j],f"relative_delta_I{j+1}":d[j]/abs(initial_vals[j]),f"dI{j+1}_dt_semidiscrete":rate[j]})
            row.update(K=v[3],Pmom=v[4],mean_w_constraint_error=v[5],mean_Uw_constraint_error=v[6])
            rows.append(row)
        s = dict(run=run["name"], nx=run["nx"], dt=run["dt"], T=FINAL,
                 max_constraint_error=float(np.max(run["values"][:,5:7])),
                 max_K_drift=float(np.max(np.abs(run["values"][:,3]-run["values"][0,3]))),
                 final_Pmom_drift=float(run["values"][-1,4]-run["values"][0,4]),
                 max_field_change=float(np.max(run["values"][:,8])),
                 I1_K_Pmom_identity_max_residual=float(np.max(np.abs(delta[:,0]+(run["values"][:,3]-run["values"][0,3])/48-(run["values"][:,4]-run["values"][0,4])/24))))
        for j in range(3):
            s.update({f"I{j+1}_initial":float(initial_vals[j]),f"I{j+1}_final":float(run["values"][-1,j]),
                      f"I{j+1}_final_drift":float(delta[-1,j]),f"I{j+1}_max_abs_drift":float(np.max(np.abs(delta[:,j]))),
                      f"I{j+1}_max_relative_drift":float(np.max(np.abs(delta[:,j]))/abs(initial_vals[j])),
                      f"I{j+1}_initial_defect_rate":float(rates[0,j]),f"I{j+1}_integrated_defect":float(integrated_rates[j]),
                      f"I{j+1}_drift_minus_integrated_defect":float(delta[-1,j]-integrated_rates[j])})
        summaries.append(s)
    write_csv(HERE/"invariant_timeseries.csv",rows)
    write_csv(HERE/"invariant_summary.csv",summaries)
    time_rows=[]
    for kind in ["centered","spectral"]:
        reference=solve(24,kind,1024,f"time_reference_{kind}",save_every=1024)
        for steps in [1,2,4,8]:
            test=solve(24,kind,steps,f"time_{kind}_{steps}",save_every=steps)
            row=dict(kind=kind,nx=24,steps=steps,dt=test["dt"],reference_dt=reference["dt"])
            for j in range(3):
                row[f"I{j+1}_time_error"]=float(abs(test["values"][-1,j]-reference["values"][-1,j]))
            row["K_time_drift"]=float(abs(test["values"][-1,3]-test["values"][0,3]))
            row["field_time_error_linf"]=float(np.max(np.abs(test["states"][-1]-reference["states"][-1])))
            time_rows.append(row)
    write_csv(HERE/"time_refinement.csv",time_rows)
    space_rows=[]
    centered=[r for r in summaries if r["run"].startswith("centered")]
    for coarse,fine in zip(centered[:-1],centered[1:]):
        entry={"nx_coarse":coarse["nx"],"nx_fine":fine["nx"]}
        for j in range(3):
            entry[f"I{j+1}_observed_order"]=float(np.log(abs(coarse[f"I{j+1}_final_drift"] / fine[f"I{j+1}_final_drift"]))/np.log(fine["nx"]/coarse["nx"]))
        space_rows.append(entry)
    write_csv(HERE/"space_refinement.csv",space_rows)
    checks["experiment"]={"M":M,"h":H,"c":C,"gamma":GAMMA,"Lx":LX,"T":FINAL,"R":R.tolist(),
                          "initial_p_mean":[-3,0,3],"initial_p_cos":[1/5,-2/5,1/5],
                          "initial_g_mean":[1,2,3],"initial_g_cos":[1/6,1/7,-1/6-1/7],
                          "time_integrator":"classical explicit RK4", "invariants":"I_n=int res_D L^n dx; not I_n/n and not line-soliton C_n"}
    checks["summary"]=summaries
    checks["space_orders"]=space_rows
    spectral24=next(r for r in runs if r["name"]=="spectral_n24")
    spectral48=next(r for r in runs if r["name"]=="spectral_n48")
    checks["spectral_24_48_final_field_difference_linf"]=float(np.max(np.abs(spectral24["states"][-1]-spectral48["states"][-1,:,:,::2])))
    checks["time_refinement"]=time_rows
    (HERE/"validation.json").write_text(json.dumps(checks,indent=2),encoding="utf-8")
    plot_results(runs,time_rows)
    print(json.dumps({"passed":checks["passed"],"summary":summaries,"space_orders":space_rows,"time_refinement":time_rows},indent=2))


if __name__ == "__main__":
    main()
