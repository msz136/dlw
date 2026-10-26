# Independent audit: physical-field perturbations and continuum certification

2026-10-26. Scope: independently perturb the physical initial fields of the current one-soliton (A), two-soliton (D), Gaussian and sinusoidal benchmarks. The current non-soliton data are the nondegenerate family `v0=4-3*u0_y`. This note distinguishes a continuum PDE certificate from a certified finite-dimensional evolution and from numerical refinement evidence.

## 1. What the existing spectrum file actually computes

`linear_spectrum.py` imports `spatial_audit_20261023/run.py:Model`. Its `Centered-SD` state is the old nodal `(u,v)` implementation with `w=v-delta0(u)`, an upper ghost extrapolation and the older physical reconstruction. It is **not** the current Section 3.2 natural-edge `(u,w)` state, where

\[
v_k=\frac{u_k-u_{k-1}}h+\frac{w_k+w_{k-1}}2,
\qquad \omega_k=\frac h4w_k.
\]

The saved eigenvalues therefore must not be relabelled as the present Centered-SD spectrum. The script also studies the zero background, whereas the Gaussian/sinusoidal tests have background `v=4`. Its eigenvalues are floating-point observations, not interval spectral enclosures. The finite-amplitude `measured_rate` includes the changing phase sampled by a discrete maximum and nonlinear terms; it is not an exact eigenvalue identity.

## 2. Continuous principal mechanism, with signs checked

The continuous equations are

\[
u_{yt}=-v_{xx}-[(u+4)u_y]_x,
\qquad
v_t=-u_{xxy}-[(u+4)v-4u]_x.
\]

Linearize at a constant pair `(U0,V0)`, put `p=delta u_y`, `q=delta v`, and write `c=U0+4`. Then

\[
p_t=-c p_x-q_{xx},\qquad
q_t=-c q_x-p_{xx}-(V_0-4)\delta u_x.
\]

For a double Fourier mode `exp(i xi x+i eta y)` with `eta != 0`, `delta u=p/(i eta)`. The matrix and its eigenvalues are

\[
\partial_t\binom p q=
\begin{pmatrix}
-ic\xi&\xi^2\\
\xi^2-(V_0-4)\xi/\eta&-ic\xi
\end{pmatrix}\binom p q,
\]
\[
\sigma_\pm=-ic\xi\pm
\sqrt{\xi^4-(V_0-4)\xi^3/\eta}.
\]

Thus the positive real branch is asymptotic to `xi^2` at high x frequency, for fixed nonzero eta. At `V0=4`, the branches are exactly `-ic xi +/- xi^2`. This is a continuous-equation mechanism. It is not created by the use of RK4.

The calculation with eta is a constant-coefficient/local or doubly periodic symbol. The paper's y strip has a prescribed lower trace, so it is not legitimate to identify eta with an eigenvalue of that closure without a separate calculation. In particular, dividing by eta at eta=0 is invalid. The cross derivative determines `u_t` only after its y-independent integration function has been fixed by the lower trace.

For xi=0 every displayed x derivative vanishes. The x mean of `u_y` and of `v` is consequently constant in time; the x mean of u is then fixed by the prescribed lower trace. A perturbation independent of x does not experience the high-x-frequency mechanism about a constant background. It can still interact with the x-dependent part of a nonconstant base wave.

### An exact strip reference for the constant-background linearization

At `(U0,V0)=(0,4)`, let `X=x-4t`, take a smooth phi with `phi(yL)=phi'(yL)=0`, and use u-only initial data `delta u0=epsilon phi(y) cos(kappa x)`, `delta v0=0`. The exact linearized response is

\[
\delta u=\epsilon\phi(y)\cos(\kappa X)\cosh(\kappa^2t),
\qquad
\delta v=\epsilon\phi'(y)\cos(\kappa X)\sinh(\kappa^2t).
\]

For v-only data `delta u0=0`, `delta v0=epsilon psi(y)cos(kappa x)`, with `psi(yL)=0`, it is

\[
\delta u=\epsilon\left(\int_{y_L}^y\psi(s)\,ds\right)
\cos(\kappa X)\sinh(\kappa^2t),
\qquad
\delta v=\epsilon\psi(y)\cos(\kappa X)\cosh(\kappa^2t).
\]

These formulae satisfy the strip's homogeneous lower perturbation traces without introducing a transverse Fourier mode. They give a useful independently checkable implementation test. They are not the full nonlinear perturbations of A, D, Gaussian or sinusoidal waves.

