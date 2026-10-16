import AdlerFactorCoordinates
import Mathlib.Tactic.Abel

namespace DLWLean
noncomputable section
open scoped BigOperators

theorem factorDifferenceMean_ambientToFactorTangent (par : FieldParameters)
    (v : AmbientPeriodicPair par) :
    factorDifferenceMean par (ambientToFactorTangent par v) =
      (par.h / 4 : ℝ) • coefficientLatticeMean par v.2 := by
  have hp : (fun j => (ambientToFactorTangent par v).1 j -
      (ambientToFactorTangent par v).2 j) = fun j => (par.h / 4 : ℝ) • v.2 j := by
    funext j
    apply Subtype.ext
    funext x
    change (1 / 2 * (v.1 j : ℝ → ℝ) x + par.h / 8 * (v.2 j : ℝ → ℝ) x) -
      (1 / 2 * (v.1 j : ℝ → ℝ) x - par.h / 8 * (v.2 j : ℝ → ℝ) x) =
      par.h / 4 * (v.2 j : ℝ → ℝ) x
    ring
  rw [factorDifferenceMean, hp, coefficientLatticeMean_smul]

theorem factorProjection_ambientToFactorTangent_eq_projected (par : FieldParameters)
    (v : AmbientPeriodicPair par) :
    factorProjection par (ambientToFactorTangent par v) =
      ((fun j => (1 / 2 : ℝ) • v.1 j + (par.h / 8 : ℝ) •
          (v.2 j - coefficientLatticeMean par v.2)),
        (fun j => (1 / 2 : ℝ) • v.1 j - (par.h / 8 : ℝ) •
          (v.2 j - coefficientLatticeMean par v.2))) := by
  unfold factorProjection
  rw [factorDifferenceMean_ambientToFactorTangent]
  apply Prod.ext <;> funext j <;> apply Subtype.ext <;> funext x
  · change (1 / 2 * (v.1 j : ℝ → ℝ) x + par.h / 8 * (v.2 j : ℝ → ℝ) x) -
      (1 / 2) * ((par.h / 4) * (coefficientLatticeMean par v.2 : ℝ → ℝ) x) =
      1 / 2 * (v.1 j : ℝ → ℝ) x + par.h / 8 *
        ((v.2 j : ℝ → ℝ) x - (coefficientLatticeMean par v.2 : ℝ → ℝ) x)
    ring
  · change (1 / 2 * (v.1 j : ℝ → ℝ) x - par.h / 8 * (v.2 j : ℝ → ℝ) x) +
      (1 / 2) * ((par.h / 4) * (coefficientLatticeMean par v.2 : ℝ → ℝ) x) =
      1 / 2 * (v.1 j : ℝ → ℝ) x - par.h / 8 *
        ((v.2 j : ℝ → ℝ) x - (coefficientLatticeMean par v.2 : ℝ → ℝ) x)
    ring

theorem factorDifferenceMean_sum (par : FieldParameters) (v : FactorPeriodicPair par) :
    (∑ j : Fin par.M, (v.1 j - v.2 j)) =
      (par.M : ℝ) • factorDifferenceMean par v := by
  unfold factorDifferenceMean coefficientLatticeMean
  rw [smul_smul, mul_inv_cancel₀]
  · rw [one_smul]
  · exact_mod_cast par.M_ne_zero

theorem factorPairing_projection_left (par : FieldParameters) (f v : FactorPeriodicPair par) :
    factorPairing par (factorProjection par f) v = factorPairing par f v -
      (1 / 2 : ℝ) * periodicCoefficientIntegral par.Lx
        (factorDifferenceMean par f * (∑ j : Fin par.M, (v.1 j - v.2 j))) := by
  have hp (j : Fin par.M) :
      (f.1 j - (1 / 2 : ℝ) • factorDifferenceMean par f) * v.1 j +
        (f.2 j + (1 / 2 : ℝ) • factorDifferenceMean par f) * v.2 j =
      f.1 j * v.1 j + f.2 j * v.2 j -
        (1 / 2 : ℝ) • (factorDifferenceMean par f * (v.1 j - v.2 j)) := by
    simp only [sub_mul, add_mul, smul_mul_assoc, mul_sub, smul_sub]
    abel
  unfold factorPairing factorProjection
  simp only [hp, Finset.sum_sub_distrib, ← Finset.smul_sum, ← Finset.mul_sum,
    map_sub, map_smul, smul_eq_mul]

theorem factorPairing_symmetric (par : FieldParameters) (f v : FactorPeriodicPair par) :
    factorPairing par f v = factorPairing par v f := by
  simp only [factorPairing, mul_comm (f.1 _) (v.1 _), mul_comm (f.2 _) (v.2 _)]

theorem factorPairing_projection_self_adjoint (par : FieldParameters)
    (f v : FactorPeriodicPair par) :
    factorPairing par (factorProjection par f) v =
      factorPairing par f (factorProjection par v) := by
  rw [factorPairing_projection_left, factorPairing_symmetric par f (factorProjection par v),
    factorPairing_projection_left, factorPairing_symmetric par v f,
    factorDifferenceMean_sum, factorDifferenceMean_sum]
  congr 3
  simp only [mul_smul_comm, mul_comm (factorDifferenceMean par f) (factorDifferenceMean par v)]

