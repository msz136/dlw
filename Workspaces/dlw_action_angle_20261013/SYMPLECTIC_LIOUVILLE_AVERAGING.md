# Symplectic linearization by averaging the original Liouville field

2026-10-13. The original physical symplectic form is CONSTANT on the balanced mean leaf. This permits a different normalization than radial Moser in the nonlinear spectral coordinates. The construction below uses the established actual compact spectral group action, its original symplecticity, and an averaged vector field; it never inverts the weak form. It closes the high weak-canonical normalization step, conditional on the preceding group-action proofs. These arguments remain branch-internal and require independent full review.

## 1. Abstract theorem in the topology actually used

Let E be a complex Hilbert space with a continuous constant skew bilinear form Ω₀ whose associated E→E* map is injective. Strong nondegeneracy is not required. Let a compact metrizable group G act near 0 by holomorphic local diffeomorphisms Φg, fixing 0 and preserving Ω₀. Assume:

1. There is a common invariant open neighborhood, with a smaller ball on which the maps and inverses are uniformly bounded and holomorphic.
2. The action is jointly continuous in g and x, and its linear representation Lg=DΦg(0) is strongly continuous and uniformly bounded with uniformly bounded inverses.

Then a smaller neighborhood has a holomorphic symplectic coordinate map Ξ, with Ξ(0)=0 and DΞ(0)=Id, satisfying

\[
\boxed{\quad\Xi^*\Omega_0=\Omega_0,\qquad
\Xi\circ\Phi_g=L_g\circ\Xi.\quad}
\tag{1}
\]

This assertion concerns an action already symplectic for a CONSTANT form on an open linear-space neighborhood. It is not a general Darboux theorem for arbitrary weak forms on Banach manifolds.

## 2. An averaged vector field, already in E

Let Eul(x)=x be the Euler vector field, so L_EulΩ₀=2Ω₀. Pull it back by the actual symplectic maps and average:

\[
W(x)=\int_G (\Phi_g^*\mathrm{Eul})(x)\,dg
=\int_G D\Phi_g(x)^{-1}\Phi_g(x)\,dg.
\tag{2}
\]

This is a Bochner integral of E-valued vectors, not an average of covectors followed by weak inversion. On a common smaller ball, the derivative maps and inverse derivatives have uniform bounds by holomorphic Cauchy estimates and the inverse group maps. Their values on fixed vectors depend continuously on g: directional derivatives can be expressed by one-complex-variable Cauchy integrals of the jointly continuous uniformly bounded maps. Hence the integrand in (2) is jointly continuous in g and x and uniformly bounded and holomorphic in x. Integration of its uniform Taylor expansions proves holomorphy of W.

Since Φg(x)=Lg x+O(||x||²), uniformly in g, and DΦg(x)⁻¹=Lg⁻¹+O(||x||),

\[
W(x)=x+R(x),\qquad R(x)=O(\|x\|^2),\quad DW(0)=\operatorname{Id}.
\tag{3}
\]

Pullback reverses composition. Haar invariance gives Φh*W=W, so W is equivariant under every actual group map. Each pulled-back Euler field satisfies L_(Φg*Eul)Ω₀=2Ω₀, because Φg*Ω₀=Ω₀. Integrating the derivative identities on any two fixed test vectors gives

\[
\boxed{\quad\mathcal L_W\Omega_0=2\Omega_0.\quad}
\tag{4}
\]

All vector fields in this argument are bounded analytic E-valued maps on smaller balls. No hypothesis on an unbounded inverse of Ω₀ has entered.

## 3. A contraction flow for every positive auxiliary time

Let ψt solve xdot=−W(x), t≥0. On a sufficiently small ball, variation of constants gives

\[
\psi_t(x)=e^{-t}x-\int_0^t e^{-(t-s)}R(\psi_s(x))\,ds.
\tag{5}
\]

If ||R(y)||≤C||y||², the scalar comparison for eᵗ||ψt|| yields, after choosing C||x||<1/2,

\[
\|\psi_t(x)\|
\le\frac{e^{-t}\|x\|}{1-C\|x\|(1-e^{-t})}
\le2e^{-t}\|x\|.
\tag{6}
\]

