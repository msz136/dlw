# Cross-N gluing through zero spectral strength

2026-10-05. Constructive proof draft. A compatible cross-stratum Poisson observable algebra and exact tau deletion are established below. This does not assert that the resulting quotient is a globally Whitney-stratified or finite-dimensional smooth manifold, nor that its Poisson structure is inherited from the original DLW field bracket J0.

## 1. The two ways a pulse can disappear are different

In the established standard soliton parameters,
S_i=p_i+q_i>0, c_i=p_i-q_i, E_i=exp[S_i(x-c_i t)+theta_i] chi_i^j.
The chosen parameter bracket is {theta_i,c_j}=-delta_ij, with every S_i a Casimir. This is the same bracket as {Q_i,P_j}=delta_ij with Q=-theta/S and P=Sc on S>0. Its Hamiltonian is H_N=(1/2)sum S_i c_i².

If theta_* tends to minus infinity at fixed positive S_*,c_*, the extra pulse leaves every compact x,j observation region and the tau functions tend locally to the lower-N tau functions. Nevertheless C1 changes by the nonzero S_*, and every spectral coefficient retains that pulse's contribution. Thus a ghost-free identification by this local amplitude-deletion limit cannot keep the prescribed C1 continuous. This is an obstruction for that topology and that conserved hierarchy, not for all possible gluings. A boundary retaining the lost spectral data would describe a pulse at infinity, not the ordinary lower-N state.

Instead use S_* -> 0 with c_* bounded and away from the poles described below. This eliminates the extra spectral contribution as well as the physical pulse. It is the gluing used in the construction.

## 2. Exact zero-strength tau cancellation

Put r_i=c_i-2a. Then
 gamma_i=-(S_i+r_i+h)/(S_i-r_i-h),
 chi_i=[(S_i+h)²-r_i²]/[(S_i-h)²-r_i²],
 A_ij=[(S_i-S_j)²-(c_i-c_j)²]/[(S_i+S_j)²-(c_i-c_j)²].
At S_*=0, provided r_* != +/-h and (c_*-c_i)² != S_i²,
 gamma_*=chi_*=1, A_i*=1, E_*=exp(theta_*).
Split the subset expansion into subsets excluding or including *. Exactly,
 G_(N+1)=(1+exp(theta_*))G_N,
 F_(N+1)=(1+exp(theta_*))F_N,
 G_(N+1),next=(1+exp(theta_*))G_N,next.
The common positive factor is independent of x,j,t, so it cancels from u=Dlog(F²/(G Gnext)), W=(4/h)Dlog(Gnext/G), and v=W+delta0 u. The extra slot has precisely zero physical effect, independently of its residual theta_*,c_*.

Several zero-strength slots yield the product of these common factors; deletion order does not matter. Work in local nonresonant slot charts where mutual denominators stay nonzero; distinct inactive velocities can always be selected. Coincident inactive spectral poles are not being assigned a value by cancelling an undefined 0/0 expression.

Every old regular state has such a zero-strength attachment chart: choose c_* sufficiently far from the finitely many forbidden velocities, also with |c_*-2a|>h. For sufficiently small positive S_*, the new gamma and chi are positive, 0<chi<1, and all new A_i*>0. Generic small positive S_* avoids subset-exponent resonances. Thus the lower-N stratum is actually approached by regular higher-N states, not merely adjoined formally.

## 3. Physical convergence is stronger than compact-local convergence

Fix old regular spectral parameters and keep c_* in a compact region away from the forbidden denominators. Each new coefficient gamma_*,chi_*,A_i* is 1+O(S_*). For any of the three tau functions, compare it with (1+E_*) times the corresponding old tau. Coefficients of terms without * agree; ratios of coefficients of terms with * are 1+O(S_*), uniformly over the finitely many subsets. All monomials are positive.

Consequently the new tau divided by this reference is between 1-C S_* and 1+C S_*, uniformly over ALL positive E_i,E_*. In particular this holds uniformly in x,j,t and theta_*.

For x derivatives of logarithms, use the finite exponential-sum identity: D log tau is the mean of its finitely many x slopes under the normalized positive monomial weights, and higher derivatives are their cumulants. Coefficient perturbation changes these normalized weights by O(S_*) in total variation. All x slopes remain bounded by sum S_i+S_*. Hence each fixed-order log derivative changes by O(S_*), uniformly. The reference log(1+E_*) cancels from the physical tau combinations. Therefore, for every fixed nonnegative m,
 sup_(x,t,j) |D_x^m(u_(N+1)-u_N)|+|D_x^m(W_(N+1)-W_N)| <= C_m S_*.
The corresponding v estimate follows from the fixed-h centered difference. This estimate is local in bounded regular spectral charts; no uniform claim is made for unbounded c_* or approach to a denominator pole. It is a finite-positive-sum argument, not a numerical convergence claim.

## 4. What is glued and what counts as a smooth observable

Take finite labeled slot charts with S_i>=0, theta_i,c_i real and the preceding denominator/positivity conditions locally satisfied. Identify permutations and erase slots with S_i=0. An active N-slot state then belongs to the N-soliton stratum. The residual theta,c of an erased slot are not physical coordinates. At each finite slot cap M this gives a quotient with strata N=0,...,M. Increasing caps introduces no actual infinite sequence of pulses.

