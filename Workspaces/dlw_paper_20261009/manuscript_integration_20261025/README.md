# Illustrated numerical text integrated into the main manuscript

**Current edition (2026-10-25):** The subsequent user-selected four-case edition is now active. Its A/D physical-field publication source and checks are in ../spatial_ad_uv_20261025/. This directory preserves the preceding six-case integration; do not republish it over the current manuscript.

2026-10-25. Reader: `../../../dlw-paper.html`.

The user authorized direct integration of the illustrated numerical draft and asked about time integration. Moving-mesh work was explicitly deferred.

Sections 5.1–5.2 now contain the six test problems, three tables, all 30 figure groups and the accompanying English analysis. Numerical values and figures come unchanged from `../report_refresh_20261024/natural_selection_20261025/`. The initial-derivative figures retain the draft's expandable presentation. Figure paths are adjusted for the root manuscript location.

Sections 4.1–4.2 now use the current natural Centered-SD reconstruction with omega. Euler, RK4 and Crank–Nicolson formulas are retained. Initial and boundary data were checked against the actual implementations. The published six-case terminal comparison uses RK4 only.

The former Section 5.3 and Table 4 belonged to the full-potential formulation. They are preserved in `archived_full_potential_time_comparison.html` and the complete `before_dlw-paper.html` snapshot. The active Section 5.3 retains its heading and source comment while current-form Euler/CN data await computation. No new evolution runs were performed. In subsequent CN work, evaluate the stopping residual in the manuscript's (u,omega) state, or explicitly state the scaling if code continues to store (u,w).

Sections 3.3–3.4 received the local substitutions needed for agreement with the already adopted Section 3.2: natural Lax coefficients, removal of primitive reconstruction terms, smooth-family consistency, and the extra-flux identity for the initial derivative difference. Proof conditions are retained. `theory_sync/EVIDENCE.md` records the algebra and its verification. Section 3.2 itself, Sections 1–2, moving-mesh and stability placeholders, conclusions and technical appendices are unchanged.

## Reproduction and validation

`theory_sync/prepare.py` reads the preserved pre-integration manuscript and generates the two theory replacements. `integrate.py` assembles the manuscript through bounded section replacements, with a concurrent-change hash guard. `validate.py` checks unchanged protected sections, all links and IDs, 429 formulas, 72 error entries, 24 minima and the exact figure/caption correspondence. Results: `validation.json` and `integration_manifest.json`.

The source templates for this publication are the illustrated draft plus the replacements in this directory. Do not run the historical all-section publisher: it contains superseded reconstruction and numerical text. The report-only preservation manifest has been advanced to this authorized manuscript state; its original manifest is preserved here.
