import ActualSpectralInvolution

/-!
The actual DLW coefficient coordinates and the two first-order factor
coordinates are related by explicit linear changes of tangents and
cotangents. Their period-integral pairings and brackets are proved here.
The remaining external Adler theorem is on arbitrary first-order factor
cotangents, with the standard opposite-sign factor bracket. In particular
the DLW normalization 1/8 is a conclusion of these integral identities.
-/
namespace DLWLean
noncomputable section
open scoped BigOperators

abbrev FactorPeriodicPair (par : FieldParameters) := AmbientPeriodicPair par

/-- Factor variations of alpha = U/2 + h*w/8 and beta = U/2 - h*w/8. -/
def factorToAmbient (par : FieldParameters) (v : FactorPeriodicPair par) :
    AmbientPeriodicPair par :=
  (v.1 + v.2, (4 / par.h : ℝ) • (v.1 - v.2))

def ambientToFactorTangent (par : FieldParameters) (v : AmbientPeriodicPair par) :
    FactorPeriodicPair par :=
  ((1 / 2 : ℝ) • v.1 + (par.h / 8 : ℝ) • v.2,
    (1 / 2 : ℝ) • v.1 - (par.h / 8 : ℝ) • v.2)

def factorDifferenceMean (par : FieldParameters) (v : FactorPeriodicPair par) :
    PeriodicCoefficient par.Lx := coefficientLatticeMean par (fun j => v.1 j - v.2 j)

/-- Orthogonal projection preserving the sum and removing the common difference. -/
def factorProjection (par : FieldParameters) (v : FactorPeriodicPair par) :
    FactorPeriodicPair par :=
  (fun j => v.1 j - (1 / 2 : ℝ) • factorDifferenceMean par v,
    fun j => v.2 j + (1 / 2 : ℝ) • factorDifferenceMean par v)

theorem factorToAmbient_inverse (par : FieldParameters) (v : AmbientPeriodicPair par) :
    factorToAmbient par (ambientToFactorTangent par v) = v := by
  apply Prod.ext <;> funext j <;> apply Subtype.ext <;> funext x
  · change (1 / 2 * (v.1 j : ℝ → ℝ) x + par.h / 8 * (v.2 j : ℝ → ℝ) x) +
      (1 / 2 * (v.1 j : ℝ → ℝ) x - par.h / 8 * (v.2 j : ℝ → ℝ) x) = _
    ring
  · change (4 / par.h) * ((1 / 2 * (v.1 j : ℝ → ℝ) x + par.h / 8 * (v.2 j : ℝ → ℝ) x) -
      (1 / 2 * (v.1 j : ℝ → ℝ) x - par.h / 8 * (v.2 j : ℝ → ℝ) x)) = _
    field_simp [ne_of_gt par.h_pos]
    <;> ring

theorem ambientToFactorTangent_inverse (par : FieldParameters) (v : FactorPeriodicPair par) :
    ambientToFactorTangent par (factorToAmbient par v) = v := by
  apply Prod.ext <;> funext j <;> apply Subtype.ext <;> funext x
  · change (1 / 2) * ((v.1 j : ℝ → ℝ) x + (v.2 j : ℝ → ℝ) x) +
      (par.h / 8) * ((4 / par.h) * ((v.1 j : ℝ → ℝ) x - (v.2 j : ℝ → ℝ) x)) = _
    field_simp [ne_of_gt par.h_pos]
    <;> ring
  · change (1 / 2) * ((v.1 j : ℝ → ℝ) x + (v.2 j : ℝ → ℝ) x) -
      (par.h / 8) * ((4 / par.h) * ((v.1 j : ℝ → ℝ) x - (v.2 j : ℝ → ℝ) x)) = _
    field_simp [ne_of_gt par.h_pos]
    <;> ring

/-- The transpose change of covectors, using the actual h-weighted pairing. -/
def ambientToFactorCotangent (par : FieldParameters) (f : AmbientPeriodicPair par) :
    FactorPeriodicPair par :=
  (par.h • f.1 + (4 : ℝ) • f.2, par.h • f.1 - (4 : ℝ) • f.2)

def factorPairing (par : FieldParameters) (f v : FactorPeriodicPair par) : ℝ :=
  periodicCoefficientIntegral par.Lx (∑ j : Fin par.M,
    (f.1 j * v.1 j + f.2 j * v.2 j))

