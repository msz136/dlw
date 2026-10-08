import VariationalReduction

namespace DLWLean
noncomputable section
open scoped BigOperators

theorem periodicCoefficient_integral_square_nonneg (par : FieldParameters)
    (q : PeriodicCoefficient par.Lx) :
    0 ≤ periodicCoefficientIntegral par.Lx (q * q) := by
  change 0 ≤ ∫ x in (0 : ℝ)..par.Lx, (q : ℝ → ℝ) x * (q : ℝ → ℝ) x
  exact intervalIntegral.integral_nonneg_of_forall par.Lx_pos.le
    (fun x => mul_self_nonneg ((q : ℝ → ℝ) x))

theorem coefficientPairing_self_zero (par : FieldParameters)
    (f : ClosedPeriodicField par) (hf : coefficientPairing par f f = 0) : f = 0 := by
  have hint : (∑ j : Fin par.M, periodicCoefficientIntegral par.Lx (f j * f j)) = 0 := by
    have h : periodicCoefficientIntegral par.Lx (∑ j : Fin par.M, f j * f j) = 0 :=
      (mul_eq_zero.mp hf).resolve_left (ne_of_gt par.h_pos)
    simpa only [map_sum] using h
  apply Subtype.ext
  funext j
  have hj : periodicCoefficientIntegral par.Lx (f j * f j) = 0 :=
    (Finset.sum_eq_zero_iff_of_nonneg
      (fun i _ => periodicCoefficient_integral_square_nonneg par (f i))).mp hint j
      (Finset.mem_univ j)
  exact periodicCoefficient_integral_square_zero par.Lx par.Lx_pos (f j) hj

theorem coefficientGradientPairing_nondegenerate (par : FieldParameters)
    (f : ClosedPeriodicPair par)
    (hf : ∀ v : ClosedPeriodicPair par, coefficientGradientPairing par f v = 0) : f = 0 := by
  have hzero (a : ClosedPeriodicField par) : coefficientPairing par a 0 = 0 := by
    change par.h * periodicCoefficientIntegral par.Lx
      (∑ j : Fin par.M, a j * (0 : PeriodicCoefficient par.Lx)) = 0
    simp
  have hp := hf (f.1, 0)
  have hs := hf (0, f.2)
  simp only [coefficientGradientPairing, hzero, add_zero, zero_add] at hp hs
  apply Prod.ext
  · exact coefficientPairing_self_zero par f.1 hp
  · exact coefficientPairing_self_zero par f.2 hs

/-- True gradients representing the same actual directional derivatives
are equal, by nondegeneracy of the genuine period integral pairing. -/
theorem coefficientGradientPairing_ext (par : FieldParameters)
    (f g : ClosedPeriodicPair par)
    (hfg : ∀ v : ClosedPeriodicPair par,
      coefficientGradientPairing par f v = coefficientGradientPairing par g v) : f = g := by
  have h := coefficientGradientPairing_nondegenerate par (f + -g) (by
    intro v
    change coefficientPairing par (f.1 + -g.1) v.1 +
      coefficientPairing par (f.2 + -g.2) v.2 = 0
    rw [coefficientPairing_add_left, coefficientPairing_add_left]
    rw [coefficientPairing_symmetric par (-g.1) v.1,
      coefficientPairing_symmetric par (-g.2) v.2,
      coefficientPairing_neg_right, coefficientPairing_neg_right,
      coefficientPairing_symmetric par v.1 g.1, coefficientPairing_symmetric par v.2 g.2]
    have hv := hfg v
    unfold coefficientGradientPairing at hv
    linarith)
  apply Prod.ext
  · apply Subtype.ext
    funext j
    apply Subtype.ext
    funext x
    have hx := congrArg (fun a : ClosedPeriodicPair par => (a.1 j : ℝ → ℝ) x) h
    change (f.1 j : ℝ → ℝ) x + -(g.1 j : ℝ → ℝ) x = 0 at hx
    change (f.1 j : ℝ → ℝ) x = (g.1 j : ℝ → ℝ) x
    linarith
  · apply Subtype.ext
    funext j
    apply Subtype.ext
    funext x
    have hx := congrArg (fun a : ClosedPeriodicPair par => (a.2 j : ℝ → ℝ) x) h
    change (f.2 j : ℝ → ℝ) x + -(g.2 j : ℝ → ℝ) x = 0 at hx
    change (f.2 j : ℝ → ℝ) x = (g.2 j : ℝ → ℝ) x
    linarith

