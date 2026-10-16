# M=2 physical trace/action closure: independent chain review

2026-10-11. Mathematical review of the AKNS state bridge §4.4–4.5/D7, its independent audit §10–13, both saved physical trace identity scripts and JSON certificates, the infinite-product tangent caution, and the final physical trace Poisson proof §§1–8. The final readback also covers the same-strong-chart action genericity proof §§1–6 and the mixed construction §16.3–16.4. No existing or current checks were executed. Shared progress/index files were not edited.

## 1. Exact push-forward and the legitimate projection

The fixed-λ physical gradient includes the source-dependent shift ζ=λ−η. With ∂ζT=L⟨h⟩ and dη=(-2v/(SL),−2u/(SL)), the term −(∂ζT)dη cancels the mean-subtractions in the fixed-ζ gradients. The resulting exact potential field is

\[
D(a,b)X_{F_\lambda}=\omega_\lambda Y_{\lambda-\eta}
-\frac{\langle R_0\rangle}{8S}(a,-b),
\qquad \omega_\lambda=\frac{S^2-\lambda^2}{16S}.
\]

Here Y=(e,−f) is the auxiliary x-normalized canonical AKNS field. In the actual period-one KLTZ normalization, XstdT=(i/L)Y. The new proof's constant, signs, gradient correction, and projection all pass independent hand review. The saved 15- and 16-check certificates support only these finite identities.

Let G=(-w_n,z_n)_n and ϑ₀=(2i)⁻¹log(w₀/z₀). Then dϑ₀(G)=i and ΠV=V−dϑ₀(V)G/i is the genuine tangent projection to the central-angle section inside χ=0. Standard trace fields are tangent to χ because χ is action-only; G is tangent as well. The derivative of the state-dependent gauge normalization is precisely removed by Π. Therefore

\[
DR\,X_{F_\lambda}=\omega_\lambda\Pi Y_{\lambda-\eta}
\]

holds at the chosen representative. This does not identify the physical Poisson tensor with the canonical tensor.

## 2. Restriction is different from reduced differentiation

If Tζ=d(ζ,I), the full canonical field, after mass-gauge projection, has noncentral angular coefficient d_n−d₀. In contrast, after substituting I₀=ρ(J), J=(I_n)_{n≠0}, the reduced functional derivative is d_n+ρ_n d₀. Those expressions cannot be interchanged. In general the mass-gauge direction is different from the characteristic direction of χ.

The proposed repair is valid: use full standard XI_n for n≠0, whose central-angle derivative is zero, before applying Π. Their projected noncentral components are exactly the single-pair angular generators. The full contour identity is

\[
\Pi X^{std}_{I_n}=-\frac{i}{\pi L}
\oint_{\Gamma_n}\frac{\Pi Y_{\zeta(z)}}{R(z)}\,dz.
\]

At a fixed state, λ=η+ζ(z) is just a contour parameter. Choose the contour to avoid λ=±S and replace ΠY by DR XFλ/ωλ. Riemann sums converge in every smooth seminorm. A refining sequence of quadratures converges in all seminorms simultaneously. Isolated zeros of ω remove no vector from the closed span: neighboring parameter values recover the missing standard field by continuity, with scalar coefficients permitted to grow.

## 3. The exact regularity condition for the ambient kernel

In noncentral Cartesian coordinates the common differential kernel is

\[
K=\{(\dot w,\dot z):z_n\dot w_n+w_n\dot z_n=0
\text{ for every }n\ne0\}.
\]

If each pair (w_n,z_n) is nonzero, its coordinate kernel is the span of (-w_n,z_n). In particular, all I_n≠0 is sufficient. Finite coordinate truncations of any rapid kernel vector converge in every h^N norm and are finite sums of the single-pair generators. Thus the physical trace fields have closed span K on this regular set.

The conclusion does not hold on the entire D7 chart: if w_n=z_n=0, that pair contributes a two-dimensional differential kernel, while every standard action and trace field has zero components there. At the constant background all noncentral pairs vanish, so the unqualified common-kernel equality is false. A zero product with exactly one nonzero coordinate is harmless for this linear closure statement.

