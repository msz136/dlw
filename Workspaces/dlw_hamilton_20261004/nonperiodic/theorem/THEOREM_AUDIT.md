# Nonperiodic Hamilton phase-space audit

Independent mathematical audit, 2026-10-04. This note distinguishes a convergent variational identity from a Hamilton vector field tangent to an actual phase space. The latter does not follow from the former.

Let `D=∂x`, `d=(1-E⁻¹)/h`, `M=(1+E⁻¹)/2`, `β=h²/32`, with `h>0`. The equations are

\[
d\{U_t+D(U^2/2+\beta w^2)+D^2U\}+MD^2w=0,
\qquad w_t=-D(Uw)+D^2w.
\]

The symmetric inverse on summable sequences is

\[
(Rf)_j=\frac h2\sum_k\operatorname{sgn}(j-k)f_k.
\]

It satisfies `dR=M`. Its right and left limits are `±h∑f/2`; thus `Rf` decays at both ends exactly when `∑f=0`. On the joint Schwartz class

\[
\mathscr S=\{f_j(x): \sup_{j,x}(1+|j|+|x|)^N|D^mf_j(x)|<\infty\quad\forall N,m\},
\]

`R : S → bounded smooth lattice step tails`, while `R : S₀ → S` continuously for `S₀={f∈S:∑f_j(x)=0}`. For `f,g∈S`, the double sum defining `⟨f,Rg⟩` is absolutely convergent and `⟨f,Rg⟩=-⟨Rf,g⟩`. Also `[R,D]=0`; hence `RD` is symmetric as a bilinear form on `S`.

## A. Convergent relative variational identity

Suppose a smooth bounded reference `B(t)=(A,C)` with bounded derivatives solves the equations in the same symmetric lattice gauge, so

\[
A_t=-D(A^2/2+\beta C^2)-D^2A-RD^2C,
\quad C_t=-D(AC)+D^2C.
\]

The terms `RDC`, `RD²C` must be defined for this background separately; exact line solutions satisfy this via their telescoping formulas, not because the background is joint Schwartz. Let `U=A+p,w=C+r`, `p,r∈S`. Define

\[
K_B[p,r]=h\sum_j\int_\mathbb R\left[
\frac C2p^2+Apr+\frac12p^2r+\beta Cr^2+\frac\beta3r^3+rp_x+\frac12rRr_x
\right]dx.\tag{A1}
\]

This is the fully linear-subtracted, quadratic-and-cubic relative energy. It is finite for every `p,r∈S`, including nonzero lattice mass of `r`; its last term is finite by absolute double summation. Derivatives along arbitrary Schwartz variations are

\[
K_p=Cp+Ar+pr-r_x,
\quad K_r=Ap+p^2/2+2\beta Cr+\beta r^2+p_x+Rr_x.\tag{A2}
\]

Consequently the constant formal Poisson operator

\[
J_0=-\begin{pmatrix}0&D\\D&0\end{pmatrix}
\]

gives the exact difference equations

\[
p_t=-D(Ap+p^2/2+2\beta Cr+\beta r^2)-p_{xx}-Rr_{xx},
\quad r_t=-D(Cp+Ar+pr)+r_{xx}.\tag{A3}
\]

The physical variable change is `u=U-2a`, `v=w+4+δ₀U`; its shear leaves `J₀` unchanged because `δ₀*=-δ₀` and `[δ₀,D]=0`.

On compact-support cylinder functionals, `J₀` is skew by x integration by parts, and Jacobi holds because its coefficients are independent of fields. It is first order in x and has lattice radius zero. Its Hamiltonian necessarily contains the all-lattice `R` term.