theorem reducedBracketValue_add_left (par : FieldParameters)
    (f g k : ClosedPeriodicPair par) :
    reducedBracketValue par (f + g) k =
      reducedBracketValue par f k + reducedBracketValue par g k := by
  simp only [reducedBracketValue, coefficientGradientPairing, Prod.fst_add, Prod.snd_add,
    coefficientPairing_add_left]
  ring

theorem reducedBracketValue_smul_left (par : FieldParameters)
    (r : ℝ) (f g : ClosedPeriodicPair par) :
    reducedBracketValue par (r • f) g = r * reducedBracketValue par f g := by
  change coefficientPairing par (r • f.1) (reducedHamiltonianVector par g).1 +
    coefficientPairing par (r • f.2) (reducedHamiltonianVector par g).2 = _
  rw [coefficientPairing_smul_left, coefficientPairing_smul_left]
  unfold reducedBracketValue coefficientGradientPairing
  ring

theorem reducedBracketValue_add_right (par : FieldParameters)
    (f g k : ClosedPeriodicPair par) :
    reducedBracketValue par f (g + k) =
      reducedBracketValue par f g + reducedBracketValue par f k := by
  rw [reducedBracketValue_skew, reducedBracketValue_add_left,
    reducedBracketValue_skew par g f, reducedBracketValue_skew par k f]
  ring

theorem reducedBracketValue_smul_right (par : FieldParameters)
    (r : ℝ) (f g : ClosedPeriodicPair par) :
    reducedBracketValue par f (r • g) = r * reducedBracketValue par f g := by
  rw [reducedBracketValue_skew, reducedBracketValue_smul_left, reducedBracketValue_skew par g f]
  ring

/-- An equality of the original functionals implies the corresponding
equality of their constructed true gradients. -/
theorem gradient_affine_relation (par : FieldParameters)
    (K F P : ClosedPeriodicPair par → ℝ) (z gK gF gP : ClosedPeriodicPair par)
    (α β κ : ℝ) (hvalue : ∀ w, K w = α * F w + β * P w + κ)
    (hK : ∀ v, HasDerivAt (fun t : ℝ => K (z + t • v))
      (coefficientGradientPairing par gK v) 0)
    (hF : ∀ v, HasDerivAt (fun t : ℝ => F (z + t • v))
      (coefficientGradientPairing par gF v) 0)
    (hP : ∀ v, HasDerivAt (fun t : ℝ => P (z + t • v))
      (coefficientGradientPairing par gP v) 0) : gK = α • gF + β • gP := by
  apply coefficientGradientPairing_ext par
  intro v
  have hpair : coefficientGradientPairing par (α • gF + β • gP) v =
      α * coefficientGradientPairing par gF v + β * coefficientGradientPairing par gP v := by
    change coefficientPairing par (α • gF.1 + β • gP.1) v.1 +
      coefficientPairing par (α • gF.2 + β • gP.2) v.2 = _
    rw [coefficientPairing_add_left, coefficientPairing_add_left,
      coefficientPairing_smul_left, coefficientPairing_smul_left,
      coefficientPairing_smul_left, coefficientPairing_smul_left]
    unfold coefficientGradientPairing
    ring
  rw [hpair]
  have hfun : (fun t : ℝ => K (z + t • v)) =
      fun t : ℝ => α * F (z + t • v) + β * P (z + t • v) + κ :=
    funext (fun t => hvalue (z + t • v))
  have hk := hK v
  rw [hfun] at hk
  have h := ((hF v).const_mul α).add ((hP v).const_mul β)
  have hc := h.add_const κ
  exact hk.unique hc

#print axioms coefficientGradientPairing_nondegenerate
#print axioms coefficientGradientPairing_ext
#print axioms gradient_affine_relation
end
end DLWLean