Define a compatible observable F as a family of symmetric functions F_N on the active charts whose pullbacks extend smoothly to admissible zero-strength faces and satisfy
 F_(N+1)|_(S_*=0)=F_N,
independently of theta_*,c_*. Require the analogous compatibility on every multiple-zero face. Smoothness is local in the slot charts; take the localized smooth-function closure of this compatible algebra. One can equip the quotient with the final topology of these charts. This is an explicitly defined differential/observable framework, not an assertion about a preselected Sobolev topology.

On each active stratum define
 {F,G}_N=-sum_i (F_theta_i G_c_i-F_c_i G_theta_i).
At a zero-strength face, F_theta_*=F_c_*=G_theta_*=G_c_*=0, since the boundary values are independent of the erased marks. The remaining terms restrict to the old bracket. Thus
 {F_(N+1),G_(N+1)}|_(S_*=0)={F_N,G_N}.
The bracket is therefore closed on compatible observables and well-defined after erasure. Antisymmetry, Leibniz and Jacobi hold chartwise and hence on the compatible algebra. Multiple-face compatibility is automatic and deletion order is immaterial.

This can equivalently be viewed as Poisson reduction at each Casimir face followed by restriction to functions constant in the irrelevant zero-slot variables. The whole unrestricted slot Poisson tensor does not descend on arbitrary non-invariant functions. The observable restriction is essential.

Physical field evaluations and their x derivatives belong to this algebra: their tau expressions are smooth at the admissible zero-strength faces and have the exact lower-N boundary values proved above. Hence their brackets restrict consistently too.

## 5. The Hamiltonian and the whole spectral hierarchy glue

For all finite N set
 H_N=(1/2)sum S_i c_i²,
 C_k^(N)=(1/k)sum[((S_i+c_i)/2)^k-((c_i-S_i)/2)^k].
Every added summand in C_k is a polynomial divisible by S_i; the Hamiltonian summand also vanishes at S_i=0. These are compatible smooth observables, not just separate formulas on disconnected strata. They therefore give a single H and a single C_k on the glued finite-soliton differential space.

Their brackets vanish identically because they are independent of theta. H generates
 Sdot_i=0, cdot_i=0, thetadot_i=-S_i c_i,
which agrees with the exact tau evolution and respects the zero-slot identification. Each active N stratum, and each fixed-S leaf inside it, remains invariant. A physical trajectory does NOT create or destroy a soliton under this flow; gluing describes limits of different initial states, not a time-dependent change of soliton number.

The formal transmission factor also glues:
 T_i(z)=[z+(S_i-c_i)/2]/[z-(S_i+c_i)/2] ->1 at S_i=0,
with the coincident numerator/denominator treated as a removable rational factor. Thus T_(N+1) becomes T_N, consistently with all the C_k.

The lattice shift theta_i->theta_i+log chi_i, c_i->c_i is canonical on each S leaf and becomes the identity on an erased slot. The pairwise scattering shift involves log A_i*, which tends to zero for an erased slot; away from velocity-order collisions it is likewise compatible with this boundary. These facts strengthen the gluing beyond the time Hamiltonian alone.

## 6. Strength and remaining limits

Established as a constructive proof draft:
- Exact deletion of zero-strength slots in the nonlinear physical tau formula for every finite N
- Uniform physical convergence in regular bounded spectral charts
- A consistent Poisson bracket on the explicitly specified cross-N compatible observable algebra
- A common Hamiltonian, common commuting spectral hierarchy and compatible lattice/time dynamics
- The previously proved Liouville structure on each active fixed-N, fixed-S regular leaf

Not established:
- A single smooth symplectic manifold containing every N; dimensions and ranks change at the boundary
- A full Whitney-stratification or globally embedded quotient theorem in a specified ambient function space
- A countably infinite soliton state, convergence of its tau determinant, or infinite sums of charges
- Original J0 inheritance, or a Hamiltonian flow that changes N
- Smoothness across arbitrary resonance/collision poles or unbounded spectral escape

One must not call the entire union one ordinary finite-dimensional Liouville system. The precise positive result is compatible finite-N Poisson/Hamiltonian gluing across zero-strength strata, with leafwise Liouville integrability on the regular strata. Formal singular-reduction theorems cannot be imported without checking their properness and topology assumptions.

## References for terminology only

Sjamaar and Lerman, Stratified symplectic spaces and reduction, Annals of Mathematics 134 (1991), 375-422, https://annals.math.princeton.edu/1991/134-2/p05 . This motivates considering singular spaces with compatible Poisson structures; our slot quotient is not claimed to satisfy that paper's reduction hypotheses.

Lê, Somberg and Vanžura, Poisson smooth structures on stratified symplectic spaces, https://arxiv.org/abs/1011.0462 . The present argument specifies its observable algebra directly rather than assuming a canonical stratified smooth structure.

## Certificate

cross_n_certificate.py verifies the zero-strength rational identities, all three tau-factor cancellations at three slots, general-form compatible-observable bracket restriction, and spectral polynomial cancellation through order12. The all-N and all-order proofs are the subset pairing and divisibility arguments above, not extrapolations from those finite tests.
