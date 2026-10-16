# General M weighted actual gap fields: independent audit

2026-10-11. Independent hand audit by `all_m_holonomy_image_audit`. No machine checks were run. All previously frozen files were left unchanged.

Read dependencies:

- `all_m_actual_trace_vector_akns_mod_frame_recovery_proof_20261011.md`, especially §5.1: actual normalized trace fields and the complete physical graph reconstruction.
- `general_m_actual_high_frequency_riesz_gap_lemma_20261011.md`, §§2–5: actual uniform windows, moving holonomy templates and Q in ℓ² of disk functions. Frozen SHA256: `88652AEFD148F0DC803732AAE7A2038891B159B49C896F424978475209DA9C46`.
- `general_m_fixed_gap_balanced_hamilton_flow_20261011.md`, read in full: fixed finite gap/center fields on the genuine balanced source, original J identification and weak Ω identity. Read-back SHA256: `83E49D069021DB00AEACF663B86E54F60D3221B6A703CBFDBD0648F00CAEE092`.
- `general_m_gap_frequency_weighted_hamilton_sequence_20261011.md`, §§1–9 read in full, including the final row/column correction; §§7–8 reread after the profile notation was changed to θ/ϑ to distinguish it from the original Casimir c. Final read-back SHA256: `008DED2A39A8A15DD7F677FDB5B6CE3EB87595ACE940ECA21FB1275A0C6FD0BA`.

The fixed-gap balanced proof passes independently. The weighted sequence argument below also passes with the explicit normalization and fixed-H interpretations recorded here.

## 1. Domain, normalization and the frequency-uniform trace estimate

Fix M≥2, m=M−1, real S=Mδ≠0, the free component means, and a nonalias uniform background. On a sufficiently small complex balanced source ball

\[
X_0=(L^2_0)^m_q\times(H^1_0)^m_d,
\]

the actual mean-normalized coefficient map \(\mathcal P(z)=(a,b,H)\), its core inverse Π and its finite physical graph are analytic. The current external B section and the centered spectral parameter are retained.

The trace-normalized fixed-principal connection is

\[
\bar A_\lambda=\lambda J_*+Q(z,x),\qquad
J_*=E_{00}-I_M/M=J_*^*,
\tag{1}
\]

with a uniform L², hence L¹, bound on Q on this ball. The imaginary part of λ times J* generates a unitary propagator. Gronwall, applied after removing it, gives for each fixed strip \(|\operatorname{Re}\lambda|\le R\)

\[
\sup_x(\|Y_\lambda(x)\|+\|Y_\lambda(x)^{-1}\|)
\le C_R,
\tag{2}
\]

independently of Im λ. Duhamel supplies the analogous uniform bounds and local analyticity for source derivatives. Thus N=Y(L) and

\[
\bar W_{\lambda,r}=Y_\lambda N_\lambda^rY_\lambda^{-1}
=\begin{pmatrix}h&e\\f&K\end{pmatrix}
\]

have uniform sup bounds for the finitely many powers 1≤r≤M−1. For the actual traces \(F_r=r^{-1}\operatorname{tr}N^r\), the auxiliary canonical field at fixed H is

\[
Y_{F_r}=(e,-f,0),\qquad \|Y_{F_r}\|_{L^2_a\times L^2_b}\le C_R.
\tag{3}
\]

The W in (3) is normalized: its raw-block version must be multiplied by \(e^{-rL(\lambda+\operatorname{tr}H)/M}\). That factor is retained in the exact trace Hamiltonian identity, even though its modulus is bounded on this strip. Original χ frame conjugacy does not change these trace functions.

## 2. The graph reconstruction is bounded and has no spectral parameter

Let C be the full finite physical graph constraint, let P select the established m²-component transverse minor, and let

\[
\mathcal V_X=(aX,-Xb,[H,X]),\qquad
T_zX=P\,DC_z[\mathcal V_X].
\]

On a smaller source ball, Tz and DΠz are uniformly invertible. For an arbitrary ambient off-diagonal input w=(wa,wb,0), define the bounded linear reconstruction operator

\[
X_{\rm corr}(w)=-T_z^{-1}P\,DC_z[w],
\]

\[
\mathcal B_zw=(D\Pi_z)^{-1}
\bigl(P_0(w+\mathcal V_{X_{\rm corr}(w)})_a,
P_0(w+\mathcal V_{X_{\rm corr}(w)})_b\bigr).
\tag{4}
\]

It is analytic in z as an operator from the ambient L² pair to X₀ and is independent of λ. The established exact trace bridge says

