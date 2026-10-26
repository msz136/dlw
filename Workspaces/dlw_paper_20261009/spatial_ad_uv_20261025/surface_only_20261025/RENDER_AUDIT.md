# Transparent-surface rendering audit

2026-10-25. Scope: implementation advice for the user's surface-only overlays. No paper, existing figure or source array was changed.

## Mechanism verified from installed Matplotlib source

`Poly3DCollection.do_3d_projection` sorts polygons inside one collection using `self._zsortfunc(zs.data)`. The three `plot_surface` calls currently create three collections. Their internal polygon orders never interleave across methods; axes-level ordering treats each surface as one artist. The old explicit `computed_zorder=False` and hand-assigned zorders impose a whole-surface order regardless of physical overlap. That is inadequate for transparent intersecting surfaces.

The candidate code also used `antialiased=True` on dense translucent faces. Shared tessellation edges can receive fractional coverage more than once and show seams. At alpha=.045, the intended method color becomes extremely pale while colored overlapping faces and facet boundaries remain visible. Stronger alpha with fewer overlaid primitives is a better starting point than further lowering alpha.

## Practical surface-only implementation

1. Remove every profile/section line. For the primary version, remove all wireframes too.
2. Construct triangles for each method's native x,y,error grid; keep native physical coordinates and a common height scale per component. Split each rectangular cell into two triangles so nonplanar quads are not rendered as ambiguous planar fills.
3. Concatenate all three methods' triangle arrays into **one** `Poly3DCollection`. Concatenate per-face RGBA arrays in the same order. Use `zsort='average'`, `edgecolors='none'`, `linewidths=0`, `antialiaseds=False`, and normal automatic axes ordering. This allows cross-method faces to participate in one depth sort.
4. Start at opacity .25–.35 with blue/orange/green method colors, or set the tallest surface modestly more transparent (.20–.25) and lower surfaces .32–.40 as an explicitly visual layer treatment. Do not normalize their heights or add offsets.
5. Use an orthographic camera, elevation about 30–40 degrees, and a modest z aspect ratio. Render 2× the intended delivery dimensions and downsample the finished raster using Lanczos. This softens raster staircase/seam artifacts without changing the sampled error field.
6. For the optional mesh version, keep only about 5×7 mesh lines per surface, very low opacity and fine width. Avoid independently forcing those lines in front of all surfaces. A texture-like sparse grid encoded in face color can be less intrusive than another separately ordered wireframe artist, though it needs checking at high curvature.

## Mesh density and visual smoothing

Use all stored x points for the narrow soliton band whenever practical. Sparse x sampling caused demonstrable peak loss in the preceding audit. Three full D meshes create roughly 2.15 million triangles per physical component, so full-native geometry is expensive for mplot3d's Python sorting. A documented display mesh with adaptive refinement near large curvature/gradient is reasonable. Preserve maxima and inspect per-row peak retention, rather than only the global maximum. Simple bilinear interpolation of sampled heights is bounded and does not overshoot; cubic smoothing can create misleading extrema and should not be used merely to make these errors look better.

If using global mesh subsampling, it should remain labelled as display-mesh sampling. No data recomputation is required. Surface lighting should communicate geometry softly; it should not introduce fake gradients that could be read as another scalar variable.

## Residual limits relevant to choice

A single Poly3DCollection uses painter-style face ordering, not a true per-pixel depth buffer. Intersecting triangles and nearly coincident surfaces can still show artifacts. Near-zero common floor surfaces may blend to gray even when no mesh is drawn. These are rendering limits, not evidence of numerical oscillation. The smaller v error still occupies roughly 1% of the common linear height because the physical peak ratio is about 70–87; transparency can reveal it but cannot make that geometry tall. Camera and opacity should improve visibility while preserving this fact.

If the parent chooses a custom rasterizer, per-pixel depth compositing of the three colored surfaces is the robust route. It can use the same native triangulation and source values, so it changes only rendering, not the error field.