theorem factorPairing_ext (par : FieldParameters) (f g : FactorPeriodicPair par)
    (hfg : ∀ v, factorPairing par f v = factorPairing par g v) : f = g := by
  classical
  apply Prod.ext <;> funext j
  · have h := hfg (Pi.single j (f.1 j - g.1 j), 0)
    simp only [factorPairing, Pi.single_apply, Pi.zero_apply, mul_zero, add_zero,
      mul_ite, Finset.sum_ite_eq', Finset.mem_univ, ↓reduceIte] at h
    have hz : periodicCoefficientIntegral par.Lx ((f.1 j - g.1 j) * (f.1 j - g.1 j)) = 0 := by
      rw [sub_mul, map_sub, h, sub_self]
    exact sub_eq_zero.mp (periodicCoefficient_integral_square_zero par.Lx par.Lx_pos _ hz)
  · have h := hfg (0, Pi.single j (f.2 j - g.2 j))
    simp only [factorPairing, Pi.single_apply, Pi.zero_apply, mul_zero, zero_add,
      mul_ite, Finset.sum_ite_eq', Finset.mem_univ, ↓reduceIte] at h
    have hz : periodicCoefficientIntegral par.Lx ((f.2 j - g.2 j) * (f.2 j - g.2 j)) = 0 := by
      rw [sub_mul, map_sub, h, sub_self]
    exact sub_eq_zero.mp (periodicCoefficient_integral_square_zero par.Lx par.Lx_pos _ hz)

theorem factorProjection_sum_add (par : FieldParameters) (f : FactorPeriodicPair par) :
    (∑ j : Fin par.M, ((factorProjection par f).1 j + (factorProjection par f).2 j)) =
      ∑ j : Fin par.M, (f.1 j + f.2 j) := by
  apply Finset.sum_congr rfl
  intro j _
  change (f.1 j - (1 / 2 : ℝ) • factorDifferenceMean par f) +
    (f.2 j + (1 / 2 : ℝ) • factorDifferenceMean par f) = _
  abel

theorem ambientToFactorCotangent_sum_add (par : FieldParameters) (f : AmbientPeriodicPair par) :
    (∑ j : Fin par.M, ((ambientToFactorCotangent par f).1 j + (ambientToFactorCotangent par f).2 j)) =
      (2 * par.h) • (∑ j : Fin par.M, f.1 j) := by
  have hp (j : Fin par.M) :
      (ambientToFactorCotangent par f).1 j + (ambientToFactorCotangent par f).2 j =
        (2 * par.h) • f.1 j := by
    apply Subtype.ext
    funext x
    change (par.h * (f.1 j : ℝ → ℝ) x + 4 * (f.2 j : ℝ → ℝ) x) +
      (par.h * (f.1 j : ℝ → ℝ) x - 4 * (f.2 j : ℝ → ℝ) x) =
        (2 * par.h) * (f.1 j : ℝ → ℝ) x
    ring
  simp_rw [hp]
  rw [Finset.smul_sum]

theorem standardFactorBracket_projection_Ward (par : FieldParameters)
    (f g : FactorPeriodicPair par)
    (hf : (∑ j : Fin par.M, (f.1 j + f.2 j)) = 0)
    (hg : (∑ j : Fin par.M, (g.1 j + g.2 j)) = 0) :
    standardFactorBracket par (factorProjection par f) (factorProjection par g) =
      standardFactorBracket par f g := by
  let Dx := (periodicSpatialEvolution par.Lx).toLinearMap
  have hn : (∑ j : Fin par.M, (-f.1 j * Dx (g.1 j))) =
      -(∑ j : Fin par.M, f.1 j * Dx (g.1 j)) := by
    rw [← Finset.sum_neg_distrib]
    apply Finset.sum_congr rfl
    intro j _
    ring
  have hp (j : Fin par.M) :
      -((f.1 j - (1 / 2 : ℝ) • factorDifferenceMean par f) *
          (Dx (g.1 j) - (1 / 2 : ℝ) • Dx (factorDifferenceMean par g))) +
        ((f.2 j + (1 / 2 : ℝ) • factorDifferenceMean par f) *
          (Dx (g.2 j) + (1 / 2 : ℝ) • Dx (factorDifferenceMean par g))) =
      (-f.1 j * Dx (g.1 j) + f.2 j * Dx (g.2 j)) +
        (1 / 2 : ℝ) • (factorDifferenceMean par f * Dx (g.1 j + g.2 j)) +
        (1 / 2 : ℝ) • ((f.1 j + f.2 j) * Dx (factorDifferenceMean par g)) := by
    rw [map_add]
    simp only [Algebra.smul_def]
    ring
  unfold standardFactorBracket factorProjection
  simp only [map_sub, map_add, map_smul]
  rw [← map_neg, ← map_add, ← Finset.sum_neg_distrib, ← Finset.sum_add_distrib]
  change periodicCoefficientIntegral par.Lx (∑ j : Fin par.M,
    (-((f.1 j - (1 / 2 : ℝ) • factorDifferenceMean par f) *
      (Dx (g.1 j) - (1 / 2 : ℝ) • Dx (factorDifferenceMean par g))) +
      ((f.2 j + (1 / 2 : ℝ) • factorDifferenceMean par f) *
        (Dx (g.2 j) + (1 / 2 : ℝ) • Dx (factorDifferenceMean par g))))) = _
  simp_rw [hp]
  rw [Finset.sum_add_distrib, Finset.sum_add_distrib,
    ← Finset.smul_sum, ← Finset.smul_sum, ← Finset.mul_sum, ← Finset.sum_mul,
    ← map_sum, hf, hg, map_zero, mul_zero, zero_mul]
  simp only [smul_zero, add_zero]
  rw [Finset.sum_add_distrib, hn, map_add, map_neg]

#print axioms factorProjection_ambientToFactorTangent_eq_projected
#print axioms factorPairing_projection_self_adjoint
#print axioms factorPairing_ext
#print axioms standardFactorBracket_projection_Ward
end
end DLWLean
