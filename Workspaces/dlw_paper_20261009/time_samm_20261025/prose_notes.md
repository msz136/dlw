# Time integration and SAMM: prose notes

2026-10-25. Writing aid only; no main-paper edits or invented numerical results.

## Sources and structure

Read current dlw-paper.html Sections 3.2, 4.1–4.4 and 5.1–5.5; natural_centered_section_20261025/section_3_2.md; and the earlier report/dlw_paper_draft.html headings en-samm, en-time, en-time-results and en-mesh-results. Equivalent English prose is in manuscript.md around lines 755–839 and 988–1057.

The earlier draft has a useful progression: controlled comparison → error table → curve definition → case-specific observations → short synthesis. Its SAMM sequence is motivation → conservation density → shared mesh → node-spacing illustration → paired accuracy comparison. Keep these structures, replacing the old PE variables and results with the current Centered-SD mathematics and data.

Current Section 4.2 already identifies the state, boundary closure, all three update rules and the C–N residual. Section 4.3 and experimental Sections 5.3–5.4 are empty. Leave 4.4/5.5 for the later stability discussion.

## Section 4.2

Retain the existing natural state \(z=(u,\omega)\), initial recurrence (34), stage-time lower boundary data, and physical recovery of \(v\). These are already clear.

The current C–N sentence says Euler prediction plus fixed-point iteration, stopped at residual \(10^{-12}\). The new numerical agent confirms the same solver but uses \(2\times10^{-14}\), with a \(2\times10^{-15}\) control. **Update the tolerance and explain the residual in the implementation's actual variables**: it solves in \((u,w)\), with \(\omega=hw/4\). A residual bound in \(w\) is not numerically identical to a bound in \(\omega\). The algebraic scaling can be stated briefly in the implementation detail or appendix, while the manuscript state remains \((u,\omega)\).

Suggested final comparison paragraph:

> The spatial-formulation and mesh comparisons use RK4. To examine time integration separately, we retain the fixed-grid Centered-SD equations and apply Euler, RK4 and Crank–Nicolson to the same initial and boundary data. In every comparison, we measure errors in the physical fields \(u\) and \(v\).

Suggested stage-coupling paragraph, once the SAMM implementation is fixed:

> For the moving-mesh calculation, we include the shared node positions in the state and advance them together with \(u\) and \(\omega\). At each RK4 stage, the current node positions determine the mapped spatial operators, and the stage fields determine the conservation density, flux and node velocity. The physical field \(v\) is recovered at those same positions through the lattice relation in Section 4.1. The field and mesh equations are therefore evaluated at a common intermediate state throughout the step.

This paragraph can instead close 4.3 if placing it in 4.2 introduces the mesh too early.

## Section 4.3: mathematical identification

The natural auxiliary equation is
\[
\omega_{k,t}=\omega_{k,xx}-[(u_k+2a)\omega_k-hu_k]_x.
\]
It gives the exact law
\[
\rho_k=1-\frac{\omega_k}{h},\qquad
q_k=(u_k+2a)\rho_k-\rho_{k,x}-2a,\qquad
\rho_{k,t}+q_{k,x}=0.
\]
Substitute \(\omega=h(1-\rho)\) to verify it. The old law uses \(W=4\omega/h\), but **do not copy the old physical identity \(W=v-\delta_0u\)**. The current identity is \(v_k=\Delta_hu_k+2(\omega_k+\omega_{k-1})/h\).

Important scope issue, already sent to the SAMM agent: the Gaussian/sinusoidal family has background \(v=4\), so initially \(\rho\approx u_y\). Its mean over the full transverse band may be zero or nonpositive. The old monitor cannot silently be used for all four cases. A constant density shift preserves the conservation equation, but the flux must be consistent. For \(\rho_c=c+1-\omega/h\),
\[
q_c=(u+2a)\rho_c-\rho_{c,x}-cu-2a(1+c)
\]
equals the original flux. Any chosen \(c\), averaging range and positivity condition must be declared if this extension is used. The numerical agent is deciding the actual experiment; do not put this optional extension into the main text before that decision.

