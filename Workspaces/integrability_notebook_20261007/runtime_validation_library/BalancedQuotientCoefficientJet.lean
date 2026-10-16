import BalancedResolventCoefficientJet

namespace DLWLean.BalancedPDO
noncomputable section
open scoped BigOperators

variable {M : ℕ} {R A : Type*} [CommRing R] [Algebra ℝ R] [Ring A] [Algebra ℝ A]
    (model : NormalPDOModel R A) (e : DifferentialJetEvaluation M R model.d)

theorem regularQuotient_jet_zero_eta (V : ℕ → ℕ → Poly M)
    (hη₀ : e.jet.value (MvPolynomial.X .eta) = 0)
    (hη₁ : e.jet.first (MvPolynomial.X .eta) = 0)
    (hη₂ : e.jet.second (MvPolynomial.X .eta) = 0) (n k : ℕ) :
    e.jet.value (regularQuotientCoefficient M V n k) =
      ∑ j ∈ Finset.range n, e.jet.value (V j k) ∧
    e.jet.first (regularQuotientCoefficient M V n k) =
      ∑ j ∈ Finset.range n, e.jet.first (V j k) ∧
    e.jet.second (regularQuotientCoefficient M V n k) =
      ∑ j ∈ Finset.range n, e.jet.second (V j k) := by
  induction n generalizing k with
  | zero => simp [regularQuotientCoefficient]
  | succ n ih =>
    cases k with
    | zero =>
      rw [regularQuotientCoefficient]
      simp only [map_add, Finset.sum_range_succ, (ih 0).1, (ih 0).2.1, (ih 0).2.2]
      exact ⟨add_comm _ _, add_comm _ _, add_comm _ _⟩
    | succ k =>
      rw [regularQuotientCoefficient]
      simp only [map_add, map_mul, e.jet.first_mul, e.jet.second_mul,
        hη₀, hη₁, hη₂, zero_mul, zero_add, add_zero,
        Finset.sum_range_succ, (ih (k + 1)).1, (ih (k + 1)).2.1, (ih (k + 1)).2.2]
      exact ⟨add_comm _ _, add_comm _ _, add_comm _ _⟩

theorem balancedQuotient_jet_sum
    (hη₀ : e.jet.value (MvPolynomial.X .eta) = 0)
    (hη₁ : e.jet.first (MvPolynomial.X .eta) = 0)
    (hη₂ : e.jet.second (MvPolynomial.X .eta) = 0) (k : ℕ) :
    e.jet.value (balancedQuotientCoefficient M k) =
      ∑ j : Fin M, e.jet.value (siteQuotientCoefficient M j k) ∧
    e.jet.first (balancedQuotientCoefficient M k) =
      ∑ j : Fin M, e.jet.first (siteQuotientCoefficient M j k) ∧
    e.jet.second (balancedQuotientCoefficient M k) =
      ∑ j : Fin M, e.jet.second (siteQuotientCoefficient M j k) := by
  have h := regularQuotient_jet_zero_eta model e (balancedSites M) hη₀ hη₁ hη₂ M k
  have h0 := h.1
  have h1 := h.2.1
  have h2 := h.2.2
  rw [← Fin.sum_univ_eq_sum_range] at h0 h1 h2
  constructor
  · exact h0.trans (Finset.sum_congr rfl (fun j _ => by simp [balancedSites, j.isLt]))
  constructor
  · exact h1.trans (Finset.sum_congr rfl (fun j _ => by simp [balancedSites, j.isLt]))
  · exact h2.trans (Finset.sum_congr rfl (fun j _ => by simp [balancedSites, j.isLt]))

theorem balancedQuotient_jet_realization (f : Fin M → R)
    (hη₀ : e.jet.value (MvPolynomial.X .eta) = 0)
    (hη₁ : e.jet.first (MvPolynomial.X .eta) = 0)
    (hη₂ : e.jet.second (MvPolynomial.X .eta) = 0)
    (hβ₀ : ∀ j, e.jet.value (balancedBeta M j) = 0)
    (hβ₁ : ∀ j, e.jet.first (balancedBeta M j) = f j)
    (hβ₂ : ∀ j, e.jet.second (balancedBeta M j) = 0) :
    CoefficientJetRealization model e (balancedQuotientCoefficient M) (-1)
      ((-2 * (M : ℝ)) • (↑model.D⁻¹ : A))
      ((-2 : ℝ) • ∑ j, firstResolventJet model (f j))
      ((-2 : ℝ) • ∑ j, secondResolventJet model (f j)) := by
  have hsite (j : Fin M) := CoefficientJetRealization.smul (-2)
    (resolventCoefficient_jet_realization model e j (f j) (hβ₀ j) (hβ₁ j) (hβ₂ j))
  have hs := CoefficientJetRealization.sum (model := model) (e := e)
    Finset.univ (siteQuotientCoefficient M) (-1)
      (fun _ : Fin M => (-2 : ℝ) • (↑model.D⁻¹ : A))
      (fun j => (-2 : ℝ) • firstResolventJet model (f j))
      (fun j => (-2 : ℝ) • secondResolventJet model (f j)) (fun j _ => hsite j)
  simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul,
    ← Finset.smul_sum, ← Nat.cast_smul_eq_nsmul ℝ, smul_smul] at hs
  have hscale : (M : ℝ) * (-2) = -2 * (M : ℝ) := by ring
  rw [hscale] at hs
  constructor
  · exact hs.bound_value
  · exact hs.bound_first
  · exact hs.bound_second
  · intro k
    exact (balancedQuotient_jet_sum model e hη₀ hη₁ hη₂ k).1.trans
      (by simpa only [map_sum] using hs.value k)
  · intro k
    exact (balancedQuotient_jet_sum model e hη₀ hη₁ hη₂ k).2.1.trans
      (by simpa only [map_sum] using hs.first k)
  · intro k
    exact (balancedQuotient_jet_sum model e hη₀ hη₁ hη₂ k).2.2.trans
      (by simpa only [map_sum] using hs.second k)

end
end DLWLean.BalancedPDO
