# Exact nonlinear boundary traces and the literal Gaussian obstruction

2026-10-24. Proof draft. All claims concern the zero lower-u, periodic-x problem actually used in the experiments. They are not claims about DLW with other boundary conditions or Gaussian data on the real line.

Continuation: the user has now approved the smooth periodic Gaussian SUM as the future Gaussian initial datum. The obstruction below remains a result about the OLD truncated-periodic Gaussian. periodic_gaussian.py verifies the approved profile's explicit boundary evaluation bounds; the interior theorem is still open in this work.

## Exact trace equations

Assume a solution has enough regularity up to y=-2 to take traces of the two PDEs, commute x,t derivatives with the trace, and define p(x,t)=u_y(x,-2,t), b(x,t)=v(x,-2,t). Since u(x,-2,t)=0 for all x,t, u_x on the boundary vanishes. With a=2 and lambda=-2 the FULL nonlinear equations imply exactly

    p_t = -b_xx - 4 p_x,
    b_t = -p_xx - 4 b_x.

This is exact boundary reduction, not a linearized interior approximation. Put r=p+b, s=p-b. Then

    r_t=-r_xx-4r_x,    s_t=s_xx-4s_x.

For the given initial profiles b(x,0)=0. Hence r0=s0=p0. For periodic frequency xi_n=2*pi*n/192,

    rhat_n(t)=exp((xi_n^2-4i xi_n)t) phat0_n,
    shat_n(t)=exp((-xi_n^2-4i xi_n)t) phat0_n.

These formulas follow by the scalar Fourier ODE, whenever the trace solution belongs to the indicated distribution/function class. No unknown nonlinear remainder occurs at this boundary.

## Sinusoidal initial data

p0=(.03*pi/4)cos(pi*x/12), so

    p=(.03*pi/4) cos((pi/12)(x-4t)) cosh((pi/12)^2 t),
    b=(.03*pi/4) cos((pi/12)(x-4t)) sinh((pi/12)^2 t).

This exactly determines the lower v trace for ANY sufficiently regular nonlinear solution of the stated initial-boundary problem, without asserting that the entire interior solution has been constructed.

boundary_certificate.py uses 100-decimal Arb interval arithmetic. It treats each stored float as its exact binary rational, and checks ALL sampled boundary nodes against this formula. The prior h=.0125 FD reference satisfies

    4.2267e-8 < max_j |v_ref(x_j,-2,.01)-b(x_j,.01)| < 4.2269e-8.

The h=.025 reference lies between 4.2267e-8 and 4.2270e-8. The new 80-digit h=.1 trajectory lies between 4.5381e-8 and 4.5383e-8. Consequently no global maximum-norm error upper bound below 1e-10 can be valid for these candidates on a domain INCLUDING this boundary. The prior published diagnostic region excluded this boundary (|y|<=1.8); the bound does NOT by itself establish the error inside that smaller region.

The numerical FD closure uses a frozen lower ghost u(-2-h,0). At later times, its centered lower derivative approximates [p(t)+p(0)]/2 rather than p(t) under a smooth expansion, because u(-2+h,t)=h p(t)+O(h^2) but the ghost remains -h p(0)+O(h^2). This identifies a boundary inconsistency. It is not simply time or arithmetic error. A canonical u,w integral reference avoids that ghost; it still needs interior stability/tail certification.

A separately generated exact-trace table (480 points, x=j/20, T=.01) has an Arb-verified representation error <1e-72. This is a concrete UPPER bound on boundary trace representation only, not on the full reference solution.

## Literal periodic Gaussian: nonexistence in the required trace class

For the current Gaussian initial data, p0(x)=(.05*pi/4)G(x), with G(x)=exp(-(x/6)^2) on [-L,L], L=96, repeated periodically. The endpoint values agree, but

    G'(L)-G'(-L)=-(32/3)exp(-256) != 0.

Integrating its Fourier coefficient twice by parts gives, for n != 0,

    Ghat_n = [G'(L)-G'(-L)] (-1)^n / (2 L xi_n^2) + o(xi_n^-2).

The remainder follows from the Riemann-Lebesgue lemma applied to G'' on the finite interval. Therefore the coefficient's absolute value has a nonzero n^-2 leading term. The required backward-heat trace has coefficients

    rhat_n(t)=exp((xi_n^2-4i xi_n)t) (.05*pi/4) Ghat_n.

For every t>0 these coefficients grow faster than every polynomial. Fourier coefficients of a periodic distribution have at most polynomial growth. Thus no periodic distribution r(t) can satisfy these trace equations with this initial datum at positive time. In particular, there is NO classical nonlinear DLW solution on a positive time interval with the stated zero-u boundary and enough regularity to admit these traces.

This is stronger than the previous generic stability objection, but has a narrow scope: it applies to the literal truncated-periodic Gaussian and the stipulated trace regularity. It does NOT prove nonexistence of all possible weak/nonstandard solutions, of the real-line Gaussian problem, or of a smoothly periodized Gaussian problem. It also does not apply to the sinusoidal initial datum, whose boundary trace is explicitly regular.

## Consequence for the requested certificate

A full smooth-solution error certificate for BOTH original cases cannot be completed as stated. For Gaussian, the target in the required regularity class is absent. For sinusoidal, the old reference is demonstrably biased at the boundary; the exact integral formulation and exact boundary traces supply a consistent replacement target, but a nonlinear interior existence/tail estimate remains missing.

Possible Gaussian alternatives must be explicit: the real-line Gaussian problem with a controlled domain approximation, or the exact periodic sum sum_m exp(-((x+192m)/6)^2). The periodic sum has Fourier coefficients proportional to exp(-9 xi_n^2), so the boundary backward-heat series exists for t<9. This fixes the proven boundary obstruction only, not the full nonlinear existence theorem. No such change is silently made in this branch.
