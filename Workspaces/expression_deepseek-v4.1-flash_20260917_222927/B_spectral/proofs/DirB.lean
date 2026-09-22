/-
  Direction B — spectral / pseudo-spectral semidiscretisation of the DLW system.
  Root module: imports the three spectral modules and prints the axiom footprint
  of every headline theorem.

  Headline results
  ----------------
  * `DLW.Spectral.mult_eq_zero_iff`,
    `DLW.Spectral.kernel_eq_zero_mode_line` — the exact kernel of the
    `y`-derivative multiplier on the retained band `-N..N` is the zero-mode line.
  * `DLW.Spectral.zeroMeanEquiv`,
    `DLW.Spectral.mult_invMult`, `DLW.Spectral.invMult_mult` — on the zero-mean
    subspace the multiplier is invertible, with inverse the mode-by-mode division
    `1/(i l)`; this is the exact statement that `w = u_y` can be solved for every
    non-zero mode and *only* the zero mode is obstructed.
  * `DLW.Spectral.mult_comp_modeProj`,
    `DLW.Spectral.modeProj_comp_mult` — the multiplier is diagonal in the mode
    basis, hence commutes with every mode projection (in particular with the
    mean).
  * `DLW.Spectral.dispersion_relation` — from the linearised DLW mode system,
    `(s + i (u0 + 2a) k)^2 = k^4 - (v0 + 2 lam) k^3 / l`, in
    `x`-wavenumber `k` and `y`-wavenumber `l`.
  * `DLW.Spectral.growth_lower_bound`,
    `DLW.Spectral.band_contains_growing_mode` — for `c = v0 + 2 lam >= 0` and any
    retained mode `l >= 1`, `Re s >= k^2 - (c/l) k` for every `k >= c/l`.  The
    bound contains **no truncation parameter**: no fixed band is uniformly stable.
  * `DLW.Spectral.sample_alias`,
    `DLW.Spectral.out_of_band_folds_into_band`,
    `DLW.Spectral.aliasing_breaks_projected_identity` — aliasing quantified and
    the un-dealiased pseudo-spectral projected identity refuted.
  * `DLW.Spectral.band_unstable_uniform_in_N` — for every truncation `N >= 1` and
    every `k > 0` the retained band contains the mode `l = -1` with
    `Re s = sqrt (k^4 + c k^3) >= k^2`; the statement contains no `N`, so a stable
    fixed truncation is not grid-uniform stability.  `band_stability_threshold` is
    the matching one-sided (`l >= 1`) neutral bound with threshold `k <= c/N`.

  Cross-reference to the shared lattice library (`Common/Operators.lean`):
  `DLW.Common.ctr_kernel` shows that the *lattice* centred difference kills every
  sequence with `w (j+1) = w (j-1)` — a class strictly larger than the constants
  on a bi-infinite lattice.  The spectral kernel above is exactly one-dimensional.
  The two are statements about different representations of the same physical
  field; see `report.md` §1.1 and §1.4, and `CONCLUSIONS.md` 结论 7 (the parity
  observation: odd grid size gives a one-dimensional centred-difference kernel,
  even grid size gives a spurious second zero mode).
-/
import Spectral.Multiplier
import Spectral.Growth
import Spectral.Aliasing
import Common.Operators

namespace DLW.Spectral

-- The shared lattice library is reachable from this root:
#check @DLW.Common.ctr_kernel
#check @DLW.Common.ctr_const
#check @DLW.Common.sbp_fwd

-- Axiom footprint of the headline theorems (expected: `propext`,
-- `Classical.choice`, `Quot.sound` only).
#print axioms DLW.Spectral.mult_eq_zero_iff
#print axioms DLW.Spectral.kernel_eq_zero_mode_line
#print axioms DLW.Spectral.invMult_mult
#print axioms DLW.Spectral.mult_invMult
#print axioms DLW.Spectral.mult_comp_modeProj
#print axioms DLW.Spectral.modeProj_comp_mult
#print axioms DLW.Spectral.dispersion_relation
#print axioms DLW.Spectral.nontrivial_dispersion_relation
#print axioms DLW.Spectral.mode_of_dispersion_relation
#print axioms DLW.Spectral.growth_lower_bound
#print axioms DLW.Spectral.exists_growing_mode
#print axioms DLW.Spectral.mode_of_nonneg_discriminant
#print axioms DLW.Spectral.neutral_mode_of_negative_discriminant
#print axioms DLW.Spectral.band_stability_threshold
#print axioms DLW.Spectral.band_instability_threshold
#print axioms DLW.Spectral.band_unstable_uniform_in_N
#print axioms DLW.Spectral.band_contains_growing_mode
#print axioms DLW.Spectral.sample_alias
#print axioms DLW.Spectral.out_of_band_folds_into_band
#print axioms DLW.Spectral.three_point_collision
#print axioms DLW.Spectral.aliasing_breaks_projected_identity

end DLW.Spectral
