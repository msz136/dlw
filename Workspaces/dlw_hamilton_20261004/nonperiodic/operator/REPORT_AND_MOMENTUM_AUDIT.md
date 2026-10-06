# Independent audit of report Sections 8–11 and momentum correction

2026-10-04. Source inspected: `Workspaces/dlw_hamilton_20261004/report.src.html`. No direct report edits made.

## Report audit

The graph-domain functional and the dynamic-domain equivalence theorem are consistent. The first variation is an `X` covector on the dense graph domain, and `D`-regularity of the gradients follows on the displayed dynamic domain. The original-equation first residual has no free mean term because `ker d` on `ℓ²_jL²_x` is zero. The dense smooth cylinder algebra is bracket closed, and its Jacobi identity follows from a constant skew matrix for each finite collection of test kernels. Mixed Jacobi with two cylinder functions and one relative Hamiltonian is valid on the dynamic domain: test Hamilton directions lie in the graph domain, the Hamiltonian Hessian is symmetric there, and its action on these directions has the required `H¹` regularity.

The physical-variable shear identity `S J₀ S*=J₀` is correct, and the explicit reference drift in physical coordinates is indispensable. The far-field claims follow from the `ℓ²H¹_x` embedding into `C₀(ℤ×ℝ)`; they concern domain snapshots and do not prove domain persistence under evolution.

Two small clarifications make the definitions fully explicit:

1. State `dK=MD` on `DomK∩DomD`; the unqualified identity is only a formal operator shorthand. All applications in the theorem lie in this common domain.
2. Under the physical shear, the graph and dynamic domains are `S Y` and `S𝒟`. Replacing `r` by physical `q=δv` without transforming the domain would change the theorem. `C(I;𝒟)` may be understood in the norm `‖y‖X₂+‖Kr‖H¹`.

## Relative momentum and a conserved correction

Define the finite momentum

\[
P[p,r]=h\sum_j\int p_jr_j\,dx,\qquad \nabla P=(r,p),\qquad J_0\nabla P=-D(p,r).
\]

On the dynamic domain,

\[
\{P,\mathcal K_B\}
=-h\sum_j\int\left[\frac12w_{*,x}p^2+U_{*,x}pr+\beta w_{*,x}r^2\right]dx.
\tag{A}
\]

Proof: write the bracket as `⟨Dr,g_w⟩+⟨Dp,g_U⟩`. Cubic terms form a total x derivative; `rDp` terms cancel. The nonlocal term is `⟨Dr,Kr⟩=0`, since `r∈H¹`, `Kr∈H¹` implies `Dr∈DomK`, and self-adjointness plus commutation with `D` makes this pairing its own negative. Integration by parts in the remaining background-weighted quadratics gives (A). All terms are absolutely integrable.

For a fixed-speed reference `B_t=−vB_x`,

\[
\partial_t\mathcal K_B=v\{P,\mathcal K_B\}.
\]

Therefore along sufficiently regular paths `C¹(I;Y)∩C(I;𝒟)` solving the relative Hamilton equation,

\[
\frac d{dt}(\mathcal K_B-vP)=0.
\]

For A, `v=p−q=−1`, giving `\mathcal K_A+P`; for B, `v=7`, giving `\mathcal K_B−7P`. These are valid conserved, explicitly reference-dependent relative quantities; `P` itself is generally not conserved. Under the physical shear,

\[
P=h\sum_j\int \delta u_j\delta v_j\,dx,
\]

because `⟨p,δ₀p⟩=0`.

## Why no constant linear combination works universally for C

For a constant combination `a\mathcal K_C+bP`, its time derivative on the relative flow is

\[
h\sum_j\int\left[
\frac12(a w_{*,t}-b w_{*,x})p^2
+(aU_{*,t}-bU_{*,x})pr
+\beta(a w_{*,t}-b w_{*,x})r^2\right]dx.
\]

Universal vanishing for all dynamic-domain states forces the background coefficients to vanish: arbitrary compact-x, finite-site `p` with `r=0` first detects the `p²` coefficient. The remaining cross coefficient can then be tested using admissible dense zero-lattice-mass `r` and finite-site `p`. If `a=0`, nonconstant benchmark profiles force `b=0`. If `a≠0`, it requires a single transport speed `v=−b/a` for the entire background. The two separated asymptotic arms of C have nonconstant profiles and speeds 11 and 7; differentiating their exact asymptotic profiles forces both `v=11` and `v=7`, a contradiction. Thus no nonzero constant combination of these two candidates is conserved for every allowed perturbation around C.

This only excludes the span of these two candidates. It does not exclude other charges, higher-degree functionals, or explicitly time-dependent conserved quantities. No independent pair of commuting charges follows from this calculation.