Choose the initial ball small enough that this estimate remains inside the analytic domain. Local Banach ODE existence and (6) continue the trajectory for all t≥0. The flow is holomorphic in x for each finite t. Equation (4) gives the exact form scaling

\[
\psi_t^*\Omega_0=e^{-2t}\Omega_0.
\tag{7}
\]

Here t is an auxiliary coordinate-construction parameter, not the original DLW time.

## 4. An analytic limit of genuine symplectic maps

Set Ξt(x)=eᵗψt(x). By (5)–(6),

\[
\Xi(x)=\lim_{t\to\infty}\Xi_t(x)
=x-\int_0^\infty e^sR(\psi_s(x))\,ds,
\qquad \|\Xi(x)-x\|\le4C\|x\|^2.
\tag{8}
\]

The integrand is bounded by 4Ce⁻ˢ||x||². Thus the limit is uniform on a common small complex ball, and the tail is exponentially small there. Holomorphic Cauchy estimates give operator-norm convergence of the derivatives on smaller balls. Consequently Ξ is holomorphic with derivative Id at 0 and has an actual local analytic inverse.

The constant form scales under the linear map x↦eᵗx by e²ᵗ. Combining this with (7) proves, for EVERY finite t,

\[
\Xi_t^*\Omega_0=\Omega_0.
\]

Derivative convergence and continuity of Ω₀ pass this identity to Ξ. Weak injectivity causes no difficulty in this limit; no inverse operator is passed through it.

Equivariance of W implies ψtΦg=Φgψt wherever both sides are defined. After choosing a common smaller initial ball this holds for all t≥0 and g, by the uniform orbit bounds. Taylor expansion at 0 gives

\[
e^t\Phi_g(\psi_t x)
=L_g\Xi_t(x)+e^tO(\|\psi_t x\|^2)
=L_g\Xi_t(x)+O(e^{-t}\|x\|^2),
\tag{9}
\]

uniformly in g. Taking the limit proves the second identity in (1). Shrinking and saturating an injectivity neighborhood as in the established group-action construction yields an invariant domain if desired. This proves the theorem.

## 5. Application to the original DLW leaf

The [infinite spectral torus theorem](INFINITE_TORUS_STATE_CHART.md) supplies precisely the common invariant neighborhood, product-topology continuity, uniform analytic bounds and strongly continuous diagonal linear representation required above. The underlying maps are the [actual original Hamilton flows](BOUNDED_PROFILE_PHYSICAL_FLOWS.md). Their preservation of the original constant Ω follows from d(i_XΩ)=d²H=0 and continuity of the bounded-profile flow construction.

Work in the ORIGINAL physical mean-leaf coordinates, centered at the uniform source. Their form is constant. Make only a fixed linear identification with the calibrated background spectral data before applying §§1–4; this sends the original form to its actual background high weights and finite low block, not to a strong unweighted form. All hypotheses are then satisfied, conditional on the previously established spectral/group inputs.

Denote the resulting symplectic linearizing data by (vα+,vα−,ζ). The exact form and generators are

