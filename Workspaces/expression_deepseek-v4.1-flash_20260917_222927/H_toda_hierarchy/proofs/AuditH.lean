/-
  Axiom audit for Direction H.

  This module imports `DirH` and prints the axiom dependencies of every headline
  theorem.  Each `#print axioms` line must report only the standard Lean axioms
  (`propext`, `Classical.choice`, `Quot.sound`) and no user axiom.
-/
import DirH

#print axioms DLW.DirH.det_two_scaling
#print axioms DLW.DirH.det_two_row_scaling
#print axioms DLW.DirH.tau_ratio_is_modulus
#print axioms DLW.DirH.levelFamily_three_term
#print axioms DLW.DirH.todaGap_eq_one
#print axioms DLW.DirH.logDeriv_eq_zero
#print axioms DLW.DirH.logDeriv_eq_zero_ratio
