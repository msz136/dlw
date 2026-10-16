# Read-only cross-review of the homotopy and source attribution

2026-10-13. Read `homotopy.py`, `intervention/summary.csv`,
`sources/common_sources.py`, the source protocol and the source audit records.
No reviewed files were changed and no major inconsistency was found.

## Common-coordinate map intervention

The homotopy applies the frozen RK4 updates to the same physical input
coordinate (p=delta_y u, v). For SD, conversion into native w=v-delta0(u)
occurs at the start time and conversion back to v occurs at the end time,
including the time-dependent prescribed ghosts. The shared initial state
is checked before any update. Intermediate maps are therefore legitimate
interventions on the two actual updates rather than mixtures of incompatible
native variables. Reused endpoints are the archived native trajectories
converted at T; the archive provenance should remain visible in reporting.

The A result varies monotonically toward larger joint RMS as lambda goes
from FD to PE. C joint RMS varies monotonically toward smaller error; C v
alone has a shallow intermediate minimum. This supplies no basis for a
universal privileged optimum at the integrable endpoint, nor for a proof
that intermediate maps are nonintegrable. The implemented interpretation
correctly avoids those claims.

## Source decomposition

The three vectors are telescoping differences at the same reference point:
analytic-x RHS minus reference derivative; true-exterior stencil RHS minus
analytic-x RHS; and periodic stencil RHS minus true-exterior RHS. Thus
their signed sum equals the physical RHS defect without a fitting step.

The analytic jets have the requisite cumulant orders: u_xx uses the third
x cumulant; v_xx uses kappa(x,x,x,y), including all three xx-xy pairings.
For SD, v_t includes delta0(u_t) and the differentiated upper error
extrapolation. The independent native RHS comparison checks this conversion.

The named y-model component retains the prescribed y closure. The boundary
follow-up here demonstrates why omitting that qualification would mislead:
moving the reconstruction trace changes the interior u defect substantially.
The reported cosine cross terms are essential: component RMS values do not
add, and equal total norms can hide large directional changes.

Snapshot RHS sources alone do not constitute terminal error attribution.
The separately validated propagation experiment is needed to connect these
sources to the observed final errors. A vanishing instantaneous x-wrap
source in the observation interior likewise does not by itself exclude
propagation from the outer computation region.
