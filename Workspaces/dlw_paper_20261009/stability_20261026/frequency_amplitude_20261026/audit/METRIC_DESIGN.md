# Frequency/amplitude experiment: independent metric audit

2026-10-26. The existing production equations use node fields `(u,w)` and edge field `v=diff(u)/h+avg(w)`. This note concerns the current finite-grid perturbation experiment, without a perturbed continuum reference.

## Exact algebraic amplitude scaling

Write the perturbation in auxiliary coordinates as `(delta u,delta w)=epsilon (r,s)`. After subtracting the production vector field and dividing by epsilon,

    dH/epsilon = (u+4)r + epsilon*r²/2
                  + h²[(w/16-1/4)s + epsilon*s²/32],
    q = diff(r)/h + avg(s),
    r_t(lower)=0,
    diff(r_t)/h = -diff(D1(dH/epsilon))/h - D2(q),
    s_t = D2(s)-D1[(u+4)s+(w-4)r+epsilon*r*s].

Thus epsilon appears only in the quadratic perturbation terms. The baseline must still evolve through every corresponding RK4 stage. This is an exact scaled nonlinear difference equation, not a linearization. The initial map from the independently imposed physical r/q to s uses the same alternating recurrence and zero lower s as before.

## Constant-state prediction

At `(u,v)=(0,4)`, let `p=diff(r)/h`. For one non-Nyquist x carrier,

    (p(t),q(t)) = phase * [[cosh(theta),sinh(theta)],
                          [sinh(theta),cosh(theta)]] (p(0),q(0)),
    theta=kappa²t, phase=exp(-4i kappa t), r_k=h sum_(j=1)^k p_j.

For the real experimental envelope phi:

- u-only: `r=phi_nodes cosh(theta) cos(kappa(x-4t))`, `q=diff(phi_nodes)/h sinh(theta) cos(kappa(x-4t))`.
- v-only: `r=I_h(phi_edges) sinh(theta) cos(kappa(x-4t))`, `q=phi_edges cosh(theta) cos(kappa(x-4t))`.

Therefore the norm response is not universally exp(theta). Native maxima also contain the sampled cosine factor, which depends on kappa and t. `constant_response.py` evaluates these exact predictions on the actual grid and observation masks. It reproduces the existing A/D v-to-u controls to their stored precision.

## Table design

For each case, group rows by kappa and epsilon and report four normalized terminal physical maxima: u-from-u, v-from-u, u-from-v, v-from-v. These use the prescribed epsilon, not the sampled initial maximum. Pair L2 gains are useful supplementary columns or a separate short panel; full periodic x is used to reduce moving-peak sampling effects, with the same native interior y regions.

Amplitude independence must be checked with differences of full normalized physical fields, not just equality of their maxima. A useful metric for each output is the largest space-time difference between the epsilon=1e-5 and epsilon=1e-7 normalized trajectories, divided by the largest space-time norm of the epsilon=1e-7 output. Report it as a relative spread, explicitly over 0<=t<=.01. For cross fields, normalize by their nonzero maximum over the whole interval, rather than dividing by their zero initial value.

Time-step halving should control the largest carrier and largest amplitude. These differences quantify time-resolution sensitivity of this discrete experiment; they are not continuum-reference error bounds. Small amplitude dependence can be interpreted only in relation to these controls and floating-point algebra checks.