**Scope of (A1)–(A3):** this proves a finite differentiable relative functional and a variational identity. It does not prove a Poisson Hamiltonian system on the affine phase space `B+S`: (A3) is generically not tangent to it. It is legitimate to use (A3) along any independently established solution remaining in this class; it is not legitimate to claim that all nearby initial data yield such a solution. Because `B(t)` changes, `K_B` explicitly depends on time and is not generally conserved. If a one-line background is a pure traveling wave, an appropriate moving frame adds the translation-momentum correction and removes explicit time dependence, but the lattice tangency obstruction remains.

## B. Necessary fixed-tail compatibility and a concrete no-go

For perturbations preserving the same bounded lattice far fields, the `p_t` tail in (A3) is

\[
\lim_{j\to\pm\infty}p_t=\mp\frac h2D^2m(x),
\qquad m(x)=\sum_jr_j(x).
\]

If `p_t∈S`, then `D²m=0`; decay in x forces `m=0`. Summing the second equation then forces

\[
m=0,\qquad n=\sum_j(Cp+Ar+pr)=0.\tag{B1}
\]

These are necessary, not sufficient. At a constant vacuum `(A,C)=(U₀,c)`, with `c≠0`, take `r=0`, `p_j=a_j f(x)`, finite nonzero `a`, `∑a=0`, and `f∈C_c∞`. Both (B1) hold. However

\[
\left.\partial_t n\right|_{t=0}=-cD\sum_jp_j^2
=-c\left(\sum_ja_j^2\right)D(f^2),\tag{B2}
\]

which does not vanish for nonzero compact `f`. Thus the two-moment constrained set is not invariant even for arbitrarily small data, and this does not depend on discretization error or a search failure.

The same obstruction occurs around line backgrounds. At `r=0`, require `∑C_jp_j=0`. The difference flux identity gives

\[
\partial_t n=D\sum_j[-2A_jC_jp_j-C_jp_j^2+p_jD C_j-C_jD p_j].\tag{B3}
\]

Choose two sites on which `C` has the same nonzero sign over the compact x support, and set

\[
p_j=\varepsilon f(x)\bigl(\delta_{j,j_1}/C_{j_1}(x)-\delta_{j,j_2}/C_{j_2}(x)\bigr).
\]

This meets both (B1). The quadratic coefficient in (B3) is

\[
-D\{f^2(1/C_{j_1}+1/C_{j_2})\},
\]

which is nonzero for a suitable compact `f`. Therefore the derivative cannot vanish for all sufficiently small `ε`. All the intended benchmarks approach `C=-4` along lattice ends, so two such sites exist on every compact x interval. This proves failure of a generic fixed-tail neighborhood around the benchmarks, as well as at vacuum.

To make a Schwartz trajectory preserve the far field, successive derivatives of (B1) impose further compatibility conditions. Merely listing these conditions does not produce an invariant Poisson manifold or an existence theorem.

## C. Why an arbitrary localized rank-one correction fails

If the first original equation and the chosen `R` gauge hold, its possible integration ambiguity is `a(x,t)·1`, because `ker d` consists of lattice-constant sequences. A correction `ρ_j λ(x,t)` with `ρ∈S`, `∑ρ=1`, changes the original equation by `dρ·λ`, which is nonzero unless `λ=0`. Hence a local mean reconstruction cannot reproduce the periodic reduction while keeping exact equivalence. A lattice-constant correction is excluded by fixed far fields; moreover its x derivative changes the constant far-field `w_t=-cD a` for `c=-4`. Periodic mean reduction cannot be transplanted unchanged to this infinite fixed-tail class.

## D. Honest conclusion

The simple candidate has a convergent relative functional and an exact formal variational identity, but a same-domain Hamilton theorem for generic localized perturbations of benchmarks 1a, 1b and two-soliton case has not been obtained. The established result is the concrete exclusion of `B+S` and its two-moment constrained subset as invariant phase spaces for this gauge and candidate. It does not exclude a different nonlocal Poisson reduction, a suitable enlarged phase space with dynamically controlled tails, a special invariant tau-function class, or another Hamilton structure. In particular it does not prove nonexistence of a Hamilton representation for the original equation.
