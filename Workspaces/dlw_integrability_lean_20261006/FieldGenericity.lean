import PhysicalBracket
import Genericity
import Mathlib.Topology.ContinuousMap.Compact
import Mathlib.Topology.Order.ProjIcc
import Mathlib.Topology.Algebra.MvPolynomial
import Mathlib.Algebra.Polynomial.Eval.Defs
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Analysis.Calculus.IteratedDeriv.Defs
import Mathlib.Algebra.MvPolynomial.Derivation
import Mathlib.Analysis.Calculus.Deriv.Comp
import Independence
import Mathlib.Analysis.Calculus.Deriv.Polynomial

/-!
Concrete smooth topology and differential-polynomial observables on the
actual mean-zero periodic fields. The topology is induced by every real
spatial derivative on the compact period interval, with the sup norm.
This module proves finite-block openness and density once a nonzero
physical minor has been constructed. It does not assume completeness or
assert a Baire instance for this space.
-/
namespace DLWLean
noncomputable section
open scoped BigOperators ContDiff

abbrev PeriodInterval (par : FieldParameters) := Set.Icc (0 : ℝ) par.Lx
abbrev CompactPeriodCoefficient (par : FieldParameters) := C(PeriodInterval par, ℝ)
abbrev FieldJetIndex (par : FieldParameters) := Bool × Fin par.M × ℕ

def periodicCompactRestriction (par : FieldParameters) :
    PeriodicCoefficient par.Lx →ₐ[ℝ] CompactPeriodCoefficient par where
  toFun f := ⟨fun x => (f : ℝ → ℝ) x,
    f.property.1.continuous.comp continuous_subtype_val⟩
  map_zero' := by ext x; rfl
  map_one' := by ext x; rfl
  map_add' f g := by ext x; rfl
  map_mul' f g := by ext x; rfl
  commutes' r := by ext x; rfl

def coefficientSpatialJet (par : FieldParameters) :
    ℕ → PeriodicCoefficient par.Lx →ₗ[ℝ] PeriodicCoefficient par.Lx
  | 0 => LinearMap.id
  | k + 1 => (periodicSpatialEvolution par.Lx).toLinearMap.comp
      (coefficientSpatialJet par k)

theorem coefficientSpatialJet_value (par : FieldParameters) (k : ℕ)
    (f : PeriodicCoefficient par.Lx) :
    (coefficientSpatialJet par k f : ℝ → ℝ) = iteratedDeriv k (f : ℝ → ℝ) := by
  induction k with
  | zero => rfl
  | succ k ih =>
    change deriv (coefficientSpatialJet par k f : ℝ → ℝ) = _
    rw [ih, iteratedDeriv_succ]

def closedPairComponent (par : FieldParameters) (component : Bool) (j : Fin par.M) :
    ClosedPeriodicPair par →ₗ[ℝ] PeriodicCoefficient par.Lx where
  toFun z := if component then z.1 j else z.2 j
  map_add' z v := by cases component <;> rfl
  map_smul' r z := by cases component <;> rfl

def fieldJet (par : FieldParameters) (i : FieldJetIndex par) :
    ClosedPeriodicPair par →ₗ[ℝ] PeriodicCoefficient par.Lx :=
  (coefficientSpatialJet par i.2.2).comp (closedPairComponent par i.1 i.2.1)

def compactFieldJet (par : FieldParameters) (i : FieldJetIndex par) :
    ClosedPeriodicPair par →ₗ[ℝ] CompactPeriodCoefficient par :=
  (periodicCompactRestriction par).toLinearMap.comp (fieldJet par i)

def compactFieldJets (par : FieldParameters) :
    ClosedPeriodicPair par →ₗ[ℝ] (FieldJetIndex par → CompactPeriodCoefficient par) :=
  LinearMap.pi (compactFieldJet par)

/-- The ordinary C-infinity topology for periodic fields: uniform control
of each finite spatial jet on one compact period interval. -/
@[instance_reducible] def closedPeriodicSmoothTopology (par : FieldParameters) :
    TopologicalSpace (ClosedPeriodicPair par) :=
  TopologicalSpace.induced (compactFieldJets par) inferInstance

