# The original Hamiltonian and its actual time in all-mode canonical coordinates

2026-10-13. This uses the additional small nonzero background domain of [ALL_MODE_SMALL_BACKGROUND.md](ALL_MODE_SMALL_BACKGROUND.md), the original weak-canonical state inverse of [SYMPLECTIC_LIOUVILLE_AVERAGING.md](SYMPLECTIC_LIOUVILLE_AVERAGING.md), and the previously established physical Hamiltonian/Poisson correspondence. It gives the original Hamiltonian's action-only representation and actual original-time trajectories on a specified infinite-dimensional spectral decay domain. It does not assert rough-E Cauchy well-posedness or a fixed bounded-angle chart invariant under time. The full chain still requires independent review and a completion audit.

## 1. The original scalar Hamiltonian is analytic on E

Use lattice period M, spatial period L, h>0, c≠0, S=hMc/8 and B=γ/(2c). Let β=h²/32 and R be the original finite skew lattice matrix. The physical Hamiltonian from the [original field derivation](../dlw_general_field_20261006/RESEARCH_NOTES.md) is

\[
K_B=h\sum_j\int_0^L
\left(\frac12U_j^2w_j+\frac\beta3w_j^3+w_jU_{j,x}
+\frac12w_j(Rw_x)_j-\gamma U_j\right)dx.
\tag{1}
\]

Keep its original normalization; no multiplication of the time generator is made. The [exact physical free-field inverse](../dlw_general_field_20261006/GENERAL_PERIOD_FREE_FIELD_POISSON.md) gives, for m=M−1,

\[
d_m=S-\sum_{j<m}d_j,\quad
b_m=B-\sum_{j<m}d_j-S^{-1}\sum_{j<m}d_jq_j,
\]
\[
b_j=b_m+q_j+d_j+2\sum_{j<k<m}d_k+d_m,
\qquad U_j=2b_j,\quad w_j=8d_j/h.
\tag{2}
\]

These formulas involve only the fixed nonzero denominator S. On E=(L²₀)^m_q×(H¹₀)^m_d, with background constants added, d and w lie in H¹⊂L∞ and b,U lie in L². The maps to those spaces are continuous polynomials. Interpret the derivative term by periodic integration by parts:

\[
\int w_jU_{j,x}=-\int w_{j,x}U_j.
\tag{3}
\]

Now U²w is integrable by ||w||∞||U||₂², wxU by ||wx||₂||U||₂, and w(Rwx) by the same L² pairing; w³ and γU are also integrable. Each term is a continuous polynomial on the complexified E. Hence K_B is genuinely holomorphic there and agrees with the original smooth-field functional. This does not yet make its Hamilton vector field bounded on E: taking the original derivative Poisson operator can lose spatial derivatives.

## 2. Invariance and full action-only representation

For smooth original fields the actual trace hierarchy and its physical bridge give the commutation of K_B with every reciprocal action. This uses the original established relation of K to the first spectral invariant and translation momentum, not a new Hamiltonian. The bounded action flows preserve spatial smoothness in a common E window. K_B is continuous on E by §1; approximating a rough field by smooth periodic fields and passing to the action-flow limit therefore proves invariance on the full E neighborhood.

On the all-mode canonical domain there is no low residual coordinate. Write Jα=vα+vα−=dαAα, dα=Lωαγα. The established Banach-valued invariant-descent theorem consequently supplies

\[
\boxed{\quad K_B=k_B(J),\qquad k_B:\ell^1\supset V\to\mathbb C
\text{ holomorphic}.\quad}
\tag{4}
\]

The function is defined on an open invariant-base neighborhood, with additive background constants retained or subtracted consistently. On a smaller ball its derivative is bounded in (ℓ¹)*=ℓ∞. Thus

\[
\Omega_\alpha(J;B)
=d_\alpha\partial_{J_\alpha}k_B(J),\qquad
|\Omega_\alpha(J;B)|\le C_B\langle n\rangle^2.
\tag{5}
\]