At `T=.01`, 160-bit Arb evaluation gives the following containing intervals (rounded outward here):

| kappa | cosh(kappa² T) | sinh(kappa² T) |
|---|---:|---:|
| pi/2 | [1.0003044188533672, 1.0003044188533674] | [.0246765146966270, .0246765146966272] |
| pi | [1.0048744093902206, 1.0048744093902208] | [.0988563536012976, .0988563536012978] |
| 2 pi | [1.0789446555261067, 1.0789446555261069] | [.4051192042946731, .4051192042946733] |
| 4 pi | [2.5284596746025343, 2.5284596746025345] | [2.3223066821785519, 2.3223066821785521] |
| 8 pi | [276.8298059443590, 276.8298059443592] | [276.8279997745738, 276.8279997745741] |

These enclosures concern only the elementary linear amplification factors.

### Current natural Centered-SD: exact finite-strip diagonal block

At a constant state `(u,w)=(U,V)`, put `d=V-4`, `c=U+4`, and keep the lower-u perturbation zero. After summing the first lattice equation upward, the trapezoidal primitive of w has diagonal entry h/2. For each non-Nyquist x Fourier mode, the diagonal block at each interior y layer is therefore

\[
B=\begin{pmatrix}
\xi^2-ic\xi&h\xi^2/2-i h^2d\xi/16\\
-id\xi&-\xi^2-ic\xi
\end{pmatrix}.
\]

Subtracting `-ic xi I` gives squared characteristic root

\[
\xi^4-i h d\xi^3/2-h^2d^2\xi^2/16
=(\xi^2-i h d\xi/4)^2.
\]

The exact eigenvalues are

\[
\lambda_\pm=-ic\xi\pm(\xi^2-i h d\xi/4),
\qquad \Re\lambda_\pm=\pm\xi^2.
\]

Ordering the unknowns as `(w0,u1,w1,u2,w2,...)` makes the full strip matrix block lower triangular. The first lower-w block has eigenvalue `-xi²-ic xi`. Each interior block has the two eigenvalues above. At the x Nyquist mode the implementation sets the first derivative multiplier to zero, so the advection terms vanish and the real eigenvalues are again `+/-xi²`; the displayed complex formula is for non-Nyquist modes. At xi=0 the matrix vanishes.

The repeated blocks and their lower-triangular coupling can produce nonnormal/Jordan transient factors. The eigenvalues alone do not establish a propagator upper bound `exp(xi² t)`. They do show that an upper estimate uniform in the x cutoff cannot be obtained merely by assigning this closed system a cutoff-independent ordinary-norm Lipschitz constant.

`audit_linear_reference.py` independently verifies both the characteristic identity and the continuous linear PDE formulae with symbolic algebra. It also constructs a small modal matrix from the actual production `rhs` using cosine/sine directions, at backgrounds `(U,V)=(0,0),(0,4),(.2,1.3)`. The largest discrepancy from the independently assembled lower-triangular matrix is `1.02e-11`. These floating-point matrix comparisons check implementation agreement; the displayed eigenvalue identity follows from exact symbolic algebra.

The same script writes `audit_linear_reference.json`, including 160-bit Arb amplification factors and ten point-evaluation enclosures for the continuous linear reference. Each recorded physical perturbation enclosure has radius below `1e-40`. Reproduce from the workspace root with `python -X utf8 Workspaces/dlw_paper_20261009/stability_20261026/audit_linear_reference.py`. The point enclosure includes evaluation arithmetic, but it still certifies only this explicit continuous linear test.

## 3. Why independent physical perturbations change the reference problem

The existing nondegenerate heat/Laplace construction proves a reference for initial data `u0=2s(y)F0(x)`, `v0=4-6s_y F0(x)`. An arbitrary independent change to u0 or v0 destroys this initial relation. Its existing truncation certificate cannot be transferred to the perturbed problem by continuity, because the needed continuous dependence estimate has not been established.

Around background 4, use

\[
a=u_y+v-4,\quad b=u_y-v+4,\quad
u=\tfrac12\int_{y_L}^y(a+b)\,ds
\]

with zero lower u, in the moving coordinate X. The full nonlinear equations become

\[
a_t=-a_{XX}-(ua)_X,\qquad
b_t=b_{XX}-(ub)_X.
\]

An independent u-only perturbation changes both a and b by `delta u_y`; a v-only perturbation changes them by opposite signs. Neither restriction suppresses the backward-diffusive variable a. On a nonconstant base solution, the linearized coefficients also vary with X,y,t.

