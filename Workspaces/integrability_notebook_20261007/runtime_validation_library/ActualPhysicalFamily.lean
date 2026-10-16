import ConstructedChargeMomentum
import GradientNondegeneracy
import ActualHamiltonianDerivative
import Independence

/-!
Assembly on the actual periodic field space. Every differential is a
linear covector representing the ordinary affine-line derivative, and
the bracket is the literal reduced integral pairing. The two inputs of
the assembly lemmas are the energy identity and spectral commutation;
they are to be supplied by their separate operator derivations.
-/
namespace DLWLean
noncomputable section
open scoped BigOperators

def gradientCovector (par : FieldParameters) (g : ClosedPeriodicPair par) :
    ClosedPeriodicPair par →ₗ[ℝ] ℝ where
  toFun v := coefficientGradientPairing par g v
  map_add' v w := by
    simp only [coefficientGradientPairing, Prod.fst_add, Prod.snd_add,
      coefficientPairing_add_right]
    ring
  map_smul' r v := by
    change coefficientPairing par g.1 (r • v.1) + coefficientPairing par g.2 (r • v.2) =
      r * (coefficientPairing par g.1 v.1 + coefficientPairing par g.2 v.2)
    rw [coefficientPairing_smul_right, coefficientPairing_smul_right]
    ring

theorem gradientCovector_add (par : FieldParameters) (f g : ClosedPeriodicPair par) :
    gradientCovector par (f + g) = gradientCovector par f + gradientCovector par g := by
  apply LinearMap.ext
  intro v
  change coefficientPairing par (f.1 + g.1) v.1 + coefficientPairing par (f.2 + g.2) v.2 =
    (coefficientPairing par f.1 v.1 + coefficientPairing par f.2 v.2) +
      (coefficientPairing par g.1 v.1 + coefficientPairing par g.2 v.2)
  rw [coefficientPairing_add_left, coefficientPairing_add_left]
  ring

theorem gradientCovector_smul (par : FieldParameters) (r : ℝ) (g : ClosedPeriodicPair par) :
    gradientCovector par (r • g) = r • gradientCovector par g := by
  apply LinearMap.ext
  intro v
  change coefficientPairing par (r • g.1) v.1 + coefficientPairing par (r • g.2) v.2 =
    r * (coefficientPairing par g.1 v.1 + coefficientPairing par g.2 v.2)
  rw [coefficientPairing_smul_left, coefficientPairing_smul_left]
  ring

def actualPhysicalK (par : FieldParameters) (z : ClosedPeriodicPair par) : ℝ :=
  physicalK par (latticeResolvent par) (closedPairCoordinates par z)

def actualPhysicalKGradient (par : FieldParameters) (z : ClosedPeriodicPair par) :
    ClosedPeriodicPair par := physicalKGradient (closedPairCoordinates par z)

theorem actualPhysicalK_hasDerivAt (par : FieldParameters) (z v : ClosedPeriodicPair par) :
    HasDerivAt (fun t : ℝ => actualPhysicalK par (z + t • v))
      (gradientCovector par (actualPhysicalKGradient par z) v) 0 := by
  exact physicalK_hasDerivAt_coordinateLine (closedPairCoordinates par z) v

def actualPhysicalFamily (par : FieldParameters) : ℕ → ClosedPeriodicPair par → ℝ
  | 0 => actualPhysicalK par
  | 1 => coefficientMomentum par
  | n + 2 => GlobalPDO.constructedCharge par (2 * n + 3)

def actualPhysicalFamilyGradient (par : FieldParameters) :
    ℕ → ClosedPeriodicPair par → ClosedPeriodicPair par
  | 0 => actualPhysicalKGradient par
  | 1 => momentumGradient
  | n + 2 => GlobalPDO.constructedChargeGradient par (2 * n + 3)

