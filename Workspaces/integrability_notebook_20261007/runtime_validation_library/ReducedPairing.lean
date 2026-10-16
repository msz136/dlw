import FieldCoordinates

/-! Finite lattice identities for gauge invariant gradient reduction. -/
namespace DLWLean
noncomputable section
open scoped BigOperators

theorem sum_mul_projector_of_zero_mean {M : ℕ}
    (f g : Fin M → ℝ) (hf : latticeMean f = 0) :
    (∑ j, f j * latticeP0 g j) = ∑ j, f j * g j := by
  by_cases hM : M = 0
  · subst M
    simp
  have hsum : ∑ j, f j = 0 := by
    have hm : (M : ℝ) ≠ 0 := by exact_mod_cast hM
    simpa [latticeMean, hm] using hf
  simp only [latticeP0, mul_sub, Finset.sum_sub_distrib,
    ← Finset.sum_mul, hsum, zero_mul, sub_zero]

theorem sum_projector_mul_of_zero_mean {M : ℕ}
    (f g : Fin M → ℝ) (hg : latticeMean g = 0) :
    (∑ j, latticeP0 f j * g j) = ∑ j, f j * g j := by
  simpa only [mul_comm] using sum_mul_projector_of_zero_mean g f hg

/-- The differential of the nonlinear closed chart at a fixed field value. -/
def chartTangentU {M : ℕ} (c : ℝ) (p s dp ds : Fin M → ℝ)
    (j : Fin M) : ℝ :=
  dp j - latticeMean (fun i => dp i * s i + p i * ds i) / c

/-- With zero common-U gradient, the nonlinear shear in the chart drops
out of the dual pairing. This proves the finite lattice chain-rule step. -/
theorem chart_pairing_gauge_reduction {M : ℕ}
    (c : ℝ) (p s dp ds fU fw : Fin M → ℝ)
    (hfU : latticeMean fU = 0) (hds : latticeMean ds = 0) :
    (∑ j : Fin M, (fU j * chartTangentU c p s dp ds j + fw j * ds j)) =
      ∑ j : Fin M, (fU j * dp j + latticeP0 fw j * ds j) := by
  have hsum : ∑ j, fU j = 0 := by
    by_cases hM : M = 0
    · subst M
      simp
    · have hm : (M : ℝ) ≠ 0 := by exact_mod_cast hM
      simpa [latticeMean, hm] using hfU
  simp only [chartTangentU, mul_sub, Finset.sum_add_distrib,
    Finset.sum_sub_distrib, ← Finset.sum_mul, hsum, zero_mul, sub_zero]
  rw [sum_projector_mul_of_zero_mean fw ds hds]

/-- Once common-U gradients and their x derivatives have zero lattice
mean, the projected reduced pairing equals the original constant pairing. -/
theorem reduced_pairing_eq_ambient {M : ℕ}
    (fU fw dxgU dxgw : Fin M → ℝ)
    (hfU : latticeMean fU = 0) (hdxgU : latticeMean dxgU = 0) :
    (∑ j : Fin M, (fU j * latticeP0 dxgw j + latticeP0 fw j * dxgU j)) =
      ∑ j : Fin M, (fU j * dxgw j + fw j * dxgU j) := by
  simp only [Finset.sum_add_distrib]
  rw [sum_mul_projector_of_zero_mean fU dxgw hfU,
    sum_projector_mul_of_zero_mean fw dxgU hdxgU]

#print axioms chart_pairing_gauge_reduction
#print axioms reduced_pairing_eq_ambient

end
end DLWLean
