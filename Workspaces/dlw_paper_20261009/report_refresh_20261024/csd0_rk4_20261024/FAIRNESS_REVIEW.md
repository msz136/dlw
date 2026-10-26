# CSD0 identification and comparison review

2026-10-24. Independent review of the historical centered representation and its comparison with the current three-method table.

## Identification

CSD0 denotes the `Centered-SD` branch in `spatial_audit_20261023/run.py`, as documented in `spatial_audit_20261023/separated/methods.md`, Sections 4.1–4.2. Its two physical fields occupy the same nodes and are advanced directly. Writing

\[
w_k=v_k-\delta_0u_k,\qquad H(u)=u^2/2+2au,\qquad A(w)=w^2/32-w/4,
\]

the equations are

\[
\begin{aligned}
\Delta_h\dot u_k&=-\mathcal D_x\Delta_h[H(u_k)+h^2 A(w_k)]
-\mathcal D_{xx}(\Delta_hu_k+\mathcal M_-w_k),\\
\dot v_k&=\delta_0\dot u_k-\mathcal D_x[(u_k+2a)w_k-4u_k]+\mathcal D_{xx}w_k.
\end{aligned}
\]

The opening of `separated/reconstruction_probe/derivation.md` gives exactly these original variables and the same first equation. It then constructs the new edge field by adding the full potential term. Thus CSD0 is the earlier nodal physical-field representation, preceding the full-potential construction. Intermediate local and flux-mean reconstruction probes are different trial constructions and are not CSD0. The earlier PE/PF labels do not determine the implementation used here; the explicit equations do.

## Common settings and measurements

The requested four cases use RK4, h=dx=0.1, dt=1e-4, T=0.01 and a=2. All share the continuous soliton references and their spectral parameters. The computational half-widths for A–D are 10, 20, 40, 40; the measurement half-widths R are 5, 10, 30, 30.

The error is the maximum absolute difference at the stored physical locations, restricted to |x|<=R and |y|<R. Initial derivative errors compare the discrete right-hand sides with analytic continuous u_t and v_t at t=0. Terminal errors compare the saved u,v fields with the exact continuous fields at T=0.01. The older `run.py` dense-x CubicSpline error measurements are replaced by this common native-grid measurement.

All implementations use the same unfiltered Fourier x derivatives, with the first-derivative Nyquist multiplier zero. They use the same continuous physical initial profiles and exact lower u_t at each RK4 stage.

## Features retained in CSD0

CSD0 advances (u,v) at y_k, as FD does. Endpoint-SD and the current full-potential Centered-SD place v at internal edge locations y_k-h/2. Each reference is evaluated at the corresponding physical locations.

For CSD0, the lower u ghost is supplied by the continuous wave. The upper ghost equals the exact background plus quadratic extrapolation of the numerical departure from that background. The same rule is differentiated in time when evaluating delta_0 u_t. The lower u_t is the integration constant in the cumulative lattice sum. This is the documented original closure; it is shared with FD for u, while Endpoint-SD and the current Centered-SD do not require that upper ghost.

Current Centered-SD advances (u,w) and reconstructs an edge v through a nonlinear map; CSD0 advances nodal (u,v). A common RK4 and step size therefore specify the common time algorithm, while each representation retains its original state and closure. The terminal table measures the resulting total physical-field error. The t=0 table provides the direct spatial derivative-defect comparison.

## Independent numeric verification

The saved arrays and records are checked by `independent_saved_audit.py`; results are recorded in `independent_saved_audit.json`. This check re-evaluates the exact initial fields, analytic initial time derivatives, and exact terminal fields, and recomputes the sampled maxima. It also independently assembles the CSD0 initial right-hand side and checks the stored source and artifact hashes.

All four cases pass. Recomputed initial derivative errors and terminal field errors agree exactly with the reported values. The independent initial right-hand-side assembly differs from the stored rate by at most 8.89e-16, due to arithmetic ordering. Every initial physical-field error is zero. All source and saved-artifact hashes match.
