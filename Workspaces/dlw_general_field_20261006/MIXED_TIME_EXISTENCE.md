# A mixed-time analytic realization of the periodic field hierarchy

2026-10-06. Constructive proof draft for arbitrary fixed finite lattice period M>=2. This supplements the algebraic hierarchy with actual general-field solutions, not an open-set Sobolev Cauchy flow.

## 1. Exact forward/backward splitting

Use the same variables, closure and R as RESEARCH_NOTES.md. Introduce A=p+(R/2)s. Since R is a constant finite skew matrix and commutes with D, the reduced equations become

A_t=-A_xx+D F(A,s),
s_t= s_xx+D G(A,s),

where p=A-Rs/2, b=(gamma-Pi(ps))/c, U=b+p,w=c+s,
F=-P0(U²/2+beta w²)-(R/2)(Uw),
G=-P0(Uw).

All products are pointwise in x and componentwise in j. F,G are polynomial maps with no x derivatives. Their coefficients depend on the fixed finite matrix R and on h,c,gamma. A,s retain zero lattice average. This identity follows by substituting the p,s equations; the cross second derivative cancels exactly. No change of time or of the physical field equations is made.

The principal matrix in (p,s) is [[-I,-R],[0,I]], and the shear T=[[I,R/2],[0,I]] conjugates it to diag(-I,I). Because R*=-R, T also preserves Jred=-[[0,P0 D],[P0 D,0]]. This is a Poisson change of variables, not a dissipative replacement of the equation. The finite-M identities were additionally checked exactly for M=2,...,8.

## 2. Local mixed boundary theorem and proof

Fix r>1/2 and the real periodic vector space X=H^r(T_L;R^M) intersect ker Pi. Prescribe A(T)=A_T and s(0)=s_0 in a bounded subset of X. There is a sufficiently small T>0 such that a unique solution in a chosen bounded ball of C([0,T];X×X) satisfies

A(t)=exp((T-t)D²) A_T - integral_t^T exp((tau-t)D²) D F(A(tau),s(tau)) d tau,
s(t)=exp(tD²) s_0 + integral_0^t exp((t-tau)D²) D G(A(tau),s(tau)) d tau.

Proof: H^r in one dimension is a Banach algebra for r>1/2. Thus the polynomial maps F,G are locally Lipschitz in X, with bounds B_R and L_R on a radius-R ball. The heat multiplier obeys
||exp(tD²)||_{H^r->H^r}<=1,
||D exp(tD²)||_{H^r->H^r}<=1/sqrt(2 e t).

Both integrals therefore have norm at most sqrt(2/e) sqrt(T) B_R, and their differences at most sqrt(2/e) sqrt(T) L_R times the sup norm difference, when the product norm and constants are chosen consistently. Choose R strictly larger than the endpoint-data bound, then T so the ball maps into itself and the latter Lipschitz constant is <1. Banach's fixed point theorem proves existence and uniqueness in that ball. The same estimate proves continuous, locally Lipschitz dependence on mixed endpoint data. Since F,G are polynomial, the contraction/implicit-function argument gives analytic dependence locally in those data.

Interior regularity: on any closed subinterval strictly inside (0,T), heat smoothing and the integrable bound t^{-(1+alpha)/2}, 0<alpha<1, bootstrap spatial regularity from H^r to H^(r+alpha). Use nested time subintervals and iterate. Thus solutions are smooth in the interior, with time regularity then following from the equations. Smooth endpoint data allow the corresponding higher-order boundary regularity. Every finite-order conserved functional is meaningful and constant on the smooth interior.

This is a theorem about prescribing one component at each time end. The initial pair (A(0),s(0)) is an output subject to the solvability condition, not arbitrary independently prescribed Cauchy data. It is fully compatible with the previously proved high-frequency obstruction to an open Sobolev Cauchy flow.

## 3. Retaining the actual Hamiltonian structure

