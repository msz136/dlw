# Independent perturbation audit addendum

2026-10-26. Read-only mathematical and numerical review of the independent-physical-field experiment. This supplements `AUDIT_DESIGN.md`. The audit code writes only its own `audit_four_case.json`.

## 1. Mixed-time existence bound: passed

For the Fourier trajectory norm

\[
 \|f\|_\rho=\sum_n e^{\rho|\xi_n|}\sup_{z,t}|f_n(z,t)|,
\]

the sum/sup order used in `certificate_design/INDEPENDENT_PERTURBATIONS.md` is appropriate. For each coefficient, the differentiated heat integral has multiplier at most

\[
 \int_0^T |\xi|e^{-s\xi^2}\,ds
 =\frac{1-e^{-T\xi^2}}{|\xi|}\le\sqrt{T/2}.
\]

The last inequality follows from `(1-exp(-x))^2 <= x/2`: the difference is zero at zero and its derivative is `2(exp(-x)-1/2)^2 >= 0`. Taking the supremum in time coefficient by coefficient, then summing, preserves this bound. The Fourier norm is a Banach algebra. On `0 <= z <= 4`, `u=(1/2) integral_0^z(A-B)` gives `||u|| <= 2||(A,B)||`. Consequently the quadratic map bound `2hR^2` and Lipschitz bound `4hR` are valid.

The `.3` datum / `.4` ball estimates at `T <= .02` give image norm at most `.332` and contraction factor at most `.16`. This certifies the specified mixed-time problem. It does not solve the initial matching equation for the independently perturbed IVP. The stable-data norm estimates in `independent_constants.py` use valid conservative Gaussian and sinusoidal bounds; no terminal datum or matching bound is supplied by those estimates.

## 2. Nonzero-base smoothing: passed with stated hypothesis

Let the known mixed solution have trajectory norm at radius `rho+sigma` at most `R`, and keep `H=B(0)` fixed. For the derivative with terminal datum `a(T)=g`, initial datum `b(0)=0`, use the variable radius

\[
 r(t)=\rho+\sigma(1-t/T).
\]

For the backward component, an interval of length `s` has multiplier bounded by

\[
 e^{-s\xi^2+\sigma s|\xi|/T}
 \le e^{\sigma^2/(2T)}e^{-s\xi^2/2}.
\]

Its integrated derivative bound is therefore `h_sigma = sqrt(T) exp(sigma^2/(2T))`. The forward component needs no radius gain and is bounded by the same constant. The terminal forcing has norm at most `exp(sigma^2/(4T)) ||g||_rho`. Linearization of the quadratic term gives `4 R h_sigma`, hence

\[
 \|DF_H\|_{\rho\to\rho+\sigma}
 \le\frac{e^{\sigma^2/(4T)}}{1-4R\sqrt T e^{\sigma^2/(2T)}}
 \le 1.744115
\]

for `T=.01`, `rho=sigma=.1`, `R=.4`. This is conditional: the actual perturbed benchmark has not been enclosed in the required ball at radius `.2`.

No compactness in the whole `(x,z)` function space follows merely from this smoothing; arbitrary low-x-mode z dependence remains. A valid way to show the same-space derivative is not bounded below is to repeat the radius argument with input radius `rho-sigma` and output radius `rho`. For a high-x single mode `g_N` normalized in `W_rho`, its weaker norm is `exp(-sigma|xi_N|)`, so

\[
 \|DF_H g_N\|_\rho\le C e^{-\sigma|\xi_N|}\longrightarrow0.
\]

Uniqueness of the linear mixed problem identifies the operators on the overlap. This establishes absence of a bounded same-space inverse under the hypotheses; it does not establish nonexistence for particular perturbed initial functions.

The first-Born sideband formula in `NONZERO_MATCHING_DERIVATIVE.md` also passes. With `p=k+q`, the integrand in the amplitude derivative is

