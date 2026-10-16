# A common infinite spectral torus and an analytic state chart

2026-10-13. This uses the new [bounded-profile ORIGINAL flows](BOUNDED_PROFILE_PHYSICAL_FLOWS.md) and the previously derived [single-index exact periods](PERIODIC_SPECTRAL_FLOWS.md). It establishes a common analytic state chart linearizing all high reciprocal flows. It does not assert that this chart is symplectic, that its finite residual data are actions, or that the original DLW time is linearized. The argument remains branch-internal and awaits independent full review of both it and its dependencies.

## 1. Common bounded-profile maps

Let I be the countable set of high complex labels in the complexification of the actual real state chart. Conjugate coordinates are independent here. For θ∈ℓ∞(I;R), define Φθ(x) as the u=1 solution of

\[
\frac{dx}{du}=X_{i\theta}(x)
=\sum_\alpha i\theta_\alpha X_{\mathcal A_\alpha}(x).
\tag{1}
\]

For every finite bound T, these maps and their relevant compositions are defined and holomorphic on a common sufficiently small complex source ball whenever ||θ||∞≤T. Their values and first derivatives have uniform bounds. This is the actual original-field ODE, not a definition through factored spectral data.

The preceding proof also gives the following continuity: on any bounded cube of real profiles, coordinatewise convergence θj→θ implies Φθj(x)→Φθ(x), uniformly on compact initial-source sets. Its proof compares with the compact image of the limiting orbit and uses the common Lipschitz bound; it does not require operator-norm convergence of the differentiated tail fields.

## 2. Periodicity and group law on one neighborhood

Choose T large enough to handle representatives θ,φ∈[0,2π]^I and sums θ+φ∈[0,4π]^I. Shrink the common source ball so all these flows and the two-step compositions are defined. For finite-support profiles, commuting analytic fields imply, as germs at 0,

\[
\Phi_\theta\circ\Phi_\varphi=\Phi_{\theta+\varphi}.
\tag{2}
\]

The exact individual return identity gives Φθ=Φθ+2πk as germs whenever k has finite integer support. Composing many single-label maps may require a smaller germ neighborhood depending on their number, but that does not shrink the domain of the simultaneous maps in (1). Both sides of each identity are holomorphic on the already chosen common ball. The identity theorem on this connected ball extends the germ identity to that ball. For periodic comparisons only pairs of bounded representatives are needed.

Exhaust the labels by finite sets. The bounded-profile convergence passes (2) and periodic representative independence to arbitrary profiles. For a composition, the uniform first-derivative bound controls the change of its initial point while the outer profile is truncated. For representative independence, two lifts in [0,2π]^I differ by 2π integers only in coordinates representing the same circle point; each finite truncation has equal maps, so the limits agree.

The cube [0,2π]^I is a compact metric space with product topology. The preceding continuity and representative independence show that the maps descend continuously to

\[
\mathbb T^I=\prod_{\alpha\in I}(\mathbb R/2\pi\mathbb Z).
\tag{3}
\]

This is continuity of the ACTUAL state at each source, jointly with the source by the uniform Lipschitz bound. It is not operator-norm continuity of the differentiated group representation.

For completeness, an invariant open neighborhood can be obtained without intersecting infinitely many open sets. Take a ball Bρ small enough that all its images lie in the preceding common domain and set

\[
U=\bigcup_{g\in\mathbb T^I}\Phi_g(B_\rho).
\tag{4}
\]

Each map has local holomorphic inverse Φ−g by (2), so U is open. Uniform orbit bounds place U inside the common domain. Equation (2) makes U invariant, and all Φg are biholomorphisms of U. Hence (3) acts on one genuine open general-field neighborhood. No finite-dimensional truncation of the source has been made.

## 3. Strongly continuous linear representation

Use the complexification of the existing [augmented high-norming state inverse](../dlw_recovery_20261011/general_m_augmented_actual_high_norming_state_inverse_recovery_20261011.md) to identify a source neighborhood with a Hilbert data neighborhood. Denote these data by z and center them at the uniform source. Their high components are calibrated norming pairs, and their finite low components are the stated nonspectral Fourier supplements. This is a true state chart.

The exact background torque and zero low action from the reciprocal-period proof give

\[
L_g=D\Phi_g(0):\quad
(z_\alpha^+,z_\alpha^-,\eta)
\longmapsto
(e^{i\theta_\alpha}z_\alpha^+,e^{-i\theta_\alpha}z_\alpha^-,\eta).
\tag{5}
\]

In a compatible Hilbert data norm, Lg and its inverse have norm one. They are strongly continuous for the product topology: truncate any fixed ℓ² vector, use ordinary finite-coordinate continuity, then bound its tail. They need not be operator-norm continuous. The finite vector η accounts for ALL low supplements, not extra high residual directions.

