# Initial charge search on the relative Hamilton domain

Independent calculation, 2026-10-04. All domains and notation are those of `WEAK_HILBERT_HAMILTON_THEOREM.md`: background `B=(A,C)`, perturbation `q=(p,r)`, `β=h²/32`, graph domain `Y`, dynamic domain `D`, Hamilton functional `K_B` and bracket `{F,G}=⟨∇F,J₀∇G⟩`.

## 1. The finite translation momentum

The quadratic perturbation momentum

\[
P[p,r]=h\sum_j\int p_jr_j\,dx\tag{1}
\]

is finite and smooth on the ambient Hilbert space X by Cauchy–Schwarz. Its gradient and generated field are

\[
\nabla P=(r,p),\qquad J_0\nabla P=(-Dp,-Dr).\tag{2}
\]

Thus its flow is x translation of the perturbation, with the minus sign shown. This strongly continuous translation group preserves the K graph domain and the spectral test algebra. At states in D, `J₀∇P∈Y`, so the mixed bracket with `K_B` obeys the common domain conditions.

The background coefficients break translation invariance of `K_B`. A direct calculation gives

\[
\boxed{\{P,K_B\}=-h\sum_j\int\left[
\frac12(D C_j)p_j^2+(D A_j)p_jr_j+\beta(D C_j)r_j^2
\right]dx.}\tag{3}
\]

One proof uses `{P,K_B}=−⟨J₀∇P,∇K_B⟩`: all terms without background coefficients form x total derivatives, while the nonlocal quadratic term vanishes because D is skew, K is self-adjoint and they commute. The remaining coefficient terms integrate to (3). Equivalently translate p,r through a fixed reference and shift the bounded reference coefficients in the opposite direction. Each integral is finite on Y.

Equation (3) generally does not vanish, so P is not a conserved quantity in this moving-reference problem. For example choose `r=0` and a compact p at one lattice site where `D C` has a nonzero sign. Such a state belongs to D and makes (3) nonzero. This is a failure of the conservation identity as a functional identity on the common domain; no existence theorem for every such initial state is assumed.

## 2. Single-line backgrounds: a conserved comoving relative energy

For a single tau phase

\[
\theta=(p_{\mathrm s}+q_{\mathrm s})x+(q_{\mathrm s}^2-p_{\mathrm s}^2)t+\chi_hj+\theta_0
=(p_{\mathrm s}+q_{\mathrm s})(x-vt)+\chi_hj+\theta_0,
\]

the velocity is exactly

\[
v=p_{\mathrm s}-q_{\mathrm s}.\tag{4}
\]

The finite-h staggered U,w reconstructions depend on the same phase shifts, so

\[
A_t=-vD A,\qquad C_t=-vD C.
\]

Only the three quadratic coefficient terms of `K_B` explicitly depend on t. Therefore

\[
\partial_tK_B=h\sum_j\int\left[
\tfrac12C_t p^2+A_tpr+\beta C_t r^2\right]dx
=v\{P,K_B\}.\tag{5}
\]

Along a solution `q∈C¹(I;Y)∩C(I;D)` of the Hamilton equation, the graph-domain chain rule and skewness of J₀ give

\[
\frac{dK_B}{dt}=\partial_tK_B,
\qquad \frac{dP}{dt}=\{P,K_B\}.
\]

Consequently

\[
\boxed{F_B=K_B-vP\quad\text{is conserved}.}\tag{6}
\]

In the coordinate `y=x-vt`, the reference becomes stationary. The translated perturbation satisfies

\[
q_t=J_0\nabla(K_{B(0)}-vP),
\]

so (6) is the autonomous comoving relative Hamiltonian. It is finite and nonconstant on Y; for example at r=0 it contains `⟨C,p²⟩/2`.

For the requested original benchmarks:

| benchmark | spectral parameters | v | conserved relative energy |
|---|---|---:|---|
| 1a / A | `(p_s,q_s)=(1,2)` | −1 | `F_A=K_A+P` |
| 1b / B | `(p_s,q_s)=(4,−3)` | 7 | `F_B=K_B−7P` |

These are charges on two different reference problems. They are not two independent charges on one phase space. Also

\[
\{P,F_B\}=\{P,K_B\}
\]

is generally nonzero, so P and F_B do not form an involutive pair. The tautological `{F_B,F_B}=0` proves no pairwise involution or additional integral.

## 3. Two-line benchmark: excluding one elementary candidate family

The two-soliton benchmark C has `(p₁,q₁)=(6,−5)` and `(p₂,q₂)=(4,−3)`. Its individual arm speeds are 11 and 7. The interaction coefficient is `4/3`; the finite-h lattice phase slopes are distinct. As `|j|→∞` the two arm neighborhoods separate in x and converge to their respective single-line profiles, with a constant phase shift on one arm.

Consider only candidates

\[
Q=aK_C+bP,\qquad a,b\in\mathbb R\text{ constant}.\tag{7}
\]

Their on-shell derivative is the explicit quadratic functional

\[
\frac{dQ}{dt}=h\sum_j\int\left[
\frac12(aC_t-bDC)p^2+(aA_t-bDA)pr+
\beta(aC_t-bDC)r^2\right]dx.\tag{8}
\]

For (8) to vanish identically on the dynamic domain, arbitrary compact p with r=0 forces `aC_t-bDC=0` pointwise. Mixed p,r tests, with r having zero lattice sum and p supported at one of its sites, force `aA_t-bDA=0` as well. These tests lie in D.

If a=0, nonconstant C forces b=0. If a≠0, set `v=−b/a`; the conditions require

\[
C_t=-vDC,\qquad A_t=-vDA
\]

with one common constant speed. The separated arm limits would require v=11 and v=7 simultaneously, a contradiction. Hence no nonzero candidate (7) satisfies the universal conservation identity on this domain.

This excludes only constant linear combinations of `K_C` and the finite quadratic perturbation momentum P. It does not exclude another time-dependent correction, another relative charge, a higher-order nonlocal density or a compatible second Poisson structure. The search has not produced two independent commuting conserved quantities on the nonperiodic common domain, and Liouville integrability remains open.
