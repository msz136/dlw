# Independent check of the sinusoidal boundary-jet result

Date: 2026-10-24. Reviewed `ACTUAL_DATA_REVIEW.md` against the exact DLW equations and the specified sinusoidal data.

**Verdict:** the conditional non-Gevrey transverse-boundary-jet proof is mathematically consistent. It is a result about the actual prescribed sinusoidal data, not a substitute Burgers datum.

Checks performed:

1. With `R=u_z+v`, `S=v-u_z` and `X=x-4t`, the exact equations have the signs stated: `R_t=-R_XX-(uR)_X+4u_X`, `S_t=S_XX-(uS)_X+4u_X`.
2. Division by the transverse factorials gives the normalized product convolution without additional binomial factors, and `U_j=(R_(j-1)-S_(j-1))/(2j)`.
3. The normalized m-th R/S jet has maximal possible Fourier frequency `(m+1)*omega`; the normalized j-th u jet has maximal frequency `j*omega`. The linear `4(U_m)_X` term therefore cannot enter the highest-harmonic equation. In the product term, reaching the maximal frequency requires both factors' positive highest harmonics.
4. The initial v field does not vanish as a full function, and its phase must be retained. Its boundary value is zero, however, and all its higher boundary jets have only the fundamental x frequency. Thus it does not contribute to any highest `(m+1)*omega` initial coefficient for `m>=1`. No alternate initial v has been inserted.
5. The phases `r_m=(-i)^m a_m`, `s_m=-(-i)^m b_m` give the stated positive triangular system. Both signs are necessary, and both are correct.
6. The selected `j=1` nonlinear term gives `a_m' >= (m+1)^2 omega^2 a_m+(m+1)omega*c*a_(m-1)`. Induction produces the factor `(m+1)` in (A1), not an extra factorial.
7. Multiplying the normalized coefficient of `U_n` by `n!` then yields exactly the factor `n!/2` in (A2). Its `exp(n^2 omega^2 t/2)` factor defeats every finite-order Gevrey upper bound.
8. The direct `m=1` check agrees with the z-squared coefficient of `-u*u_x` at time zero. Transport changes only phases and does not alter the sup norm.

Required scope: all y derivatives and enough x,t regularity must extend to the lower boundary to justify the jet hierarchy. The theorem excludes **uniform** analytic/Gevrey-y regularity up to that boundary at a positive time. A C-infinity function can have such rapidly growing jets, so this is not a classical nonexistence theorem. It also does not exclude all possible sup-norm reference-error certificates in weaker solution classes.

Consequently it is valid to use this result to reject a geometric or finite-Gevrey Chebyshev-tail assumption for the exact sine target. It is invalid to infer a positive lower bound for the candidate's physical-field error, or to infer that no continuous solution exists, from this result alone.
