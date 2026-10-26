## 4. Numerical formulation and linear stability

We use the physical-field equations to examine how spatial approximation and time integration affect the computed waves. Section 4.1 describes the common x operators and the three spatial formulations. In Section 4.2, we specify the initial and boundary data and introduce the time integrators used in the experiments.

### 4.1 Fourier differentiation and spatial formulations

We apply Fourier differentiation in x to all three methods. On a uniform grid of spacing \(\Delta x\), the calligraphic operators \(\mathcal D_x\) and \(\mathcal D_{xx}\) have multipliers \(\mathrm i\xi\) and \(-\xi^2\), respectively; they are distinct from Hirota's bilinear derivatives. The first-derivative multiplier is zero at the Nyquist frequency, while the second derivative retains its multiplier. Products are evaluated at the nodes.

Write u and v for the physical fields in each numerical method. For both semi-discrete formulations, u lies at nodes \(y_k\) and v at edge midpoints \(y_k-h/2\); FD uses both fields at \(y_k\). Let \(H(u)=u^2/2+2au\), \(A(w)=w^2/32-w/4\), \(\Delta_hq_k=(q_k-q_{k-1})/h\), \(\mathcal M_-q_k=(q_k+q_{k-1})/2\) and \(\delta_0q_k=(q_{k+1}-q_{k-1})/(2h)\). Endpoint-SD follows (27)–(28):
\[
\begin{aligned}
\Delta_h\dot u_k&=-\mathcal D_x\Delta_hH(u_k)-\mathcal D_{xx}v_k,\\
\dot v_k&=-\mathcal D_x[(\mathcal M_-u_k+2a-2h)v_k+hv_k^2/4-4\mathcal M_-u_k-h(\Delta_hu_k)^2/4]-\mathcal D_{xx}\Delta_hu_k.
\end{aligned}
\]

For Centered-SD, we use the full-potential reconstruction (35). The numerical primitive \(\mathcal J\) has multiplier \(1/(\mathrm i\xi)\) at nonzero, non-Nyquist frequencies and zero at the zero and Nyquist modes. Consequently, \(\mathcal D_{xx}\mathcal J=\mathcal D_x\) exactly. Its normalization is the same in every test. The reconstruction and its evolution are
\[
\begin{aligned}
v_k&=\Delta_hu_k+\mathcal M_-w_k+h^2\mathcal J\Delta_hA(w_k),\\
\Delta_h\dot u_k&=-\mathcal D_x\Delta_hH(u_k)-\mathcal D_{xx}v_k,\\
\dot w_k&=\mathcal D_{xx}w_k-\mathcal D_x[(u_k+2a)w_k-4u_k],\\
\dot v_k&=\Delta_h\dot u_k+\mathcal M_-\dot w_k+h^2\mathcal J\Delta_h[A'(w_k)\dot w_k].
\end{aligned}
\]
For time stepping, we advance u,w and reconstruct v. Substituting the reconstruction into the first equation gives the equivalent implementation
\[
\Delta_h\dot u_k=-\mathcal D_x\Delta_h[H(u_k)+h^2A(w_k)]-\mathcal D_{xx}[\Delta_hu_k+\mathcal M_-w_k].
\]
This avoids repeated nonlinear inversion during the time stages. The chain-rule equation for \(\dot v\) is used in the initial-defect measurements.

The direct discretization of the continuous system gives the FD baseline:
\[
\begin{aligned}
\Delta_h\dot u_k&=-\mathcal D_x\Delta_hH(u_k)-\mathcal D_{xx}\mathcal M_-v_k,\\
\dot v_k&=-\mathcal D_x[(u_k+2a)v_k-4u_k]-\mathcal D_{xx}\delta_0u_k.
\end{aligned}
\]
In each method, the prescribed lower value of \(\dot u\) determines the integration constant when summing its lattice difference.

### 4.2 Initial and boundary data and time integration

We specify the initial and boundary data from the continuous exact waves, then advance the resulting systems with forward Euler, classical RK4 and Crank–Nicolson. All physical fields initially sample the same continuous solution at their respective locations. For Centered-SD, the integrated state is \(z=(u_k,w_k)_k\), and v is recovered from the fixed reconstruction in Section 4.1. Thus the time methods below act on this auxiliary state.

At initialization, we set the lower auxiliary trace to \(w_0=(v-u_y)(x,y_0,0)\) and solve
\[
\frac12w_k+h\mathcal J A(w_k)=v_k-\Delta_hu_k-\frac12w_{k-1}+h\mathcal J A(w_{k-1})
\]
successively along y. A damped fixed-point iteration selects the branch used in the experiments, with a maximum fixed-point residual below \(2\times10^{-12}\). Thereafter, every w node, including its lower trace, evolves by its own equation. The lower u value and its time derivative are supplied by the exact continuous wave. The reconstructed v values occupy the internal edges; no upper y ghost is required by this Centered-SD formulation.

Endpoint-SD uses its backward lattice relations and the exact lower data. For FD, the upper u ghost is obtained by extrapolating the departure from the exact background: with \(e_k=u_k-u_k^*\), set \(u_{N+1}=u_{N+1}^*+3e_N-3e_{N-1}+e_{N-2}\). The x interval is periodic and extends beyond the region where errors are measured. No filtering, dealiasing or artificial viscosity is applied.

Writing \(\dot z=F(t,z)\), forward Euler gives \(z^{n+1}=z^n+\Delta t F(t_n,z^n)\). Classical RK4 uses
\[
\begin{aligned}
K_1&=F(t_n,z^n),&K_2&=F(t_n+\Delta t/2,z^n+\Delta t K_1/2),\\
K_3&=F(t_n+\Delta t/2,z^n+\Delta t K_2/2),&K_4&=F(t_n+\Delta t,z^n+\Delta t K_3),\\
z^{n+1}&=z^n+\frac{\Delta t}{6}(K_1+2K_2+2K_3+K_4).
\end{aligned}
\]
Crank–Nicolson solves
\[
z^{n+1}=z^n+\frac{\Delta t}{2}[F(t_n,z^n)+F(t_{n+1},z^{n+1})].
\]
We use an Euler prediction followed by fixed-point iteration, accepting a step when the maximum absolute equation residual is below \(10^{-12}\). Boundary data are evaluated at the appropriate stage time. The reported errors are always errors in the physical u,v fields, including when the integrator advances u,w.
