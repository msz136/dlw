# Independent physical-field perturbations

2026-10-26. The user explicitly chose independent perturbations of u and v and asked to continue seeking a certified reference for the full continuous equation. Structure-preserving perturbations are not a substitute for this target.

## Current scope

Use the manuscript's four current cases: A (one soliton), D (two solitons), Gaussian and sinusoidal. Work with current natural Centered-SD, not the old node-field implementation behind `linear_spectrum.py`. The existing time/SAMM text is user-updated and must not be overwritten by the earlier session's draft.

Main exploratory grid: h=dx=.1, RK4, dt=1e-4, T=.01. The perturbation has amplitude epsilon=1e-6 and the same physical x wavenumber kappa=pi/2 in each case, corresponding to Fourier indices 5, 20, 48 and 48. A transverse envelope sin²(pi(y-yL)/(yR-yL)) makes the perturbation and its first y derivative vanish at the boundary. The two tests prescribe either (delta u,delta v)=(epsilon phi,0) or (0,epsilon phi), with phi the envelope times cos(kappa x). The auxiliary initial values are reconstructed from these physical data.

The solution difference between perturbed and unperturbed numerical trajectories is calculated by an algebraically equivalent difference equation. This avoids losing a small perturbation when subtracting two O(1) states. It remains a diagnostic of the nonlinear numerical evolution, not a continuum error certificate. Initial physical-field matching, agreement of the difference RHS with direct RHS subtraction, and time-step controls are recorded.

## Refinement and target definition

The preliminary A pilot uses the earlier x-mode index 4 and is kept separately. For its y refinement, freeze physical y endpoints; the production soliton model otherwise moves the lower prescribed boundary by h/2 as h changes. Record a stopped run at its actual stopping time and preserve its last state.

For soliton PDE certification, the reference IVP must also specify how whole-line soliton data and the finite periodic computational interval are connected. Periodic samples are not an exact periodic continuation of a whole-line soliton. An unchanged whole-line problem would require a spatial-domain truncation estimate in addition to the frequency-tail and time bounds.

## Reference acceptance condition

A continuous reference is accepted only when existence in a specified class, exact initial/boundary matching, unresolved x/y tails, and evaluation errors are bounded. Its physical-field error bounds eta_u,eta_v must be small relative to the numerical discrepancies being measured. At present these bounds are null for the independent nonlinear perturbations. Finite-grid agreement, a finite-dimensional ODE enclosure, and the exact constant-background linear response are each kept distinct from this target.

## Current analytic routes

The exact continuum split A=u_y+v-4, B=v-u_y-4 in X=x-4t gives A_t=-A_XX-(uA)_X and B_t=B_XX-(uB)_X. The first component has a backward heat principal part. The background linear equation and the current natural lattice can be analyzed explicitly. A nonlinear continuous certificate additionally needs data-specific control of the unstable tail or an exact validation of the mixed-time initial matching map. No filtering, regularization, or special pairing of delta u and delta v is introduced to bypass this requirement.