namespace DLWFieldTopology
scoped instance (par : FieldParameters) :
    TopologicalSpace (ClosedPeriodicPair par) := closedPeriodicSmoothTopology par

end DLWFieldTopology
open scoped DLWFieldTopology

namespace DLWFieldTopology
scoped instance (par : FieldParameters) :
    ContinuousAdd (ClosedPeriodicPair par) :=
  continuousAdd_induced (compactFieldJets par).toAddMonoidHom

scoped instance (par : FieldParameters) :
    ContinuousSMul ℝ (ClosedPeriodicPair par) :=
  continuousSMul_induced (compactFieldJets par)
end DLWFieldTopology

theorem compactFieldJets_continuous (par : FieldParameters) :
    Continuous (compactFieldJets par) := continuous_induced_dom

theorem compactFieldJet_continuous (par : FieldParameters) (i : FieldJetIndex par) :
    Continuous (compactFieldJet par i) :=
  (continuous_apply i).comp (compactFieldJets_continuous par)

/-- A periodic function is determined by its values on one period. -/
theorem periodicCompactRestriction_injective (par : FieldParameters) :
    Function.Injective (periodicCompactRestriction par) := by
  intro f g h
  apply Subtype.ext
  funext x
  let n : ℤ := Int.floor (x / par.Lx)
  have hlo : (n : ℝ) * par.Lx ≤ x :=
    (le_div_iff₀ par.Lx_pos).mp (Int.floor_le (x / par.Lx))
  have hhi : x < ((n : ℝ) + 1) * par.Lx :=
    (div_lt_iff₀ par.Lx_pos).mp (Int.lt_floor_add_one (x / par.Lx))
  have hy : x - (n : ℝ) * par.Lx ∈ Set.Icc (0 : ℝ) par.Lx := by
    constructor <;> linarith
  have heq := congrArg (fun F : CompactPeriodCoefficient par =>
    F ⟨x - (n : ℝ) * par.Lx, hy⟩) h
  change (f : ℝ → ℝ) (x - (n : ℝ) * par.Lx) =
    (g : ℝ → ℝ) (x - (n : ℝ) * par.Lx) at heq
  rw [f.property.2.sub_int_mul_eq n, g.property.2.sub_int_mul_eq n] at heq
  exact heq

theorem compactFieldJets_injective (par : FieldParameters) :
    Function.Injective (compactFieldJets par) := by
  intro z v h
  apply Prod.ext
  · apply Subtype.ext
    funext j
    apply periodicCompactRestriction_injective par
    have hj := congrArg (fun jets => jets (true, j, 0)) h
    exact hj
  · apply Subtype.ext
    funext j
    apply periodicCompactRestriction_injective par
    have hj := congrArg (fun jets => jets (false, j, 0)) h
    exact hj

theorem compactFieldJets_isEmbedding (par : FieldParameters) :
    Topology.IsEmbedding (compactFieldJets par) :=
  (compactFieldJets_injective par).isEmbedding_induced

namespace DLWFieldTopology
scoped instance (par : FieldParameters) : T2Space (ClosedPeriodicPair par) :=
  (compactFieldJets_isEmbedding par).t2Space
end DLWFieldTopology

def compactPeriodExtension (par : FieldParameters) (f : CompactPeriodCoefficient par) : ℝ → ℝ :=
  fun x => f (Set.projIcc 0 par.Lx par.Lx_pos.le x)

theorem compactPeriodExtension_continuous (par : FieldParameters)
    (f : CompactPeriodCoefficient par) : Continuous (compactPeriodExtension par f) :=
  f.continuous.comp continuous_projIcc

def compactPeriodIntegralLinear (par : FieldParameters) :
    CompactPeriodCoefficient par →ₗ[ℝ] ℝ where
  toFun f := ∫ x in (0 : ℝ)..par.Lx, compactPeriodExtension par f x
  map_add' f g := by
    change (∫ x in (0 : ℝ)..par.Lx,
      compactPeriodExtension par f x + compactPeriodExtension par g x) = _
    exact intervalIntegral.integral_add
      ((compactPeriodExtension_continuous par f).intervalIntegrable 0 par.Lx)
      ((compactPeriodExtension_continuous par g).intervalIntegrable 0 par.Lx)
  map_smul' r f := by
    change (∫ x in (0 : ℝ)..par.Lx, r * compactPeriodExtension par f x) =
      r * ∫ x in (0 : ℝ)..par.Lx, compactPeriodExtension par f x
    exact intervalIntegral.integral_const_mul r _