\[
X_{F_r(\lambda)}=\mathcal B_z\bigl(\omega(\lambda)Y_{F_r(\lambda)}\bigr),
\qquad \omega(\lambda)=\frac{S^2-\lambda^2}{16S}.
\tag{5}
\]

Consequently

\[
\|X_{F_r(\lambda)}\|_{X_0}\le C(1+|\lambda|^2).
\tag{6}
\]

For arbitrary w, (4) need not make its entire ambient corrected triple tangent to all unused constraints. This causes no problem: the full graph tangency and actual Hamiltonian identity are already established for the weighted trace inputs in (5) and their contour combinations. In particular \(\mathcal B_zY_g\) by itself is not being declared an original Hamiltonian field.

## 3. Uniform fixed windows and finite gap/center fields

Let i=(ℓ,n), n≥N, index the actual uniform centers λᵢ, which are imaginary and satisfy \(\lambda_i=i\kappa_n+p_\ell+O(n^{-1})\). Take fixed λ circles Γᵢ of one sufficiently small radius. At the background, the normalized monodromy collision multipliers have a known frequency-dependent unit-modulus phase. The multiplier circles are centered at those respective multipliers; their radii and resolvent bounds are uniform.

One must not use a single unrotated circle around 1 for all trace-normalized N. The moving-template construction may use a circle around 1 only after its explicitly retained scalar normalization. The known phase rotates circles without changing the uniform norm estimates.

After shrinking the common source ball, Duhamel's uniform small-perturbation bound preserves all these multiplier circles. The characteristic determinant stays uniformly bounded away from zero on them. Newton's identities and their fixed multiplier-contour formulas therefore give a uniform bound for the finite coefficients dᵢ,r in

\[
dD_i=\sum_{r=1}^{M-1}d_{i,r}(\lambda,z)\,dF_r(\lambda,z).
\tag{7}
\]

The exact background exponent slope and the noalias gap give a uniform nonzero bound for Dᵢ on Γᵢ; a further uniform small source perturbation preserves it. Both actual roots lie in the fixed λ window, so their absolute center aᵢ obeys \(|a_i-\lambda|\le2r\) on its circle, independently of n. Thus the contour weights

\[
K_{g,i,r}=\frac{(a_i-\lambda)d_{i,r}}{2\pi iD_i},
\qquad K_{a,i,r}=-\frac{d_{i,r}}{4\pi iD_i}
\tag{8}
\]

are uniformly bounded. The fixed-gap balanced proof supplies the exact X₀-valued identities

\[
X_{g_i}=\sum_r\oint_{\Gamma_i}K_{g,i,r}X_{F_r(\lambda)}\,d\lambda,
\qquad
X_{a_i}=\sum_r\oint_{\Gamma_i}K_{a,i,r}X_{F_r(\lambda)}\,d\lambda.
\tag{9}
\]

Equations (6), (8) and the fixed contour lengths give

\[
\|X_{g_i}\|_{X_0}+\|X_{a_i}\|_{X_0}\le C(1+n^2).
\tag{10}
\]

This concerns the absolute actual center a. It does not supply the original Hamiltonian field of the separate holonomy eigenvalue needed to replace a by a relative center.

## 4. The refined canonical gap estimate requires fixed H

Use the established moving holonomy grid and its actual calibrated rank-two compression

\[
B_i(\zeta)=\operatorname{diag}(e^{L\zeta},1)+Q_i(\zeta),
\qquad (Q_i)_i\in\ell^2(A_r),
\tag{11}
\]

where Ar is the Banach space of matrix functions continuous on the closed disk and holomorphic inside it. The larger-disk Cauchy upgrade is part of the construction. H varies analytically with the source in (11), but when taking an auxiliary canonical a,b derivative it is held fixed. This fixes the holonomy grid, its slow eigenbasis and its scalar normalization during that derivative.

On the uniform ambient coefficient neighborhood,

\[
\|D_{a,b}Q_i\|_{\mathcal L(L^2_a\times L^2_b,A_r)}\le C
\tag{12}
\]

uniformly in i. This follows from the actual fixed-principal ODE derivative bound, followed by uniformly bounded Riesz, intertwiner and compression operations. The holonomy-calibrated full remainder is also analytic into ℓ²(Ar), so its derivative and coordinate restrictions have the required bounds. Freezing the background H₀ instead of using the current H would generally leave a constant slow-block tail; that replacement would invalidate (11).

The half-gap functional G of a two-dimensional disk matrix satisfies G(0)=DG(0)=0 at the uncoupled template. Uniform scalar analytic estimates give