theorem factorPairing_actual_coordinate_change (par : FieldParameters)
    (f : AmbientPeriodicPair par) (v : FactorPeriodicPair par) :
    factorPairing par (ambientToFactorCotangent par f) v =
      ambientPairing par f (factorToAmbient par v) := by
  have hpoint (j : Fin par.M) :
      ((par.h • f.1 j + (4 : ℝ) • f.2 j) * v.1 j +
        (par.h • f.1 j - (4 : ℝ) • f.2 j) * v.2 j) =
      par.h • (f.1 j * (v.1 j + v.2 j) +
        f.2 j * ((4 / par.h : ℝ) • (v.1 j - v.2 j))) := by
    apply Subtype.ext
    funext x
    change (par.h * (f.1 j : ℝ → ℝ) x + 4 * (f.2 j : ℝ → ℝ) x) *
        (v.1 j : ℝ → ℝ) x +
        (par.h * (f.1 j : ℝ → ℝ) x - 4 * (f.2 j : ℝ → ℝ) x) *
        (v.2 j : ℝ → ℝ) x =
      par.h * ((f.1 j : ℝ → ℝ) x * ((v.1 j : ℝ → ℝ) x + (v.2 j : ℝ → ℝ) x) +
        (f.2 j : ℝ → ℝ) x * ((4 / par.h) * ((v.1 j : ℝ → ℝ) x - (v.2 j : ℝ → ℝ) x)))
    field_simp [ne_of_gt par.h_pos]
    <;> ring
  unfold factorPairing ambientToFactorCotangent ambientPairing ambientVariationPairing factorToAmbient
  simp only [Pi.add_apply, Pi.sub_apply, Pi.smul_apply]
  simp_rw [hpoint]
  rw [← Finset.smul_sum, map_smul, smul_eq_mul]

/-- Standard independent first-order factor bracket: opposite signs. -/
def standardFactorBracket (par : FieldParameters) (f g : FactorPeriodicPair par) : ℝ :=
  -periodicCoefficientIntegral par.Lx (∑ j : Fin par.M,
    f.1 j * (periodicSpatialEvolution par.Lx).toLinearMap (g.1 j)) +
    periodicCoefficientIntegral par.Lx (∑ j : Fin par.M,
      f.2 j * (periodicSpatialEvolution par.Lx).toLinearMap (g.2 j))

def independentFactorBracket (par : FieldParameters) (f g : FactorPeriodicPair par) : ℝ :=
  (1 / 8 : ℝ) * standardFactorBracket par f g

theorem standardFactorBracket_actual_coordinate_change (par : FieldParameters)
    (f g : AmbientPeriodicPair par) :
    standardFactorBracket par (ambientToFactorCotangent par f)
      (ambientToFactorCotangent par g) =
        8 * ambientConstantBracket par f.1 f.2 g.1 g.2 := by
  let Dx := (periodicSpatialEvolution par.Lx).toLinearMap
  have hpoint (j : Fin par.M) :
      -((par.h • f.1 j + (4 : ℝ) • f.2 j) *
          (par.h • Dx (g.1 j) + (4 : ℝ) • Dx (g.2 j))) +
        ((par.h • f.1 j - (4 : ℝ) • f.2 j) *
          (par.h • Dx (g.1 j) - (4 : ℝ) • Dx (g.2 j))) =
      (-8 * par.h) • (f.1 j * Dx (g.2 j) + f.2 j * Dx (g.1 j)) := by
    apply Subtype.ext
    funext x
    change -((par.h * (f.1 j : ℝ → ℝ) x + 4 * (f.2 j : ℝ → ℝ) x) *
          (par.h * (Dx (g.1 j) : ℝ → ℝ) x + 4 * (Dx (g.2 j) : ℝ → ℝ) x)) +
        ((par.h * (f.1 j : ℝ → ℝ) x - 4 * (f.2 j : ℝ → ℝ) x) *
          (par.h * (Dx (g.1 j) : ℝ → ℝ) x - 4 * (Dx (g.2 j) : ℝ → ℝ) x)) =
      (-8 * par.h) * ((f.1 j : ℝ → ℝ) x * (Dx (g.2 j) : ℝ → ℝ) x +
        (f.2 j : ℝ → ℝ) x * (Dx (g.1 j) : ℝ → ℝ) x)
    ring
  unfold standardFactorBracket ambientToFactorCotangent ambientConstantBracket
  simp only [Pi.add_apply, Pi.sub_apply, Pi.smul_apply, map_add, map_sub, map_smul]
  rw [← map_neg, ← map_add, ← Finset.sum_neg_distrib, ← Finset.sum_add_distrib]
  change periodicCoefficientIntegral par.Lx (∑ j : Fin par.M,
    (-((par.h • f.1 j + (4 : ℝ) • f.2 j) *
      (par.h • Dx (g.1 j) + (4 : ℝ) • Dx (g.2 j))) +
      ((par.h • f.1 j - (4 : ℝ) • f.2 j) *
        (par.h • Dx (g.1 j) - (4 : ℝ) • Dx (g.2 j))))) = _
  simp_rw [hpoint]
  rw [← Finset.smul_sum, map_smul, smul_eq_mul]
  ring

theorem independentFactorBracket_actual_coordinate_change (par : FieldParameters)
    (f g : AmbientPeriodicPair par) :
    independentFactorBracket par (ambientToFactorCotangent par f)
      (ambientToFactorCotangent par g) = ambientConstantBracket par f.1 f.2 g.1 g.2 := by
  rw [independentFactorBracket, standardFactorBracket_actual_coordinate_change]
  ring

#print axioms factorPairing_actual_coordinate_change
#print axioms independentFactorBracket_actual_coordinate_change
end
end DLWLean