theorem actualPhysicalFamily_hasDerivAt (par : FieldParameters) (n : ℕ)
    (z v : ClosedPeriodicPair par) :
    HasDerivAt (fun t : ℝ => actualPhysicalFamily par n (z + t • v))
      (gradientCovector par (actualPhysicalFamilyGradient par n z) v) 0 := by
  rcases n with _ | _ | n
  · exact actualPhysicalK_hasDerivAt par z v
  · exact coefficientMomentum_hasDerivAt par z v
  · exact GlobalPDO.constructedChargeGradient_hasDerivAt par (2 * n + 3) z v

theorem constructedCharge_gradientCovector (par : FieldParameters) (n : ℕ)
    (z : ClosedPeriodicPair par) :
    gradientCovector par (GlobalPDO.constructedChargeGradient par n z) =
      fieldPolynomialDifferential par (GlobalPDO.periodicDensityPolynomial par n) z := by
  apply LinearMap.ext
  intro v
  exact fieldEulerGradient_pairing par (GlobalPDO.periodicDensityPolynomial par n) z v

theorem actualPhysicalKGradient_eq_of_energy (par : FieldParameters) (κ : ℝ)
    (henergy : ∀ z : ClosedPeriodicPair par,
      actualPhysicalK par z = (-8 * par.G) * GlobalPDO.constructedCharge par 1 z +
        (par.gamma / par.c) * coefficientMomentum par z + κ)
    (z : ClosedPeriodicPair par) :
    actualPhysicalKGradient par z =
      (-8 * par.G) • GlobalPDO.constructedChargeGradient par 1 z +
        (par.gamma / par.c) • momentumGradient z :=
  gradient_affine_relation par (actualPhysicalK par) (GlobalPDO.constructedCharge par 1)
    (coefficientMomentum par) z (actualPhysicalKGradient par z)
    (GlobalPDO.constructedChargeGradient par 1 z) (momentumGradient z)
    (-8 * par.G) (par.gamma / par.c) κ henergy
    (actualPhysicalK_hasDerivAt par z)
    (GlobalPDO.constructedChargeGradient_hasDerivAt par 1 z)
    (coefficientMomentum_hasDerivAt par z)

theorem reducedBracketValue_self_zero (par : FieldParameters) (g : ClosedPeriodicPair par) :
    reducedBracketValue par g g = 0 := by
  have h := reducedBracketValue_skew par g g
  linarith

/-- Actual reduced-bracket assembly of the final family. No abstract
bracket on a substitute function space is used here. -/
theorem actualPhysicalFamily_commutes_of_energy_and_spectral (par : FieldParameters)
    (κ : ℝ)
    (henergy : ∀ z : ClosedPeriodicPair par,
      actualPhysicalK par z = (-8 * par.G) * GlobalPDO.constructedCharge par 1 z +
        (par.gamma / par.c) * coefficientMomentum par z + κ)
    (hspectral : ∀ (m n : ℕ) (z : ClosedPeriodicPair par), 0 < m → 0 < n →
      reducedBracketValue par (GlobalPDO.constructedChargeGradient par m z)
        (GlobalPDO.constructedChargeGradient par n z) = 0) :
    ∀ (m n : ℕ) (z : ClosedPeriodicPair par),
      reducedBracketValue par (actualPhysicalFamilyGradient par m z)
        (actualPhysicalFamilyGradient par n z) = 0 := by
  intro m n z
  have hKC (k : ℕ) (hk : 0 < k) :
      reducedBracketValue par (actualPhysicalKGradient par z)
        (GlobalPDO.constructedChargeGradient par k z) = 0 := by
    rw [actualPhysicalKGradient_eq_of_energy par κ henergy,
      reducedBracketValue_add_left, reducedBracketValue_smul_left,
      reducedBracketValue_smul_left, hspectral 1 k z (by omega) hk,
      reducedBracketValue_skew par (momentumGradient z),
      GlobalPDO.constructedCharge_bracket_momentum_zero]
    ring
  have hKP : reducedBracketValue par (actualPhysicalKGradient par z) (momentumGradient z) = 0 := by
    rw [actualPhysicalKGradient_eq_of_energy par κ henergy,
      reducedBracketValue_add_left, reducedBracketValue_smul_left,
      reducedBracketValue_smul_left, GlobalPDO.constructedCharge_bracket_momentum_zero,
      reducedBracketValue_self_zero]
    ring
  rcases m with _ | _ | m
  · rcases n with _ | _ | n
    · exact reducedBracketValue_self_zero par _
    · exact hKP
    · exact hKC _ (by omega)
  · rcases n with _ | _ | n
    · rw [reducedBracketValue_skew]
      simpa only [actualPhysicalFamilyGradient, hKP, neg_zero]
    · exact reducedBracketValue_self_zero par _
    · rw [reducedBracketValue_skew]
      exact neg_eq_zero.mpr (GlobalPDO.constructedCharge_bracket_momentum_zero par _ z)
  · rcases n with _ | _ | n
    · rw [reducedBracketValue_skew]
      exact neg_eq_zero.mpr (hKC _ (by omega))
    · exact GlobalPDO.constructedCharge_bracket_momentum_zero par _ z
    · exact hspectral _ _ z (by omega) (by omega)

