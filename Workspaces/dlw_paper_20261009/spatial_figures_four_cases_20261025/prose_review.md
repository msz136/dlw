# Four-case prose and quantitative review

2026-10-25. Editorial recommendations only; no manuscript, report, plotting source or numerical result has been changed by this audit. The selected records are A, C, Gaussian and Sinusoidal. Their reader-facing names are **One-soliton**, **Two-soliton**, **Gaussian** and **Sinusoidal**. Source keys A/C remain in data/provenance files.

## Required replacement map

Section 5 opening: replace “six wave problems / four exact soliton solutions” by four problems comprising one one-soliton and one two-soliton reference plus the Gaussian/sinusoidal problems. Keep the existing introduction of Sections 5.1 and 5.2.

Section 5.1:

- Replace its first paragraph, which currently introduces A/B/C/D. Keep a=2, lambda=-2, rho_i=1 and zero phase shifts.
- Table 1 retains A and C only, with descriptive names. A has spectral pair (1,2), R=5 and periodic x interval [-10,10); C has pairs (6,-5),(4,-3), R=30 and periodic x interval [-40,40).
- Remove the B and D profile paragraphs and their figures from active presentation. Rename the A/C profile descriptions and captions.
- Keep the region, Gaussian/sinusoidal definitions, continuous reference, certificate and error-measure paragraphs unchanged in substance. Change captions/figure references after renumbering.
- Parameter and error tables must use the four descriptive names. The actual selected numbers stay unchanged.

Section 5.2:

- Filter both error tables to A/C/Gaussian/Sinusoidal and change their labels. Keep all three methods.
- Change the initial-table link and expandable summary from “six cases” to “four cases.”
- Replace the paragraph beginning “Endpoint-SD gives the smallest...” by the four-case paragraph below.
- Keep the Q-flux identity and its explanation.
- Keep the common RK4 setup and the Gaussian/sinusoidal 0.43% observation.
- Rewrite the A/D soliton paragraph for the one-soliton case alone; remove the B-error cluster statement entirely.
- Rewrite the C statement as the two-soliton paragraph below.
- Replace the old section introduction to “Physical-field sections and spatial error distributions” because it currently promises a separate complete heatmap after every section figure.
- Remove B/D headings, their explanations and all four corresponding comparison figures. Replace the repetitive “The corresponding heatmaps...” paragraphs by one clear explanation of the compact figure design.
- Keep the four retained case-specific explanations interspersed with their figures. Avoid adding the same ranking both before and after each figure.
- In the optional initial-derivative figure block, keep only four cases and adjust labels/captions. An error line joins actual data samples; it must not imply a separate curve-fitting procedure.

No changes are required in Sections 4.2, 4.3, 5.3 or 5.4 for this edit.

## Proposed Section 5 opening

We use four wave problems to examine how the spatial formulation affects the accuracy of the physical fields. A one-soliton solution provides a single localized wave, and a two-soliton solution introduces the interaction of two wave profiles. Gaussian and sinusoidal initial data extend the comparison to localized and periodic smooth fields. Section 5.1 introduces these test problems, their continuous references and the error measures. In Section 5.2, we first evaluate the numerical time derivatives at the initial state, where the difference from the continuous derivatives measures the spatial discretization error. We then advance the same initial fields with RK4 and examine how these differences develop in the coupled evolution of u and v.

## Proposed Section 5.1 opening and profile descriptions

All tests use a=2 and lambda=-2. The one- and two-soliton references are obtained from the continuous Gram determinant solutions in Section 2.1, with rho_i=1 and zero phase shifts. Their spectral parameters and regions are listed in Table 1.

The one-soliton case contains a single oblique wave with negative pulses in both physical fields. The heatmaps show its spatial orientation, while the sections at y=0 resolve the pulse shape in u and v.

The two-soliton case combines two positive u ridges with different orientations. They meet in a region of higher amplitude, while the corresponding v field contains two negative troughs. The heatmaps locate both wave branches and their interaction; the central sections show the resulting profiles along x.

The Gaussian and sinusoidal profile descriptions already in the manuscript can be retained after their figure references are updated.

## Proposed Section 5.2 initial-table discussion

Endpoint-SD gives the smallest u_t error in all four tests. Centered-SD reduces the v_t error relative to Endpoint-SD by factors ranging from approximately 60 to 125. It also gives the smallest v_t error in the one-soliton, Gaussian and sinusoidal cases, while FD gives the smallest value in the two-soliton case. The first and second components therefore favor different spatial approximations.

Retain the following two existing paragraphs and displayed identity concerning Q_k=omega_k^2/2-h omega_k. They apply without modification to the selected four cases.

## Proposed Section 5.2 terminal-table transition

