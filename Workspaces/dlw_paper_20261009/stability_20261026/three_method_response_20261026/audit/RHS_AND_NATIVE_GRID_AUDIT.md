# Native physical-response audit

2026-10-26. Latest user scope is each spatial method's own response to the same independently prescribed physical initial perturbation: perturbed trajectory minus that method's unperturbed trajectory. Curves use native physical-field sites and paper observation windows. No common-grid alignment, pairwise method discrepancy, or agreement-time threshold is used. Earlier common-grid designs are preserved under `superseded_common_grid/` and are outside the current result.

## Initial data and native sites

The u nodes are shared. Endpoint-SD v is at y-h/2, natural Centered-SD v at adjacent u midpoints, and FD v at the u nodes. Each method samples the same analytic physical initial functions and the same epsilon*sin²(pi*(y-yL)/(yR-yL))*cos(kappa*x) at its native physical-field positions. Thus the sample maximum of a given initial perturbation can differ slightly between native grids even when the underlying function and prescribed epsilon are identical. Normalize by the prescribed epsilon and label the curves as native sampled maxima.

Both physical components are initialized directly; the natural Centered-SD auxiliary values are then reconstructed to realize them. A u-only input has zero physical v perturbation up to arithmetic roundoff, and conversely for a v-only input. The lower u trace is shared by each perturbed/background pair. Endpoint-SD keeps its lower exact ghost and open chain. FD keeps its existing upper exact-background plus quadratic perturbation ghost. Natural Centered-SD starts with zero lower auxiliary perturbation and evolves that auxiliary trace. These are the existing spatial closures, not new boundary data fitted to the response.

Maxima use |x|<=5, |y|<5 for A; |x|<=30, |y|<30 for D; all periodic x and |y|<=1.8 for Gaussian/sine, separately at each field's native sites. All main trajectories use h=dx=.1, RK4 dt=1e-4, epsilon=1e-6, kappa=pi/2, and T=.01.

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