/-- The actual energy identity, an odd-charge minor, and the actual
momentum extra direction give the final independent covectors. -/
theorem actualPhysicalFamily_independent_of_odd_minor (par : FieldParameters)
    (κ : ℝ)
    (henergy : ∀ z : ClosedPeriodicPair par,
      actualPhysicalK par z = (-8 * par.G) * GlobalPDO.constructedCharge par 1 z +
        (par.gamma / par.c) * coefficientMomentum par z + κ)
    {N : ℕ} (z : ClosedPeriodicPair par) (directions : Fin (N + 1) → ClosedPeriodicPair par)
    (extra : ClosedPeriodicPair par)
    (hminor : (covectorMinor
      (fun i : Fin (N + 1) => gradientCovector par
        (GlobalPDO.constructedChargeGradient par (2 * i.val + 1) z)) directions).det ≠ 0)
    (hannihilate : ∀ i, gradientCovector par (momentumGradient z) (directions i) = 0)
    (hextra : gradientCovector par (momentumGradient z) extra ≠ 0) :
    LinearIndependent ℝ (fun i : Fin (N + 2) =>
      gradientCovector par (actualPhysicalFamilyGradient par i.val z)) := by
  let dC := fun i : Fin (N + 1) => gradientCovector par
    (GlobalPDO.constructedChargeGradient par (2 * i.val + 1) z)
  let dP := gradientCovector par (momentumGradient z)
  have hcons : dC = Fin.cons (dC 0) (fun i : Fin N => dC i.succ) := by
    funext i
    refine Fin.cases ?_ (fun j => ?_) i <;> rfl
  change (covectorMinor dC directions).det ≠ 0 at hminor
  rw [hcons] at hminor
  have hind := physical_covectors_independent_from_odd_minor
    (dC 0) dP (fun i : Fin N => dC i.succ) directions extra
    par.G (par.gamma / par.c) par.G_ne_zero hminor hannihilate hextra
  convert hind using 1
  funext i
  refine Fin.cases ?_ (fun j => ?_) i
  · simp only [Fin.cons_zero, Fin.val_zero, actualPhysicalFamilyGradient,
      actualPhysicalKGradient_eq_of_energy par κ henergy,
      gradientCovector_add, gradientCovector_smul]
    rfl
  · refine Fin.cases ?_ (fun k => ?_) j
    · rfl
    · change gradientCovector par (GlobalPDO.constructedChargeGradient par
        (2 * k.val + 3) z) = gradientCovector par
          (GlobalPDO.constructedChargeGradient par (2 * (k.val + 1) + 1) z)
      congr 2

#print axioms actualPhysicalFamily_hasDerivAt
#print axioms actualPhysicalKGradient_eq_of_energy
#print axioms actualPhysicalFamily_commutes_of_energy_and_spectral
#print axioms actualPhysicalFamily_independent_of_odd_minor
end
end DLWLean