For a periodic interval with equal endpoint fluxes, the old velocity is
\[
\dot x_i=\frac{\bar q(x_i,t)-\bar q(x_L,t)}{\bar\rho(x_i,t)}.
\]
If fixed endpoints have unequal fluxes, fixed normalized cumulative-density labels \(\eta_i=i/N\) give
\[
\dot x_i=\frac{\bar q(x_i,t)-\bar q_L(t)+\eta_i[\bar q_L(t)-\bar q_R(t)]}{\bar\rho(x_i,t)}.
\]
Publish only the implemented version. The latter reduces to the former when the endpoint fluxes agree.

## Section 4.3: proposed prose

> A uniform grid assigns the same resolution to weakly varying regions and to the narrow parts of a wave profile. We introduce a self-adaptive moving mesh method to redistribute the \(x\) nodes as the fields evolve. The \(y\) lattice remains uniform, and every transverse layer uses the same moving \(x\) nodes. This shared mesh preserves the lattice pairing in the Centered-SD equations while allowing the numerical resolution in \(x\) to follow the solution.

> The auxiliary equation in Section 3.2 supplies the conservation law used to determine the mesh. Setting \(\rho_k=1-\omega_k/h\) and choosing the flux to vanish on the zero-field background gives [density/flux display]. Substitution into the \(\omega_k\) equation yields \(\rho_{k,t}+q_{k,x}=0\). Thus the density evolves through a spatial flux already present in the semi-discrete system.

> Since the \(x\) nodes are shared by all transverse layers, we average the density and flux over the selected \(y\) layers, [average display]. The averaged quantities satisfy the same conservation relation. We choose the initial node positions by equidistributing the cumulative density, so that intervals in regions of larger \(\bar\rho\) receive more nodes. During evolution, the cumulative-density labels determine the node motion.

Follow with the implemented cumulative integral and node velocity. State the actual transverse averaging range and weights. The old method used mapped centered differences whereas current 4.1 uses Fourier derivatives. The fixed/moving pair must use the same operators, so its uniform control need not equal the earlier Fourier row.

> For the fixed- and moving-mesh comparison, we evaluate \(x\) derivatives through the same computational coordinate \(\xi\). Writing \(x=x(\xi,t)\) and \(J=x_\xi\), the chain rule gives [mapped derivative display]. Centered differences on the uniform \(\xi\) grid then provide the numerical operators. The uniform-grid member of this comparison has \(x_i=\xi_i\) and \(J_i=1\).

If mapped Fourier derivatives are actually used, replace “Centered differences” accordingly. The chain-rule formulas are
\[
\mathcal D_x z=J^{-1}\mathcal D_\xi z,\qquad
\mathcal D_{xx}z=J^{-2}\mathcal D_{\xi\xi}z-J^{-3}(\mathcal D_\xi J)(\mathcal D_\xi z).
\]

> At a moving node, the time derivative also includes the change in its position. We therefore advance
\[
\dot u=F_u+\mathcal V\mathcal D_xu,\quad
\dot\omega=F_\omega+\mathcal V\mathcal D_x\omega,\quad
\dot x=\mathcal V.
\]
> Here \(F_u\) and \(F_\omega\) are the Centered-SD right-hand sides evaluated on the current mesh. Because every layer has the same node velocity, the lattice reconstruction of \(v\) is retained during the coupled evolution. Setting \(\mathcal V=0\) recovers the fixed-mesh equations. The conditions \(\bar\rho>0\) and \(J>0\) ensure that the node velocity is defined and that the node ordering is preserved.

This ends the construction without introducing the reserved stability subsection.

## Section 5.3: proposed opening and measurement

> Having compared the spatial formulations, we now retain Centered-SD on the fixed grid and examine the effect of time integration. Forward Euler, classical RK4 and Crank–Nicolson use the same initial fields, boundary data and spatial operators, with \(h=\Delta x=0.1\) and \(\Delta t=10^{-4}\). We follow each calculation from \(t=0\) to \(T=0.01\), measuring both the final errors and their development during the evolution.

> At each recorded time, we evaluate the maximum absolute error over the native locations of each physical field,
\[
E_u^{(m)}(t_n)=\max_{(x_i,y_k)\in\mathcal G_u}|u^{(m)}_{i,k}(t_n)-u^*(x_i,y_k,t_n)|,
\qquad
E_v^{(m)}(t_n)=\max_{(x_i,y_{k-1/2})\in\mathcal G_v}|v^{(m)}_{i,k}(t_n)-v^*(x_i,y_{k-1/2},t_n)|.
\]
> Here \(m\) denotes the time integrator, and the spatial regions are those specified in Section 5.1. The two error histories describe how the largest discrepancy in each field changes with time. Table [N] gives their values at \(T=0.01\), while Figures [range] show the time histories for the four test problems.

