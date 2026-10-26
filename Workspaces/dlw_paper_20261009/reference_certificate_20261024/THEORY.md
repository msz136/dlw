# Certified reference for nonlinear DLW: target and feasibility

2026-10-24. Proof draft with exact algebraic checks; no certified nonlinear continuum reference has been obtained. Numerical diagnostics are separate from the statements below.

Latest continuation is in BOUNDARY_THEOREM.md. The user approved replacing the old truncated-periodic Gaussian by its smooth periodic SUM. The old-data setup and diagnostics below are retained with their original scope. Exact lower-boundary evaluation certificates are now available; no full-domain certificate is implied.

## 1. Fixed target

The intended continuum system has a=2, lambda=-2:

    u_yt = -v_xx - [(u+2a)u_y]_x,
    v_t  = -u_xxy - [(u+2a)v-4u]_x.

Use x in [-96,96) periodic, y in [-2,2], u(x,-2,t)=0. The initial profiles are e(y)=sin(pi(y+2)/4), with Gaussian (u,v)=(.05,.03)e(y)exp(-(x/6)^2), or sinusoidal (.03 e(y)cos(pi*x/12), .02 e(y)sin(pi*x/12)). Initial and boundary compatibility and the function space must be part of an existence/stability theorem. No extra v=0 boundary condition at later times is imposed. No linearization replaces the nonlinear target.

Old FD code uses frozen-background quadratic ghost extrapolation at the upper y endpoint, and frozen lower ghost values. These are numerical closure rules, not an already-proved convergent continuum boundary prescription. New full-potential Centered-SD has a separate lower auxiliary w trace; matching a common continuum problem requires checking this trace. None of these issues are resolved by time refinement.

## 2. Requested certificate

For each physical field in a specified norm, prove ||q_ref(T)-q(T)|| <= eta(T). If D=||q_num(T)-q_ref(T)||, require eta <= .01 D. Then max(0,D-eta) <= ||q_num-q|| <= D+eta. A common vector max-norm certificate can be used for each component, but the budget must be tested against each component's D, not only the larger discrepancy. Native-grid discrepancies certify only those evaluation points; a continuum supremum requires controlled reconstruction/interpolation.

A high-precision numerical value is not exact. The certificate must account for initial representation, time reconstruction, full continuous PDE residual, boundary closure, unresolved spatial modes, and roundoff/enclosure arithmetic. Errors must be counted once under a coherent norm and boundary lift.

## 3. Conditional residual bound (proof draft)

Let X be a normed solution space in which the actual initial-boundary problem has local existence and a continuation principle on the tube considered. Lift boundary data consistently. Suppose the reference trajectory qbar is differentiable, its residual is bounded by rho, initial error by e0, and, along the error equation, the upper right derivative satisfies

    D+ E <= rho + L E + B E^2,   E(0)<=e0,

with nonnegative, verified constants and E=||q-qbar||. This inequality can come from a one-sided stability estimate; a two-sided Lipschitz estimate is sufficient but not necessary. In an infinite-dimensional PDE the derivative and continuation statements are hypotheses to prove, not consequences of writing a residual.

Choose R>0 and let

    eta = (e0+T*rho) exp((L+B R)T).

If eta<R, then E(t)<=eta for all 0<=t<=T. Proof: before the first exit from the R tube, E^2<=R E; Gronwall gives E(t)<R, contradicting a first exit. Continuation extends the solution to T under the stated hypothesis. The tighter exponential-integral formula can replace this sufficient bound. certificate.py evaluates this sufficient scalar inequality using outward Decimal upper arithmetic. It does not verify the PDE hypotheses.

To certify a finite Fourier/y ODE, the residual must be enclosed on every full time segment (e.g. polynomial time reconstruction plus interval operations). Midpoint residual samples are only diagnostics. To certify the continuum solution, there must additionally be a controlled infinite-dimensional argument; a finite ODE certificate alone does not supply this.

## 4. Exact obstruction to a cutoff-independent ordinary-norm estimate

For Endpoint-SD with zero prescribed left u, linearize at u=v=0. The first evolving site is a closed 2x2 Fourier block. With nonzero non-Nyquist x frequency xi and general lambda,

    B(xi) = [[-2a i xi, h xi^2],
             [xi^2/h-lambda i xi, -(2a+lambda h)i xi]].

It has eigenvalues sigma_plus=xi^2-i(2a+lambda h)xi and sigma_minus=-xi^2-2a i xi. A plus eigenvector is (1,1/h-i lambda/xi). Direct substitution verifies both equations. Thus the first-site propagator has norm at least exp(xi^2 T) in any induced norm. This lower bound also obstructs a uniform bound for the full chain: first-site dynamics do not depend on later sites.

More explicitly, normalize a real sine/cosine pair associated with this eigenvector to have terminal norm d. The exact linear solution exp(B(t-T)) times that terminal vector has zero residual, initial norm d exp(-xi^2 T), and final norm d. A bound E(T)<=C E(0) valid for all such modes requires C>=exp(xi^2 T). Ordinary Sobolev weights do not fix this: the same frequency weight occurs at both times.

