# Independent audit: nonlinear residual information cannot bound the maximum error

2026-10-26. Independent mathematical/algebraic audit of `../../reference_certificate_20261024/RESIDUAL_NO_GO_CLOSURE.md` (path relative to the parent stability directory). This is an independently reviewed proof draft, not proof-assistant verification. The theorem below concerns a specified information model. It does not prove that all conceivable certifications of a particular exact datum are impossible.

## 1. Audited statement, including the stronger quantifiers

Let `x` be periodic with length `L>0`, `z∈[0,Z]`, and `T>0`. Use the moving coordinate `X=x−4t`. Define the full nonlinear physical residuals

\[
\begin{aligned}
\mathcal R_1(u,v)&=u_{zt}+v_{XX}+\partial_X(uu_z),\\
\mathcal R_2(u,v)&=v_t+u_{XXz}+\partial_X(uv)-4u_X.
\end{aligned}
\]

Fix one real periodic exact target `(U,V)` on this cylinder. Assume enough regularity for all displayed derivatives to be continuous; assume `U,U_X` are smooth enough in `(X,t)` on each fixed interior transverse slice for the usual uniformly parabolic evolution kernel below to exist and be continuous for positive elapsed time. A sufficient convenient assumption is smoothness in `(X,t)`, with bounded `U_z,U_Xz,V,V_X,U_zX` on the closed cylinder. Infinite transverse smoothness is not needed.

Let `J` be any nonempty open interval compactly contained in the requested transverse observation region. Fix an arbitrary finite set of space-time sample points (or finitely many full transverse grid lines). Then:

> For every residual tolerance `r>0` and every terminal discrepancy `M>0`, there exists a real periodic sufficiently regular approximate field `(u_app,v_app)` with exactly the target's full initial functions, exactly the target's prescribed boundary traces, and the target's values and all existing local derivatives at every specified sample point, such that
> \[
> \max_{i=1,2}\|\mathcal R_i(u_{\rm app},v_{\rm app})\|_\infty\le r,
> \qquad
> \|v_{\rm app}(T)-V(T)\|_{L^\infty(X\times J)}=M.
> \]

The approximate field can additionally agree with the target in an open neighborhood of both transverse endpoints and for a fixed initial time interval. Thus exact initial derivatives and boundary derivatives are preserved too.

Consequently, over the class with **no additional quantitative amplitude, derivative, spectral-tail, or transverse-resolution restriction**, the supremum of terminal maximum error compatible with an arbitrarily small positive full residual budget and finite-grid equality is infinite. There is no finite universal error bound based only on those inputs and fixed target constants.

If one imposes a fixed amplitude cap on the candidates, the same construction at any one fixed small `M>0` still excludes every error modulus `ω(r)→0`. An amplitude cap allows trivial finite bounds; the stronger “no finite bound” formulation must not be asserted under that extra input.

## 2. Exact transformation and nonlinear subtraction

For any field put

\[
a=u_z+v,\qquad b=u_z-v,
\]
\[
R_a=a_t+a_{XX}+\partial_X(ua)-4u_X,
\quad
R_b=b_t-b_{XX}+\partial_X(ub)+4u_X.
\]

Direct differentiation gives

\[
\mathcal R_1=(R_a+R_b)/2,\qquad
\mathcal R_2=(R_a-R_b)/2.
\]

Let `A0=U_z+V`, `B0=U_z−V`. For variations `d=δu` and `e=d_z=δv`, one has `δa=2e`, `δb=0`. Therefore

\[
\begin{aligned}
\Delta R_a={}&2e_t+2e_{XX}
 +\partial_X(2Ue+dA_0+2de)-4d_X,\\
\Delta R_b={}&\partial_X(dB_0)+4d_X.
\end{aligned}
\]

The term `2∂X(de)` is retained. The argument therefore applies to the full nonlinear residual, not just its derivative at the target. These identities were checked independently by symbolic expansion in `no_go_algebra_audit.py`.

## 3. High-frequency terminal profile

Choose `z*∈J` away from the finite collection of sample transverse coordinates, and put `U*(X,t)=U(X,z*,t)`. For `k_n=2πn/L`, solve

\[
\phi_{n,t}=-\phi_{n,XX}-\partial_X(U_*\phi_n),
\qquad \phi_n(X,T)=\cos(k_nX).
\]

With `τ=T−t`, this is the ordinary forward uniformly parabolic equation

\[
\psi_\tau=\psi_{XX}+\partial_X[U_*(X,T-\tau)\psi].
\]

Maximum principle and finite-time smoothness give

\[
\|\phi_n\|_\infty\le C:=e^{T\|U_{*,X}\|_\infty},
\qquad W_n:=\|\phi_{n,X}\|_\infty<\infty.
\]

For `t≤T/2`, the elapsed forward parabolic time is at least `T/2`. The kernel `K(X,t;Y,T)` is continuous on the compact set `(X,t,Y)∈T_L×[0,T/2]×T_L`; hence the set of functions `Y↦K(X,t;Y,T)` is compact in `L¹(Y)`. Its Fourier coefficients tend to zero uniformly on that compact set (finite-net approximation plus the ordinary Riemann–Lebesgue lemma). Thus