### The proposed ultraanalytic fixed point does not close as stated

For the Fourier norm `||f||_r=sum_k exp(r xi_k²)|f_k|`, the product is not bounded from the radius-r space to itself. For a single mode `f_K=exp(-r K²)exp(iKX)`,

\[
\|f_K\|_r=1,\qquad \|f_K^2\|_r=e^{2rK^2}\to\infty.
\]

The elementary convolution estimate only gives `||fg||_(r/2) <= ||f||_r ||g||_r`. Thus `(ua)_X` and `(ub)_X` lose a factor of two in the Gaussian radius at each nonlinear multiplication. A small amplitude does not repair the unbounded same-radius bilinear map. The transverse Volterra integral is bounded but does not remove this x-frequency loss.

In contrast, the analytic norm with weight `exp(r|xi|)` is a convolution algebra, but the backward heat multiplier `exp(t xi²)` is unbounded between every two such spaces of finite radii for any `t>0`.

These facts do not prove that each of the four requested perturbed IVPs has no solution. They show exactly why an ordinary analytic or a fixed-radius Gaussian-norm contraction cannot simply be asserted. A viable theorem must supply a genuinely different scale-of-spaces argument, structural cancellation, or an independently verified bound on the backward branch's entire tail. The earlier positive tail-majorant route already fails under a nonlinear harmonic cascade. The existing mixed initial/final theorem gives a solution after prescribing the unstable component at final time; it does not prove that its initial trace matches the independently prescribed perturbed a0. That matching map's range remains the unresolved step.

## 4. Continuum domain and boundary must be frozen before refinement

Two current numerical conveniences matter for certification:

1. The continuous A/D solitons live on the whole x line. Their samples on a finite interval are not exactly periodic at the finite endpoints. For a perturbed continuum IVP one must either retain the whole-line problem and prove a truncation/tail error bound, or explicitly define a periodicized datum/new boundary problem. Periodic sampling is not an exact equality of these problems.
2. The production soliton y nodes currently run from `-half+h/2` to `half-h/2`; hence the lower trace location moves when h is refined. The non-soliton grid uses fixed `[-2,2]`. A convergence/certification study needs fixed physical yL,yR and the same lower trace at every h. For a new experiment, A `[-10,10]`, D `[-40,40]`, and Gaussian/sinusoidal `[-2,2]` are explicit candidate strips, with u,w at nodes and v at edge midpoints. This is a new experiment definition and must be documented, rather than silently changing existing tables.

The independent perturbation should vanish at the lower boundary together with its first y derivative for u, and vanish there for v. This preserves both the prescribed u trace and the initial lower w trace. The latter must then evolve by its auxiliary equation; v should not also be forced to the unperturbed boundary at positive times. The current natural formulation does not require an upper-y ghost condition. Retaining a ghost rule from the legacy nodal code would change the experiment.

## 5. A fixed, reproducible perturbation protocol

Write `r=(y-yL)/(yR-yL)`. Use

\[
\Phi_{\kappa,n}(x,y)=\cos(\kappa x+\theta)
\sin^2(\pi r)\cos(n\pi r),\qquad \theta=0.
\]

Normalize using the continuous supremum or a proven upper bound, not a grid-dependent maximum. For example the unnormalized factor already has absolute value at most one; report the raw amplitude epsilon as the maximum allowed perturbation.

Run u-only and v-only separately:

\[
(u_0^\epsilon,v_0^\epsilon)=(u_0+\epsilon\Phi,v_0),
\quad\text{or}\quad
(u_0^\epsilon,v_0^\epsilon)=(u_0,v_0+\epsilon\Phi).
\]

- Primary amplitude: epsilon=1e-6 in physical-field units. Amplitude controls: 1e-7 and 1e-5. Record actual initial maxima in both fields; do not rescale by the background v=4.
- x-focused family: n=0 and kappa in `{pi/2, pi, 2pi}`. These wavelengths divide the existing x periods 20,80,192 and are fixed across mesh refinements. The sin² factor is the necessary y boundary envelope, so do not describe this as a literally y-independent perturbation.
- y-only family: kappa=0, n in `{1,2,4}`. It changes the x means, which are then invariants under x-divergence evolution with fixed lower trace; retain these means instead of discarding the zero mode.
- xy family, after the separate tests: kappa in `{pi/2,pi,2pi}` and n in `{1,2,4}`. Fix the modes before examining results.
- Use the same current natural Centered-SD closure for the base and perturbed numerical runs. Compare the perturbed computation with its own perturbed reference, not with the unperturbed exact solution when calling the quantity a numerical error.