def compactPeriodIntegral (par : FieldParameters) :
    CompactPeriodCoefficient par →L[ℝ] ℝ :=
  (compactPeriodIntegralLinear par).mkContinuous par.Lx (by
    intro f
    have hbound := intervalIntegral.norm_integral_le_of_norm_le_const
      (a := (0 : ℝ)) (b := par.Lx)
      (f := compactPeriodExtension par f) (C := ‖f‖)
      (fun x _ => f.norm_coe_le_norm (Set.projIcc 0 par.Lx par.Lx_pos.le x))
    simpa only [compactPeriodIntegralLinear, LinearMap.coe_mk, AddHom.coe_mk,
      sub_zero, abs_of_pos par.Lx_pos, mul_comm] using hbound)

theorem compactPeriodIntegral_restriction (par : FieldParameters)
    (f : PeriodicCoefficient par.Lx) :
    compactPeriodIntegral par (periodicCompactRestriction par f) =
      periodicCoefficientIntegral par.Lx f := by
  change (∫ x in (0 : ℝ)..par.Lx, (f : ℝ → ℝ)
    (Set.projIcc 0 par.Lx par.Lx_pos.le x)) = ∫ x in (0 : ℝ)..par.Lx, (f : ℝ → ℝ) x
  apply intervalIntegral.integral_congr
  intro x hx
  have hx' : x ∈ Set.Icc (0 : ℝ) par.Lx :=
    (Set.uIcc_of_le par.Lx_pos.le ▸ hx)
  change (f : ℝ → ℝ) (Set.projIcc 0 par.Lx par.Lx_pos.le x) = (f : ℝ → ℝ) x
  rw [Set.projIcc_of_mem par.Lx_pos.le hx']

/-- A genuine finite differential polynomial, allowing smooth fixed test
functions as coefficients, evaluated on the actual periodic field jets. -/
def fieldDifferentialPolynomial (par : FieldParameters)
    (p : MvPolynomial (FieldJetIndex par) (PeriodicCoefficient par.Lx))
    (z : ClosedPeriodicPair par) : PeriodicCoefficient par.Lx :=
  MvPolynomial.eval (fun i => fieldJet par i z) p

def fieldPolynomialIntegral (par : FieldParameters)
    (p : MvPolynomial (FieldJetIndex par) (PeriodicCoefficient par.Lx))
    (z : ClosedPeriodicPair par) : ℝ :=
  periodicCoefficientIntegral par.Lx (fieldDifferentialPolynomial par p z)

theorem compactRestriction_fieldPolynomial (par : FieldParameters)
    (p : MvPolynomial (FieldJetIndex par) (PeriodicCoefficient par.Lx))
    (z : ClosedPeriodicPair par) :
    periodicCompactRestriction par (fieldDifferentialPolynomial par p z) =
      MvPolynomial.eval (fun i => compactFieldJet par i z)
        (MvPolynomial.map (periodicCompactRestriction par).toRingHom p) := by
  change (periodicCompactRestriction par).toRingHom (MvPolynomial.eval₂Hom (RingHom.id _)
    (fun i => fieldJet par i z) p) = _
  rw [MvPolynomial.map_eval₂Hom]
  exact MvPolynomial.eval₂_eq_eval_map (f := (periodicCompactRestriction par).toRingHom)
    (fun i => compactFieldJet par i z) p

theorem fieldPolynomialIntegral_continuous (par : FieldParameters)
    (p : MvPolynomial (FieldJetIndex par) (PeriodicCoefficient par.Lx)) :
    Continuous (fieldPolynomialIntegral par p) := by
  have hcompact : Continuous (fun z => MvPolynomial.eval
      (fun i => compactFieldJet par i z)
      (MvPolynomial.map (periodicCompactRestriction par).toRingHom p)) :=
    (MvPolynomial.continuous_eval _).comp
      (continuous_pi (compactFieldJet_continuous par))
  have h := (compactPeriodIntegral par).continuous.comp hcompact
  convert h using 1
  funext z
  change fieldPolynomialIntegral par p z = compactPeriodIntegral par
    (MvPolynomial.eval (fun i => compactFieldJet par i z)
      (MvPolynomial.map (periodicCompactRestriction par).toRingHom p))
  rw [← compactRestriction_fieldPolynomial,
    compactPeriodIntegral_restriction]
  rfl

/-- Integrate the finitely many actual coefficient functions of an
ordinary polynomial. This is a coefficient-wise linear operation. -/
def integrateCoefficientPolynomial {R : Type*} [CommRing R] [Algebra ℝ R]
    (integral : R →ₗ[ℝ] ℝ) (p : Polynomial R) : Polynomial ℝ :=
  ∑ n ∈ p.support, Polynomial.monomial n (integral (p.coeff n))

theorem integrateCoefficientPolynomial_coeff {R : Type*} [CommRing R] [Algebra ℝ R]
    (integral : R →ₗ[ℝ] ℝ) (p : Polynomial R) (n : ℕ) :
    (integrateCoefficientPolynomial integral p).coeff n = integral (p.coeff n) := by
  classical
  by_cases hn : p.coeff n = 0 <;>
    simp [integrateCoefficientPolynomial, Polynomial.finsetSum_coeff,
      Polynomial.coeff_monomial, Polynomial.mem_support_iff, hn]

theorem integrateCoefficientPolynomial_eval {R : Type*} [CommRing R] [Algebra ℝ R]
    (integral : R →ₗ[ℝ] ℝ) (p : Polynomial R) (t : ℝ) :
    (integrateCoefficientPolynomial integral p).eval t =
      integral (p.eval (algebraMap ℝ R t)) := by
  classical
  rw [Polynomial.eval_eq_sum (p := p), Polynomial.sum_def, map_sum]
  simp only [integrateCoefficientPolynomial, Polynomial.eval_finsetSum,
    Polynomial.eval_monomial]
  apply Finset.sum_congr rfl
  intro n _
  have hsmul : p.coeff n * algebraMap ℝ R t ^ n = t ^ n • p.coeff n := by
    rw [Algebra.smul_def, map_pow]
    exact mul_comm _ _
  rw [hsmul, map_smul, smul_eq_mul, mul_comm]

def fieldPolynomialLine (par : FieldParameters)
    (p : MvPolynomial (FieldJetIndex par) (PeriodicCoefficient par.Lx))
    (z v : ClosedPeriodicPair par) : Polynomial (PeriodicCoefficient par.Lx) :=
  MvPolynomial.eval₂Hom Polynomial.C
    (fun i => Polynomial.C (fieldJet par i z) +
      Polynomial.C (fieldJet par i v) * Polynomial.X) p

theorem fieldPolynomialLine_eval (par : FieldParameters)
    (p : MvPolynomial (FieldJetIndex par) (PeriodicCoefficient par.Lx))
    (z v : ClosedPeriodicPair par) (t : ℝ) :
    (fieldPolynomialLine par p z v).eval (algebraMap ℝ (PeriodicCoefficient par.Lx) t) =
      fieldDifferentialPolynomial par p (z + t • v) := by
  have h := MvPolynomial.map_eval₂Hom Polynomial.C
    (fun i => Polynomial.C (fieldJet par i z) +
      Polynomial.C (fieldJet par i v) * Polynomial.X)
    (Polynomial.evalRingHom (algebraMap ℝ (PeriodicCoefficient par.Lx) t)) p
  have hcoef : (Polynomial.evalRingHom
      (algebraMap ℝ (PeriodicCoefficient par.Lx) t)).comp Polynomial.C = RingHom.id _ := by
    ext r
    simp
  rw [hcoef] at h
  simp only [Polynomial.coe_evalRingHom, Polynomial.eval_add, Polynomial.eval_C,
    Polynomial.eval_mul, Polynomial.eval_X] at h
  change (fieldPolynomialLine par p z v).eval _ =
    MvPolynomial.eval₂Hom (RingHom.id _) (fun i => fieldJet par i (z + t • v)) p
  have hvars : (fun i : FieldJetIndex par => fieldJet par i (z + t • v)) =
      (fun i => fieldJet par i z +
        fieldJet par i v * algebraMap ℝ (PeriodicCoefficient par.Lx) t) := by
    funext i
    rw [map_add, map_smul, Algebra.smul_def, mul_comm]
  rw [hvars]
  exact h

/-- Actual differential-polynomial integrals restrict to finite real
polynomials on every affine line in the physical field space. -/
theorem fieldPolynomialIntegral_alongLine (par : FieldParameters)
    (p : MvPolynomial (FieldJetIndex par) (PeriodicCoefficient par.Lx))
    (z v : ClosedPeriodicPair par) :
    ∃ q : Polynomial ℝ, ∀ t : ℝ,
      fieldPolynomialIntegral par p (z + t • v) = q.eval t := by
  refine ⟨integrateCoefficientPolynomial (periodicCoefficientIntegral par.Lx)
    (fieldPolynomialLine par p z v), ?_⟩
  intro t
  rw [integrateCoefficientPolynomial_eval, fieldPolynomialLine_eval]
  rfl

def fieldPolynomialVariation (par : FieldParameters) (v : ClosedPeriodicPair par) :
    Derivation (PeriodicCoefficient par.Lx)
      (MvPolynomial (FieldJetIndex par) (PeriodicCoefficient par.Lx))
      (MvPolynomial (FieldJetIndex par) (PeriodicCoefficient par.Lx)) :=
  MvPolynomial.mkDerivation (PeriodicCoefficient par.Lx)
    (fun i => MvPolynomial.C (fieldJet par i v))

theorem fieldPolynomialLine_coeff_zero (par : FieldParameters)
    (p : MvPolynomial (FieldJetIndex par) (PeriodicCoefficient par.Lx))
    (z v : ClosedPeriodicPair par) :
    (fieldPolynomialLine par p z v).coeff 0 = fieldDifferentialPolynomial par p z := by
  simpa [← Polynomial.coeff_zero_eq_eval_zero] using fieldPolynomialLine_eval par p z v 0

/-- The coefficient of t in the exact affine-line polynomial is the
formal variation evaluated on the original field. -/
theorem fieldPolynomialLine_coeff_one (par : FieldParameters)
    (p : MvPolynomial (FieldJetIndex par) (PeriodicCoefficient par.Lx))
    (z v : ClosedPeriodicPair par) :
    (fieldPolynomialLine par p z v).coeff 1 =
      fieldDifferentialPolynomial par (fieldPolynomialVariation par v p) z := by
  induction p using MvPolynomial.induction_on with
  | C r =>
    simp [fieldPolynomialLine, fieldPolynomialVariation, fieldDifferentialPolynomial]
  | add p q hp hq =>
    simp only [fieldPolynomialLine, map_add, Polynomial.coeff_add] at *
    rw [hp, hq]
    simp only [fieldDifferentialPolynomial, MvPolynomial.eval_add]
  | mul_X p i hp =>
    have hmul : fieldPolynomialLine par (p * MvPolynomial.X i) z v =
        fieldPolynomialLine par p z v *
          (Polynomial.C (fieldJet par i z) + Polynomial.C (fieldJet par i v) * Polynomial.X) := by
      simp only [fieldPolynomialLine, map_mul, MvPolynomial.eval₂Hom_X']
    rw [hmul]
    rw [mul_add, Polynomial.coeff_add, Polynomial.coeff_mul_C,
      ← mul_assoc, Polynomial.coeff_mul_X, Polynomial.coeff_mul_C,
      hp, fieldPolynomialLine_coeff_zero]
    simp only [fieldDifferentialPolynomial, Derivation.leibniz, Algebra.smul_def,
      Algebra.algebraMap_self, RingHom.id_apply, MvPolynomial.eval_add,
      MvPolynomial.eval_mul, MvPolynomial.eval_X,
      fieldPolynomialVariation, MvPolynomial.mkDerivation_X, MvPolynomial.eval_C]
    ring

theorem fieldPolynomialIntegral_hasDerivAt (par : FieldParameters)
    (p : MvPolynomial (FieldJetIndex par) (PeriodicCoefficient par.Lx))
    (z v : ClosedPeriodicPair par) :
    HasDerivAt (fun t : ℝ => fieldPolynomialIntegral par p (z + t • v))
      (fieldPolynomialIntegral par (fieldPolynomialVariation par v p) z) 0 := by
  let q := integrateCoefficientPolynomial (periodicCoefficientIntegral par.Lx)
    (fieldPolynomialLine par p z v)
  have h := q.hasDerivAt (0 : ℝ)
  convert h using 1
  · funext t
    rw [integrateCoefficientPolynomial_eval, fieldPolynomialLine_eval]
    rfl
  · simp only [← Polynomial.coeff_zero_eq_eval_zero, Polynomial.coeff_derivative, zero_add,
      Nat.cast_zero, zero_add, mul_one, q, integrateCoefficientPolynomial_coeff,
      fieldPolynomialLine_coeff_one]
    rfl

theorem fieldPolynomialVariation_add (par : FieldParameters) (v w : ClosedPeriodicPair par) :
    fieldPolynomialVariation par (v + w) =
      fieldPolynomialVariation par v + fieldPolynomialVariation par w := by
  apply MvPolynomial.derivation_ext
  intro i
  simp [fieldPolynomialVariation, map_add]

theorem fieldPolynomialVariation_smul (par : FieldParameters) (r : ℝ)
    (v : ClosedPeriodicPair par) :
    fieldPolynomialVariation par (r • v) =
      algebraMap ℝ (PeriodicCoefficient par.Lx) r • fieldPolynomialVariation par v := by
  apply MvPolynomial.derivation_ext
  intro i
  simp [fieldPolynomialVariation, map_smul, Algebra.smul_def, MvPolynomial.algebraMap_eq]

/-- The actual affine-line derivative is a linear covector on all closed
periodic tangent fields. -/
def fieldPolynomialDifferential (par : FieldParameters)
    (p : MvPolynomial (FieldJetIndex par) (PeriodicCoefficient par.Lx))
    (z : ClosedPeriodicPair par) : ClosedPeriodicPair par →ₗ[ℝ] ℝ where
  toFun v := fieldPolynomialIntegral par (fieldPolynomialVariation par v p) z
  map_add' v w := by
    rw [fieldPolynomialVariation_add]
    simp only [Derivation.add_apply, fieldPolynomialIntegral, fieldDifferentialPolynomial,
      MvPolynomial.eval_add, map_add]
  map_smul' r v := by
    rw [fieldPolynomialVariation_smul]
    simp only [Derivation.smul_apply, fieldPolynomialIntegral, fieldDifferentialPolynomial,
      MvPolynomial.smul_eval]
    change periodicCoefficientIntegral par.Lx
      (r • MvPolynomial.eval (fun i => fieldJet par i z) (fieldPolynomialVariation par v p)) = _
    exact map_smul (periodicCoefficientIntegral par.Lx) r _

theorem fieldPolynomialDifferential_hasDerivAt (par : FieldParameters)
    (p : MvPolynomial (FieldJetIndex par) (PeriodicCoefficient par.Lx))
    (z v : ClosedPeriodicPair par) :
    HasDerivAt (fun t : ℝ => fieldPolynomialIntegral par p (z + t • v))
      (fieldPolynomialDifferential par p z v) 0 :=
  fieldPolynomialIntegral_hasDerivAt par p z v

def PolynomialAlongFieldLines (par : FieldParameters)
    (f : ClosedPeriodicPair par → ℝ) : Prop :=
  ∀ z v, ∃ p : Polynomial ℝ, ∀ t : ℝ, f (z + t • v) = p.eval t

inductive FieldPolynomialObservable (par : FieldParameters) :
    (ClosedPeriodicPair par → ℝ) → Prop
  | constant (r : ℝ) : FieldPolynomialObservable par (fun _ => r)
  | integral (p : MvPolynomial (FieldJetIndex par) (PeriodicCoefficient par.Lx)) :
      FieldPolynomialObservable par (fieldPolynomialIntegral par p)
  | add {f g} : FieldPolynomialObservable par f → FieldPolynomialObservable par g →
      FieldPolynomialObservable par (fun z => f z + g z)
  | mul {f g} : FieldPolynomialObservable par f → FieldPolynomialObservable par g →
      FieldPolynomialObservable par (fun z => f z * g z)

theorem FieldPolynomialObservable.continuous {par : FieldParameters}
    {f : ClosedPeriodicPair par → ℝ} (hf : FieldPolynomialObservable par f) :
    Continuous f := by
  induction hf with
  | constant r => exact continuous_const
  | integral p => exact fieldPolynomialIntegral_continuous par p
  | add _ _ ihf ihg => exact ihf.add ihg
  | mul _ _ ihf ihg => exact ihf.mul ihg

theorem FieldPolynomialObservable.alongLines {par : FieldParameters}
    {f : ClosedPeriodicPair par → ℝ} (hf : FieldPolynomialObservable par f) :
    PolynomialAlongFieldLines par f := by
  induction hf with
  | constant r =>
    intro z v
    exact ⟨Polynomial.C r, fun t => by simp⟩
  | integral p => exact fieldPolynomialIntegral_alongLine par p
  | add _ _ ihf ihg =>
    intro z v
    obtain ⟨p, hp⟩ := ihf z v
    obtain ⟨q, hq⟩ := ihg z v
    exact ⟨p + q, fun t => by simp only [Polynomial.eval_add, hp t, hq t]⟩
  | mul _ _ ihf ihg =>
    intro z v
    obtain ⟨p, hp⟩ := ihf z v
    obtain ⟨q, hq⟩ := ihg z v
    exact ⟨p * q, fun t => by simp only [Polynomial.eval_mul, hp t, hq t]⟩

theorem FieldPolynomialObservable.sum {par : FieldParameters} {I : Type*}
    (s : Finset I) (f : I → ClosedPeriodicPair par → ℝ)
    (hf : ∀ i ∈ s, FieldPolynomialObservable par (f i)) :
    FieldPolynomialObservable par (fun z => ∑ i ∈ s, f i z) := by
  classical
  induction s using Finset.induction_on with
  | empty => simpa using FieldPolynomialObservable.constant (par := par) 0
  | @insert i s hi ih =>
    simpa only [Finset.sum_insert hi] using
      (hf i (Finset.mem_insert_self i s)).add
        (ih (fun j hj => hf j (Finset.mem_insert_of_mem hj)))

theorem FieldPolynomialObservable.prod {par : FieldParameters} {I : Type*}
    (s : Finset I) (f : I → ClosedPeriodicPair par → ℝ)
    (hf : ∀ i ∈ s, FieldPolynomialObservable par (f i)) :
    FieldPolynomialObservable par (fun z => ∏ i ∈ s, f i z) := by
  classical
  induction s using Finset.induction_on with
  | empty => simpa using FieldPolynomialObservable.constant (par := par) 1
  | @insert i s hi ih =>
    simpa only [Finset.prod_insert hi] using
      (hf i (Finset.mem_insert_self i s)).mul
        (ih (fun j hj => hf j (Finset.mem_insert_of_mem hj)))

def fieldPolynomialMinor (par : FieldParameters) {N : ℕ}
    (p : Matrix (Fin N) (Fin N)
      (MvPolynomial (FieldJetIndex par) (PeriodicCoefficient par.Lx)))
    (z : ClosedPeriodicPair par) : ℝ :=
  Matrix.det (fun i j => fieldPolynomialIntegral par (p i j) z)

theorem fieldPolynomialMinor_observable (par : FieldParameters) {N : ℕ}
    (p : Matrix (Fin N) (Fin N)
      (MvPolynomial (FieldJetIndex par) (PeriodicCoefficient par.Lx))) :
    FieldPolynomialObservable par (fieldPolynomialMinor par p) := by
  classical
  have hdet : fieldPolynomialMinor par p =
      (fun z => ∑ permutation : Equiv.Perm (Fin N),
        (Equiv.Perm.sign permutation : ℝ) *
          ∏ i, fieldPolynomialIntegral par (p (permutation i) i) z) := by
    funext z
    exact Matrix.det_apply' _
  rw [hdet]
  apply FieldPolynomialObservable.sum
  intro permutation _
  apply FieldPolynomialObservable.mul (FieldPolynomialObservable.constant _)
  apply FieldPolynomialObservable.prod
  intro i _
  exact FieldPolynomialObservable.integral _

/-- A concrete nonzero differential-polynomial minor yields an open dense
set in the actual compact-jet topology, without a Baire-space assumption. -/
theorem fieldPolynomialMinor_openDense (par : FieldParameters) {N : ℕ}
    (p : Matrix (Fin N) (Fin N)
      (MvPolynomial (FieldJetIndex par) (PeriodicCoefficient par.Lx)))
    (witness : ClosedPeriodicPair par) (hwitness : fieldPolynomialMinor par p witness ≠ 0) :
    IsOpen {z : ClosedPeriodicPair par | fieldPolynomialMinor par p z ≠ 0} ∧
      Dense {z : ClosedPeriodicPair par | fieldPolynomialMinor par p z ≠ 0} := by
  have hp := fieldPolynomialMinor_observable par p
  apply openDense_nonzero_of_polynomialAlongLinesTo _ witness hp.continuous _ hwitness
  intro z
  exact hp.alongLines z (witness - z)

/-- The entries are the actual directional derivatives of the displayed
differential-polynomial charge integrals, proved immediately above. -/
def fieldPolynomialDerivativeMinor (par : FieldParameters) {N : ℕ}
    (charges : Fin N → MvPolynomial (FieldJetIndex par) (PeriodicCoefficient par.Lx))
    (directions : Fin N → ClosedPeriodicPair par) : ClosedPeriodicPair par → ℝ :=
  fieldPolynomialMinor par (fun i j => fieldPolynomialVariation par (directions j) (charges i))

theorem fieldPolynomialDerivativeMinor_openDense (par : FieldParameters) {N : ℕ}
    (charges : Fin N → MvPolynomial (FieldJetIndex par) (PeriodicCoefficient par.Lx))
    (directions : Fin N → ClosedPeriodicPair par) (witness : ClosedPeriodicPair par)
    (hwitness : fieldPolynomialDerivativeMinor par charges directions witness ≠ 0) :
    IsOpen {z : ClosedPeriodicPair par | fieldPolynomialDerivativeMinor par charges directions z ≠ 0} ∧
      Dense {z : ClosedPeriodicPair par | fieldPolynomialDerivativeMinor par charges directions z ≠ 0} :=
  fieldPolynomialMinor_openDense par _ witness hwitness

theorem fieldPolynomialDifferentials_independent_of_minor (par : FieldParameters) {N : ℕ}
    (charges : Fin N → MvPolynomial (FieldJetIndex par) (PeriodicCoefficient par.Lx))
    (directions : Fin N → ClosedPeriodicPair par) (z : ClosedPeriodicPair par)
    (hminor : fieldPolynomialDerivativeMinor par charges directions z ≠ 0) :
    LinearIndependent ℝ (fun i => fieldPolynomialDifferential par (charges i) z) :=
  linearIndependent_of_covectorMinor_det_ne_zero _ directions hminor

/-- Finite-block generic independence in the actual smooth field topology,
for any specified differential-polynomial charges with a proven witness. -/
theorem fieldPolynomialDifferentials_generically_independent (par : FieldParameters) {N : ℕ}
    (charges : Fin N → MvPolynomial (FieldJetIndex par) (PeriodicCoefficient par.Lx))
    (directions : Fin N → ClosedPeriodicPair par) (witness : ClosedPeriodicPair par)
    (hwitness : fieldPolynomialDerivativeMinor par charges directions witness ≠ 0) :
    ∃ S : Set (ClosedPeriodicPair par), IsOpen S ∧ Dense S ∧
      ∀ z ∈ S, LinearIndependent ℝ (fun i => fieldPolynomialDifferential par (charges i) z) := by
  have hgeneric := fieldPolynomialDerivativeMinor_openDense par charges directions witness hwitness
  refine ⟨{z | fieldPolynomialDerivativeMinor par charges directions z ≠ 0},
    hgeneric.1, hgeneric.2, ?_⟩
  intro z hz
  exact fieldPolynomialDifferentials_independent_of_minor par charges directions z hz

#print axioms coefficientSpatialJet_value
#print axioms compactFieldJets_isEmbedding
#print axioms fieldPolynomialIntegral_continuous
#print axioms fieldPolynomialIntegral_alongLine
#print axioms fieldPolynomialIntegral_hasDerivAt
#print axioms fieldPolynomialDifferentials_generically_independent
#print axioms fieldPolynomialMinor_openDense

end
end DLWLean