This conclusion concerns closed spans of actual finite Hamiltonian velocities. It does not identify the unclosed velocity image of a fiber with K and does not assert a regular infinite-dimensional fiber manifold. The stated infinite-product example demonstrates why that distinction is necessary.

## 4. A rigorous additional step for physical action-field closure

Trace-field closure alone should not be presented as action-field closure without a convergence argument. One available repair uses the continuous transpose of the actual state chart.

Write R as physical potential map, full canonical KLTZ map, central-angle gauge normalization, and noncentral projection. The gauge normalization differential is a diagonal multiplier plus a rank-one term whose covector has only central support; its transpose preserves all smooth sequence levels. Canonicity of the *full auxiliary* KLTZ chart gives

\[
(DB)^*=J_{pot}^{-1}(DB)^{-1}J_{seq},
\]

with the fixed normalization constants included in Jpot. The inverse is bounded on every H^N/h^N level, hence this transpose preserves smooth covectors. The actual potential differential Λ has the displayed local first-order part and mean-zero K part; its explicit transpose preserves smoothness with at most one derivative loss. Consequently DR* maps rapid sequence covectors continuously to smooth ordinary ∫dx physical gradients. Composing with the original Juv costs one further derivative and is continuous in the Fréchet smooth topology.

Let h(J)=η on the physical section and define

\[
f_\lambda(J)=d(\lambda-h(J),\rho(J),J).
\]

Its genuine reduced derivatives are

\[
b_n=\partial_{J_n}f_\lambda
=d_n+\rho_n d_0-d_\zeta h_n.
\]

Analyticity on an ℓ¹ action neighborhood implies b∈ℓ∞ at the fixed state. The action Cartesian covector (b_n z_n,b_n w_n) is rapid; its finite truncations converge in every sequence seminorm. Applying DR* and Juv yields the actual physical identity

\[
X_{F_\lambda}=\lim_{m\to\infty}
\sum_{0<|n|\le m}b_n X^{phys}_{I_n}.
\]

Conversely the saved A5–A7 identities express each physical XI_n as a contour integral of physical fixed-λ trace fields; the η coefficient vanishes by A6 rather than being omitted. These two implications prove equality of physical action and trace closed spans, hence equality with K on the regular set. Only the functional chain rule uses d_n+ρ_n d₀−dζh_n; this is separate from the full canonical projected velocity.

If fixed-ζ physical trace fields are used instead, their chain rule is XΔζ=XFλ+(∂λFλ)Xη. One must retain Xη, or equivalently the translation/momentum direction, until it has independently been shown to lie in the trace closure. The direct fixed-λ route avoids this extra dependency.

## 5. Original real structure and internal differential kernels

At a real physical state with real S, Fbarλ=overline(Fλ). Work with real fields XReFλ and XImFλ. First prove the complex closure, then realify its finite approximants using conjugation on the original source. The complex common kernel is conjugation-invariant because it also equals the common dFλ kernel. This gives the original real closure without identifying canonical single-pair generators with the physical real slice. Re/Im action fields can be treated the same way.

On the smooth mean-zero source, Juv is invertible with mean-zero primitive K and gives a continuous weak symplectic form Ω. Since the traces factor through the reduced actions and the A5–A6 contour identities recover action differentials from trace differentials,

\[
\bigcap_\lambda\ker dF_\lambda=K,
\qquad K^{\perp_\Omega}=K.
\]

For the strong-coherent domain, let j be ambient evaluation of its internal tangent and define A=∩ker dI_n on that internal tangent, using both real and imaginary parts on the real domain. The naturality identity dI_n(ξ)=dI_n^ambient(jξ) is required. Pull back Ω to ω=j*Ω. If the already established finite physical trace flows preserve this same domain, their internal directions lie in A. Then j(A)⊂K proves A⊂A⊥ω, while ξ⊥ωA annihilates all actual trace directions and hence all dI_n by A5–A6. Therefore

\[
A^{\perp_\omega}=A.
\]

