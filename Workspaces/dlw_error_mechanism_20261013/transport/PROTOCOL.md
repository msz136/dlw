# Frozen protocol: common-state source / propagation experiment

Frozen before the first validation or production run, 2026-10-13.

## Question and scope

Separate the one-step injection error and its linear transport for the actual paper SD(PE) and FD implementations. This identifies mechanisms of those fixed algorithms. It does not isolate abstract integrability from all other properties of an algorithm.

## Frozen input

Import `Workspaces/dlw_three_tracks_20261013/generate_shared.py:load_solver()` and its existing `shared/solver_cells.json`; do not edit them. Use paper cases A and C with their full original buffered domains, original lower prescribed trace and upper error extrapolation, uniform dx=dy=0.1, RK4, dt=1e-4, T=0.01. The x derivatives are the actual second-order centered d1 and three-point d2, not older fourth-order stencils.

## Common coordinate and maps

Use z=(p,v), p=diff_y(u)/h, with the lower u trace fixed to the continuous exact reference at time t. FD uses these coordinates directly. SD stores (p,W), W=v-delta0(u), and is converted with the same time-dependent affine reconstruction, including both exact boundary traces and the upper error extrapolation. Define the actual common-coordinate step

Psi_S(t,z) = T_S(t+dt) RK4_S(t,T_S(t)^(-1) z).

The affine map is applied at both ends of every step. Its derivative includes the linear upper ghost extrapolation; the time-dependent affine part is not discarded.

## Independently calculated sources and transport

At every time node form z*(t) solely from the continuous exact Gram solution, and independently compute

d_S(t)=Psi_S(t,z*(t))-z*(t+dt), B_S(t)=D_z Psi_S(t,z*(t)).

Starting from zero error, evolve four predictions

e_(S<-T)(n+1)=B_S(n)e_(S<-T)(n)+d_T(n), S,T in {SD,FD}.

No source or coefficient is fitted to a final numerical error. B is evaluated by analytic RK4 tangent propagation and checked against complex-step and central differences on a small case before the original A/C domains are run. Simultaneously evolve both actual unmodified maps from the same z*(0).

For each source also accumulate a_T(n)=sum_(k<n)d_T(k), with no propagation, and the sum of individual source norms. Report norms and angles between a_T and e_(S<-T), not merely endpoint error norms.

## Causal intervention

For A, run the actual nonlinear corrected maps Psi_(S,lambda)=Psi_S-lambda*d_S(t), for lambda=0,0.5,1. The source is the independently evaluated reference defect above, unchanged by the evolving corrected state. Lambda=0 must reproduce the frozen original solver; lambda=1 following the exact reference is an algebraic calibration; the lambda=0.5 amplitude and shape response provides the substantive source-scaling test. The corresponding linear prediction is (1-lambda)e_(S<-S).

## Primary outcomes

Evaluate physical errors (delta u,delta v) on exactly the original native-grid evaluation window; also report full-domain norms separately. Delta u is the affine derivative h*cumsum(delta p) with zero lower error trace. The joint norm is sqrt(mean(delta u^2)+mean(delta v^2)); report each field's RMS and Linf as well. Report diagonal closure residual ||e_actual-e_pred||/||e_actual||, prediction/actual norm ratio and cosine. The four-cell counterfactual matrix uses a fixed source definition and a fixed propagator definition. Effects are conditional on linearization; nonlinear closure residuals determine whether attribution is justified.

## Saved evidence

Every step: time, source and accumulated-source norms, all four prediction norms, propagation gain and angle, actual error and closure metrics; A intervention metrics. At the 21 equally spaced existing diagnostic frames: all four predicted physical error fields, two unpropagated source sums, and both actual physical errors on the evaluation window (float64, compressed without downcasting). Save complete final common-coordinate vectors and settings/hashes in NPZ/JSON. Compare lambda=0 final states against the prior frozen-solver endpoint archives.

## Optional source decomposition extension

After the primary experiment, the independently derived y-model/x-stencil/x-wrap residual interface may be propagated as extra sources, with its consistency and time quadrature error reported. This extension will not replace or retrospectively redefine the primary one-step sources.