\[
 ip c_q e^{-Tk^2}\left[-(f\phi+f'I\phi)e^{-2kqt}
                  +2f\phi e^{-2q(k+q)t}\right].
\]

Integration gives its two stated `J` terms. At `z=2`, `f=phi=1`, `f'=0`, inverse-heat preconditioning yields asymptotic `i c_q exp(T(2kq+q^2))/(2q)`. This is the derivative in background amplitude at zero, not a conclusion about any fixed nonzero amplitude.

## 3. Four-case stored arrays: passed

`audit_four_case.py` independently checks all four `A,D,Gaussian,Sinusoidal` NPZ files against their JSON metadata. It recomputes physical `v=diff(u)/h+average(w)`, the exact intended independent initial perturbations, the terminal native-site maxima, the saved terminal arrays, full-period discrete L2 gains, and 8x Fourier-interpolation peaks. All asserted comparisons pass. All artifact and listed source hashes match. The baseline agrees bit-for-bit with the previously saved RK4 baseline in every case. The maximum initial physical-field mapping residual is at roundoff level (at most `1.0587911840678754e-22`).

These are valid diagnostics of the selected finite-grid nonlinear trajectories. The experiments do not supply a continuous nonlinear reference certificate, an existence theorem for the perturbed IVP, or a time-discretization error enclosure. The status `certificate=false`, with null reference bounds, is correct.

## 4. Exact constant-background control and domain geometry

The production natural Centered-SD linearization at `(u,w)=(0,4)` simplifies in `X=x-4t`. Write `p=Delta_h u` and `v=p+M_-w`. The exact linear equations are

\[
 p_t=-v_{XX},\qquad v_t=-p_{XX},\qquad u_{\rm lower}=0.
\]

For one x frequency `kappa`, put `s=kappa^2 T`. Then

\[
 \begin{pmatrix}p(T)\\v(T)\end{pmatrix}
 =\begin{pmatrix}\cosh s&\sinh s\\\sinh s&\cosh s\end{pmatrix}
 \begin{pmatrix}p(0)\\v(0)\end{pmatrix},\qquad
 u(T)=\cosh(s)u(0)+\sinh(s)J_hv(0),
\]

where `J_h` is the h-weighted prefix sum over edges. The x carrier is advected by `4T`. This is an exact finite-h linear control for the current closure. The continuum control has `Delta_h` replaced by `partial_y` and `J_h` by the lower-boundary integral.

For a v-only perturbation with envelope `phi(y)=sin^2(pi(y-yL)/L)`,

\[
 J\phi(y)=\frac{y-y_L}{2}-\frac{L}{4\pi}
                    \sin\frac{2\pi(y-y_L)}L.
\]

The native-site maximum of its cross-u response depends strongly on the y interval and observation window. At `T=.01`, `kappa=pi/2`, the independently recomputed comparisons are:

| Background | Observed cross-u gain | Constant finite-h control | Observed/control |
|---|---:|---:|---:|
| A | 0.224532876 | 0.222478086 | 1.009236 |
| D | 0.973820818 | 0.971576991 | 1.002309 |
| Gaussian | 0.049297893 | 0.049293801 | 1.000083 |
| Sinusoidal | 0.049299179 | 0.049293801 | 1.000109 |

The continuous native-site controls are `0.222476466`, `0.971576705`, and `0.049291305` for A, D, and either non-soliton respectively. Here `L=19.9,79.9,4`, maximum observed u-site `y=4.95,29.95,1.8`, and maximum primitive `9.03354235,39.45037185,1.99836316`. The same fixed native x lattice contributes `max|cos(kappa(x-4T))|=cos(.02*pi)` at this time. This explains most of the D-versus-A cross-u difference through the transverse primitive and interval geometry. Calling that difference evidence of a stronger two-soliton interaction would be unsupported.

The same control does not explain all cross-field effects on solitons. For a u-only perturbation the observed cross-v gains are `.09186346` (A) and `.10277999` (D), whereas the constant finite-h controls are `.00388696` and `.000968342`. Those differences require the variable wave background. Gaussian/sinusoidal u-only cross-v gains are close to the constant control (`.01934814`, `.01933150`, versus `.01926320`).

For RK4, replace `exp(T lambda_+)` and `exp(T lambda_-)` by `R(dt lambda_+)^100` and `R(dt lambda_-)^100`, with `lambda_+=kappa^2-4i kappa`, `lambda_-=-kappa^2-4i kappa` and the usual fourth-order stability polynomial. The computed constant-control field differences from exact-in-time values are below `5e-21` in absolute units for amplitude `1e-6`; these ordinary floating-point evaluations are not outward-rounded enclosures.

## 5. Suitable manuscript scope

The constant-state linear formulas, the exact current-lattice spectrum, and the stored finite-grid response data can support the stability subsection. A precise introduction is: “We measure the response of the fully discrete Centered-SD evolution to independent perturbations of the initial physical fields.” A separate constant-state result can explain short-x-wave sensitivity and the cross-field primitive.

The tables and curves should be called perturbation amplitudes or gains, not errors against a certified perturbed continuous solution. General propagator bounds cannot be inferred from the real parts `+/- xi^2` alone because the repeated lower-triangular lattice blocks may be nonnormal. The matching theorem is useful progress toward continuous certification; exact initial matching and infinite-tail bounds remain unresolved for the selected independent perturbations.

## 6. Final correction/tail review and manuscript normalization

The added first initial-data correction `(D11a)` passes. Starting with the initial variations `a0=alpha exp(k^2 t)` and `b0=beta exp(-k^2 t)`, the coefficient of `lambda epsilon` in `ubar*a+w*Abar` is

\[
 c_q\left[-(f\alpha+f'I\alpha)e^{(k^2+q^2)t}
       +2f\alpha e^{(k^2-q^2)t}
       +f'I\beta e^{(q^2-k^2)t}\right].
\]

Forward integration of the unstable branch with zero initial correction gives exactly the sign, factor `-ip exp(Tp^2)`, and three `J` arguments in `(D11a)`. An independent 100-digit quadrature of this Duhamel integral reproduces all four sine amplitudes in the note; values are stored in `audit_matching_correction.json`.

For each of its three terms, `exp(Tp^2)|J(d)| <= T exp(T(k+|q|)^2)`. Multiplying by the Gaussian coefficient and analytic weight yields the stated majorant. The transverse sum of absolute coefficients is at most `3+4kap` for v perturbations (`|Iphi|<=2`) and `5kap` for u perturbations (`|phi'|<=kap`, `Iphi'=phi`), where `kap=pi/4`. The two half-amplitude real-cosine carriers sum to one; the two signs of q give the remaining factor 2 in the code. Both the Gaussian amplitude `.05` and physical perturbation amplitude `1e-6` are included. The adjacent-majorant ratio decreases with q; its value at n=129 is approximately `.08344163457`. The geometric bounds are therefore valid:

\[
 1.182671159870137\times10^{-78}\quad(v),\qquad
 7.562108147324024\times10^{-79}\quad(u).
\]

These certify only the omitted Gaussian q-tail in the first matching correction. They do not bound the sum of higher corrections or a full perturbed solution error. The note states this scope correctly.

The stripped `section44.html` and `section55.html` were reviewed. Section 5.5 consistently divides its maximum responses by the prescribed `epsilon`, while its L2 pair gain and the quoted 8x interpolation gain use the measured initial norms/peaks. Thus the Gaussian v-only maximum `.99683` is correct in that table even though the earlier initial-peak-normalized gain is `.99837`. The A/D constant controls and percentage comparisons use compatible normalizations.

One small precision amendment was requested for Section 4.4: the displayed propagator with factor `exp(-ic xi t)` and later growing eigenvalue `xi^2-4i xi` must explicitly be restricted to non-Nyquist modes. At the special Nyquist mode of the implemented first derivative, the advection multiplier is zero, so that factor is 1 and the growing eigenvalue is `xi^2`. The preceding real-branch statement already handles this correctly.
