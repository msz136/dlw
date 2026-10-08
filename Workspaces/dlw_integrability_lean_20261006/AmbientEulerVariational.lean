import PeriodicVariationalCalculus
import VariationalReduction
import PolynomialIntegralVariation
import Mathlib.Algebra.MvPolynomial.PDeriv

namespace DLWLean
noncomputable section
open scoped BigOperators

abbrev AmbientPeriodicPair (par : FieldParameters) :=
  (Fin par.M → PeriodicCoefficient par.Lx) × (Fin par.M → PeriodicCoefficient par.Lx)
abbrev AmbientJetIndex (par : FieldParameters) := Bool × Fin par.M × ℕ

def ambientSpatialJet (par : FieldParameters) :
    ℕ → PeriodicCoefficient par.Lx →ₗ[ℝ] PeriodicCoefficient par.Lx
  | 0 => LinearMap.id
  | n + 1 => (periodicSpatialEvolution par.Lx).toLinearMap.comp (ambientSpatialJet par n)

theorem ambientSpatialJet_eq_iterate (par : FieldParameters) (n : ℕ)
    (f : PeriodicCoefficient par.Lx) :
    ambientSpatialJet par n f = periodicSpatialIterate n f := by
  induction n with
  | zero => rfl
  | succ n ih =>
    change (periodicSpatialEvolution par.Lx).toLinearMap (ambientSpatialJet par n f) = _
    rw [ih]
    exact (Function.iterate_succ_apply' _ n f).symm

def ambientComponent (par : FieldParameters) (b : Bool) (j : Fin par.M) :
    AmbientPeriodicPair par →ₗ[ℝ] PeriodicCoefficient par.Lx where
  toFun z := if b then z.1 j else z.2 j
  map_add' z v := by cases b <;> rfl
  map_smul' r z := by cases b <;> rfl

def ambientJet (par : FieldParameters) (i : AmbientJetIndex par) :
    AmbientPeriodicPair par →ₗ[ℝ] PeriodicCoefficient par.Lx :=
  (ambientSpatialJet par i.2.2).comp (ambientComponent par i.1 i.2.1)

def ambientPolynomialValue (par : FieldParameters)
    (p : MvPolynomial (AmbientJetIndex par) (PeriodicCoefficient par.Lx))
    (z : AmbientPeriodicPair par) : PeriodicCoefficient par.Lx :=
  MvPolynomial.eval (fun i => ambientJet par i z) p

def ambientPolynomialIntegral (par : FieldParameters)
    (p : MvPolynomial (AmbientJetIndex par) (PeriodicCoefficient par.Lx))
    (z : AmbientPeriodicPair par) : ℝ :=
  periodicCoefficientIntegral par.Lx (ambientPolynomialValue par p z)

def ambientPolynomialVariation (par : FieldParameters) (v : AmbientPeriodicPair par) :
    Derivation (PeriodicCoefficient par.Lx)
      (MvPolynomial (AmbientJetIndex par) (PeriodicCoefficient par.Lx))
      (MvPolynomial (AmbientJetIndex par) (PeriodicCoefficient par.Lx)) :=
  MvPolynomial.mkDerivation (PeriodicCoefficient par.Lx)
    (fun i => MvPolynomial.C (ambientJet par i v))

theorem ambient_variation_eq_sum_pderiv {R σ : Type*} [CommRing R]
    (p : MvPolynomial σ R) (f : σ → R) :
    MvPolynomial.mkDerivation R (fun i => MvPolynomial.C (f i)) p =
      ∑ i ∈ p.vars, MvPolynomial.C (f i) * MvPolynomial.pderiv i p := by
  classical
  let E : Derivation R (MvPolynomial σ R) (MvPolynomial σ R) :=
    ∑ i ∈ p.vars, (MvPolynomial.C (f i) : MvPolynomial σ R) •
      (MvPolynomial.pderiv i : Derivation R (MvPolynomial σ R) (MvPolynomial σ R))
  have hE : MvPolynomial.mkDerivation R (fun i => MvPolynomial.C (f i)) p = E p := by
    apply MvPolynomial.derivation_eq_of_forall_mem_vars
    intro i hi
    simp [E, MvPolynomial.pderiv_X, Pi.single_apply, hi, Derivation.smul_apply]
  rw [hE]
  simp [E, Derivation.smul_apply, smul_eq_mul]

def ambientPolynomialLine (par : FieldParameters)
    (p : MvPolynomial (AmbientJetIndex par) (PeriodicCoefficient par.Lx))
    (z v : AmbientPeriodicPair par) : Polynomial (PeriodicCoefficient par.Lx) :=
  MvPolynomial.eval₂Hom Polynomial.C
    (fun i => Polynomial.C (ambientJet par i z) +
      Polynomial.C (ambientJet par i v) * Polynomial.X) p

theorem ambientPolynomialLine_eval (par : FieldParameters)
    (p : MvPolynomial (AmbientJetIndex par) (PeriodicCoefficient par.Lx))
    (z v : AmbientPeriodicPair par) (t : ℝ) :
    (ambientPolynomialLine par p z v).eval (algebraMap ℝ (PeriodicCoefficient par.Lx) t) =
      ambientPolynomialValue par p (z + t • v) := by
  have h := MvPolynomial.map_eval₂Hom Polynomial.C
    (fun i => Polynomial.C (ambientJet par i z) +
      Polynomial.C (ambientJet par i v) * Polynomial.X)
    (Polynomial.evalRingHom (algebraMap ℝ (PeriodicCoefficient par.Lx) t)) p
  have hcoef : (Polynomial.evalRingHom
      (algebraMap ℝ (PeriodicCoefficient par.Lx) t)).comp Polynomial.C = RingHom.id _ := by
    ext r
    simp
  rw [hcoef] at h
  simp only [Polynomial.coe_evalRingHom, Polynomial.eval_add, Polynomial.eval_C,
    Polynomial.eval_mul, Polynomial.eval_X] at h
  change (ambientPolynomialLine par p z v).eval _ =
    MvPolynomial.eval₂Hom (RingHom.id _) (fun i => ambientJet par i (z + t • v)) p
  have hvars : (fun i : AmbientJetIndex par => ambientJet par i (z + t • v)) =
      (fun i => ambientJet par i z +
        ambientJet par i v * algebraMap ℝ (PeriodicCoefficient par.Lx) t) := by
    funext i
    rw [map_add, map_smul, Algebra.smul_def, mul_comm]
  rw [hvars]
  exact h

theorem ambientPolynomialLine_coeff_zero (par : FieldParameters)
    (p : MvPolynomial (AmbientJetIndex par) (PeriodicCoefficient par.Lx))
    (z v : AmbientPeriodicPair par) :
    (ambientPolynomialLine par p z v).coeff 0 = ambientPolynomialValue par p z := by
  rw [Polynomial.coeff_zero_eq_eval_zero]
  simpa using ambientPolynomialLine_eval par p z v 0

theorem ambientPolynomialLine_coeff_one (par : FieldParameters)
    (p : MvPolynomial (AmbientJetIndex par) (PeriodicCoefficient par.Lx))
    (z v : AmbientPeriodicPair par) :
    (ambientPolynomialLine par p z v).coeff 1 =
      ambientPolynomialValue par (ambientPolynomialVariation par v p) z := by
  induction p using MvPolynomial.induction_on with
  | C r =>
    simp [ambientPolynomialLine, ambientPolynomialVariation, ambientPolynomialValue]
  | add p q hp hq =>
    simp only [ambientPolynomialLine, map_add, Polynomial.coeff_add] at *
    rw [hp, hq]
    simp only [ambientPolynomialValue, MvPolynomial.eval_add]
  | mul_X p i hp =>
    have hline : ambientPolynomialLine par (p * MvPolynomial.X i) z v =
        (ambientPolynomialLine par p z v) *
          (Polynomial.C (ambientJet par i z) + Polynomial.C (ambientJet par i v) * Polynomial.X) := by
      unfold ambientPolynomialLine
      rw [map_mul, MvPolynomial.eval₂Hom_X']
    rw [hline, mul_add, Polynomial.coeff_add, Polynomial.coeff_mul_C,
      ← mul_assoc, Polynomial.coeff_mul_X, Polynomial.coeff_mul_C,
      hp, ambientPolynomialLine_coeff_zero]
    simp only [ambientPolynomialValue, Derivation.leibniz, Algebra.smul_def,
      Algebra.algebraMap_self, RingHom.id_apply, MvPolynomial.eval_add,
      MvPolynomial.eval_mul, MvPolynomial.eval_X,
      ambientPolynomialVariation, MvPolynomial.mkDerivation_X, MvPolynomial.eval_C]
    ring

theorem ambientPolynomialIntegral_hasDerivAt (par : FieldParameters)
    (p : MvPolynomial (AmbientJetIndex par) (PeriodicCoefficient par.Lx))
    (z v : AmbientPeriodicPair par) :
    HasDerivAt (fun t : ℝ => ambientPolynomialIntegral par p (z + t • v))
      (ambientPolynomialIntegral par (ambientPolynomialVariation par v p) z) 0 := by
  have h := linear_polynomial_evaluation_hasDerivAt_zero
    (periodicCoefficientIntegral par.Lx) (ambientPolynomialLine par p z v)
  rw [ambientPolynomialLine_coeff_one] at h
  have hf : (fun t : ℝ => ambientPolynomialIntegral par p (z + t • v)) =
      (fun t : ℝ => periodicCoefficientIntegral par.Lx
        ((ambientPolynomialLine par p z v).eval (algebraMap ℝ (PeriodicCoefficient par.Lx) t))) := by
    funext t
    rw [ambientPolynomialLine_eval]
    rfl
  rw [hf]
  exact h

def ambientPairing (par : FieldParameters) (f v : AmbientPeriodicPair par) : ℝ :=
  ambientVariationPairing par f.1 f.2 v.1 v.2

theorem ambientPairing_add_left (par : FieldParameters)
    (f g v : AmbientPeriodicPair par) :
    ambientPairing par (f + g) v = ambientPairing par f v + ambientPairing par g v := by
  simp only [ambientPairing, ambientVariationPairing, Prod.fst_add, Prod.snd_add,
    Pi.add_apply, add_mul]
  simp only [Finset.sum_add_distrib, map_add]
  ring

theorem ambientPairing_sum_left (par : FieldParameters) {σ : Type*}
    (s : Finset σ) (f : σ → AmbientPeriodicPair par) (v : AmbientPeriodicPair par) :
    ambientPairing par (∑ i ∈ s, f i) v = ∑ i ∈ s, ambientPairing par (f i) v := by
  classical
  induction s using Finset.induction_on with
  | empty => simp [ambientPairing, ambientVariationPairing]
  | @insert i s hi ih => simp only [Finset.sum_insert hi, ambientPairing_add_left, ih]

def ambientSingleGradient (par : FieldParameters) (i : AmbientJetIndex par)
    (a : PeriodicCoefficient par.Lx) : AmbientPeriodicPair par :=
  if i.1 then (Pi.single i.2.1 (par.h⁻¹ • a), 0)
  else (0, Pi.single i.2.1 (par.h⁻¹ • a))

theorem ambientSingleGradient_pairing (par : FieldParameters) (i : AmbientJetIndex par)
    (a : PeriodicCoefficient par.Lx) (v : AmbientPeriodicPair par) :
    ambientPairing par (ambientSingleGradient par i a) v =
      periodicCoefficientIntegral par.Lx (a * ambientComponent par i.1 i.2.1 v) := by
  classical
  obtain ⟨b, j, n⟩ := i
  cases b <;>
    simp only [ambientSingleGradient, Bool.false_eq_true, ↓reduceIte,
      ambientPairing, ambientVariationPairing, Pi.zero_apply, zero_mul, add_zero, zero_add,
      ambientComponent, LinearMap.coe_mk, AddHom.coe_mk]
  all_goals
    simp only [Pi.single_apply, ite_mul, zero_mul, Finset.sum_ite_eq',
      Finset.mem_univ, ↓reduceIte, smul_mul_assoc, map_smul, smul_eq_mul]
    rw [← mul_assoc, mul_inv_cancel₀ (ne_of_gt par.h_pos), one_mul]

def ambientEulerTerm (par : FieldParameters)
    (p : MvPolynomial (AmbientJetIndex par) (PeriodicCoefficient par.Lx))
    (z : AmbientPeriodicPair par) (i : AmbientJetIndex par) : PeriodicCoefficient par.Lx :=
  (-1 : ℝ) ^ i.2.2 • ambientSpatialJet par i.2.2
    (ambientPolynomialValue par (MvPolynomial.pderiv i p) z)

def ambientEulerGradient (par : FieldParameters)
    (p : MvPolynomial (AmbientJetIndex par) (PeriodicCoefficient par.Lx))
    (z : AmbientPeriodicPair par) : AmbientPeriodicPair par :=
  ∑ i ∈ p.vars, ambientSingleGradient par i (ambientEulerTerm par p z i)

theorem ambientEulerGradient_pairing (par : FieldParameters)
    (p : MvPolynomial (AmbientJetIndex par) (PeriodicCoefficient par.Lx))
    (z v : AmbientPeriodicPair par) :
    ambientPairing par (ambientEulerGradient par p z) v =
      ambientPolynomialIntegral par (ambientPolynomialVariation par v p) z := by
  classical
  rw [ambientEulerGradient, ambientPairing_sum_left]
  simp_rw [ambientSingleGradient_pairing]
  unfold ambientPolynomialIntegral ambientPolynomialVariation
  rw [ambient_variation_eq_sum_pderiv]
  simp only [ambientPolynomialValue, map_sum,
    MvPolynomial.eval_mul, MvPolynomial.eval_C, map_sum]
  apply Finset.sum_congr rfl
  intro i hi
  rw [mul_comm (ambientJet par i v)]
  change periodicCoefficientIntegral par.Lx
      (((-1 : ℝ) ^ i.2.2 • ambientSpatialJet par i.2.2
        (MvPolynomial.eval (fun i => ambientJet par i z) (MvPolynomial.pderiv i p))) *
          ambientComponent par i.1 i.2.1 v) =
    periodicCoefficientIntegral par.Lx
      (MvPolynomial.eval (fun i => ambientJet par i z) (MvPolynomial.pderiv i p) *
        ambientSpatialJet par i.2.2 (ambientComponent par i.1 i.2.1 v))
  rw [ambientSpatialJet_eq_iterate, ambientSpatialJet_eq_iterate,
    smul_mul_assoc, map_smul, smul_eq_mul,
    periodicCoefficientIntegral_iterated_parts]

/-- Actual Euler first variation, valid for every pair of smooth periodic
coefficient fields and every smooth periodic direction. -/
theorem ambientEulerGradient_hasDerivAt (par : FieldParameters)
    (p : MvPolynomial (AmbientJetIndex par) (PeriodicCoefficient par.Lx))
    (z v : AmbientPeriodicPair par) :
    HasDerivAt (fun t : ℝ => ambientPolynomialIntegral par p (z + t • v))
      (ambientPairing par (ambientEulerGradient par p z) v) 0 := by
  rw [ambientEulerGradient_pairing]
  exact ambientPolynomialIntegral_hasDerivAt par p z v

#print axioms ambientEulerGradient_pairing
#print axioms ambientEulerGradient_hasDerivAt
end
end DLWLean
