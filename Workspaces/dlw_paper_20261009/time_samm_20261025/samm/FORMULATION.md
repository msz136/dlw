# Current natural Centered-SD SAMM

> **Superseded.** These runs use the pinned-node velocity and a lower-row transport error. The published
> comparison is `../samm_periodic/` (periodic mean-flux velocity, corrected lower row). This file is kept
> for provenance only; see `../README.md`.

The implementation advances `(u,w,s)`, with `omega=h*w/4`, shared nodes `x_i=xi_i+s_i`, and physical edge field

\[
v_k=\Delta_hu_k+\frac{w_k+w_{k-1}}2.
\]

All y layers share the same x grid. This is the physical-field formulation of current Section 3.2, with its auxiliary reconstruction represented by w. No x antiderivative or previous full-potential term is introduced.

## Conservation law

Equation (37) gives
\[
w_{k,t}=w_{k,xx}-[(u_k+2a)w_k-4u_k]_x.
\]
Set
\[
\rho_k=1-\frac{w_k}{4}=1-\frac{\omega_k}{h},\qquad
q_k=(u_k+2a)\rho_k-\rho_{k,x}-2a.
\]
Then `rho_t+q_x=0`. This follows by substituting `w=4(1-rho)`; the flux identity is `(u+2a)w-4u=8a-4(u+2a)rho`. The constant makes the flux zero on the zero-field background.

The shared monitor and flux are arithmetic averages over all N_y stored nodal layers:
\[
\bar\rho=N_y^{-1}\sum_k\rho_k,\qquad
\bar q=N_y^{-1}\sum_k q_k.
\]
The experiments use the two zero-background soliton benchmarks A and D and the positive monitor above. The Gaussian/sinusoidal family has a nonzero second-field background and is outside this mesh comparison.

## Grid and velocity

The computational grid is periodic, `xi_i=-L/2+i Delta xi`, `i=0,...,N_x-1`; `x_N=x_0+L`. The left reference node is pinned. Initial nodes equidistribute the continuous monitor calculated from the exact initial u/v and the same discrete-y reconstruction:
\[
\int_{x_0}^{x_i(0)}\bar\rho(x,0)\,dx
=\frac{i}{N_x}\int_{x_0}^{x_0+L}\bar\rho(x,0)\,dx.
\]
Initial cumulative integration uses 40,001 dense x samples and linear inversion. The fields are evaluated afresh at the resulting nodes. Their initial physical values are exact samples, not interpolated uniform-grid states.

For a fixed interval with arbitrary endpoint fluxes, the normalized mass coordinate gives
\[
\mathcal V_i=\frac{\bar q_i-\bar q_L+\eta_i(\bar q_L-\bar q_R)}{\bar\rho_i}.
\]
For the periodic computational domain used here, endpoint fluxes coincide. Thus the implemented velocity is
\[
\mathcal V_i=\frac{\bar q_i-\bar q_0}{\bar\rho_i},\qquad \mathcal V_0=0.
\]
At each RK4 stage, the density and flux are computed from that stage's fields and coordinates. The conservation law is exact before x discretization; the mapped centered discretization approximates it. Discrete mass and cell-density balance are measured rather than declared exact.

## Mapped centered differences and ALE

Both uniform and adaptive runs use the same three-point computational differences
\[
\delta_\xi f_i=\frac{f_{i+1}-f_{i-1}}{2\Delta\xi},\qquad
\delta_{\xi\xi}f_i=\frac{f_{i+1}-2f_i+f_{i-1}}{\Delta\xi^2}.
\]
Writing `J=1+delta_xi s`, the physical operators are
\[
\mathcal D_x f=\frac{\delta_\xi f}{J},\qquad
\mathcal D_{xx}f=\frac{\delta_{\xi\xi}f}{J^2}
-\frac{(\delta_\xi J)(\delta_\xi f)}{J^3}.
\]
The natural field equations use these operators in place of x derivatives. Moving-node rates add the common transport term to each evolving field:
\[
\dot u_k=F_{u,k}+\mathcal V\mathcal D_xu_k,\qquad
\dot w_k=F_{w,k}+\mathcal V\mathcal D_xw_k,\qquad
\dot x_i=\mathcal V_i.
\]
Equivalently, physical v obeys the corresponding ALE transport because the common x operators commute with the y difference and averaging.

For the lower u trace only, prescribed continuous data give `du_0/dt=u_t^*(x_i,y_0,t)+V_i u_x^*(x_i,y_0,t)`. Both derivatives come from analytic tau moments. The Eulerian interior u_t is reconstructed upward from that exact lower Eulerian rate. The lower w trace is initialized from `v^*-u_y^*=4(log g)_{xy}`, and then evolves with the same w equation as every other layer. There is no upper-y ghost in this backward-difference natural formulation. Periodic x differences close every layer. The physical v values remain at adjacent y midpoints.

## Paired configurations

- A: x/y computational half-width 10, N_x=N_y=200, error region |x|<=5 and |y|<5.
- D: x/y computational half-width 40, N_x=N_y=800, error region |x|<=30 and |y|<30.
- Both: a=2, h=Delta xi=.1, RK4, Delta t=1e-4, T=.01.
- Uniform: x=xi throughout.
- Frozen: the equidistributed initial x nodes are held fixed.
- SAMM: the same equidistributed initial nodes evolve with the stated conservation-based velocity.

The fixed-grid values in this comparison use centered x differences and are distinct from Section 5.2's Fourier-x results. This matched pair isolates the effect of the mesh under one spatial differentiation rule. Initial/final nodes, averaged density, fields, exact values and native error histories are retained in each NPZ.
