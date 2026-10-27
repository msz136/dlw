# Three-method physical perturbation audit

2026-10-26. Audit of Endpoint-SD, current natural Centered-SD and FD under shared physical initial functions, RK4 and prescribed lower u trace. The comparison concerns computed perturbation responses.

## Physical grids and comparison

All three methods use the same u nodes y. Endpoint-SD uses v sites y-h/2; the natural Centered-SD v sites (y[1:]+y[:-1])/2 coincide with Endpoint-SD sites [1:] up to floating point. FD uses v at y. Thus no interpolation is needed for u or for Endpoint-SD versus Centered-SD v. FD v is interpolated cubically in y onto the common interior edge sites. Record the initial interpolation discrepancy explicitly. A useful sensitivity diagnostic adds the known initial analytic profile to the interpolation of the evolved increment, making the comparison identical at t=0; it should not replace the primary plain-cubic result silently.

Each method samples the same analytic physical functions u0,v0 and the same perturbation epsilon*sin²(pi*(y-yL)/(yR-yL))*cos(kappa*x) at its own physical sites. Zero lower u perturbation and zero lower auxiliary w perturbation for Centered-SD are consistent with phi(yL)=phi_y(yL)=0. Endpoint-SD's first v site lies a half-step below the first u node; its perturbation is the corresponding analytic sample, not a newly imposed v boundary condition.

The lower prescribed u trace is common. FD also retains its existing upper background-plus-quadratic-perturbation ghost rule; Endpoint-SD and natural Centered-SD use their open/backward evolution without an upper ghost. These are part of the spatial formulations being compared, and should not be described as identical boundary closure operators.

Use paper observation windows: |x|<=5, |y|<5 for A; |x|<=30, |y|<30 for D; full periodic x and |y|<=1.8 for Gaussian/sine. Interpolation uses full available y data and is then restricted to the common observation region.

For normalized physical responses R_m=(delta u_m,delta v_m)/epsilon, define

    d_ij(t)=max(||R_i,u-R_j,u||inf, ||R_i,v-R_j,v||inf)
    scale(t)=max(1,max_m ||R_m,u||inf,max_m ||R_m,v||inf)
    D(t)=max_i<j d_ij(t)/scale(t).

The floor 1 corresponds to the prescribed initial amplitude and avoids division by a zero cross-response. This is a symmetric operational agreement metric, not a reference error. Pairwise distances with the same common scale can identify which methods separate. Agreement through t means all earlier recorded values remain below the chosen tolerance; report the last sample before the first crossing and the first sample above, with dt resolution. Useful reported tolerances are 1%,5%,10%. If not crossed, report agreement through the full completed horizon, not an extrapolated time.

## Exact normalized nonlinear difference equations

Write r=delta u/epsilon and s=delta v/epsilon for Endpoint-SD/FD, with background U,V. Put

    H_delta=(U+2a)r+epsilon*r²/2.

Then the interior difference of u_t is

    -diff(Dx H_delta)/h - Dxx s[1:]                 Endpoint-SD,
    -diff(Dx H_delta)/h - Dxx (s[1:]+s[:-1])/2     FD,

and r_t is recovered by the same h*cumsum with lower value zero.

For Endpoint-SD let Uprev=(fixed lower ghost,U[:-1]), rprev=(0,r[:-1]), A=(U+Uprev)/2, ar=(r+rprev)/2, p=(U-Uprev)/h, pr=(r-rprev)/h. The normalized nonlinear flux difference is exactly

    (A+2a-2h+h*V/2)*s + (V-4)*ar - h*p*pr/2
      +epsilon*(ar*s+h*(s²-pr²)/4),

and s_t is minus its x derivative minus Dxx pr.

For FD, the normalized flux difference is

    (U+2a)*s+(V-4)*r+epsilon*r*s,

and s_t is minus its x derivative minus Dxx C_h^0 r. The homogeneous ghost operator C_h^0 uses zero lower ghost and upper ghost 3*r[-1]-3*r[-2]+r[-3]. This follows by subtracting the same affine background ghost rule.

For natural Centered-SD use r=delta u/epsilon and s=delta w/epsilon. Its physical v response is q=diff(r)/h+(s[1:]+s[:-1])/2. The flux difference is

    (U+2a)r+epsilon*r²/2+h²*((W/16-1/4)*s+epsilon*s²/32),

and s_t=Dxx s-Dx((U+2a)*s+(W-4)*r+epsilon*r*s). All epsilon quadratic terms must remain; these equations represent full nonlinear differences, not a linearized surrogate.