Call these “error histories” or “error growth”; the maximum can change its spatial location, so this graph does not track a material error packet. No warning sentence is needed in the paper.

Results can use one paragraph per case, or one paragraph for the solitons and one for the two smaller-amplitude tests. Follow the earlier draft’s specific observations, but only after inspecting current data. Do not reuse old claims about which Euler/RK4 field is smaller. A near-overlap claim should also be checked numerically.

Suggested caption:

> [Case]. Maximum absolute errors in \(u\) (left) and \(v\) (right) for Centered-SD with forward Euler, RK4 and Crank–Nicolson. Each value is evaluated over the native field locations in the region specified in Section 5.1. The calculations use \(h=\Delta x=0.1\) and \(\Delta t=10^{-4}\).

The old \(10^{-13}\) Gaussian/sinusoidal reference certificate covers initial derivative and terminal field samples. The time agent will evaluate the same continuous expression at each intermediate time and keep the certificate scope explicit. Do not automatically extend the old bound to all new curve samples.

## Section 5.4: proposed opening and measurements

> We next use Centered-SD to examine how the distribution of the shared \(x\) nodes affects the computed fields. The uniform and adaptive calculations have the same node count, the same \(y\) lattice and the same RK4 time integrator. Both use the mapped spatial operators described in Section 4.3. The adaptive calculation begins from the equidistributed conservation density and advances the node positions together with the fields to \(T=0.01\).

> To show how the density allocates resolution, Figure [N] plots the local spacing \((x_{i+1}-x_i)/\Delta x\) at the interval midpoint. The value one corresponds to the uniform mesh. Values below one indicate a concentration of nodes, while values above one indicate wider intervals. The initial and final adaptive distributions show how the mesh develops during the calculation.

Follow with an actual observation about the location and extent of redistribution. The old claim that the distribution is mostly established at initialization is a possible outcome, not a conclusion to preserve before seeing new data.

> Table [N] compares the terminal physical-field errors on the fixed and adaptive meshes. For each field, we also report the relative change
\[
\mathcal R_f=100\left(1-\frac{E_f^{\mathrm{SAMM}}(T)}{E_f^{\mathrm{fixed}}(T)}\right)\%,\qquad f=u,v.
\]
> Positive values correspond to a reduction in error. The comparison keeps the spatial operators and time advancement fixed while changing the node distribution.

If all changes are positive, “percentage reduction” is natural. If mixed, use “relative change” and describe the actual response directly. Do not reuse the old four-case improvement claim or percentages.

If spatial profiles are added, use the earlier maximum-over-y profile definition at the native moving x coordinates; those coordinates can themselves be the plotting abscissae. An additional interpolation to a common x grid is unnecessary merely to draw a curve. Distinguish any separately computed common-grid reconstructed error statistic.

Suggested mesh caption:

> [Case]. Local \(x\)-spacing normalized by the uniform spacing \(\Delta x=0.1\), shown at interval midpoints. The curves show the adaptive mesh at \(t=0\) and \(T=0.01\); the horizontal line gives the uniform spacing.

Suggested field-error caption:

> [Case] at \(T=0.01\). Maximum-over-\(y\) absolute error profiles in \(u\) (left) and \(v\) (right) for the uniform and self-adaptive meshes. Both calculations use Centered-SD, the same number of nodes and RK4 with \(\Delta t=10^{-4}\).

Close with two connected observations: what the density did to the nodes, then how this affected each physical field. Keep stability and general optimality outside this subsection.

## Section-introduction additions

Section 4 introduction:

> In Section 4.3, we use a conservation law of Centered-SD to construct a shared moving mesh and couple its node motion to the field evolution.

Section 5 introduction:

> Section 5.3 retains Centered-SD and compares the physical-field errors produced by three time integrators throughout the evolution. Section 5.4 then examines the effect of redistributing the shared \(x\) nodes through the conservation-based moving mesh.

Leave the existing stability headings for later work.