Consequences: (i) arbitrary small ordinary-norm residual/initial errors cannot yield a cutoff-uniform certificate by ordinary Gronwall; (ii) fixed-resolution certificates are not ruled out, but their constants/precision may be severe; (iii) this calculation does NOT prove nonexistence for either prescribed nonlinear initial datum, and does NOT prove impossibility of tailored weighted-space or stable-subspace certification. It also does not replace a separate analysis of the continuous y problem or Centered-SD.

At T=.01, taking the highest non-Nyquist frequency on [-96,96) for dx=.1,.05,.025 gives growth log10 factors approximately 4.28,17.13,68.55. These are worst-direction amplification factors for the linear Endpoint block, NOT upper error bounds, observed nonlinear growth rates, or sufficient precision prescriptions. They explain why a grid-independent small L cannot simply be assumed.

## 5. Gaussian periodic extension

The currently coded profile G(x)=exp(-(x/6)^2) has matching values at x=+-96, but G'(96)=-16/3 exp(-256) and G'(-96)=+16/3 exp(-256). The derivative jump of its periodic extension has magnitude (32/3)exp(-256), nonzero despite being tiny. Its Fourier coefficients consequently have an algebraic leading tail (n^-2) by integration by parts. Thus this literal periodic extension is not a globally smooth/analytic periodic datum. It cannot be silently treated as an analytic periodic Gaussian in a convergence proof. The periodized SUM of translated Gaussians would be a different, smooth datum and is not substituted here.

The sinusoid is exactly periodic and initially has only Fourier indices +-8 on this domain. Nonlinear products generate higher harmonics. Initial finite support alone is not an all-time tail bound.

## 6. Status and next mathematical step

The scalar certificate infrastructure and exact stability obstruction are established at the levels stated above. Missing: an appropriate continuum solution class/existence theorem for these exact data and closure, controlled high-frequency tails on a positive time interval, and validated full residual enclosures. Repeated grid/time solves below only test whether the existing candidate reference is usable; they do not discharge these proof obligations.

No certifiable reference or new accuracy ranking is inserted into the paper. Next work must either prove a data-specific tail/stability estimate for the unchanged problem, or explicitly select a revised well-posed problem (boundary/solution class/initial data), before spending large computation on a claimed continuum reference. Changing the PDE or filtering modes is not an unannounced numerical fix.

## 7. A boundary-consistent continuum reference formulation (exact, not linearized)

For the zero lower u boundary, define w=v-u_y and (I f)(y)=integral from -2 to y of f(s) ds. Integrating the first continuous equation gives exactly

    u_t = -u_xx - [u^2/2+4u]_x - I w_xx,
    w_t =  w_xx - [(u+4)w-4u]_x,
    v   =  u_y+w.

Proof: I v_xx=u_xx+I w_xx because u(-2)=0; subtract u_yt from v_t to obtain the second equation. Conversely, differentiate the first equation in y and add w_t to u_yt to recover both physical equations. This equivalence requires the displayed derivatives and integrals to exist and the prescribed lower trace to hold. It is an exact reformulation of the nonlinear target.

The initial auxiliary field is fully specified: w0=v0-partial_y u0. With e'=pi/4 cos(pi(y+2)/4), the Gaussian has w0=(.03 e-.05 e')G; the sinusoid has w0=.02 e sin(pi*x/12)-.03 e' cos(pi*x/12). At y=-2, u=0 implies w_t=w_xx-4w_x; the lower w trace is consequently determined by its initial value through a linear heat-advection equation. For the sinusoid it is exactly

    w(x,-2,t)=-(.03*pi/4) exp(-(pi/12)^2 t) cos((pi/12)(x-4t)).

No upper y ghost or separate upper boundary is needed in this integral formulation. This identifies a common continuum target more cleanly than taking the old FD ghost extrapolation as a theorem. It does NOT prove that the old FD upper closure converges to this target.

For subsequent certification, one must control u_y as well as u and w: a bound in max(||u||,||w||) alone does not imply a small physical v error. For example use a y-C1 Fourier-Wiener norm (sum of each mode's y supremum plus its y-derivative supremum), which is an algebra. I is bounded in that norm by 5 on this length-4 interval. On a fixed Fourier-Galerkin cutoff K, ||Dx||<=K and ||Dxx||<=K^2. In E=max(||eu||,alpha||ew||), a sufficient linear bound is

    Llin = K^2+4K+max(5 K^2/alpha,4 alpha K),

and around a reference of norm at most M, L=Llin+2 K M and B=K bound the quadratic error terms. These finite-cutoff estimates are deliberately conservative. The y-C1 norm implies ||ev||<=||eu||+||ew||<=(1+1/alpha) E; this factor must enter the physical-error certificate. The unbounded K dependence again prevents this finite-cutoff estimate alone from certifying the omitted x modes. The norm, field reconstruction factor, and cutoff dependence cannot be omitted from the proof.