Equation (5) for infinite profiles also follows directly by differentiating the bounded-profile vector field at the background. Its derivative is a bounded diagonal multiplier; the jointly analytic synthesis proof supplies this derivative without claiming operator-norm convergence of finite multiplier truncations.

## 4. Infinite Haar averaging and the inverse

Let dg be normalized product Haar measure on the compact metric group (3). On the common invariant data neighborhood define

\[
\Psi(z)=\int_{\mathbb T^I}L_g^{-1}\Phi_g(z)\,dg.
\tag{6}
\]

For each z the integrand is a continuous Hilbert-valued function on a compact space, so its Bochner integral exists. On a fixed smaller ball the integrand maps are holomorphic and uniformly bounded. Cauchy estimates on still smaller balls give uniform Taylor remainder bounds; integrating those Taylor series proves Fréchet holomorphy of Ψ. In particular,

\[
\Psi(0)=0,\qquad D\Psi(0)=I.
\tag{7}
\]

The second equality uses Lg⁻¹DΦg(0)=I for EVERY g; it does not interchange an unproved operator-norm continuous representation with Haar integration. Uniform quadratic remainder estimates justify the derivative directly.

The analytic inverse function theorem gives a genuine local analytic inverse of Ψ. To retain group invariance, take an injectivity ball for Ψ, then saturate a smaller ball using the uniform orbit bounds, as in (4), with the saturation still contained in the injectivity ball. Thus Ψ is a biholomorphic chart on a common invariant neighborhood.

Haar invariance and the group law yield

\[
\boxed{\quad\Psi(\Phi_h(z))=L_h\Psi(z).\quad}
\tag{8}
\]

Indeed substitute k=gh in (6); since Lg⁻¹=Lh Lk⁻¹, the factor Lh exits the integral. All integrations take place on the common invariant domain, so no index-dependent source neighborhoods are being integrated.

## 5. Exact nonlinear coordinates and remaining symplectic questions

Write the coordinates of Ψ as (Zα+,Zα−,η). Differentiate (8) along an individual circle direction and use holomorphic continuation of the generating time. The exact original Hamilton identities are

\[
\boxed{\quad
\{Z_\beta^\pm,\mathcal A_\alpha\}
=\pm\delta_{\alpha\beta}Z_\beta^\pm,
\qquad \{\eta_j,\mathcal A_\alpha\}=0
\quad}\tag{9}
\]

for EVERY high label on the same neighborhood. The coordinate map has a controlled actual state inverse. Thus this removes the infinite joint-domain and infinite Bochner-inverse gaps left by the finite-family result.

Every product Iα=Zα+Zα− is invariant under all high period flows. These products belong to ℓ¹, but they are not here identified with the canonical physical actions Aα. The finite η coordinates are also invariant under these flows; they are not asserted invariant under the original DLW Hamiltonian.

For each fixed α on a neighborhood where both factors are nonzero, Θ α=½log(Zα+/Zα−) gives {Θα,Aβ}=δαβ. This does not provide a common open ℓ² logarithmic chart for every α: arbitrary small ℓ² perturbations can close a sufficiently small coordinate. A full all-angle statement still needs its declared relative topology and nonzero reference profile. Equations (8)–(9) are instead regular Cartesian statements through closed high gaps.

The source flows preserve the original Ω, so its pushforward by Ψ is an invariant weak symplectic form for (5), with the original weighted linear form at 0. Averaging the state map does NOT make this form constant or diagonal. A legitimate weak symplectic normalization must still prove that its required covectors have Hamilton fields in the actual topology; a strong-symplectic Darboux or Moser theorem cannot be imported without that range estimate.

Complex conjugation maps label α to its reflected label and angle θα to −θ reflected. This is a Haar-preserving group automorphism. The original state chart and flow reality identities therefore make Ψ compatible with the physical real structure. Compact real directions use paired imaginary profiles; complementary real scaling directions remain. No compact real torus for the original DLW evolution is claimed.

## 6. Updated full objective

We now have a genuine common infinite spectral torus action and a nonlinear analytic STATE inverse linearizing all its high generators, conditional on the declared actual spectral and individual-period inputs. To finish the full goal one must still normalize the original weak form, supply complete invariant low data, prove a full action inverse on an explicit topology, and identify the original Hamiltonian and its evolution domain in those coordinates. None of these remaining tasks follows merely from (9). The complete action–angle/original-time goal remains ACTIVE.

Subsequent progress: [INVARIANT_BASE_ACTION_INVERSE.md](INVARIANT_BASE_ACTION_INVERSE.md) gives analytic invariant descent to ℓ¹ products, an actual weighted HIGH-action inverse with η retained, and a further state change making every high action an exact weighted Cartesian product. It does not remove the remaining weak-form correction, complete the low actions, or prove original-time linearization.