This statement is valid without using injectivity of j, surjectivity onto K, or any equality with the internal tangent of the actual common fiber. In the actual phase construction, j has already been proved injective by the mixed §16.3–16.4 relative-extension argument, equation (16.9); the phase evaluation kernel is zero. The remaining ghost/injectivity question concerns the different map from the actual fiber's internal tangent into the phase internal tangent. The self-orthogonality of this explicitly defined internal *action differential kernel* must not be renamed an unproved fiber-tangent equality.

## 6. Scope

The projection/contour repair and the internal action-differential-kernel argument pass. The physical action-field statement also passes after the smooth transpose convergence step above is included. All conclusions are conditional M=2 results on the stated small-background common chart and regular noncentral-pair set. They do not resolve all-M inverse coordinates, all-M nonlinear closed-span maximality, or the identification of actual fiber internal tangents.

## 7. Final source readback: PASS

Read the final physical trace Poisson closure proof, including §4.4 equations (31)–(38), and independently differentiated the two physical gradients in (6). No script, old certificate, or current check was executed.

The previously incomplete displayed u_t formula is corrected by its additional term

\[
-\frac{(\lambda-2v)(\lambda-V)}{16S}E.
\]

Indeed

\[
Dg_v=2qF-2A(S+u)E
 +\frac{(\lambda-2v)(\lambda-V)}S E
 -\frac{2(\lambda-2v)q}S h.
\]

Multiplying by −1/16 gives exactly the corrected first line of (7). The v_t formula needs no change: using A_x=−2vv_x/S² and r=A(S+u)−v_x/S gives

\[
Dg_u=-(\lambda+2v)F+A(\lambda-2v)E+4SAh.
\]

The A_x and v_x terms cancel explicitly. Thus the final (7), its derivative-free regularity assertion, and the algebraic path to (9)–(11) are consistent with the original physical gradients rather than an omitted spectral term.

The new §4.4 supplies the previously needed convergence step. Equations (31)–(32) give a continuous transpose of the full chart followed by the actual Λ* and Juv; (34) contains both ρ and η̃ derivatives with the correct signs. The bounded action derivative coefficients multiply rapid Cartesian coordinates, so (35) follows from genuine smooth covector convergence. Equations (36)–(38) give the reverse inclusion and original physical realification. For the mixed source seminorm H^N(u)×H^{N+1}(v), the claimed N+2 sequence bound follows more precisely because Λ* has a zeroth-order u-covector component and a first-order v-covector component; Juv then yields respectively H^N and H^{N+1}. These steps do not assert physical canonicity.

The final §7 correctly distinguishes phase and fiber maps. Actual mixed §16.3–16.4 first merges a finite collection of plot velocities using relative coordinate-axis extension, then uses a relative parabola/constant-line extension to annihilate any zero ambient velocity. Equation (16.9) therefore already excludes phase ghosts. That argument does not provide relative extension within an action fiber; injection of the fiber map and an unclosed fiber-tangent equality remain separate questions. The proof of A⊥ω=A is valid as written and does not need to reuse phase injection.

The separate action genericity argument also passes this readback. Its contour residue yields I_{−n}^{[2]}=B_n/γ_n=κ_nQ_nP_n with κ_n=Lk_n²/(16S)≠0, using the specified physical-to-KLTZ negative index and the zero source-shift contribution at the background double point. Actual strong Hilbert curves supply nonzero analytic witnesses and finite action Jacobian minors. Countably many open dense conditions are imposed on one real Hilbert parameter ball, so Baire gives a dense, residual, nonempty parameter set. The ball can be shrunk once inside the common low state chart without losing these witnesses, since their ε parameters can be taken arbitrarily small. This is a result about that single parameter ball; no global diffeological genericity follows.

**Final verdict: PASS for the stated conditional M=2 theorem.** The final source now proves the physical trace and physical action closed-span equalities, real ambient maximal isotropy, the closed ambient velocity image of the actual common fiber, and self-orthogonality of the explicitly defined internal common differential kernel. Its regular-state input is nonempty in the specified strong chart. Remaining issues are the fiber internal-tangent map/possible fiber ghosts, the unclosed fiber-tangent equality, a regular common-level manifold, global action-angle coordinates, and the corresponding state inverse/closure result for M>2. They are not missing steps in the theorem now stated, but they remain outside its scope and leave the user's general-field all-M objective unresolved.