This is an actual nonlinear frequency function, not just the background Hessian. No explicit elementary closed formula for kB is asserted; it is defined by the proved actual canonical state reconstruction and the unique analytic invariant descent.

## 3. Translation and the external B parameter

The original momentum P=hΣ∫p_js_j generates negative spatial translation in the physical variables. Its dependence on free fields is analytic on E by their affine p,s relation (or by the corresponding bilinear q,d expression up to fixed-mean constants).

The symplectic Liouville chart can be chosen spatially equivariant. Indeed the actual action flows commute with spatial translation, the physical Euler field commutes with this linear translation action, and so do its averaged field, contraction flow and limiting map. The fixed background spectral linear map sends translation to Fourier phases. With the stated Born convention,

\[
T_s(v_\alpha^+,v_\alpha^-)
=(e^{ik_ns}v_\alpha^+,e^{-ik_ns}v_\alpha^-).
\]

Contracting the negative-translation vector field with the exact canonical form yields

\[
\boxed{\quad P(J)=P(0)+\sum_\alpha\frac{-ik_n}{d_\alpha}J_\alpha.\quad}
\tag{6}
\]

The coefficient sequence is bounded, with O(1/|n|) size, so this is a legitimate ℓ¹ analytic functional. Its normalization is fixed by the ORIGINAL translation generator.

To retain external B(t), write U=U⁰+2B and γ=2Bc. The mean closure gives ΣU⁰w=0 and Σw=Mc. Substitution in (1), with derivatives in x unaffected by B, gives

\[
K_B=K_0+2BP-2B^2cMhL,
\tag{7}
\]

using ΣU⁰=−Σps/c. Fixed-mean conventions for P may add another scalar-only function of B, which has no Hamilton field. Therefore, on the centered source coordinates, the true instantaneous frequencies are

\[
\Omega_\alpha(J;B(t))
=\Omega_\alpha^0(J)-2ik_nB(t),\qquad
\Omega_\alpha^0=d_\alpha\partial_{J_\alpha}k_0.
\tag{8}
\]

Real B contributes the expected translation phase. Reconstructing the physical U through (2) retains its explicit 2B(t) term and its derivative when B varies. No B_t=0 constraint, auxiliary clock, or time rescaling is introduced. For classical reconstruction one may take B real C¹ on the time interval; the centered phase formula only needs its time integral.

## 4. Explicit original-time trajectories

Given initial canonical data v(0) in the domain specified next, set Jα=vα+(0)vα−(0) and

