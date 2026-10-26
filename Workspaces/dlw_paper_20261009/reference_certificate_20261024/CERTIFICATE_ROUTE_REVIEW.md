# Full-continuum certificate route: independent review

2026-10-24. Mathematical review for the requested nonlinear reference at T=0.01. This document supplies a precise certificate test and identifies why the present finite computations do not yet pass it. It does not certify a reference or assert nonexistence for the specified Gaussian or sinusoidal data.

**Subsequent correction, 2026-10-24:** `TAIL_MAJORANT_REVIEW.md` proves that (R2) has no summable nonnegative supersolution whenever any nonzero Fourier frequency carries a positive error or residual seed. Thus (R2) is a retired route for the present numerical candidates, not an outstanding envelope-search task. The original conditions below are retained to identify exactly what fails. `ACTUAL_DATA_REVIEW.md`, independently checked in `ACTUAL_DATA_INDEPENDENT_REVIEW.md`, additionally excludes finite-order Gevrey-y regularity at positive time for the actual sinusoidal data, conditional on smooth existence. Neither result proves nonexistence in every classical solution class.

## 1. A useful exact physical-field formulation

Put z=y+2 in [0,ell], ell=4, and I f(z)=integral_0^z f(s) ds. With the prescribed u(x,0,t)=0 define

    a=u_y+v,  b=u_y-v,  u=I(a+b)/2,  v=(a-b)/2.

The full nonlinear DLW equations imply, exactly,

    a_t=-a_xx-[(u+4)a-4u]_x,
    b_t= b_xx-[(u+4)b+4u]_x.

Conversely these equations and u=I(a+b)/2 recover the physical equations and the lower u boundary. In the advected x coordinate the 4 a_x and 4 b_x terms disappear:

    a_t=-a_xx-(u a)_x+4u_x,
    b_t= b_xx-(u b)_x-4u_x.                 (R1)

This formulation is useful for certification because physical v is an algebraic combination of a,b. A certificate for a,b does not need a separate numerically differentiated y reconstruction of v.

## 2. An explicit all-mode sufficient certificate

The periodic Fourier frequencies are xi_n=2 pi n/192. Let abar,bbar be a reference trajectory, with ubar=I(abar+bbar)/2. All y and time reconstructions used to define these functions must be explicit. Let rho_a,n(t),rho_b,n(t) enclose the full continuous residual of (R1), in a Banach algebra B of y functions. One choice is C^1([0,4]) with ||f||_B=||f||_infty+||f_y||_infty; then ||I||_B<=J=5. Let A_n,B_n,U_n bound the B norms of the Fourier coefficients of abar,bbar,ubar, respectively.

Seek nonnegative, continuous envelopes alpha_n(t), beta_n(t) for the Fourier coefficients of a-abar,b-bbar. Set

    gamma_n=J(alpha_n+beta_n)/2,
    P_a,n = 2 J |xi_n| (alpha_n+beta_n)
          + |xi_n| [ U*alpha + gamma*A + gamma*alpha ]_n,
    P_b,n = 2 J |xi_n| (alpha_n+beta_n)
          + |xi_n| [ U*beta + gamma*B + gamma*beta ]_n.

Here * is convolution over every integer Fourier index. A sufficient envelope test is

    alpha_n(t) >= exp(xi_n^2 t) e_a,n
                 + integral_0^t exp(xi_n^2(t-s)) [rho_a,n(s)+P_a,n(s)] ds,
    beta_n(t)  >= exp(-xi_n^2 t) e_b,n
                 + integral_0^t exp(-xi_n^2(t-s)) [rho_b,n(s)+P_b,n(s)] ds,  (R2)

for every n and every t in [0,T]. The initial e_a,n,e_b,n enclose the exact prescribed initial functions minus the reference initial functions. The factor 2 J in the linear coupling follows from 4||I(e_a+e_b)/2||.

An all-mode proof must also establish summability, for example a uniform finite sum of (1+xi_n^2)(A_n+B_n+alpha_n+beta_n), together with time regularity and y regularity adequate for (R1). Under these hypotheses the Fourier series define classical fields. The standard first-exit comparison, initially with strict versions of (R2), bounds each finite Fourier approximation; uniform tails and compactness yield a solution of the continuum equations. Identifying this solution as the unique solution in a broader class would require a uniqueness argument in that class; it cannot be inferred from an ordinary-norm Gronwall inequality. This is a proof scheme, not a completed existence theorem for the current data: its decisive hypothesis is the all-mode supersolution (R2).

At the terminal time the requested physical error bounds follow explicitly:

    eta_u <= (ell/2) sum_n (alpha_n(T)+beta_n(T)),
    eta_v <= (1/2) sum_n (alpha_n(T)+beta_n(T)).                 (R3)

One can use ell=4, rather than J=5, in (R3), because only physical sup norms are required there. Arithmetic enclosures, time residuals, y reconstruction residuals and x tails enter (R2), rather than being counted independently a second time in (R3).

