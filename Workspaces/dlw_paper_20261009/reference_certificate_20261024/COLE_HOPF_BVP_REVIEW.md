# Coupled Cole–Hopf and a parabolic boundary-value route

2026-10-24. Independent feasibility note. This note does not duplicate the actual-data y-jet results and does not supply an error-certified reference.

## Exact compatibility condition

Use the exact transformed system

    q_t=-q_xx-4q_x+Vq,
    r_t= r_xx-4r_x-Vr,
    V=-(1/2) partial_x I(qr),

with u=2 q_x/q, w=4+qr, v=u_y+w. The lower potential gauge is V(x,0,t)=0. For the sinusoidal data, q0 is the positive periodic function specified in INTERIOR_EXISTENCE_REVIEW.md. For the Gaussian, first factor out the conserved spatial-mean exponential to work with periodic variables.

Prescribe a terminal q_T and the actual initial r_0. With S_+(t)=exp(t(partial_xx+4 partial_x)) and S_-(t)=exp(t(partial_xx-4 partial_x)), the exact two-time integral problem is

    q(t)=S_+(T-t)q_T - integral_t^T S_+(s-t)[V(s)q(s)] ds,
    r(t)=S_-(t)r_0 - integral_0^t S_-(t-s)[V(s)r(s)] ds,
    V(t)=-(1/2)partial_x I(q(t)r(t)).                         (B1)

Both heat operators in (B1) run in their stable direction. A constructive parabolic boundary-value proof can in principle use their smoothing estimates and explicitly enclose the spatial derivative in V. Nonvanishing of q must also be certified for physical-field reconstruction. This is a substantive alternative to the impossible positive forward antiheat majorant, because it puts the unstable component's datum at the terminal time.

However, the original initial-value problem is obtained only if the extra exact compatibility equation holds:

    q_0 = S_+(T)q_T - integral_0^T S_+(s)[V(s)q(s)] ds.       (B2)

Here V is the potential of the same validated pair in (B1), not a freely chosen coefficient. Validating (B1) with an arbitrary q_T does not validate the requested initial data. A small finite-mode or ordinary-norm defect in (B2) is insufficient, because its unstable tail remains uncontrolled. To provide the requested certificate one would have to solve (B2) in an admissible infinite-dimensional class, or prove that its exact solution lies in a certified terminal enclosure. No such range/compatibility theorem has been established for the actual q_0,r_0.

Consequently (B1) is a mathematically coherent revised formulation for a further proof, but it is not an already available completion of this task. Choosing q_T by a fine forward calculation and validating (B1) afterwards does not eliminate the requirement (B2).

## Why factorial Fourier tails of q_0 alone do not prove nonexistence

In the uncoupled backward heat equation, the Bessel/factorial Fourier tail of exp(c sin(omega x)) excludes a positive-time distributional solution. The same inference is invalid when V is unknown, even if V is bounded and analytic.

For an explicit example, fix any positive periodic analytic q_0 and set

    q(x,t)=q_0(x),
    V(x,t)=q_0,xx(x)/q_0(x)+4q_0,x(x)/q_0(x).

Then q_t=-q_xx-4q_x+Vq holds exactly. When q_0=exp(c sin(omega x)), V is a bounded trigonometric polynomial involving only the first two harmonics. Thus an extremely regular bounded potential can cancel the apparent antiheat incompatibility completely.

This example does not solve the DLW coupled equations: the chosen V need not satisfy V_y=-(qr)_x/2 for the prescribed r_0. Its purpose is precise: neither boundedness nor analyticity of V permits transferring the uncoupled backward-heat no-go theorem to the actual data. A valid compatibility or nonexistence proof must use the q,r,V coupling.

## Current feasibility conclusion

The exact transformation provides a stable-direction two-time formulation and the explicit compatibility equation (B2). It supplies no verified q_T satisfying that equation, no full-field reference enclosure, and no numeric eta_u or eta_v for the prescribed initial-value problem. The data-specific y-regularity obstruction established separately may limit suitable spaces for (B1)–(B2); it must not be replaced by an unsupported claim that the coupled q potential cannot cancel high-frequency growth.

The remaining question is a nonlinear range problem for (B2), not a precision setting in the existing solver. Without its resolution, candidate trajectories and finite-cutoff convergence remain uncertified for the continuous initial-value target.