\[
\|DG(Q_i)\|_{A_r^*}\le C\|Q_i\|_{A_r}.
\tag{13}
\]

Let Ygᵢ denote the auxiliary canonical field of the actual gap gᵢ with H held fixed. Composition of (12)–(13) yields

\[
\|Y_{g_i}\|_{L^2_a\times L^2_b}
\le C\|Q_i\|_{A_r}.
\tag{14}
\]

Hence the sequence of these fields belongs to ℓ² of the ambient L² pair. It is analytic there: the sequence DG(Qᵢ) is analytic into ℓ² of the disk-space duals, while the sequence of derivative operators in (12) is analytic and locally bounded in ℓ∞ operator norm; their coordinatewise composition is a bounded bilinear map into ℓ². One can equivalently use coordinate analyticity, the locally uniform ℓ² bound and Banach-valued holomorphy.

The absolute gap and the moving-grid half-gap coincide because a scalar normalization, similarity, and translation of the spectral coordinate do not change its two zeros' difference. Therefore the same contour chain rule at fixed H gives exactly

\[
Y_{g_i}=\sum_r\oint_{\Gamma_i}K_{g,i,r}Y_{F_r(\lambda)}\,d\lambda.
\tag{15}
\]

No assertion that H is an original physical Casimir is used. Only the auxiliary canonical bracket freezes H.

## 5. Exact weight division and the ℓ² balanced field sequence

Set \(\omega_i=\omega(\lambda_i)\). For sufficiently large n these constants are nonzero and \(|\omega_i|\asymp n^2\). On the fixed λ circle, write λ=λᵢ+ζ. The exact identity

\[
\frac{\omega(\lambda)}{\omega_i}-1
=-\frac{\zeta(2\lambda_i+\zeta)}{S^2-\lambda_i^2}
\tag{16}
\]

has modulus at most C/n. If the equivalent moving-holonomy contour is used instead, its bounded displacement from λᵢ gives the same estimate.

Combining (5), (9) and (15), and using the λ independence and linearity of Bz, gives the exact decomposition

\[
\boxed{\displaystyle
\frac{X_{g_i}}{\omega_i}=\mathcal B_z\left(Y_{g_i}+E_i\right),}
\tag{17}
\]

\[
E_i=\sum_r\oint_{\Gamma_i}K_{g,i,r}
\left(\frac{\omega(\lambda)}{\omega_i}-1\right)
Y_{F_r(\lambda)}\,d\lambda,
\qquad \|E_i\|_2\le\frac Cn.
\tag{18}
\]

The error sequence is analytic into ℓ² of the ambient L² pair: its coordinate maps are analytic and the uniform majorant C/n has a square-summable tail, giving locally uniform convergence of the finite coordinate projections. Equation (14) controls the other term. Therefore

\[
\boxed{\displaystyle
z\longmapsto\left(\frac{X_{g_{\ell n}}(z)}{\omega_{\ell n}}\right)_{
1\le\ell\le m,\ n\ge N}
\in\ell^2(X_0)
\quad\text{is analytic and locally bounded}.}
\tag{19}
\]

All finite graph corrections, including the physical H commutator, remain inside Bz. An ambient H-fixed estimate alone would not prove (19) without the exact original trace bridge (5).

## 6. ℓ² profiles give genuine original Hamiltonian flows

For a fixed profile \(\theta=(\theta_i)\in\ell^2\), distinct from the original Casimir c, define

\[
\mathscr H_\theta(z)=\sum_i \theta_i\frac{g_i(z)}{\omega_i},\qquad
\mathscr X_\theta(z)=\sum_i \theta_i\frac{X_{g_i}(z)}{\omega_i}.
\tag{20}
\]

The scalar sum is analytic: g is analytic into ℓ¹, the weight reciprocals are bounded, and θ belongs to ℓ∞. The field sum converges absolutely in X₀ by Cauchy–Schwarz and (19). It converges locally uniformly, as do its source derivatives on smaller balls by analytic Cauchy estimates. Both maps are jointly analytic in the ℓ² profile and the source.

For each finite partial sum, the fixed-gap balanced proof supplies the exact original weak symplectic identity. The same proof identifies the continuous weak form as

\[
\Omega(U,V)=-16\int_0^L
\left[(D_0^{-1}U_q)\cdot V_d+(D_0^{-1}U_d)\cdot V_q\right]dx,
\tag{21}
\]

on the fixed-mean X₀ leaf. Scalar analytic partial sums converge with their derivatives in X₀ dual norm; field partial sums converge in X₀; Ω is continuous. Passing to the limit proves