This test is genuinely checkable if a finite list of envelopes plus an analytic formula for every remaining mode is provided and all inequalities are enclosed on full time intervals. It is not passed by residual samples, by a finite number of modes, or by computing two trajectories at different precisions.

## 3. The obstruction is also in the interior

The known exact lower-boundary heat/antiheat formulas do not remove the interior high-frequency issue. Linearize (R1) at zero and take one x Fourier mode. On a,b the operator is

    A_xi = diag(xi^2,-xi^2)
         + 2 i xi I [[1,1],[-1,-1]].                         (R4)

Fix any z0<4 and restrict to pairs of continuous functions vanishing on [0,z0]. This is an invariant space for I and for (R4); hence all these perturbations have identically zero lower traces. The Volterra operator on this space is compact and quasinilpotent. Direct block multiplication gives

    A_xi^2 = (xi^4 Id + 4 i xi^3 I) Id_2.

Equivalently the block resolvent determinant is

    (lambda^2-xi^4) Id - 4 i xi^3 I.

It is invertible when lambda is not +/-xi^2, because the Volterra spectrum is {0}. To check both remaining spectral points without inferring invertibility from a formal determinant alone, choose continuous, rapidly oscillating functions f_j supported away from the lower strip, with ||f_j||=1 and ||I f_j|| tending to zero. For example a smooth fixed cutoff times sin(j z), normalized, has this property by integration by parts. The vectors (f_j,0) and (0,f_j) are approximate eigenvectors of (R4) for +xi^2 and -xi^2, respectively. Thus

    spectrum(A_xi)={+xi^2,-xi^2},
    ||exp(t A_xi)|| >= exp(t xi^2).                           (R5)

This is a continuous-y, interior statement, not an Endpoint-SD spectral calculation. It applies even after all lower traces are imposed exactly. It rules out a frequency-independent ordinary-norm forward stability estimate at the zero solution. It does not establish nonexistence or a quantitative instability rate about either particular nonlinear reference trajectory.

## 4. Why the obvious infinite-tail norms do not close (R2)

Consider the customary weighted Fourier l1 norm with positive, symmetric, submultiplicative weights w_n and w_0=1. Submultiplicativity, needed to bound quadratic products in the same norm, gives w_n<=w_1^|n|. Thus the weight grows at most exponentially. The antiheat multiplier exp(xi_n^2 T) is unbounded from this space to any Fourier norm dominating physical amplitude for every T>0. Ordinary analytic-strip weights do not solve the problem.

A Gaussian weight exp(sigma n^2) can control a linear antiheat evolution for times shorter than its available Gaussian radius. It is not a Banach-algebra weight. For a single n-mode, the ratio between the weighted norm of its square and the square of its weighted norm is exp(2 sigma n^2), which is unbounded. Thus it is invalid to combine a Gaussian antiheat bound with an ordinary same-space quadratic Lipschitz estimate. Calling the datum entire or Gevrey does not supply the missing product estimate.

The approved periodic Gaussian has an adequate Gaussian Fourier tail initially, and the sinusoid has finite Fourier support initially. Neither fact supplies a propagated nonlinear tail satisfying (R2). Nonlinear convolution can generate every harmonic. Even if a polynomial reference has a residual supported only through 2N, the error generated by that residual subsequently participates in the nonlinear convolution; it is not restricted to 2N.

These facts identify a specific failed verifier, rather than prove the actual nonlinear solution does not exist. A different certificate may exploit additional nonlinear structure or a rigorously known admissible solution manifold. That structure has not been established here.

## 5. What finite reference convergence establishes and what remains

Suppose the N-mode candidate and its time integrator are enclosed rigorously. Such an enclosure controls the finite projected ODE only. To promote it to (R3), one still needs all unresolved alpha_n,beta_n in (R2), or a different rigorous infinite-dimensional argument providing the same information. Agreement of N and 2N, even to arbitrary precision, bounds neither the first omitted unstable mode nor subsequent nonlinear transfer to it.

An exact linear diagnostic makes this distinction explicit. At any omitted Fourier index n, terminal amplitude d can coexist with zero residual and initial amplitude d exp(-xi_n^2 T). Alternatively a zero-initial-error forcing of magnitude approximately d xi_n^2 exp(-xi_n^2 T) can produce terminal amplitude d. Finite retained-mode observations miss both. This is an estimator counterexample, not a modification of the specified initial data and not evidence that the current reference has such an error.

Current eligibility result: no verified all-mode envelope, no full nonlinear continuum residual-stability theorem, and therefore no finite numerical eta_u,eta_v is justified. The computable finite reference values may be delivered as candidate data with their actual convergence diagnostics. They must not be called an error-certified continuous solution, and the target inequality eta_q <= 0.01 ||q_num-q_ref|| cannot yet be asserted.

The proposed search for an all-mode supersolution of (R2) is now ruled out by `TAIL_MAJORANT_REVIEW.md`. A different, data-specific continuum argument is required. Further finite grid or precision refinements cannot repair that failed test, and no such alternative certificate has been established here.

