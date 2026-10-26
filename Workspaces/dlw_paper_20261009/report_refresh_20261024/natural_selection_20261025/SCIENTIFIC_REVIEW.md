# Natural Centered-SD: formula alignment and numerical interpretation

2026-10-25. Independent read-only audit of the adopted Section 3.2 and existing six-case trajectories. Quantities are in `scientific_analysis.json`.

## Exact correspondence to the adopted equations

The implementation's variable w equals 4 omega/h. Consequently,

    v = Delta_h u + M_- w = Delta_h u + 2(omega_k+omega_{k-1})/h,
    h^2 A(w) = omega^2/2-h omega,
    A(w)=w^2/32-w/4.

The existing local-gauge solver is exactly the adopted natural formulation. Its w evolution scales to equation (37). Its v time derivative is Delta_h u_t + M_- w_t, the differentiated reconstruction (39). The lower omega trace is h/4 times the implementation's lower w; it evolves by the same omega equation after initialization.

For common initial u,v and the same lower u_t, subtracting the natural and endpoint first equations and summing gives

    u_t^C-u_t^E = -h^2 D_x[A(w_k)-A(w_0)]
               = -D_x[(omega_k^2/2-h omega_k)-(omega_0^2/2-h omega_0)].

An independent Fourier assembly verifies this identity on all six full initial grids, with maximum discrepancy 4.024e-14. On a smooth bounded branch w=O(1), this changes the h^2 coefficient of u_t. The previous full-potential statement that the two u defects are identical must therefore be replaced by this identity.

## Initial data and final numerical patterns

Endpoint-SD has the lowest initial u_t defect in all six cases. Natural Centered-SD has the lowest initial v_t defect in A, D, Gaussian and sinusoidal; FD has the lowest in B and C. Natural Centered-SD reduces v_t errors relative to Endpoint-SD in all six cases.

At T=.01 the natural Centered-SD v errors are lower than Endpoint-SD by factors 71.72, 51.86, 70.12, 86.64 and 60.20 in A, C, D, Gaussian and sinusoidal, respectively. It has the lowest final v error in A, D, Gaussian and sinusoidal. The improvement relative to FD in those four cases is 1.846, 1.679, 3.167 and 3.478, respectively. Final u minima belong to FD in A, B and D and Endpoint-SD in C, Gaussian and sinusoidal.

For both non-soliton profiles, every method and both fields satisfy E(T)/(T E_rate(0)) between .995771 and 1.002084. Thus the final error scales differ from T times the initial derivative-defect norms by at most .43%. This is a particularly clean observed relation between the two tables.

In A and D, the endpoint u ratios are 18.97 and 23.07; natural Centered-SD gives 1.013 and 1.384. The centered final u errors are 2.803 and 2.758 times smaller than endpoint, although their initial u derivative defects are 6.680 and 6.044 times larger. The first equation explicitly couples u evolution to the spatial curvature of v through -D_xx v. This supplies an equation-based explanation for why a componentwise initial ranking may change during the evolution. The data do not separately identify the contribution of every evolving forcing term; no numerical-channel attribution was performed.

Case B has final u errors .162762-.167704 and v errors .0338418-.0340873 for all three methods, despite large differences in their initial v_t defects. The evidence here establishes the common elevated final error scale; a specific Fourier instability or boundary mechanism requires a separate diagnostic. Do not import a high-frequency explanation merely from the final maxima.

## Manuscript dependencies

- Section 4.1: replace the primitive J reconstruction and chain term with the omega recurrence and its linear time derivative. Retain the h^2 A(w) flux, or equivalently omega^2/2-h omega.
- Section 4.2: replace damped nonlinear inversion by the linear recurrence (34); state may be described as (u,omega), equivalent to the code's fixed scaling (u,w). Initial lower omega is h(v-u_y)/4; subsequent lower trace evolves.
- Section 3.4: remove the bounded J assumption, primitive term in (53), extra primitive in exact fields, and shared first-coefficient claim. The natural reconstruction is v=Delta_h Z. The exact difference identity above provides the changed initial u statement.
- Sections 5.2-5.3 currently contain full-potential h/dx scans and Euler/RK4/CN data. Those values belong to that reconstruction and should not be relabelled. The current six-case initial and common-RK4 final comparisons use the adopted natural reconstruction.

## Suggested English paragraphs

The two comparisons follow the same initial data through two stages of the computation. We first evaluate the spatial equations at t=0, where the exact time derivatives reveal the error introduced by each formulation. We then evolve the fields with a common RK4 discretization and examine how this initial discrepancy develops in the physical solution. This connects the local approximation of the equations with the accuracy of the computed waves.

The initial defects show a clear difference between the two physical fields. Endpoint-SD gives the smallest u_t error in all six cases, whereas the centered formulation substantially reduces the v_t error. The latter improvement follows the second-order centered approximation of the second equation. In A and D, and for the Gaussian and sinusoidal profiles, Centered-SD also gives a smaller v_t defect than FD. The different sizes of the u_t defects can be traced to the additional flux in the centered first equation. With the same physical initial values and lower boundary derivative, subtracting the two semi-discrete equations gives [the exact difference identity above]. Since omega is proportional to h on a smooth branch, this contribution changes the second-order coefficient of the first-field error.

The Gaussian and sinusoidal tests provide a direct connection between the initial and final comparisons. For both profiles, the final error in each field is within 0.43% of T times its initial derivative-defect norm for all three methods. The ranking in the initial table is therefore retained after this short evolution. Centered-SD gives v errors of 6.967e-9 and 4.706e-9, approximately 87 and 60 times smaller than Endpoint-SD, and approximately 3.2 and 3.5 times smaller than FD. Its u errors lie between those of Endpoint-SD and FD. These two profiles make the different contributions of the spatial formulations visible at both stages of the calculation.

The soliton tests show how the coupling between the fields affects their subsequent accuracy. In A and D, Centered-SD begins with a larger u_t defect than Endpoint-SD but reaches T=.01 with a smaller u error. At the same time, its v error is reduced by factors of about 72 and 70. The first equation couples u evolution to the spatial curvature of v, so the approximation of the second field also enters the evolution of the first. The two fields must therefore be read together when interpreting the final results. FD gives the smallest u error in these two tests, while Centered-SD gives the smallest v error.

Case C has closely grouped final u errors, all about 1.15e-4. The v comparison remains more separated, with 5.442e-4 for Endpoint-SD, 1.049e-5 for Centered-SD and 8.998e-6 for FD. Case B exhibits a stronger change during the evolution: the three formulations reach similar errors near .16 in u and .034 in v, even though their initial v_t defects differ substantially. Together, the six cases distinguish the error initially introduced by a spatial formulation from its development through the coupled field equations. The centered reconstruction gives a consistent reduction of the second-field error across the Gaussian, sinusoidal and several soliton profiles, while the first-field results show the role of the additional nonlinear flux and the subsequent coupling.