The response and reference error are different quantities:

\[
G_f(t)=\|f^\epsilon(t)-f^0(t)\|/\epsilon,
\qquad
D_f(t)=\|f_{\rm num}^\epsilon(t)-f_{\rm ref}^\epsilon(t)\|.
\]

When the exact perturbed fields are unavailable, the base/perturbed numerical difference measures the response of that fixed numerical closure. It must not be labelled the certified continuum response. Keep a time-step control and independent spatial refinements, and record the maximum reached time and failed trajectories without replacing them by extrapolated values.

## 6. What can be certified at a fixed cutoff

The current finite natural-edge equations are smooth polynomial ODEs after boundary data are supplied. Interval Taylor/Picard integration can in principle enclose their exact solution, including initial Gram/Laplace evaluation and roundoff. A rigorous residual theorem is also available if the residual is enclosed over every entire time slab and the trajectory tube is validated.

For a simple finite-cutoff bound, use the Fourier l1 norm in x and the maximum over y nodes; let `E=max(E_u,beta E_w)`. Let K bound the represented Fourier frequencies, Ly the discrete integration length, and `M_u,M_w` verified bounds on the reference trajectory. Taking the lower u trace exactly, a conservative polynomial estimate is

\[
D^+E\le\rho+LE+BE^2,
\]
\[
L=\max\left\{
2K(M_u+4)+K^2+
\frac{2Kh^2(M_w/16+1/4)+K^2L_y}{\beta},\quad
K^2+K(M_u+4)+\beta K(M_w+4)
\right\},
\]
\[
B=\max\{K+Kh^2/(16\beta^2),K\}.
\]

The factor two in the first line permits the nonlinear flux at both the current and lower y node. The quadratic bound follows from `H=u²/2+4u+h²(w²/32-w/4)` and the product `uw`. The centered x-DFT product, including aliasing as defined by the finite ODE, is bounded in the discrete Fourier l1 algebra. The integral of w has norm at most Ly. For `E(0)<=e0`, if

\[
\eta=(e_0+T\rho)e^{(L+BR)T}<R,
\]

then the finite ODE solution stays in the radius-R tube and satisfies `E<=eta`. In physical fields the natural-edge reconstruction gives

\[
\|e_v\|_\infty\le(2/h+1/\beta)\eta,
\qquad \|e_u\|_\infty\le\eta.
\]

This is a conditional finite-dimensional certificate template. No verified values of the trajectory bounds or full-slab residual have been obtained in this audit. The `K²` growth and unresolved infinite tail prevent treating this formula as a continuum PDE bound. Refining the finite ODE until two answers agree does not discharge that missing tail theorem.

## 7. What the requested continuum guarantee must contain

For each perturbed initial-boundary problem the needed assertion is

\[
\|f^\epsilon-f_{\rm ref}^\epsilon\|\le\eta_f,
\quad
\eta_f\le .01\,D_f,
\quad f=u,v.
\]

A successful certificate must bound initial representation, spatial tails, temporal evaluation/reconstruction, continuous PDE residual, boundary/domain approximation and arithmetic under one stated solution class. If the reported norm is a maximum over native points, the bound applies at those points; a full-space maximum additionally needs interpolation/reconstruction control.

For now, the four independent-field perturbed PDEs do not inherit such a certificate from the unperturbed solutions. The exact linear test in Section 2 is certifiable, and the fixed-cutoff nonlinear ODE route in Section 6 is certifiable after further computation; neither supplies the missing nonlinear continuum bound. This is a precise outstanding mathematical condition, not a proof of nonexistence for those four data.

## Evidence read

- `stability_20261026/linear_spectrum.py` and `linear_spectrum.json`.
- `spatial_audit_20261023/run.py`, especially its nodal centered reconstruction and ghost rule.
- `spatial_audit_20261023/separated/reconstruction_probe/rerun_20261024.py` for the natural `(u,w)` right-hand side, used with the current local reconstruction.
- `reference_certificate_20261024/THEORY.md` for the exact Volterra reformulation and certificate scope.
- `reference_certificate_20261024/RESIDUAL_NO_GO_CLOSURE.md` for the residual-only obstruction, with its stated regularity assumptions and proof-draft status.
- `reference_certificate_20261024/nondegenerate_benchmarks/PROOF.md` and `reference.py` for the actual certified unperturbed family and its restricted initial pairing.

No manuscript, numerical source, previous data, progress log or index was modified by this audit.
