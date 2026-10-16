# Actual nonlinear norming evolution: center invariance and moving-frame commutator

2026-10-13. Companion to [the exact period theorem](PERIODIC_SPECTRAL_FLOWS.md). This derives the evolution of the EXISTING calibrated norming candidates; the averaged coordinates in that theorem are newly constructed coordinates and must not be confused with them.

## 1. The center is constant, the frame is not

Along X_Aα every actual monodromy characteristic class is preserved. Thus the target cluster's absolute branch center aβ is constant. The complete slow matrix satisfies Hdot=[Kslow,H], so hℓ(H) is constant too. Consequently the moving-grid center cβ=aβ−K_n−hℓ is constant. This conclusion follows from the full field bridge, not merely from Dcβ(0)=0.

At λ=aβ let Tβ map a fixed reference two-plane to the actual Riesz two-plane, including the existing source-dependent slow eigenbasis, compression intertwiner, and the fixed background calibration Cβ. Its reference projector is P0. The actual calibrated block has the form

\[
 M_\beta=\sigma_\beta P_0T_\beta^{-1}N_{a_\beta}T_\beta P_0,
 \tag{1}
\]

where the nonzero scalar σβ accounts for the difference between determinant-normalized and moving-grid-normalized monodromy. It depends on λ, trH and hℓ(H), all fixed along the present orbit; hence σdot=0. The background calibration χβ is source independent.

Since Pdot=[Gα(aβ;0),P] and Tβ⁻¹ P Tβ=P0, the matrix

\[
 \mathcal V_{\alpha\beta}=P_0T_\beta^{-1}
 (G_\alpha(a_\beta;0)T_\beta-\dot T_\beta)P_0
 \tag{2}
\]

is the complete moving-frame generator on that plane. The uncompressed expression commutes with P0. Differentiating (1), with λdot=0, gives the exact identity

\[
 \boxed{\dot M_\beta=[\mathcal V_{\alpha\beta},M_\beta].}
 \tag{3}
\]

The term −T⁻¹Tdot is essential. Dropping it would calculate norming evolution in a different frame.

## 2. The exact obstruction to raw reciprocal scaling

Write ν+=M12/χ, ν−=M21/χ, δ=(M11−M22)/χ and V=(vij). Equation (3) gives

\[
 \boxed{\dot\nu^+=(v_{11}-v_{22})\nu^+-v_{12}\delta,\qquad
 \dot\nu^-=-(v_{11}-v_{22})\nu^-+v_{21}\delta,}
 \tag{4}
\]

\[
 \boxed{\dot\delta=2(v_{12}\nu^--v_{21}\nu^+),\qquad
 \frac d{dt}(\nu^+\nu^-)=-\tfrac12\delta\dot\delta.}
 \tag{5}
\]

Thus the raw product ν+ν− is not shown invariant by isospectrality. What is exactly invariant is ν+ν−+δ²/4, the discriminant of the calibrated matrix divided by 4χ². This quantity still carries the moving scalar normalization of that block.

A PURE characteristic invariant is obtained by det-normalizing the actual block:

\[
 \widehat M=M/\sqrt{\det M},\quad
 b=\widehat M_{12},\quad c=\widehat M_{21},\quad
 d=\widehat M_{11}-\widehat M_{22}.
\]

Choose the determinant root by its nonzero background value. Then

\[
 \boxed{\mathcal S_\beta=bc+d^2/4
 =\frac{(\operatorname{tr}M)^2}{4\det M}-1.}
 \tag{6}
\]

Sβ is invariant under arbitrary block similarity and nonzero scalar normalization, at the actual class-defined center aβ. It is a holomorphic function of actual characteristic classes evaluated at that class-defined center. Chain rule and established spectral involution therefore show that all these Sβ mutually commute, and commute with every reciprocal Aα. At fixed β their actual low Hamilton fields exist by the same finite contour/trace chain rule used for the actual center fields.

Using κ=½log(μ+/μ−),

\[
 \mathcal S_\beta=\sinh^2\kappa_\beta(a_\beta),
 \quad\mathcal S_\beta^{[2]}=-L^2\gamma_\beta^2g_\beta^{[2]}/4
 =\nu_\beta^{+,[1]}\nu_\beta^{-,[1]}.
 \tag{7}
\]

The apparent evaluation at a branch cut is unambiguous: sinh²κ is single-valued and analytic there. Its expression through trace and determinant in (6) defines it even at a closed gap. The local square-root representation of κ gives Sβ=−gβ fβ with fβ analytic and fβ(0)=L²γβ²/4≠0. For each fixed β, after shrinking its neighborhood, Sβ=0 iff gβ=0. No index-uniform inverse of the factor or full action equivalence is inferred solely from this fixed-index statement.

## 3. A fixed-index quartic drift identity

At the actual uniform source the calibrated diagonal first variations vanish at the exact center (zero component means and the diagonal Born calculation). Hence ν±=O(||x||), δ=O(||x||²). The unit norming linearization of X_Aα and the independent target linear Born coordinates imply

\[
 v_{12}(0)=v_{21}(0)=0,\qquad
 v_{11}(0)-v_{22}(0)=\delta_{\alpha\beta}.
\]

For example, a nonzero v12(0) would produce an unwanted linear diagonal commutator proportional to ν−, while the diagonal variation must start at quadratic order; independence of ν± forces both offdiagonals to vanish. Analyticity gives vij,off=O(||x||), for each FIXED pair α,β. Equations (4)–(5) then yield

\[
 \dot\nu_\beta^\pm=\pm\delta_{\alpha\beta}\nu_\beta^\pm+O(\|x\|^2),
 \qquad\frac d{dt}(\nu_\beta^+\nu_\beta^-)=O(\|x\|^4).
 \tag{8}
\]

The exact quartic correction is δ²/4. This is an algebraic order result, not a uniform high-frequency estimate, a nonzero DLW drift example, or proof that the O(||x||²) term in the individual torques is nonzero. Isospectrality alone permits the mixing terms; the exact period theorem provides a nonlinear coordinate change that removes them for each FIXED FINITE family.

## 4. Consequence for the infinite construction

There are now two explicit options: control the infinite Bochner averages using simultaneous period-flow bounds; or solve the moving-frame equations (2)–(5) for globally compatible norming corrections. Either route must control all labels on a common source neighborhood, include finite low data, and preserve the original weak symplectic pairing. The displayed finite identities do not supply those missing estimates.
