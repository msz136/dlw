# General M finite actual gaps: involution and order-zero fields

2026-10-11. Independent short hand audit by `all_m_holonomy_image_audit`. No machine checks were run. Existing frozen manuscripts and audit hashes were preserved.

PASS: a locally selected finite actual gap is a scalar contour functional of the existing actual trace family. The original affine free-field connection gives its gradient one derivative of regularity, hence a locally analytic Hamiltonian field of the same Sobolev order. Involution follows from the already proved actual trace bracket identities. The statements below are local for each fixed finite collection of windows; they do not assert bounds uniform over all frequencies or flows on the balanced X₀ state space.

## 1. Fixed multiplier circle and the finite trace coordinates

Let N(λ,z) be the actual trace-normalized monodromy, with det N=1. In a neighborhood of a fixed source state and a fixed spectral window, choose one fixed multiplier circle Γμ enclosing precisely the selected rank-two cluster and avoiding the remaining spectrum throughout the window. Its Riesz projection P is analytic, including at a collision within that cluster.

Put

\[
F_r(\lambda,z)=\operatorname{Tr}N(\lambda,z)^r,
\qquad 1\le r\le M-1,
\]

\[
T_j(\lambda,z)=\operatorname{Tr}[P(\lambda,z)N(\lambda,z)^j],
\qquad j=1,2.
\]

If \(p(\mu)=\det(\mu I-N)\), then

\[
T_j=\frac1{2\pi i}\oint_{\Gamma_\mu}
\mu^j\frac{\partial_\mu p(\mu)}{p(\mu)}\,d\mu.
\tag{1}
\]

Newton's identities express every characteristic coefficient except the fixed determinant through F₁,…,F₍M−1₎. Therefore (1), whose denominator stays nonzero on the fixed circle, makes T₁ and T₂ locally analytic functions of this finite trace vector. No global branch of log p or ordering of the two multipliers is needed.

The selected discriminant is

\[
D=2T_2-T_1^2=(\nu_1-\nu_2)^2.
\tag{2}
\]

It follows that its source differential has the exact form

\[
\delta D(\lambda,z)=\sum_{r=1}^{M-1}
\alpha_r(\lambda,z)\,\delta F_r(\lambda,z),
\tag{3}
\]

with locally analytic scalar coefficients. The dependence of P on the source is already included in this characteristic-polynomial calculation; no projector variation is omitted.

## 2. Fixed spectral window and the gradient of the actual gap

Choose a fixed spectral contour Γλ inside that window, enclosing exactly two zeros of D counted with multiplicity and containing no zero on the contour. Define absolute spectral power sums, center, and half-gap-squared by

