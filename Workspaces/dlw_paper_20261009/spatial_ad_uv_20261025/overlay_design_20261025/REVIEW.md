# Independent candidate review

2026-10-25. Inspected `summary_D.png`, `zoom_D.png`, `log_Gaussian.png`, their plotting code and the numerical metadata. The existing manuscript and figures were not modified.

**Recommended: E, linear 3D with transverse maxima.** The shared three-method 3D view retains the spatial organization. The compact lower curves reveal the small v errors while showing how the worst transverse error varies along x. The axes and legend are clear, without clipped labels. This is the strongest option for the stated goal of keeping three methods together and making their differences readable.

The lower curves compute the maximum over **all native y samples at each displayed x**, using the full stored arrays. They are not maxima over only the seven displayed 3D slices. The notation should be explained as a sampled/native maximum, consistent with the error table. Its maxima and metadata agree with direct calculations from the source arrays. These curves summarize transverse magnitude; the upper 3D panel retains the y locations.

**F, full height with a second height range, is valid but less efficient.** It doubles the 3D panels, and truncated Endpoint fragments compete with the smaller methods in the lower row. The lower panels keep the same physical values and common method scale. They omit values beyond the displayed upper limit: the implementation masks above `cap * 1.06`, matching the plotted upper range. A caption must state that those line segments are omitted and that gaps do not mean zero error. “Height zoom” alone is too easy to misread without this explanation.

**D, common logarithmic height, is a useful secondary candidate.** The floor is shared by all methods for a component and equals its largest error times 1e-4. Values below that floor are omitted; no artificial epsilon is added to the plotted error. The labels correctly show decades. The logarithmic transform separates the smaller v methods, but it also makes the zero-crossing neighborhoods of the absolute error appear as deep valleys, so the visual remains busy. These are sparse 3D cross-sections on a log-height scale, not filled surfaces.

All three variants use every native x point on the chosen lines. Seven target y levels are mapped to the nearest native y level for each method; SD and FD may differ by a half-grid placement. The page/caption should state this once. No smoothing, vertical offsets or methodwise normalization were found.

Data checks independently confirmed the `summary`, `zoom` and `log` definitions for both D and Gaussian. The parent was notified of the required truncation and native-maximum wording.
