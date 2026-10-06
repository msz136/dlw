# Infinite-lattice primitive: domain and a tangency obstruction

Independent analysis, 2026-10-04. Let `D=∂x`, `d=(1−E⁻¹)/h`, `M=(1+E⁻¹)/2`, `β=h²/32`, and set `U=u+2a`, `w=v−δ₀u−4`. The physical equations are

\[
d\{U_t+D(\tfrac12U^2+\beta w^2)\}+D^2(dU+Mw)=0,
\qquad w_t=-D(Uw)+D^2w.
\]

## 1. The primitive on a precisely stated domain

For `f∈ℓ¹(ℤ)`, define

\[
(Rf)_j=\frac h2\left(\sum_{k<j}f_k-\sum_{k>j}f_k\right).
\]

This is a well-defined map `ℓ¹→ℓ∞` with `‖Rf‖∞≤(h/2)‖f‖₁`, and

\[
dRf=Mf,\qquad
\lim_{j\to\pm\infty}(Rf)_j=\pm\frac h2\sum_kf_k.
\]

Thus the primitive preserves zero far fields exactly when the lattice sum of its input vanishes. If `∑f=0` and `∑(1+|j|)|f_j|<∞`, then

\[
\|Rf\|_{\ell^1}\le h\sum_j(|j|+\tfrac12)|f_j|.
\]

More generally it loses one polynomial lattice weight, and maps zero-sum lattice Schwartz sequences to Schwartz sequences. For two `ℓ¹` inputs its skew identity is exact:

\[
\sum_jg_j(Rf)_j=-\sum_jf_j(Rg)_j.
\]

The double series is absolutely convergent, so no principal-value convention is hidden in this identity. On smooth `x`-dependent fields with locally controlled `ℓ¹` derivatives, `D` commutes with `R`. Consequently `RD` is symmetric for the joint pairing `h∑j∫dx`, whenever the `x` boundary terms vanish and the displayed pairings converge absolutely. The zero-sum condition must be checked for `Df`, rather than silently imposed on `f`.

For an exact tau line soliton, `W*=w*+4` is exponentially localized in `j` for every fixed `x`, and its lattice sum is constant in `x`. Therefore `RDw*=RDW*` is legitimate. This says nothing about neighboring perturbations with nonconstant lattice mass.

## 2. Necessary compatibility for the specified vacuum tails

Take a fixed exact background `B=(U*,w*)`, with `U*→U₀=2a`, `w*→c=−4` as `j→±∞`, and perturb it by jointly Schwartz `(p,r)`. Write `U=U*+p`, `w=w*+r` and define the finite relative sums

\[
A(x)=\sum_jr_j(x),\qquad
Q(x)=\sum_j\{U_jw_j-U_j^*w_j^*\}.
\]

The integrated candidate is

\[
U_t=-D(\tfrac12U^2+\beta w^2+DU+RDw),
\qquad w_t=-D(Uw-Dw).
\]

For `U_t−U*t` to have zero tails, the primitive limit requires `D²A=0`. Joint localization in `x` makes this `A=0`. Summing the second equation gives

\[
A_t=-DQ+D^2A.
\]

Hence persistence of `A=0` requires `Q=0`, again using joint localization in `x`. These are necessary constraints on classical fixed-tail solutions, not optional choices of inverse.

## 3. The two constraints are not an invariant phase space

Even at the constant vacuum they fail at the next time derivative. Set `r=0`, `p₀=f(x)`, `p₁=−f(x)`, and all other `p_j=0`, where `f` is a nonzero smooth compactly supported bump. Both `A=0` and `Q=c∑p=0` hold. Direct substitution gives

\[
Q_t=-cD\sum_jp_j^2=8D(f^2),\qquad
A_{tt}=-DQ_t=-8D^2(f^2).
\]

The first identity uses both equations, including the product term in `Q`; omitting this term gives an incorrect cancellation. Thus an initially admissible compact perturbation leaves the compatibility constraints immediately at second order in time. A twice differentiable solution which retains joint-Schwartz deviations and the prescribed vacuum tails cannot pass through this datum.

