# Figure reference and proposed text

Reviewed 2026-10-25. Sources: `Paper/sources/dlw_y_lattice_20261018/DLW_y_lattice_and_2HS.pdf`, physical PDF pages 12–17; `report/dlw_paper_draft.html`, English test descriptions and spatial-comparison captions. Existing exact C/D profile images were visually checked. PDF source pages are rendered as esd-12.png through esd-17.png in this directory.

## Observed reference style

The ESD PDF puts one case into a compact 2-by-2 figure. The upper row is u and the lower row v; the left column gives an x slice near y=0 and the right column an x-y heatmap. Each heatmap has a narrow adjacent colorbar. The axes are thin, the background white, there are no grid lines, and the plot text is simple sans serif. Slice curves use the standard blue/orange/green sequence and heatmaps use viridis. Small panel titles name the field and time. In the PDF, the slices compare three times; in the requested figures these can instead compare the exact solid line and numerical symbols at the common final time.

The source PDF devotes an entire page to each modest-size figure, leaving large white margins. The useful reference is the compact panel layout and its plotting conventions, not those page floats. Preserve a consistent field order and method order across the six cases. For errors, keep a common color scale across all three methods within each field and case. If a log scale is used, label it explicitly. Initial-field colorbars may use their own physical ranges.

## Source-matched test descriptions

### A: one soliton (1,2)

Case A contains a single oblique wave with negative pulses in both physical fields. The initial heatmaps show the narrow wave band across the region, while the central sections resolve its transverse pulse shape. This gives a simple profile on which to compare the representation of the two fields before introducing interacting waves.

### B: one soliton (4,-3)

Case B reverses the polarity of the first field: u forms a positive ridge, while v remains a negative trough. Its amplitude, width and orientation also differ from Case A. The two single-wave tests therefore examine more than a change of sign; they expose the methods to different spatial scales within the same exact solution family.

### C: two solitons (6,-5), (4,-3)

Case C combines two positive u ridges with different orientations. They meet in a region of higher amplitude, and the corresponding v field contains two negative troughs whose shapes change near the interaction. The heatmaps identify both wave branches and their meeting region, while the central sections give a one-dimensional view through this spatial structure.

### D: two solitons (1,2), (4,-3)

Case D combines the two parameter pairs used in Cases A and B. A stronger negative u trough appears together with a smaller positive ridge, while both v wave bands remain negative. The unequal amplitudes and widths make this a useful complement to Case C, since the numerical approximation must resolve two features of different polarity and strength within the same field.

### Gaussian

The Gaussian test starts from a positive localized u profile with a sinusoidal envelope in y. The second field varies about the constant background v=4: it lies below this value in the lower half of the region and above it in the upper half. Both variations inherit the same Gaussian dependence on x. This gives a smooth localized benchmark in which the two physical fields have different transverse structures.

### Sinusoidal

The sinusoidal test replaces the localized Gaussian factor by cos(pi x/12), while retaining the same transverse envelope and the same relation v0=4-3u0_y. The resulting u field alternates in sign along x. The deviation of v from its background also oscillates, with its transverse sign reversed across y=0. This provides a periodic counterpart to the Gaussian test with the same boundary conditions and reference construction.

## Captions

These templates assume the ESD-style 2-by-2 initial figure: u above v, central sections left and exact x-y distributions right. Match the panel positions to the actual exported figure before publication.

- A: Exact initial fields for the (1,2) one-soliton solution. The upper row shows u and the lower row v. The left panels give the sections at y=0; the right panels show the distributions in the x-y plane.
- B: Exact initial fields for the (4,-3) one-soliton solution, with a positive u ridge and a negative v trough. The upper row shows u and the lower row v; central sections and spatial distributions are arranged as in Figure [A].
- C: Exact initial fields for the (6,-5; 4,-3) two-soliton solution. The two u ridges and the corresponding v troughs meet within the displayed region. The left panels show y=0 sections and the right panels the full spatial distributions.
- D: Exact initial fields for the mixed-polarity (1,2; 4,-3) two-soliton solution. The u field contains a positive ridge and a deeper negative trough; the v field contains two negative wave bands. The field and panel ordering is the same as in Figure [C].
- Gaussian: Gaussian initial fields u0=0.05 sin(pi(y+2)/4)G(x) and v0=4-3u0_y. The left panels show the sections at y=0, and the right panels the two-dimensional fields. The central v section equals its background value 4.
- Sinusoidal: Sinusoidal initial fields u0=0.03 sin(pi(y+2)/4)cos(pi x/12) and v0=4-3u0_y. The y=0 sections appear on the left and the spatial distributions on the right. The displayed x window contains [actual number] periods.

Final-section template:

    Physical-field sections at y=0 and T=0.01 for Case [case]. Solid curves show the continuous reference solution; symbols show Endpoint-SD, Centered-SD and FD, using RK4 with h=Delta x=0.1 and Delta t=10^-4. Numerical profiles are interpolated to y=0 from their native field locations, and symbols are shown at selected x nodes.

If the final comparison integrates slices and errors into a single 2-by-4 figure:

    Case [case] at T=0.01. The upper row shows u and the lower row v. The first column compares the reference y=0 sections (solid curves) with the numerical profiles (symbols). The remaining columns show the absolute-error heatmaps for Endpoint-SD, Centered-SD and FD, respectively. Error maps use each field's native positions, with a common color scale across methods within each row.

Standalone error-map template:

    Absolute physical-field errors at T=0.01 for Case [case]. Columns show Endpoint-SD, Centered-SD and FD; rows show |u_h-u*| and |v_h-v*|. Each field uses a common color scale across the three methods. All methods use RK4 with h=Delta x=0.1 and Delta t=10^-4.

## Details that affect interpretation

At y=0, both new reference families have v=4 at every time, not just initially: the exact formula is v=4+s_y times a smooth function and s_y vanishes there. A flat exact v line is therefore expected. A v-4 axis or error inset can show the small numerical departure clearly; label that plotted quantity explicitly.

Some y=0 sections are between native y sites. Soliton u and FD v are on half-shifted nodes; Gaussian/sinusoidal edge v is also half-shifted. Display interpolation must be stated once in the caption. Norms and error heatmaps should keep the original native positions.

The old draft's test descriptions remain useful, but its PE/PF rankings and spatial-error pictures belong to older implementations. Spatial claims about the new heatmaps must be based on their actual rendered distributions. The present numerical tables support the amplitude comparisons listed in SCIENTIFIC_REVIEW.md.