\[
s_j=\frac1{2\pi i}\oint_{\Gamma_\lambda}
\lambda^j\frac{D'}D\,d\lambda,\qquad
a=\frac{s_1}2,\qquad g=\frac{s_2}2-a^2.
\tag{4}
\]

Both contours are fixed on the source neighborhood. Differentiation and integration by parts give

\[
\delta s_j=-\frac{j}{2\pi i}\oint_{\Gamma_\lambda}
\lambda^{j-1}\frac{\delta D}{D}\,d\lambda,
\]

\[
\boxed{\displaystyle
\delta g=\frac1{2\pi i}\oint_{\Gamma_\lambda}
(a-\lambda)\frac{\delta D}{D}\,d\lambda.}
\tag{5}
\]

Combining (3) and (5) yields the variational gradient identity

\[
\nabla g=
\sum_{r=1}^{M-1}\frac1{2\pi i}\oint_{\Gamma_\lambda}
\frac{(a-\lambda)\alpha_r(\lambda,z)}{D(\lambda,z)}
\nabla F_r(\lambda,z)\,d\lambda.
\tag{6}
\]

The coefficients depend on the source but are scalar and independent of the spatial variable x. State dependence does not create extra terms in (6): the differential chain rule evaluates the displayed coefficients at the state. The fixed contours and the nonzero boundary denominators give local bounds for these coefficients and all their source derivatives.

## 3. One derivative gained by the original affine connection

Use the original free-field coordinates z, in which the spatial connection is affine, at each fixed spectral parameter:

\[
A(\lambda,z(x))=A_*(\lambda)+\sum_i C_i(\lambda)z_i(x).
\tag{7}
\]

The matrices Cᵢ have no x dependence and no source derivatives. Fix a common strong periodic Sobolev domain Hˢ on which this connection and the original free Poisson tensor J are defined; for example s≥1 suffices for the elementary Sobolev product argument below.

Let Y solve Y′=AY, Y(0)=I, let T=Y(L), and let

\[
N=e^{-\frac1M\int_0^L\operatorname{tr}A\,dx}T,
\qquad W_r(x)=Y(x)N^rY(x)^{-1}.
\]

The actual monodromy variation gives

\[
\delta F_r=r\int_0^L
\operatorname{Tr}\left[
\left(W_r-\frac{F_r}{M}I\right)\delta A\right]dx.
\tag{8}
\]

Since N is a scalar multiple of T, it commutes with T. Hence Wᵣ(L)=Wᵣ(0). Also

\[
W_r'=[A,W_r].
\tag{9}
\]

The finite-interval ODE and Sobolev product estimates give a periodic Wᵣ in Hˢ⁺¹, depending analytically on the Hˢ source and locally uniformly on compact λ contours. Thus each original free-coordinate gradient component

\[
(\nabla F_r)_i=
r\operatorname{Tr}\left[
\left(W_r-\frac{F_r}{M}I\right)C_i(\lambda)\right]
\tag{10}
\]

is in Hˢ⁺¹. On a fixed-mean leaf, subtracting any needed constant component means does not alter this conclusion or the Hamiltonian field.

For the original first-order free Poisson tensor, J maps these gradients to Hˢ fields. Applying J to (6) is legitimate and gives

\[
X_g=\sum_{r=1}^{M-1}\frac1{2\pi i}\oint_{\Gamma_\lambda}
\frac{(a-\lambda)\alpha_r}{D}\,X_{F_r}(\lambda,z)\,d\lambda
\in H^s.
\tag{11}
\]

The map z↦Xg is locally analytic on this strong Hˢ domain. Consequently each real Hamiltonian component has a local unique Hˢ flow by the usual Banach-space ODE theorem. This argument specifically uses the original affine connection; it does not infer the field order from the state-coordinate inverse or from its balanced L²×H¹ chart.

## 4. Involution and real components

Use the already proved actual trace identities on their common domain,

\[
\{F_r(\lambda),F_s(\mu)\}=0,
\qquad \{F_r(\lambda),C_j\}=0.
\tag{12}
\]

The Poisson bracket is bilinear in the first differentials. Substitution of (6), with spatially constant scalar weights and fixed compact contours, therefore proves

\[
\{g,h\}=0,\qquad\{g,C_j\}=0
\tag{13}
\]

for any finite selected gap functions g,h. No derivative of the contour weights is inserted into this first-differential bracket. Commutation with Cⱼ retains the regularity/domain assumptions of the existing actual trace bridge; the order-zero gap argument alone does not enlarge the domain of a higher hierarchy Hamiltonian.

For real source fields, N(\(\overline\lambda\),z)=\(\overline{N(\lambda,z)}\). The conjugate of a gap is the gap obtained from the conjugate spectral and multiplier contours. Applying the same proof also gives \(\{g,\overline h\}=0\). Hence every real and imaginary component of any finite gap collection Poisson-commutes with the others and with real Cⱼ. Their same-order real analytic Hamiltonian fields commute locally.

The result is local for each fixed finite collection. It does not give uniform high-frequency field bounds, a balanced X₀ flow theorem, canonical norming variables, action normalization, Hamiltonian completeness, or a Liouville conclusion.