The obstruction also occurs arbitrarily close to every benchmark soliton. At any fixed time choose sites 0 and 1 and

\[
r=0,\qquad
p_0=\varepsilon w_1^*\phi(x),\qquad
p_1=-\varepsilon w_0^*\phi(x).
\]

Then `A=Q=0` identically. Put `p=εa`. Under the integrated candidate,

\[
Q_t=\varepsilon L_B(a)-\varepsilon^2D\sum_jw_j^*a_j^2,
\]

where

\[
L_B(a)=\sum_j\left[-w_j^*D(U_j^*a_j)-w_j^*D^2a_j
+a_jw_{jt}^*-U_j^*D(w_j^*a_j)\right].
\]

The quadratic coefficient equals

\[
-D\{w_0^*w_1^*(w_0^*+w_1^*)\phi^2\}.
\]

In a bump placed far out in `x` at these fixed sites, it tends to `128D(φ²)`, whereas the linear coefficient tends to zero exponentially. Taking the bump sufficiently far out proves the existence of arbitrarily small compatible perturbations with `Q_t≠0`. Alternatively, a nonzero quadratic coefficient alone proves that not all sufficiently small `ε` can have `Q_t=0`.

Enforcing `Q_t=0` introduces a further constraint; its preservation can introduce more. No invariant infinite constraint manifold is constructed here. This failure excludes the claimed neighborhood consisting of arbitrary jointly Schwartz fixed-tail perturbations, and the neighborhood cut out only by `A=Q=0`. It does not exclude Hamilton structures on a different phase space or for another Poisson operator.

## 4. The constant bracket does not automatically descend

The constant formal operator `J=−[[0,D],[D,0]]` is skew and satisfies Jacobi on unconstrained test-functional algebras. On the proposed manifold `A=0`, a conormal is

\[
dC_\varphi=(0,\varphi(x)\mathbf1),\qquad
C_\varphi=h\int\varphi(x)\sum_jr_j(x)\,dx.
\]

But

\[
JdC_\varphi=(-D\varphi(x)\mathbf1,0)
\]

is not a decaying tangent vector. Therefore this bracket does not descend to the constraint manifold by mere restriction. A proved reduction or replacement bracket is required; declaring the constraints a phase space is insufficient. The finite-periodic mean reconstruction works by a genuinely lattice-constant kernel direction, which is unavailable among decaying infinite-lattice perturbations.

## 5. A finite relative expression is weaker than a Hamilton theorem

The local background-subtracted polynomial terms are integrable for `(p,r)` jointly Schwartz because all derivatives of the benchmark backgrounds are bounded. The nonlocal cross term in the literal difference of densities need not be absolutely integrable if `D∑r≠0`. One can instead define it by polarization:

\[
\mathcal H_B[p,r]=h\sum_j\int\left[
\tfrac12(U^2w-U^{*2}w^*)+\frac\beta3(w^3-w^{*3})
+wDU-w^*DU^*+rRDw^*+\tfrac12rRDr\right]dx.
\]

Every term here is absolutely integrable for jointly Schwartz deviations, given polynomially controlled `RDw*`. Its variational derivative is the formal full gradient

\[
\delta_U\mathcal H_B=Uw-Dw,\qquad
\delta_w\mathcal H_B=\tfrac12U^2+\beta w^2+DU+RDw.
\]

The functional is a background-dependent renormalization with an explicit polarization convention; it is not an assertion that the literal double integral of the original density difference converges. For time-dependent `B`, `\mathcal H_B` itself is explicitly time-dependent, and a relative-coordinate evolution also subtracts `B_t`. Most importantly, finite energy and a valid first variation do not ensure that `Jδ\mathcal H_B` is tangent to the chosen affine space. The preceding counterexample prevents treating this formula as a complete fixed-tail Hamilton theorem.