\[
\tau_\alpha(t)=t\Omega_\alpha^0(J)-2ik_n\int_0^tB(s)ds,
\]
\[
\boxed{\quad
v_\alpha^+(t)=e^{\tau_\alpha(t)}v_\alpha^+(0),\qquad
v_\alpha^-(t)=e^{-\tau_\alpha(t)}v_\alpha^-(0).
\quad}\tag{9}

Every Jα and Aα is constant. Whenever this sequence curve is differentiable in ℓ², direct contraction with Σdα⁻¹dvα+∧dvα− gives dKB for all ℓ² test vectors. The series identity is justified by ∂JkB∈ℓ∞ and the ℓ² pairing. Pulling back through the actual symplectic inverse gives

\[
\iota_{\dot x(t)}\Omega_{\rm physical}=dK_{B(t)}.
\tag{10}
\]

On the smooth fields obtained below, the original derivative Poisson operator applied to the variational gradient is a smooth mean-zero vector. It satisfies the same identity (10), by the established physical Poisson correspondence. Weak injectivity then identifies it with xdot. Thus (9) reconstructs actual original physical solutions, not merely abstract isospectral paths.

## 5. A nonempty infinite-dimensional two-sided time domain

Fix a sufficiently small ℓ¹ action ball where (5) holds for B=0, with constant C. For σ>0 define the Gaussian spectral Hilbert space

\[
\|v\|_\sigma^2
=\sum_\alpha e^{2\sigma\langle n\rangle^2}
(|v_\alpha^+|^2+|v_\alpha^-|^2).
\tag{11}
\]

Choose any finite T with CT<σ. Take initial data in a sufficiently small ball of this Hilbert space so that its ℓ² norm and its action sequence lie in the canonical and action domains. For real B the translation factor in (9) has modulus one. Equations (5) and (9) give, for |t|≤T,

\[
\|v(t)\|_{\sigma-C|t|}\le\|v(0)\|_\sigma.
\tag{12}
\]

The small initial bound consequently keeps the whole trajectory in the same canonical ℓ² neighborhood. A positive margin σ−CT makes every polynomially weighted derivative summable; v(t) is continuously differentiable in ℓ² (and in every fixed Fourier Sobolev space), and spatially smooth. The trajectory depends analytically on initial spectral data into weaker Gaussian spaces with a strictly positive margin, by the analytic frequencies and locally uniform exponential bounds. Reality-compatible initial data remain real under the original conjugation pairing.

Spatial equivariance of the actual canonical inverse supplies smooth physical reconstruction: the translation orbit of a rapidly decaying v is differentiable to every order as an ℓ²-valued map, and composition with the analytic inverse gives all physical spatial derivatives in E. These are the same reconstructed fields at every order, not separate Sobolev inverses. The argument applies uniformly along (12), so (10) is a classical smooth-field identity on the entire time interval. Spatial analyticity also follows from a small complex translation strip, although Gaussian Fourier decay of the physical field itself is not claimed.

The data ball in (11) is infinite-dimensional and allows every Fourier channel to be nonzero. Its reconstruction is a specified subdomain of the general-field neighborhood, not a finite-gap or soliton ansatz. It is not E-open, and (12) is a loss-of-Gaussian-radius statement, not rough-E Cauchy stability. For a fixed σ, the permitted T is limited by the frequency bound and the chart size.

## 6. Angles, linearization, and topology

On every nonzero coordinate pair, continue a logarithm along the interval in (9). The lifted angle satisfies exactly

\[
\theta_\alpha(t)=\theta_\alpha(0)+\tau_\alpha(t),
\qquad A_\alpha(t)=A_\alpha(0).
\tag{13}
\]

For constant B this is linear motion with constant original-time frequencies. For external B(t), its additional term is precisely the known spatial translation. The Cartesian formula (9) is single-valued and valid without logarithm choices.

The local simultaneous logarithmic chart previously defined in bounded relative angles need not contain this entire trajectory, since Ωα can grow like n². Equation (13) is a coordinatewise continued lift; equivalently, use Cartesian coordinates and a family of local angle charts along the trajectory. One must NOT claim that replacing the angle norm by sup|θα|/n² automatically creates an injective Banach logarithmic chart: its 2πi period lattice accumulates at zero in that norm. This issue does not affect the actual sequence flow or physical reconstruction in (9)–(12).

## 7. Current theorem and audit still needed

On the stated small nonzero uniform backgrounds, the combined construction now gives all-mode original weak-canonical state coordinates, a complete action-only scalar Hamiltonian, and explicit original-time solution formulas on a nonempty infinite-dimensional Gaussian spectral domain, with the original real structure and external B bridge retained. All these statements depend on the earlier actual spectral, exact-period, bounded-profile and symplectic-limit proofs.

Before treating the complete research objective as achieved, the entire dependency chain and the precise original Hamilton/time normalizations must undergo a fresh completion audit; no finite algebra check substitutes for it. Arbitrary larger nonalias backgrounds, a rough-E Cauchy theory and a globally single bounded-angle time chart are not consequences of this local theorem. The research goal remains ACTIVE pending that audit and any resulting repairs.

Subsequent disposition: the branch-internal audit is recorded in [COMPLETION_AUDIT.md](COMPLETION_AUDIT.md), §§12–15, and the current result in [LOCAL_ACTION_ANGLE_THEOREM.md](LOCAL_ACTION_ANGLE_THEOREM.md). The internal pass is complete for that restricted local proof draft; independent full review remains outstanding. Analytic dependence into a fixed weaker Gaussian space uses a strictly positive extra radius margin and, if needed, a smaller initial ball.