For fixed component x means, use zero-mean variations and canonical coordinates Q=s, P=D^-1 A (subtract fixed means in these definitions). The bracket becomes {Q,P}=identity on the projected function space, using the weighted h sum integral pairing. The Hamiltonian is exactly the old K expressed through p=A-Rs/2, not a newly invented endpoint energy.

For sufficiently regular mixed solutions, define the type-II action
S_T(Q_0,P_T)=<P_T,Q(T)> - integral_0^T [<P,Q_t>-K(P,Q)] dt.
The standard variation, integrating the P delta Q_t term by parts and using Hamilton's equations, gives

d S_T = <P(0),delta Q_0> + <Q(T),delta P_T>.

Consequently the mixed endpoint map defines a canonical relation between the initial and terminal states. Equivalently, the pullbacks of the symplectic two-forms from the two time ends agree. On these infinite-dimensional spaces the symplectic form is weak; this variation identity does not assert a strong Banach cotangent equivalence or a globally surjective initial-data map.

## 4. Nontriviality and independent conserved blocks on actual solutions

The algebraic trace identities persist along every smooth mixed-boundary solution, since these solve the same physical equations. They are not special solitons.

For any fixed finite set of nonzero x Fourier modes, the linearized constant-background system is a finite-dimensional ODE. Its mixed endpoint problem is uniquely solvable for small T by the same contraction argument. Evaluation at an interior time is invertible on this finite Fourier space: any prescribed finite-mode state extends by the ODE to both endpoints, and these endpoint values recover it uniquely. Thus one can choose finite-mode endpoint variation directions whose first-order fields at an interior time equal the earlier independent b-mode witness (s=0, p0=2b,p1=-2b, other p=0).

The nonlinear solution depends analytically on the endpoint amplitudes. At uniform equilibrium the first variation of each translation-invariant local spectral functional is constant in x and hence vanishes on our fixed-mean tangent space. Consequently the order-epsilon² spectral variation is its quadratic form on that chosen first-order witness; second-order changes in the solution do not alter it. The same Vandermonde Jacobian argument applies to any prescribed finite odd-trace block. This realizes the generic independence certificates on actual non-soliton trajectories, not merely hypothetical field configurations. It still does not prove spectral completeness of the hierarchy.

## 5. Numerical corroboration, separate from the proof

mixed_time_probe.py uses M=3, h=1/8, c=-4, gamma=-16, T=.02 and three-site smooth trigonometric mixed endpoint data. It solves the coupled heat integral equations by Picard iteration with exact heat multipliers and second-order exponential quadrature in time; x has 64 Fourier points. No tau function is used.

For 32,64,128,256 time steps, Picard converged in 9 iterations to an increment approximately 2e-15. Hamiltonian drift was 1.57e-10,3.92e-11,9.78e-12,2.44e-12; Q4 drift was 1.10e-9,2.74e-10,6.85e-11,1.71e-11. Drift decreases by about four under time-step halving. Mean closure errors were at roundoff. These are numerical checks of implementation and compatibility, not a replacement for the fixed-point or conservation proofs.

## 6. Literature orientation and next boundary

A related use of short-time contraction for backward-forward parabolic systems is Cirant--Gianni--Mannucci, arXiv:1806.08138, https://arxiv.org/abs/1806.08138 . Their paper concerns mean-field games; the DLW polynomial shear and the estimates above are our direct derivation, not an application asserted without checking hypotheses.

Established in this draft: an all-finite-M mixed-time existence construction on an infinite-dimensional general field class, preserving the actual field Hamiltonian and every already proved spectral conservation law, with a canonical endpoint relation and independent finite conserved blocks realized on actual smooth solutions.

Still a separate mathematical target: complete spectral/action coordinates and maximality/completeness of the commuting algebra. Infinite independence alone does not answer that stronger question. The mixed-boundary construction does not provide an arbitrary-initial-data Liouville flow; it provides an analytically meaningful realization of the original integrable equations despite the Cauchy instability.
