# Current Centered-SD: time integration and moving meshes

2026-10-25. User-authorized scope: complete manuscript Sections 4.2–4.3 and 5.3–5.4, with current Centered-SD time-error curves and SAMM comparisons. Preserve stability sections for subsequent discussion. Do not change the current spatial comparison, including the latest heatmap repair.

## Time comparison

Use A/D/Gaussian/Sinusoidal and the current natural-edge state (u,w), equivalent to manuscript omega=h*w/4. Euler, RK4 and Crank–Nicolson share h=dx=.1, dt=1e-4, T=.01, initial data, stage boundary closure and Fourier x differentiation. At every saved time, calculate the maximum absolute difference from the continuous reference over the same native regions as the published spatial comparison. The curves describe total physical-field error histories. They do not isolate a pure temporal error by changing the reference.

For each case, plot two aligned panels E_u(t), E_v(t), with three time-method curves. All native recorded times are joined without smoothing. Keep a linear time axis and include the zero initial error. Reproduce the published RK4 endpoints, verify the CN residual, and quantify temporal/tolerance sensitivity before writing conclusions.

## Mesh comparison

Use the same current natural Centered-SD on A/D solitons. Both uniform and adaptive computations use matched mapped-centered x operators, the same node count, y spacing, RK4 and final time. The density is obtained from the conserved omega equation, with rho=1-omega/h. Shared x nodes are determined by the transverse average. Document the actual initial distribution, domain/endpoints, velocity formula, boundary data along moving trajectories, and ALE transport. Preserve positive density and ordered nodes; record any failure rather than silently changing parameters.

The Gaussian/sinusoidal benchmark background v=4 is outside this zero-background density comparison. No new monitor or density tuning is introduced for those cases in this task.

## Figure specification

Time-curve reference: plot-is-all-you-need/gallery/oa-tech-pone-0116670-f16, borrowing the paired aligned line panels and single shared legend. Use the existing paper's white background, STIX/serif labels, thin axes, and distinguish integrators with color plus line style. No raw-point cloud or smoothing. Mesh presentation follows the existing paper's paired field/spacing logic; actual spatial coordinates and spacing ratios remain explicit.

Figures are stored under this directory with PNG and PDF exports. All manuscript captions use normal publication prose, without design-choice or workflow commentary. Numeric claims must be supplied by the current runs, not by the earlier PE manuscript.

## Corrections during execution (2026-10-25, after the runs above)

The mesh comparison was executed with two changes, both documented in `README.md`: the node velocity uses
the periodic mean-flux constant instead of the pinned node 0, and the lower-row transport uses the nodal
velocity array. Current data are in `samm_periodic/`; the superseded runs are kept under the two
`diagnostic_*` directories. The manuscript comparison uses mapped centred differences for both members, as
recorded in the published Sections 4.3 and 5.4.