\[
\boxed{\quad
\Omega=\sum_\alpha w_\alpha\,dv_\alpha^+\wedge dv_\alpha^-
+\Omega_{\rm low},\qquad
X_{A_\alpha}=v_\alpha^+\partial_{v_\alpha^+}-v_\alpha^-\partial_{v_\alpha^-}.
\quad}\tag{10}

Here Ωlow is the finite constant background symplectic form and wα=(Lωαγα)⁻¹, with |wα|≈n⁻². The coordinate map and its inverse are analytic on genuine general-field neighborhoods with all infinitely many modes retained.

Contract (10) with X_Aα. The original moment-map identity gives dAα=d(wαvα+vα−). Both functions vanish at the background, so on a connected neighborhood

\[
\boxed{\quad A_\alpha=w_\alpha v_\alpha^+v_\alpha^-.\quad}
\tag{11}

This canonical normalization does not need the separate product rescaling from the preceding note, although it confirms that note's product identities. On a suitable common domain, composing this new chart with the inverse of the previous Cartesian chart gives an action-preserving symplectic normalization of its actual ΩU. Therefore the weighted-adjoint criterion in the preceding note is no longer required to complete THIS normalization step. That criterion and its radial-failure example remain valid, but its sufficient hypothesis need not be forced onto the actual inverse.

All finite coordinate differentials now have actual Hamilton fields: for example {vα+,vβ−}=δαβ/wα, with other high Cartesian brackets zero and no high/low cross brackets. The infinite form remains weak in exactly the original topology. No unweighted Hilbert Darboux chart has been claimed.

Physical reality is preserved. Conjugation acts on the complex spectral group through the reflected-angle automorphism and preserves Haar measure. It commutes with the Euler field, the average (2), the negative flow, and the limit. Thus the symplectic chart restricts to the original real mean leaf.

## 6. Actual high angles and their declared relative topology

For each fixed nonzero pair define θα=½log(vα+/vα−) on a local branch. Then

\[
w_\alpha\,dv_\alpha^+\wedge dv_\alpha^-
=d\theta_\alpha\wedge dA_\alpha.
\tag{12}
\]

For ALL high indices simultaneously, choose a base sequence v* with both factors nonzero, inside the canonical neighborhood. Set Aα*=wαvα*+vα*−. On a sufficiently small open ball in the RELATIVE Banach variables (ρ,ϑ)∈ℓ∞⊕ℓ∞ define

\[
v_\alpha^+=v_\alpha^{*,+}(1+\rho_\alpha)^{1/2}e^{\vartheta_\alpha},\qquad
v_\alpha^-=v_\alpha^{*,-}(1+\rho_\alpha)^{1/2}e^{-\vartheta_\alpha},
\quad A_\alpha=A_\alpha^*(1+\rho_\alpha).
\tag{13}

Use the square root and exponential branches near 1 and 0. This is an injective analytic parametrization with an analytic inverse IN THE TRANSPORTED RELATIVE TOPOLOGY. It is not a local diffeomorphism onto an E-open set: division by the vanishing base amplitudes is not bounded in the ordinary ℓ² topology. It preserves infinitely many freely varying high coordinates; no finite-dimensional restriction is introduced.

Explicitly, write aα=vα+/vα*,+−1 and bα=vα−/vα*,−−1, and put the norm ||a||∞+||b||∞ on the relative source neighborhood ||a||∞+||b||∞<ε. In this concrete Banach topology the inverse of (13) is

\[
\rho_\alpha=(1+a_\alpha)(1+b_\alpha)-1,\qquad
\vartheta_\alpha=\tfrac12\log\frac{1+a_\alpha}{1+b_\alpha}.
\tag{13a}
\]

For ε sufficiently small the logarithm and square-root series converge in the Banach algebra ℓ∞ and are mutual inverses on smaller open neighborhoods. This supplies an explicit relative norm and inverse, rather than defining the topology only by naming the parametrization. The physical relative domain is its image under the already established canonical state inverse.

Since Σ|Aα*|<∞, the pulled-back form converges absolutely on bounded relative tangent vectors and is

\[
\boxed{\quad
\Omega=\sum_\alpha A_\alpha^*\,d\vartheta_\alpha\wedge d\rho_\alpha
+\Omega_{\rm low}.
\quad}\tag{14}

It is weakly nondegenerate on this relative domain: finite-coordinate tests detect each nonzero high tangent, and the finite low block is nondegenerate. The single-coordinate identities {ϑα,Aβ}=δαβ and mutual angle commutation hold there. Generic unbounded frequency sequences need not generate a flow in the ℓ∞ angular topology; the original-time domain remains a separate requirement.

## 7. What remains for the complete objective

This construction provides the previously missing ORIGINAL weak canonical high chart, full state reconstruction, exact high action products and a specified relative high action–angle domain. It leaves a finite constant symplectic low block. The actual spectral traces, being analytic and high-flow invariant, are functions of the high products and these low variables by the established invariant-descent theorem.

The remaining work is to supply enough independent commuting low spectral integrals on the relevant general-field domain and to express the original Hamiltonian and its genuine time evolution in complete actions. In particular, low integrability on the common fixed core alone would not automatically give its parameter-dependent completion at arbitrary high actions. Original H's smooth/strong-domain restrictions and possibly unbounded angular frequencies must be retained. Thus the full action–angle and ORIGINAL-TIME objective remains ACTIVE, not completed by (10)–(14).