We next advance all three formulations to T=0.01 using RK4 with Delta t=10^-4. The spatial grids, initial physical fields and reference solutions remain the same. Table 3 measures how the errors develop when the two fields evolve together.

## Proposed compact-figure introduction

The four figures below place the three spatial formulations together for each test. The profile panels compare the continuous solution at y=0 with numerical values marked by distinct symbols. The error panels use continuous curves in the corresponding method colors, making the differences visible on their own scale.

If the error panels use the maximum over y at each x, add this precise sentence and its formula:

For each field q, the error curve is the transverse maximum e_q(x)=max_{y in G_q(x)}|q_h(x,y,T)-q*(x,y,T)| over the field's native locations in the stated region. It records where the spatial error is concentrated along x while the central profiles show how accurately the wave shape is reproduced.

This is particularly useful for Gaussian/sinusoidal v because v(x,0,t)=4 exactly; a y=0-only error panel mostly displays roundoff and section-reconstruction noise. A maximum-over-y curve preserves the physical error signal without enlarging that numerical noise. If the parent chooses y=0-only errors instead, omit the transverse-maximum definition and state explicitly that errors are taken along the same section.

## Proposed four result paragraphs, each preceding its figure

### One-soliton case

In the one-soliton case, the three methods reproduce the central pulse profiles, while their errors separate more clearly on the smaller scales of the error panels. Centered-SD reduces the final u and v errors relative to Endpoint-SD by factors of approximately 2.8 and 72. Its u error is smaller even though Endpoint-SD had the smaller initial u_t defect. The first equation couples the evolution of u to the curvature of v through -v_xx, so the second-field error also enters the subsequent first-field evolution. FD gives the smallest final u error, while Centered-SD gives the smallest v error.

### Two-soliton case

For the two-soliton case, the final u errors are closely grouped near 1.15 x 10^-4. The v errors are more widely separated: 5.442 x 10^-4 for Endpoint-SD, 1.049 x 10^-5 for Centered-SD and 8.998 x 10^-6 for FD. Centered-SD therefore reduces the second-field error by a factor of approximately 52 relative to Endpoint-SD, with FD giving the smallest value. The profile and error panels relate these magnitudes to the spatial structure of the interacting waves.

### Gaussian case

The Gaussian profile remains close to its continuous reference after the short evolution. Endpoint-SD gives the smallest u error, while Centered-SD gives the smallest v error. The centered v error is 6.967 x 10^-9, approximately 3.2 times smaller than FD and 87 times smaller than Endpoint-SD. The central v profile stays at its background value of four; its variation away from the central section accounts for the spatial error shown in the transverse-maximum curves.

### Sinusoidal case

The sinusoidal case gives the same ordering of the three methods as the Gaussian case. The central profiles compare the first field over two periods, while the error curves show the repeated spatial pattern. Centered-SD gives a v error of 4.706 x 10^-9, approximately 3.5 times smaller than FD and 60 times smaller than Endpoint-SD. Its u error lies between the Endpoint-SD and FD values.

## Proposed final synthesis

For the Gaussian and sinusoidal tests, E_u(T)/(T E_{u_t}) and E_v(T)/(T E_{v_t}) differ from one by at most 0.43% across all three formulations. The initial derivative defects thus explain their short-time error levels quantitatively. The soliton results also show the effect of coupled evolution: the initial advantage of Endpoint-SD in u_t does not persist in the one-soliton u field, while the centered reconstruction substantially improves v in both soliton tests. Reading the two components together connects the initial spatial approximation with the accuracy of the computed wave.

## Caption templates

For the main compact figures with transverse maxima:

> [Case name] at T=0.01. Left: continuous profiles at y=0 (black solid curves) and numerical values (symbols). Right: transverse maximum absolute errors as functions of x, with one continuous curve for each spatial formulation. Numerical profiles use native y=0 values when available and the verified local section reconstruction otherwise. All methods use h=Delta x=0.1 and RK4 with Delta t=10^-4.

For Gaussian/sinusoidal captions append:

> The central v profile equals four. The displayed x window is [-24,24]; tabulated maxima use the full periodic interval [-96,96).

For initial-derivative compact figures, replace “profiles at T=0.01” with “initial time derivatives at t=0,” fields u/v with u_t/v_t, and remove the time-integration clause.

## Quantitative evidence

`four_case_quantitative_review.json` records selected source values, source hashes, winners and all quoted ratios. The maximum non-soliton deviation from T times the initial defect is 0.4228986%, safely summarized as 0.43%. The one-soliton centered error reductions relative to Endpoint-SD are 2.80348 in u and 71.7192 in v; the two-soliton reduction in v is 51.8558. Gaussian/sinusoidal centered v reductions relative to FD are 3.16652 and 3.47806.