\[
\alpha_n:=\sup_{0\le t\le T/2}\|\phi_n(t)\|_\infty\longrightarrow0.
\]

This uses only well-posedness of a scalar forward parabolic problem. It assumes no forward well-posedness for the nonlinear DLW initial-value problem. No uniform estimate on `W_n` is required: the transverse width will be chosen after `W_n` is known to be finite.

## 4. Narrow transverse support preserves exact data and samples

Take a fixed smooth real compactly supported `F` on `(0,1)`, rescaled so that `f=F'` satisfies `||f||∞=1`; by the fundamental theorem of calculus, `||F||∞≤1`. Choose a smooth cutoff `χ(t)` that is zero for `t≤T/4`, equals one for `t≥T/2`, and satisfies `0≤χ≤1`. Let `H=||χ'||∞`.

For a width `δ>0` with `[z*,z*+δ]⊂J` and avoiding all sample transverse coordinates, set

\[
d_n=M\delta F\!\left(\frac{z-z_*}{\delta}\right)\chi(t)\phi_n(X,t),
\quad
e_n=M f\!\left(\frac{z-z_*}{\delta}\right)\chi(t)\phi_n(X,t).
\]

Then `e_n=∂z d_n` exactly; `δb=0` is an exact identity. Both perturbations vanish near both transverse boundaries, near all the selected transverse sample lines, and on the initial time interval. At `t=T`, the product separates, `||f||∞=||cos(k_nX)||∞=1`, so `||e_n(T)||∞=M`.

The terminal maximum holds over the full periodic `X` interval. For an observation interval in `X` with nonempty interior, the same equality holds for all sufficiently large `n`, since a cosine extremum then lies in that interval.

## 5. Full residual estimate and explicit parameter selection

Set the fixed finite background constants

\[
P=\|U_z\|_\infty,\ Q=\|U_{Xz}\|_\infty,
\ M_a=\|A_0\|_\infty,\ M_b=\|B_0\|_\infty,
\ N_a=\|A_{0,X}\|_\infty,\ N_b=\|B_{0,X}\|_\infty.
\]

Cancellation with the scalar terminal equation and the inequalities `|U−U*|≤δP`, `|U_X−U*X|≤δQ` give

\[
\max_i\|\Delta\mathcal R_i\|_\infty
\le MH\alpha_n+\frac{M\delta}{2}K_n(M),
\]
\[
K_n(M)=(2Q+N_a+N_b)C
 +(2P+M_a+M_b+8)W_n+4MCW_n.
\]

The final term includes the entire quadratic perturbation product. The factor `||F||∞≤1` has merely been enlarged to one.

For given `r>0,M>0`, first choose `n` so large that `MHα_n<r/2`. Let `d_J>0` be an available width staying in `J` and away from the finite sample lines. Then choose

\[
0<\delta<\min\left(d_J,\frac{r}{M[1+K_n(M)]}\right).
\]

The second term is strictly less than `r/2`, proving the theorem. Constants belonging to the target are held fixed throughout. Only the approximate field's carrier and width vary. The width may depend on `M`; that is legitimate in the claimed `∀r∀M∃app` quantifier order.

For a fixed `M`, taking `n→∞` and `δ_n≤1/[n(1+W_n)]` recovers the original no-vanishing-modulus theorem. Thus the published draft's original statement is valid under the explicit parabolic-kernel/background hypotheses.

## 6. Exact scope for the active independently perturbed problem

The theorem applies to the exact independently perturbed A/D/Gaussian/sine target **if such a target exists with the stated regularity**. It preserves whatever exact initial functions that target has, including the specified independent physical-field perturbation. It does not rely on a zero background or a heat/Laplace compatibility relation.

The interior construction does not actually require `U(X,0,t)=0`: it preserves any prescribed lower trace, since the variation vanishes near the boundary. This extends the mechanism to the soliton boundary traces. The zero-trace assumption in the earlier draft was convenient for writing an integral reconstruction, but is unnecessary for the local subtraction proof.

It establishes that small full residuals, exact initial/boundary data and any finite family of point/grid observations cannot, by themselves, certify a maximum-norm reference. It neither proves that the active independently perturbed target exists nor that it fails to exist. It does not exclude certification using a proved quantitative tail/derivative condition, an exact integrable construction or another substantially stronger information source.

It also does not prove that the existing numerical candidate has a particular actual error. The bad approximate field is constructed existentially; no claim identifies it with that candidate. The construction uses unlimited transverse concentration and `X` frequencies. Any admissible class forbidding those requires its own analysis.

## 7. Audit outcome

- Exact moving-coordinate residual identities: passed.
- Exact full nonlinear subtraction, including quadratic term: passed.
- Uniform Fourier decay of the positive-time scalar parabolic kernel: valid with the stated kernel regularity.
- Preservation of entire initial functions, endpoint traces and finite point/grid information: passed.
- Original no-vanishing-error-modulus statement: valid.
- Stronger `∀r>0∀M>0` unbounded-error statement: valid without candidate amplitude/derivative/tail caps.
- Unconditional impossibility of every exact-data certification method: not established and not implied.

The remaining positive route must supply additional structural or tail information about the actual target and candidate. Merely making a full residual, a numerical grid gap or a floating-point error smaller cannot close that missing condition.
