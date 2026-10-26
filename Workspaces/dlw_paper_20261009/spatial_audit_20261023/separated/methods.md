## 4. Numerical formulation and linear stability

We use the physical-field equations to examine how spatial approximation and time integration affect the computed waves. Section 4.1 describes the spatial operators for Endpoint-SD, Centered-SD and the direct finite-difference formulation (FD). In Section 4.2, we specify the initial and boundary data and introduce the three time integrators used in the experiments.

### 4.1 Fourier differentiation and spatial formulations

For the numerical comparisons, we apply the same Fourier differentiation in \(x\) to all three spatial formulations. On a uniform grid of spacing \(\Delta x\), let \(\mathcal D_x\) and \(\mathcal D_{xx}\) denote the first- and second-derivative operators. The calligraphic notation distinguishes these numerical operators from Hirota's bilinear derivatives. Their Fourier multipliers are \(\mathrm i\xi\) and \(-\xi^2\), respectively. For an even number of grid points, the first-derivative multiplier at the Nyquist frequency is set to zero, while the second derivative retains its multiplier. Nonlinear products are evaluated at the nodes.

We write \(u_k,v_k\) for the physical fields in each method. For Endpoint-SD, \(v_k\) is located at \(y_k-h/2\), whereas \(u_k\) is located at \(y_k\). Both Centered-SD fields and both FD fields are evaluated at \(y_k\). With \(\Delta_h q_k=(q_k-q_{k-1})/h\), \(\mathcal M_-q_k=(q_k+q_{k-1})/2\) and \(\delta_0q_k=(q_{k+1}-q_{k-1})/(2h)\), the Endpoint-SD equations (27)–(28) become

\[
\begin{aligned}
\Delta_h\dot u_k&=-\mathcal D_x\Delta_h(u_k^2/2+2au_k)-\mathcal D_{xx}v_k,\\
\dot v_k&=-\mathcal D_x\left[(\mathcal M_-u_k+2a-2h)v_k+\frac h4v_k^2-4\mathcal M_-u_k-\frac h4(\Delta_hu_k)^2\right]-\mathcal D_{xx}\Delta_hu_k.
\end{aligned}
\]

For Centered-SD, we discretize (35) in the same way. This gives

\[
\begin{aligned}
\Delta_h\dot u_k={}&-\mathcal D_x\Delta_h\left[\frac{u_k^2}{2}+2au_k+\frac{h^2}{32}(v_k-\delta_0u_k)^2-\frac{h^2}{4}(v_k-\delta_0u_k)\right]\\
&-\mathcal D_{xx}\left[\Delta_hu_k+\mathcal M_-(v_k-\delta_0u_k)\right],\\
\dot v_k={}&\delta_0\dot u_k-\mathcal D_x\left[(u_k+2a)(v_k-\delta_0u_k)-4u_k\right]+\mathcal D_{xx}(v_k-\delta_0u_k).
\end{aligned}
\]

As a comparison, we discretize the continuous DLW equations directly in \(y\), using the same Fourier operators in \(x\). The resulting FD formulation is

\[
\begin{aligned}
\Delta_h\dot u_k&=-\mathcal D_x\Delta_h(u_k^2/2+2au_k)-\mathcal D_{xx}\mathcal M_-v_k,\\
\dot v_k&=-\mathcal D_x[(u_k+2a)v_k-4u_k]-\mathcal D_{xx}\delta_0u_k.
\end{aligned}
\]

In each formulation, we recover \(\dot u_k\) by summing its lattice difference from a prescribed lower value. Substitution into the second equation then gives \(\dot v_k\). Thus, the current fields and boundary data determine the derivatives needed for time integration.

### 4.2 Initial and boundary data and time integration

We specify the initial and boundary data from the continuous exact waves and advance the physical fields with forward Euler, classical RK4 and Crank–Nicolson. The state \(z=(u_k,v_k)_k\) contains the nodal values of both fields. At each stage, we use the current state and the prescribed boundary data to evaluate \(\dot z=F(t,z)\).

All methods start from samples of the same continuous solution at their respective physical locations. The lower value of \(u\) and its time derivative are supplied by that solution; the lattice sum starts from the first prescribed \(u\) node. Endpoint-SD uses backward lattice relations. For Centered-SD and FD, the upper value needed by \(\delta_0\) is obtained by extrapolating the departure from the exact background. Writing \(u_k^*(t)\) for this background and \(e_k=u_k-u_k^*\), we use \(u_{N+1}=u_{N+1}^*+3e_N-3e_{N-1}+e_{N-2}\). The same relation is differentiated in time when evaluating \(\delta_0\dot u\) for Centered-SD. The \(x\) interval is periodic, with boundaries placed beyond the region used to measure errors. We use no filtering, dealiasing or artificial viscosity.

Forward Euler evaluates the derivative at the beginning of each step, giving \(z^{n+1}=z^n+\Delta t\,F(t_n,z^n)\). For RK4, we evaluate four stages,

\[
\begin{aligned}
K_1&=F(t_n,z^n),&K_2&=F(t_n+\Delta t/2,z^n+\Delta t K_1/2),\\
K_3&=F(t_n+\Delta t/2,z^n+\Delta t K_2/2),&K_4&=F(t_n+\Delta t,z^n+\Delta t K_3),\\
z^{n+1}&=z^n+\frac{\Delta t}{6}(K_1+2K_2+2K_3+K_4).
\end{aligned}
\]

Crank–Nicolson averages the derivatives at the two ends of the step:

\[
z^{n+1}=z^n+\frac{\Delta t}{2}\left[F(t_n,z^n)+F(t_{n+1},z^{n+1})\right].
\]

We solve this implicit equation by fixed-point iteration, starting from an Euler prediction. Each accepted step has a maximum absolute equation residual below \(10^{-12}\). Boundary values are evaluated at the time of each stage or implicit iteration.
