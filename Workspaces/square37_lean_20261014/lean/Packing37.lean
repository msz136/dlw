import CertificateWalls
import CertificatePairs0
import CertificatePairs1
import CertificatePairs2
import CertificatePairs3
import CertificatePairs4
import CertificatePairs5
import CertificatePairs6

namespace Packing37
open PackingGeometry

theorem all_strict_separated : ∀ i j : Fin 37, i < j →
    QStrictSeparated (squares i) (squares j) (normal i j).1 (normal i j).2 := by
  intro i j h
  fin_cases i
  · exact row_0 j h
  · exact row_1 j h
  · exact row_2 j h
  · exact row_3 j h
  · exact row_4 j h
  · exact row_5 j h
  · exact row_6 j h
  · exact row_7 j h
  · exact row_8 j h
  · exact row_9 j h
  · exact row_10 j h
  · exact row_11 j h
  · exact row_12 j h
  · exact row_13 j h
  · exact row_14 j h
  · exact row_15 j h
  · exact row_16 j h
  · exact row_17 j h
  · exact row_18 j h
  · exact row_19 j h
  · exact row_20 j h
  · exact row_21 j h
  · exact row_22 j h
  · exact row_23 j h
  · exact row_24 j h
  · exact row_25 j h
  · exact row_26 j h
  · exact row_27 j h
  · exact row_28 j h
  · exact row_29 j h
  · exact row_30 j h
  · exact row_31 j h
  · exact row_32 j h
  · exact row_33 j h
  · exact row_34 j h
  · exact row_35 j h
  · exact row_36 j h

theorem all_separated : ∀ i j : Fin 37, i < j →
    QSeparated (squares i) (squares j) (normal i j).1 (normal i j).2 :=
  fun i j h => (all_strict_separated i j h).weak

theorem closed_disjoint : ∀ i j : Fin 37, i ≠ j → ∀ p : Point,
    ¬ ((squares i).real.closed p ∧ (squares j).real.closed p) := by
  intro i j hij p hp
  rcases lt_or_gt_of_ne hij with h | h
  · exact real_closed_separated (squares i) (squares j) _ _ (all_strict_separated i j h) p hp
  · exact real_closed_separated (squares j) (squares i) _ _ (all_strict_separated j i h) p ⟨hp.2, hp.1⟩

theorem certified_packing : IsPacking (side : ℝ) (fun i => (squares i).real) :=
  packing_of_rational_certificate side squares normal all_unit all_bounds all_separated

theorem exists_packing_37 : ∃ s : Fin 37 → Square,
    IsPacking ((659861960924437 / 100000000000000) : ℝ) s := by
  refine ⟨fun i => (squares i).real, ?_⟩
  simpa [side] using certified_packing

#print axioms all_unit
#print axioms all_bounds
#print axioms all_separated
#print axioms closed_disjoint
#print axioms certified_packing
#print axioms exists_packing_37

end Packing37