\[
d\mathscr H_\theta[V]=\Omega(\mathscr X_\theta,V),\qquad V\in X_0.
\tag{22}
\]

This is the actual original Hamiltonian identity. It requires no uniform estimate for an infinite sum of raw ODE adjoints or raw H¹ trace gradients. If a distributional original J-gradient is desired, its unique zero-mean representative is obtained from \(J^{-1}\mathscr X_\theta=-16\operatorname{offdiag}(D_0^{-1})\mathscr X_\theta\); identity (22) already establishes the Hamiltonian field.

The analytic Banach ODE theorem gives a genuine local X₀ flow for every real Hamiltonian component of (20), with the conjugate windows included for real and imaginary parts. A bounded profile d with an extra frequency weight is also allowed: \(\theta_{\ell n}=d_{\ell n}/n\) belongs to ℓ², giving \(\sum d_{\ell n}g_{\ell n}/(n\omega_{\ell n})\). The estimate does not justify arbitrary bounded profiles without that extra weight, or profiles of the unweighted g fields.

## 7. Smooth persistence and the scope of the result

The gap functions are translation invariant and the original J is translation-equivariant. Finite profile fields are therefore equivariant, and the locally uniform analytic limit in (20) remains equivariant. Its unique low-domain flow commutes with translations. For smooth initial data, the translation orbit is a smooth X₀-valued curve; composing it with the analytic low flow proves smooth persistence on the same low time window.

Finite profile fields and their source derivatives converge locally uniformly to the profile field. Their flows converge with each fixed order of source derivatives on a common smaller X₀ time window. Applying this to the smooth translation orbit gives convergence of the trajectories in every fixed spatial Sobolev order. Thus conservation of any fixed original Cⱼ on finite-profile smooth trajectories passes to the smooth profile trajectory without treating Cⱼ as a differentiable functional on all of X₀.

The conclusion is an ordinary balanced-low Hamiltonian flow with a specified weighted coefficient class. It does not supply a common internal presentation of all-hierarchy strong plots, a canonical norming/action inverse, class-kernel maximality, an arbitrary ℓ∞ profile theorem, or general M Liouville completeness.

## 8. Audit of the saved final statements

The final weighted main manuscript identified above passes the independent derivation in §§1–7 of this audit. Its corrected display \(W=\begin{pmatrix}c&e\\f&D\end{pmatrix}\), with e a row and f a column, agrees with the canonical field \((e,-f,0)\) and the exact physical trace bridge. The two previously frozen main dependencies retain the read-back hashes recorded above.

The main manuscript's infinite original gradient assertion has precisely the regularity warranted by the balanced field. Since \((\mathscr X_\theta)_q\in L^2_0\) and \((\mathscr X_\theta)_d\in H^1_0\), its representative is

\[
\widetilde\nabla\mathscr H_\theta
=-16\bigl(D_0^{-1}(\mathscr X_\theta)_d,
D_0^{-1}(\mathscr X_\theta)_q\bigr)
\in (H^2_0)^m\times(H^1_0)^m.
\tag{23}
\]

Equation (22) identifies this representative as the original variational gradient modulo the fixed means, and the original J maps it to \(\mathscr X_\theta\). This gain follows from the convergent actual balanced field; no infinite raw-adjoint H¹ summability claim is needed.

The finite trace and gap involution also passes to two ℓ²-profile Hamiltonians θ,ϑ through the continuous Ω form and the convergent field sums, giving \(\Omega(\mathscr X_\theta,\mathscr X_\vartheta)=0\). Differentiating their Hamiltonian identities and using constant, closed, weakly nondegenerate Ω gives a zero commutator of the analytic fields. Their local flows therefore commute wherever both compositions are defined. Real conjugate-paired truncations preserve the real source leaf.

The retained restrictions in the main manuscript are accurate: the crude absolute-center/gap estimate is quadratic in frequency, the square-summable normalized sequence is proved for gap fields, the stronger profile result includes the extra square-summable coefficient restriction, and smooth Cⱼ conservation uses smooth persistence and truncation. There is no missing use of an unproved uniform high-frequency raw gradient estimate or an arbitrary bounded-profile theorem. No mathematical blocker remains for these stated results.

Final notation reread, 2026-10-11: main §§7–8 now use θ/ϑ for the time profiles and leave the original Casimir c, including \(B=\Gamma/(2c)\), unchanged. This round changes notation and the cited final hash only; the mathematical statements and the independent PASS verdict are unchanged.
