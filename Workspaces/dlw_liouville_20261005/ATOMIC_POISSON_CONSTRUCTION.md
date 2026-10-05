# A single N-independent Poisson observable algebra via finite atomic measures

2026-10-05. This supplies a concrete global observable representation for the zero-strength gluing in CROSS_N_GLUING_PROOF.md. It is a construction from the chosen soliton-moduli bracket, not a derivation of the original field J0. It does not turn an infinite atomic measure into a proved DLW solution.

## 1. Erasing zero slots becomes literal equality

Represent a finite soliton configuration by
 mu=sum_(i=1)^N S_i delta_(S_i,theta_i,c_i).
The first coordinate of each support point records S_i as well as its role as the atomic weight. Permuting labels changes nothing. A slot with S_i=0 contributes the zero measure, independently of theta_i,c_i, so deletion is exact equality of representations. For distinct active marks this is injective up to permutation; duplicate identical active marks are excluded by the regular spectral domain.

For a smooth test function phi(S,theta,c), set
 M_phi(mu)=integral phi dmu=sum_i S_i phi(S_i,theta_i,c_i).
Use finite cylindrical observables F=f(M_phi1,...,M_phir). Include smooth tests with polynomial growth in S,c and bounded-in-theta derivatives, and local compactly supported tests. This class contains all the polynomial spectral moments and H, separates finite atomic configurations, and is closed under the test-function bracket below. Localize this observable algebra when local charts are needed.

A Hausdorff initial topology can be specified by these separating observables. On bounded spectral sets zero-strength addition converges in these observables; local compact tests give the usual weak-measure information, while polynomial tests retain the declared moments. Do not identify this automatically with compact-local convergence of physical fields or with a particular Sobolev topology. Spectral escape to infinity requires additional moment control.

## 2. An N-independent bracket

On test functions define
 [phi,psi]_B=-S(phi_theta psi_c-phi_c psi_theta).
This is a Poisson/Lie bracket on the mark space: its bivector is -S partial_theta wedge partial_c, and S is a Casimir. In particular it obeys Jacobi.

For linear moment observables define
 {M_phi,M_psi}(mu)=M_[phi,psi]_B(mu),
and for cylinders extend by the chain rule:
 {f(M_phi),g(M_psi)}=sum_(a,b) f_a g_b M_[phi_a,psi_b]_B.

On every finite-atomic stratum, direct differentiation in the previously chosen parameter bracket {theta_i,c_j}=-delta_ij gives
 {M_phi,M_psi}_N=-sum_i S_i²(phi_theta psi_c-phi_c psi_theta)(S_i,theta_i,c_i),
which is exactly the stated measure expression. Thus it is independent of slot labels and of zero-strength padding. If two cylinder descriptions define the same function on the permitted atomic configurations, their pullbacks agree on every regular parameter chart, so their brackets agree there and on the glued faces. Jacobi and Leibniz follow either from the test Lie bracket's linear-Poisson construction or directly from the canonical charts. This proves a well-defined common Poisson algebra without writing N into its definition.

The algebra is rich enough locally: near any regular N-atom state, choose disjoint small spectral mark neighborhoods and cutoffs vanishing near S=0. Moment tests supported in those neighborhoods recover the individual S,theta,c coordinates locally. Consequently it reproduces the full local canonical bracket and rank2N, not merely a small algebra of commuting constants.

## 3. One Hamiltonian, one hierarchy

The same functions work on the whole glued finite-atomic set:
 H(mu)=M_(c²/2)(mu),
 C_k(mu)=M_(b_k)(mu),
 b_k(S,c)=[((S+c)/2)^k-((c-S)/2)^k]/(k S),
where b_k is extended polynomially at S=0. The numerator is odd in S and divisible by S, so there is no singularity. Its value there is (c/2)^(k-1).

Because the tests c²/2 and b_k are theta-independent, all their brackets vanish. At N active atoms they are exactly H_N and C_k^(N). At a zero-strength boundary the measure loses the atom and all these observables retain the lower-N value.

For any M_phi,
 {M_phi,H}=integral [-S c phi_theta]dmu.
Thus the Hamiltonian flow is the pushforward of mu under
 (S,theta,c)->(S,theta-S c t,c).
It is exactly the soliton parameter time flow. Active N stays fixed along a trajectory; the closure connects initial states with different N but is not a particle-creation evolution.

Each regular N-atom stratum retains the fixed-S Liouville description. The sequence C_k is common to all strata, but it is not infinitely functionally independent at an N-atom point: the spectral part has at most2N independent variables there and a fixed-S leaf needs N commuting integrals.

## 4. Physical realization and the boundary

Restrict the atomic set to admissible finite configurations satisfying the previously stated positive, nonresonant soliton conditions. On each regular stratum the tau-to-field map is the established moduli realization. The zero-strength tau factor cancellation proves that this map respects zero-slot erasure, while the uniform positive-polynomial estimate in CROSS_N_GLUING_PROOF.md proves physical convergence along these attachment charts.

This is a stronger statement than using the same formula separately for each N: the same observables and Poisson algebra are defined on an actual common set of finite atomic configurations, and the physical zero-strength boundary is compatible with them.

Still unresolved: a globally Whitney-stratified embedding of the physical image, resonant/coincident spectral strata, general unbounded spectral limits, the original field bracket, and physical DLW solutions for infinitely many atoms. The measure construction can be written formally on broader measure spaces, but no such broader physical theorem is claimed.
