# Nondegenerate Gaussian and sinusoidal comparison

The two initial fields are

\[
u_0=A\sin(\pi(y+2)/4)F(x),\qquad v_0=4-3\partial_yu_0.
\]

Gaussian: \(A=.05\), \(F(x)=\sum_{j\in\mathbb Z}e^{-((x+192j)/6)^2}\).
Sinusoidal: \(A=.03\), \(F(x)=\cos(\pi x/12)\).
The relation \(v=4-3u_y\) is imposed only at the initial time. The positive-time
reference is the complete continuous DLW solution from the two-heat-equation
and Laplace-transform construction; it is not the old compatible Burgers family.

## Common parameters and metric

- \(a=2\), \(\Delta x=h=.1\), RK4, \(\Delta t=10^{-4}\), \(T=.01\).
- 1920 periodic x samples on \([-96,96)\); 41 nodal y samples on \([-2,2]\).
- Fourier x differentiation; first-derivative Nyquist multiplier zero;
  unmodified second derivative; no filtering or dealiasing.
- Errors are sampled absolute maxima over all x nodes and native field sites
  satisfying \(|y|\le1.8+10^{-12}\). Endpoint-SD and current Centered-SD use edge
  v fields; CSD0 and FD use nodal v fields. All references use those native sites.

The eight experiments completed to \(T=.01\). `results.json` records terminal
u/v errors; `initial_results.json` records initial u_t/v_t defects.
`validation.json` verifies the saved fields, physical map, reference arrays,
reported errors, and file hashes. The four existing soliton experiments are
outside this directory and were not rerun or changed.

## Four representations

Endpoint-SD, CSD0, and FD evolve physical u/v directly. CSD0 is the original
`Model(..., 'Centered-SD')` branch in the spatial audit code: it defines
\(w=v-\delta_0u\) internally at every RHS evaluation.

The current Centered-SD evolves u/w and reconstructs edge v by the full-potential
map. Its inverse initialization matches the prescribed edge v to less than
\(10^{-12}\), starting from the exact lower trace \(w_0=4-4u_{0y}\). Its maximum
initial physical discrepancy is \(9.9921\times10^{-13}\). No relation between the
physical fields is imposed after initialization.

All methods prescribe the exact continuous lower u_t. Endpoint-SD uses the exact
lower ghost u. CSD0 and FD use the same exact background plus quadratic
extrapolation of the numerical departure at the upper ghost; CSD0 applies the
time derivative of this same closure to u_t. Current Centered-SD evolves all w
nodes and needs no upper y ghost. Reference ghosts y=-2.1,2.1 are evaluated by the
same analytic extension of the continuous solution. Boundary values are shared
on the common RK4 half-step grid, independently of the numerical state.

## Analytic initial reference

The original continuous PDE, integrated from u(x,-2,t)=0, gives

\[
u_t(0)=3u_{0,xx}-(u_0+4)u_{0,x},\qquad
v_t(0)=-u_{0,xxy}+3[u_{0,x}u_{0,y}+(u_0+4)u_{0,xy}].
\]

`run.py::initial_data` evaluates these derivatives analytically. Initial Gaussian
periodic sums use j=-1,0,1, with their omitted tails addressed by reference
certification. `audit_saved.py` independently implements the four RHS maps and
the analytic initial derivatives. Its outputs distinguish implementation checks
from the continuous reference enclosure.

## Reproduce

From the workspace root:

```powershell
python Workspaces/dlw_paper_20261009/report_refresh_20261024/nondegenerate_rk4_20261024/run.py Gaussian
python Workspaces/dlw_paper_20261009/report_refresh_20261024/nondegenerate_rk4_20261024/run.py Sinusoidal
python Workspaces/dlw_paper_20261009/report_refresh_20261024/nondegenerate_rk4_20261024/run.py collect
```

Existing completed records are retained. `run.py initial` recomputes the initial
checks only. Each terminal JSON stores the sources and state-file SHA256 hashes.
See `REFERENCE_GRID.md` and `reference_certificate.json` for the actual reference
enclosure and its applicable scope.
