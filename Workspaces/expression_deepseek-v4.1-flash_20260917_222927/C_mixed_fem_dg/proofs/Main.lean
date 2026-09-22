/-
  Direction C entry point: imports the FEM/DG-in-y formalisation and re-prints the
  axiom footprint of the headline theorems (`#print axioms`).
-/
import C_FEM_DG

namespace DLWC

#print axioms DLWC.p1_mass_det
#print axioms DLWC.p1_mass_det_ne_zero
#print axioms DLWC.p1_stiffness_kills_constant
#print axioms DLWC.mass_symbol_ne_zero
#print axioms DLWC.p1_symbol_pos_in_band
#print axioms DLWC.muP1_nyquist_zero
#print axioms DLWC.dg_symbol_no_nyquist_zero
#print axioms DLWC.p1_symbol_normalisation
#print axioms DLWC.dg_upwind_dissipation_identity
#print axioms DLWC.dg_upwind_dissipation_nonneg

end DLWC
