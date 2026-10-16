import SpectralVariation
import Mathlib.Algebra.Algebra.Hom
import Mathlib.Tactic.FieldSimp
import QuadraticSymbol
import Independence
import Mathlib.Analysis.SpecialFunctions.Integrals.Basic
import Mathlib.Analysis.Calculus.IteratedDeriv.Lemmas

/-!
Second-order resolvent algebra. A relative two-jet keeps evaluation at
epsilon=0 separate from differentiation, so the opposite factor variations
are compatible with both factors having the same evaluated value.
-/
namespace DLWLean
noncomputable section

variable {A B : Type*} [Ring A] [Algebra ℝ A] [Ring B] [Algebra ℝ B]

structure AlgebraJet2 (A B : Type*) [Ring A] [Algebra ℝ A]
    [Ring B] [Algebra ℝ B] where
  value : A →ₐ[ℝ] B
  first : A →ₗ[ℝ] B
  second : A →ₗ[ℝ] B
  first_mul : ∀ a b, first (a * b) = first a * value b + value a * first b
  second_mul : ∀ a b, second (a * b) =
    second a * value b + first a * first b + first a * first b + value a * second b

/-- The interface is realized by an actual algebra derivation followed by
an evaluation homomorphism; its second map is evaluation composed with v². -/
def AlgebraEvolution.jet2 (v : AlgebraEvolution A) (evaluation : A →ₐ[ℝ] B) :
    AlgebraJet2 A B where
  value := evaluation
  first := evaluation.toLinearMap.comp v.toLinearMap
  second := evaluation.toLinearMap.comp (v.toLinearMap.comp v.toLinearMap)
  first_mul a b := by
    simp only [LinearMap.comp_apply, AlgHom.toLinearMap_apply, v.leibniz, map_add, map_mul]
  second_mul a b := by
    simp only [LinearMap.comp_apply, AlgHom.toLinearMap_apply, v.leibniz, map_add, map_mul]
    abel

theorem AlgebraJet2.first_one (j : AlgebraJet2 A B) : j.first 1 = 0 := by
  have h := j.first_mul (1 : A) 1
  simp only [map_one, one_mul, mul_one] at h
  have hs := congrArg (fun b : B => b - j.first 1) h
  simpa only [sub_self, add_sub_cancel_right] using hs.symm

theorem AlgebraJet2.second_one (j : AlgebraJet2 A B) : j.second 1 = 0 := by
  have h := j.second_mul (1 : A) 1
  simp only [map_one, j.first_one, zero_mul, add_zero, one_mul, mul_one] at h
  have hs := congrArg (fun b : B => b - j.second 1) h
  simpa only [sub_self, add_sub_cancel_right] using hs.symm

theorem AlgebraJet2.first_inverse (j : AlgebraJet2 A B) (u : Aˣ) :
    j.first (↑u⁻¹ : A) =
      -j.value (↑u⁻¹ : A) * j.first (u : A) * j.value (↑u⁻¹ : A) := by
  have h : j.first (u : A) * j.value (↑u⁻¹ : A) +
      j.value (u : A) * j.first (↑u⁻¹ : A) = 0 := by
    rw [← j.first_mul, Units.mul_inv, j.first_one]
  have hi := congrArg (fun b : B => j.value (↑u⁻¹ : A) * b) h
  simp only [mul_add, ← mul_assoc, ← map_mul, Units.inv_mul, map_one,
    one_mul, mul_zero] at hi
  simpa only [neg_mul, mul_assoc] using eq_neg_of_add_eq_zero_right hi

theorem AlgebraJet2.second_inverse (j : AlgebraJet2 A B) (u : Aˣ) :
    j.second (↑u⁻¹ : A) =
      j.value (↑u⁻¹ : A) * j.first (u : A) * j.value (↑u⁻¹ : A) *
        j.first (u : A) * j.value (↑u⁻¹ : A) +
      j.value (↑u⁻¹ : A) * j.first (u : A) * j.value (↑u⁻¹ : A) *
        j.first (u : A) * j.value (↑u⁻¹ : A) -
      j.value (↑u⁻¹ : A) * j.second (u : A) * j.value (↑u⁻¹ : A) := by
  have h : j.second (u : A) * j.value (↑u⁻¹ : A) +
      j.first (u : A) * j.first (↑u⁻¹ : A) +
      j.first (u : A) * j.first (↑u⁻¹ : A) +
      j.value (u : A) * j.second (↑u⁻¹ : A) = 0 := by
    rw [← j.second_mul, Units.mul_inv, j.second_one]
  have hi := congrArg (fun b : B => j.value (↑u⁻¹ : A) * b) h
  simp only [mul_add, ← mul_assoc, ← map_mul, Units.inv_mul, map_one,
    one_mul, mul_zero] at hi
  have hsol := eq_neg_of_add_eq_zero_right hi
  rw [j.first_inverse] at hsol
  rw [hsol]
  noncomm_ring

theorem AlgebraJet2.value_inverse (j : AlgebraJet2 A B) (u : Aˣ) (base : Bˣ)
    (hvalue : j.value (u : A) = (base : B)) :
    j.value (↑u⁻¹ : A) = (↑base⁻¹ : B) := by
  have hprod : j.value (↑u⁻¹ : A) * (base : B) = 1 := by
    rw [← hvalue, ← map_mul, Units.inv_mul, map_one]
  calc
    j.value (↑u⁻¹ : A) = j.value (↑u⁻¹ : A) *
        ((base : B) * (↑base⁻¹ : B)) := by simp
    _ = (j.value (↑u⁻¹ : A) * (base : B)) * (↑base⁻¹ : B) :=
      (mul_assoc _ _ _).symm
    _ = (↑base⁻¹ : B) := by rw [hprod, one_mul]

/-- M=others+2 resolvents on the two-active-site slice: the remaining
factors all have zero perturbation and the same base resolvent. -/
def balancedInverseSum (plus minus background : Aˣ) (others : ℕ) : A :=
  (↑plus⁻¹ : A) + (↑minus⁻¹ : A) + (others : ℝ) • (↑background⁻¹ : A)

theorem balancedInverseSum_value (j : AlgebraJet2 A B)
    (plus minus background : Aˣ) (base : Bˣ) (others : ℕ)
    (hplus : j.value (plus : A) = (base : B))
    (hminus : j.value (minus : A) = (base : B))
    (hbackground : j.value (background : A) = (base : B)) :
    j.value (balancedInverseSum plus minus background others) =
      ((others : ℝ) + 2) • (↑base⁻¹ : B) := by
  simp only [balancedInverseSum, map_add, map_smul,
    j.value_inverse plus base hplus, j.value_inverse minus base hminus,
    j.value_inverse background base hbackground, add_smul, two_smul]
  abel

theorem balancedInverseSum_first (j : AlgebraJet2 A B)
    (plus minus background : Aˣ) (base : Bˣ) (others : ℕ) (f : B)
    (hplus : j.value (plus : A) = (base : B))
    (hminus : j.value (minus : A) = (base : B))
    (hbackground : j.value (background : A) = (base : B))
    (hfirstplus : j.first (plus : A) = -f)
    (hfirstminus : j.first (minus : A) = f)
    (hfirstbackground : j.first (background : A) = 0) :
    j.first (balancedInverseSum plus minus background others) = 0 := by
  simp only [balancedInverseSum, map_add, map_smul, j.first_inverse,
    j.value_inverse plus base hplus, j.value_inverse minus base hminus,
    j.value_inverse background base hbackground, hfirstplus, hfirstminus,
    hfirstbackground, mul_zero, zero_mul, smul_zero, add_zero]
  noncomm_ring

theorem balancedInverseSum_second (j : AlgebraJet2 A B)
    (plus minus background : Aˣ) (base : Bˣ) (others : ℕ) (f : B)
    (hplus : j.value (plus : A) = (base : B))
    (hminus : j.value (minus : A) = (base : B))
    (hbackground : j.value (background : A) = (base : B))
    (hfirstplus : j.first (plus : A) = -f)
    (hfirstminus : j.first (minus : A) = f)
    (hfirstbackground : j.first (background : A) = 0)
    (hsecondplus : j.second (plus : A) = 0)
    (hsecondminus : j.second (minus : A) = 0)
    (hsecondbackground : j.second (background : A) = 0) :
    j.second (balancedInverseSum plus minus background others) =
      (4 : ℝ) • ((↑base⁻¹ : B) * f * (↑base⁻¹ : B) * f * (↑base⁻¹ : B)) := by
  have hfour : (4 : ℝ) = 2 + 2 := by norm_num
  simp only [balancedInverseSum, map_add, map_smul, j.second_inverse,
    j.value_inverse plus base hplus, j.value_inverse minus base hminus,
    j.value_inverse background base hbackground, hfirstplus, hfirstminus,
    hfirstbackground, hsecondplus, hsecondminus, hsecondbackground,
    mul_zero, zero_mul, add_zero, sub_zero, smul_zero,
    hfour, add_smul, two_smul]
  noncomm_ring

theorem AlgebraJet2.scaled_value_inverse (j : AlgebraJet2 A B)
    (sumUnit : Aˣ) (base : Bˣ) (M : ℝ) (hM : M ≠ 0)
    (hvalue : j.value (sumUnit : A) = M • (↑base⁻¹ : B)) :
    j.value (↑sumUnit⁻¹ : A) = M⁻¹ • (base : B) := by
  have hprod : (M⁻¹ • (base : B)) * j.value (sumUnit : A) = 1 := by
    rw [hvalue]
    simp only [Algebra.smul_mul_assoc, Algebra.mul_smul_comm,
      smul_smul, Units.mul_inv, mul_inv_cancel₀ hM, one_smul]
  calc
    j.value (↑sumUnit⁻¹ : A) = 1 * j.value (↑sumUnit⁻¹ : A) := (one_mul _).symm
    _ = ((M⁻¹ • (base : B)) * j.value (sumUnit : A)) *
        j.value (↑sumUnit⁻¹ : A) := by rw [hprod]
    _ = (M⁻¹ • (base : B)) *
        (j.value (sumUnit : A) * j.value (↑sumUnit⁻¹ : A)) := mul_assoc _ _ _
    _ = M⁻¹ • (base : B) := by
      rw [← map_mul, Units.mul_inv, map_one, mul_one]

def zeroEtaNormalized (M B₀ : ℝ) (sumUnit : Aˣ) : A :=
  M • (↑sumUnit⁻¹ : A) + B₀ • (1 : A)

theorem zeroEtaNormalized_value (j : AlgebraJet2 A B) (sumUnit : Aˣ)
    (base : Bˣ) (M B₀ : ℝ) (hM : M ≠ 0)
    (hvalue : j.value (sumUnit : A) = M • (↑base⁻¹ : B)) :
    j.value (zeroEtaNormalized M B₀ sumUnit) = (base : B) + B₀ • (1 : B) := by
  simp only [zeroEtaNormalized, map_add, map_smul, map_one,
    j.scaled_value_inverse sumUnit base M hM hvalue, smul_smul,
    mul_inv_cancel₀ hM, one_smul]

theorem zeroEtaNormalized_first (j : AlgebraJet2 A B) (sumUnit : Aˣ)
    (M B₀ : ℝ) (hfirst : j.first (sumUnit : A) = 0) :
    j.first (zeroEtaNormalized M B₀ sumUnit) = 0 := by
  simp only [zeroEtaNormalized, map_add, map_smul, j.first_one,
    j.first_inverse, hfirst, mul_zero, zero_mul, smul_zero, add_zero]

theorem zeroEtaNormalized_second (j : AlgebraJet2 A B) (sumUnit : Aˣ)
    (base : Bˣ) (M B₀ : ℝ) (f : B) (hM : M ≠ 0)
    (hvalue : j.value (sumUnit : A) = M • (↑base⁻¹ : B))
    (hfirst : j.first (sumUnit : A) = 0)
    (hsecond : j.second (sumUnit : A) =
      (4 : ℝ) • ((↑base⁻¹ : B) * f * (↑base⁻¹ : B) * f * (↑base⁻¹ : B))) :
    j.second (zeroEtaNormalized M B₀ sumUnit) =
      (-4 / M) • (f * (↑base⁻¹ : B) * f) := by
  have hop : (base : B) *
      ((↑base⁻¹ : B) * f * (↑base⁻¹ : B) * f * (↑base⁻¹ : B)) * (base : B) =
      f * (↑base⁻¹ : B) * f := by simp [mul_assoc]
  calc
    j.second (zeroEtaNormalized M B₀ sumUnit) =
        M • (-(j.value (↑sumUnit⁻¹ : A) *
          ((4 : ℝ) • ((↑base⁻¹ : B) * f * (↑base⁻¹ : B) * f * (↑base⁻¹ : B))) *
            j.value (↑sumUnit⁻¹ : A))) := by
      simp only [zeroEtaNormalized, map_add, map_smul, j.second_one, smul_zero,
        add_zero, j.second_inverse, hfirst, hsecond, mul_zero, zero_mul,
        zero_sub]
    _ = -(M * (M⁻¹ * 4 * M⁻¹)) •
        ((base : B) * ((↑base⁻¹ : B) * f * (↑base⁻¹ : B) * f *
          (↑base⁻¹ : B)) * (base : B)) := by
      rw [j.scaled_value_inverse sumUnit base M hM hvalue]
      simp only [Algebra.smul_mul_assoc, Algebra.mul_smul_comm, smul_smul,
        smul_neg, neg_smul, mul_assoc]
    _ = (-4 / M) • (f * (↑base⁻¹ : B) * f) := by
      rw [hop]
      congr 1
      field_simp

/-- At a vanishing first variation, the second Leibniz rule on powers
has the same trace telescoping as an ordinary first variation. -/
theorem trace_second_power_weighted (tr : CyclicTrace B)
    (j : AlgebraJet2 A B) (L : A) (hfirst : j.first L = 0) (n k : ℕ) :
    tr.toLinearMap (j.value L ^ k * j.second (L ^ (n + 1))) =
      ((n + 1 : ℕ) : ℝ) * tr.toLinearMap (j.value L ^ (k + n) * j.second L) := by
  induction n generalizing k with
  | zero => simp
  | succ n ih =>
    rw [pow_succ, j.second_mul]
    simp only [hfirst, mul_zero, add_zero, map_pow]
    rw [mul_add, map_add]
    have hcycle : tr.toLinearMap (j.value L ^ k *
        (j.second (L ^ (n + 1)) * j.value L)) =
        tr.toLinearMap (j.value L ^ (k + 1) * j.second (L ^ (n + 1))) := by
      calc
        tr.toLinearMap (j.value L ^ k * (j.second (L ^ (n + 1)) * j.value L)) =
            tr.toLinearMap ((j.value L ^ k * j.second (L ^ (n + 1))) * j.value L) :=
          congrArg tr.toLinearMap (mul_assoc _ _ _).symm
        _ = tr.toLinearMap (j.value L * (j.value L ^ k * j.second (L ^ (n + 1)))) :=
          tr.cyclic _ _
        _ = tr.toLinearMap ((j.value L * j.value L ^ k) * j.second (L ^ (n + 1))) :=
          congrArg tr.toLinearMap (mul_assoc _ _ _).symm
        _ = tr.toLinearMap (j.value L ^ (k + 1) * j.second (L ^ (n + 1))) := by
          simp only [pow_succ']
    rw [hcycle, ih (k + 1), ← mul_assoc, ← pow_add]
    have hexp : k + 1 + n = k + (n + 1) := by omega
    rw [hexp]
    push_cast
    ring

theorem trace_second_power (tr : CyclicTrace B) (j : AlgebraJet2 A B)
    (L : A) (hfirst : j.first L = 0) (n : ℕ) (hn : 0 < n) :
    tr.toLinearMap (j.second (L ^ n)) =
      (n : ℝ) * tr.toLinearMap (j.value L ^ (n - 1) * j.second L) := by
  cases n with
  | zero => simp at hn
  | succ k =>
    simpa only [Nat.succ_eq_add_one, Nat.add_sub_cancel, zero_add,
      pow_zero, one_mul] using trace_second_power_weighted tr j L hfirst k 0

/-- The second Taylor coefficient of the normalized trace power. -/
def spectralSecondCoefficient (tr : CyclicTrace B) (j : AlgebraJet2 A B)
    (L : A) (n : ℕ) : ℝ :=
  (n : ℝ)⁻¹ * (1 / 2 : ℝ) * tr.toLinearMap (j.second (L ^ n))

theorem spectralSecondCoefficient_eq (tr : CyclicTrace B) (j : AlgebraJet2 A B)
    (L : A) (hfirst : j.first L = 0) (n : ℕ) (hn : 0 < n) :
    spectralSecondCoefficient tr j L n =
      (1 / 2 : ℝ) * tr.toLinearMap (j.value L ^ (n - 1) * j.second L) := by
  have hcast : (n : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr (Nat.ne_of_gt hn)
  rw [spectralSecondCoefficient, trace_second_power tr j L hfirst n hn]
  field_simp

theorem zeroEtaNormalized_spectral_second (tr : CyclicTrace B)
    (j : AlgebraJet2 A B) (sumUnit : Aˣ) (base : Bˣ) (M B₀ : ℝ)
    (f : B) (hM : M ≠ 0)
    (hvalue : j.value (sumUnit : A) = M • (↑base⁻¹ : B))
    (hfirst : j.first (sumUnit : A) = 0)
    (hsecond : j.second (sumUnit : A) =
      (4 : ℝ) • ((↑base⁻¹ : B) * f * (↑base⁻¹ : B) * f * (↑base⁻¹ : B)))
    (n : ℕ) (hn : 0 < n) :
    spectralSecondCoefficient tr j (zeroEtaNormalized M B₀ sumUnit) n =
      (-2 / M) * tr.toLinearMap
        (((base : B) + B₀ • (1 : B)) ^ (n - 1) * (f * (↑base⁻¹ : B) * f)) := by
  rw [spectralSecondCoefficient_eq tr j (zeroEtaNormalized M B₀ sumUnit)
    (zeroEtaNormalized_first j sumUnit M B₀ hfirst) n hn,
    zeroEtaNormalized_value j sumUnit base M B₀ hM hvalue,
    zeroEtaNormalized_second j sumUnit base M B₀ f hM hvalue hfirst hsecond]
  simp only [Algebra.mul_smul_comm, map_smul, smul_eq_mul]
  ring

/-- Starting data for the two-active-site perturbation. The inputs are
the factor values and their affine variations, together with invertibility
of their resolvent sum. No quadratic coefficient is an input. -/
structure BalancedResolventStart (j : AlgebraJet2 A B) where
  plus : Aˣ
  minus : Aˣ
  background : Aˣ
  sumUnit : Aˣ
  base : Bˣ
  f : B
  others : ℕ
  sum_eq : (sumUnit : A) = balancedInverseSum plus minus background others
  value_plus : j.value (plus : A) = (base : B)
  value_minus : j.value (minus : A) = (base : B)
  value_background : j.value (background : A) = (base : B)
  first_plus : j.first (plus : A) = -f
  first_minus : j.first (minus : A) = f
  first_background : j.first (background : A) = 0
  second_plus : j.second (plus : A) = 0
  second_minus : j.second (minus : A) = 0
  second_background : j.second (background : A) = 0

namespace BalancedResolventStart

variable {j : AlgebraJet2 A B} (s : BalancedResolventStart j)

def latticeLength : ℝ := (s.others : ℝ) + 2

theorem latticeLength_ne_zero : s.latticeLength ≠ 0 := by
  unfold latticeLength
  exact ne_of_gt (add_pos_of_nonneg_of_pos (Nat.cast_nonneg s.others) (by norm_num))

theorem value_sum : j.value (s.sumUnit : A) =
    s.latticeLength • (↑s.base⁻¹ : B) := by
  rw [s.sum_eq]
  exact balancedInverseSum_value j s.plus s.minus s.background s.base s.others
    s.value_plus s.value_minus s.value_background

theorem first_sum : j.first (s.sumUnit : A) = 0 := by
  rw [s.sum_eq]
  exact balancedInverseSum_first j s.plus s.minus s.background s.base s.others s.f
    s.value_plus s.value_minus s.value_background
    s.first_plus s.first_minus s.first_background

theorem second_sum : j.second (s.sumUnit : A) =
    (4 : ℝ) • ((↑s.base⁻¹ : B) * s.f * (↑s.base⁻¹ : B) * s.f *
      (↑s.base⁻¹ : B)) := by
  rw [s.sum_eq]
  exact balancedInverseSum_second j s.plus s.minus s.background s.base s.others s.f
    s.value_plus s.value_minus s.value_background
    s.first_plus s.first_minus s.first_background
    s.second_plus s.second_minus s.second_background

/-- The source factor data yield the actual second variation of L. -/
theorem normalized_second (B₀ : ℝ) :
    j.second (zeroEtaNormalized s.latticeLength B₀ s.sumUnit) =
      (-4 / s.latticeLength) • (s.f * (↑s.base⁻¹ : B) * s.f) :=
  zeroEtaNormalized_second j s.sumUnit s.base s.latticeLength B₀ s.f
    s.latticeLength_ne_zero s.value_sum s.first_sum s.second_sum

/-- The source factor data also yield the quadratic spectral coefficient. -/
theorem spectral_second (tr : CyclicTrace B) (B₀ : ℝ) (n : ℕ) (hn : 0 < n) :
    spectralSecondCoefficient tr j
      (zeroEtaNormalized s.latticeLength B₀ s.sumUnit) n =
      (-2 / s.latticeLength) * tr.toLinearMap
        (((s.base : B) + B₀ • (1 : B)) ^ (n - 1) *
          (s.f * (↑s.base⁻¹ : B) * s.f)) :=
  zeroEtaNormalized_spectral_second tr j s.sumUnit s.base s.latticeLength B₀ s.f
    s.latticeLength_ne_zero s.value_sum s.first_sum s.second_sum n hn

end BalancedResolventStart

section FourierWitness

open scoped ContDiff BigOperators

/-- Connect the derived balanced operator jet to the scalar calculation.
The remaining premise is exactly the normal-form residue multiplication
rule, not a premise specifying the charge's second derivative. The finite
binomial coefficient proving that rule is `quadraticResidueNormalForm_eq`.
An actual PDO implementation must realize this trace identity. -/
theorem BalancedResolventStart.odd_spectral_second_of_normal_form
    {j : AlgebraJet2 A B} (s : BalancedResolventStart j) (tr : CyclicTrace B)
    (period : ℝ) (g : ℝ → ℝ) (hsmooth : ContDiff ℝ ∞ g)
    (hperiodic : Function.Periodic g period) (k : ℕ)
    (hnormal : tr.toLinearMap ((s.base : B) ^ (2 * k) *
      (s.f * (↑s.base⁻¹ : B) * s.f)) =
        ∫ x in (0 : ℝ)..period, g x * iteratedDeriv (2 * k) g x) :
    spectralSecondCoefficient tr j
      (zeroEtaNormalized s.latticeLength 0 s.sumUnit) (2 * k + 1) =
      (2 / s.latticeLength) * (-1 : ℝ) ^ (k + 1) *
        ∫ x in (0 : ℝ)..period, (iteratedDeriv k g x) ^ 2 := by
  rw [s.spectral_second tr 0 (2 * k + 1) (by omega)]
  simp only [zero_smul, add_zero, Nat.add_sub_cancel]
  rw [hnormal, integral_periodic_even_derivative period g hsmooth hperiodic k,
    pow_succ]
  ring

def periodicFourierFrequency (period : ℝ) (mode : ℕ) : ℝ :=
  (mode : ℝ) * (2 * Real.pi) / period

def periodicCosine (period : ℝ) (mode : ℕ) (x : ℝ) : ℝ :=
  Real.cos (periodicFourierFrequency period mode * x)

theorem periodicFourierFrequency_mul_period (period : ℝ) (hperiod : period ≠ 0)
    (mode : ℕ) :
    periodicFourierFrequency period mode * period = (mode : ℝ) * (2 * Real.pi) := by
  unfold periodicFourierFrequency
  exact div_mul_cancel₀ _ hperiod

theorem periodicFourierFrequency_pos (period : ℝ) (hperiod : 0 < period)
    (mode : ℕ) (hmode : 0 < mode) : 0 < periodicFourierFrequency period mode := by
  exact div_pos (mul_pos (Nat.cast_pos.mpr hmode)
    (mul_pos (by norm_num) Real.pi_pos)) hperiod

theorem periodicFourierFrequency_injective (period : ℝ) (hperiod : period ≠ 0) :
    Function.Injective (periodicFourierFrequency period) := by
  intro m n h
  apply Nat.cast_injective (R := ℝ)
  have hpi : (2 * Real.pi : ℝ) ≠ 0 := ne_of_gt (mul_pos (by norm_num) Real.pi_pos)
  exact mul_right_cancel₀ hpi ((div_left_inj' hperiod).mp h)

theorem periodicCosine_smooth (period : ℝ) (mode : ℕ) :
    ContDiff ℝ ∞ (periodicCosine period mode) :=
  Real.contDiff_cos.comp (contDiff_const.mul contDiff_id)

theorem periodicCosine_periodic (period : ℝ) (hperiod : period ≠ 0) (mode : ℕ) :
    Function.Periodic (periodicCosine period mode) period := by
  intro x
  simp only [periodicCosine, mul_add, periodicFourierFrequency_mul_period period hperiod,
    Real.cos_add_nat_mul_two_pi]

theorem integral_periodicCosine_zero (period : ℝ) (hperiod : 0 < period)
    (mode : ℕ) (hmode : 0 < mode) :
    (∫ x in (0 : ℝ)..period, periodicCosine period mode x) = 0 := by
  have hfreq := ne_of_gt (periodicFourierFrequency_pos period hperiod mode hmode)
  change (∫ x in (0 : ℝ)..period,
    Real.cos (periodicFourierFrequency period mode * x)) = 0
  rw [intervalIntegral.integral_comp_mul_left Real.cos hfreq]
  simp only [mul_zero, integral_cos,
    periodicFourierFrequency_mul_period period (ne_of_gt hperiod), Real.sin_zero,
    sub_zero, smul_eq_mul]
  have hsin : Real.sin ((mode : ℝ) * (2 * Real.pi)) = 0 :=
    (Real.sin_periodic.nat_mul_eq mode).trans Real.sin_zero
  rw [hsin, mul_zero]

theorem integral_periodicCosine_sq (period : ℝ) (hperiod : 0 < period)
    (mode : ℕ) (hmode : 0 < mode) :
    (∫ x in (0 : ℝ)..period, periodicCosine period mode x ^ 2) = period / 2 := by
  have hfreq := ne_of_gt (periodicFourierFrequency_pos period hperiod mode hmode)
  change (∫ x in (0 : ℝ)..period,
    (fun y => Real.cos y ^ 2) (periodicFourierFrequency period mode * x)) = _
  rw [intervalIntegral.integral_comp_mul_left (fun y => Real.cos y ^ 2) hfreq]
  simp only [mul_zero, integral_cos_sq, Real.cos_zero, Real.sin_zero,
    mul_zero, sub_zero, smul_eq_mul]
  have hsin : Real.sin (periodicFourierFrequency period mode * period) = 0 := by
    rw [periodicFourierFrequency_mul_period period (ne_of_gt hperiod)]
    exact (Real.sin_periodic.nat_mul_eq mode).trans Real.sin_zero
  rw [hsin]
  simp only [mul_zero, zero_add]
  field_simp

theorem integral_cosine_zero_of_endpoint (period frequency : ℝ)
    (hfrequency : frequency ≠ 0) (hendpoint : Real.sin (frequency * period) = 0) :
    (∫ x in (0 : ℝ)..period, Real.cos (frequency * x)) = 0 := by
  rw [intervalIntegral.integral_comp_mul_left Real.cos hfrequency]
  simp [integral_cos, hendpoint]

/-- Orthogonality on the genuine interval of length period. -/
theorem integral_periodicCosine_mul (period : ℝ) (hperiod : 0 < period)
    (m n : ℕ) (hm : 0 < m) (hn : 0 < n) :
    (∫ x in (0 : ℝ)..period, periodicCosine period m x * periodicCosine period n x) =
      if m = n then period / 2 else 0 := by
  by_cases hmn : m = n
  · subst n
    simpa [pow_two] using integral_periodicCosine_sq period hperiod m hm
  · simp only [hmn, ite_false]
    let km := periodicFourierFrequency period m
    let kn := periodicFourierFrequency period n
    have hkm : 0 < km := periodicFourierFrequency_pos period hperiod m hm
    have hkn : 0 < kn := periodicFourierFrequency_pos period hperiod n hn
    have hdiff : km - kn ≠ 0 := by
      intro hz
      exact hmn (periodicFourierFrequency_injective period (ne_of_gt hperiod)
        (sub_eq_zero.mp hz))
    have hsin (mode : ℕ) :
        Real.sin (periodicFourierFrequency period mode * period) = 0 := by
      rw [periodicFourierFrequency_mul_period period (ne_of_gt hperiod)]
      exact (Real.sin_periodic.nat_mul_eq mode).trans Real.sin_zero
    have hplusendpoint : Real.sin ((km + kn) * period) = 0 := by
      simp only [add_mul, Real.sin_add, hsin m, hsin n, zero_mul, mul_zero, add_zero,
        km, kn]
    have hminusendpoint : Real.sin ((km - kn) * period) = 0 := by
      simp only [sub_mul, Real.sin_sub, hsin m, hsin n, zero_mul, mul_zero, sub_zero,
        km, kn]
    have hproduct : (fun x => periodicCosine period m x * periodicCosine period n x) =
        fun x => (1 / 2 : ℝ) *
          (Real.cos ((km + kn) * x) + Real.cos ((km - kn) * x)) := by
      funext x
      simp only [add_mul, sub_mul, Real.cos_add, Real.cos_sub, periodicCosine, km, kn]
      ring
    rw [hproduct, intervalIntegral.integral_const_mul,
      intervalIntegral.integral_add]
    · rw [integral_cosine_zero_of_endpoint period (km + kn) (ne_of_gt (add_pos hkm hkn))
        hplusendpoint,
        integral_cosine_zero_of_endpoint period (km - kn) hdiff hminusendpoint]
      ring
    · exact (Real.continuous_cos.comp (continuous_const.mul continuous_id)).intervalIntegrable
        0 period
    · exact (Real.continuous_cos.comp (continuous_const.mul continuous_id)).intervalIntegrable
        0 period

theorem periodicCosine_even_derivative (period : ℝ) (mode k : ℕ) (x : ℝ) :
    iteratedDeriv (2 * k) (periodicCosine period mode) x =
      (-1 : ℝ) ^ k * periodicFourierFrequency period mode ^ (2 * k) *
        periodicCosine period mode x := by
  have h := congrFun (iteratedDeriv_comp_const_mul
    (n := 2 * k) Real.contDiff_cos (periodicFourierFrequency period mode)) x
  simp only [Real.iteratedDeriv_even_cos, Pi.mul_apply, Pi.pow_apply, Pi.neg_apply,
    Pi.one_apply] at h
  change iteratedDeriv (2 * k) (fun y => Real.cos
    (periodicFourierFrequency period mode * y)) x = _
  simpa only [periodicCosine, mul_assoc, mul_comm, mul_left_comm] using h

/-- Exact nonzero-mode derivative energy, using actual periodic integration
by parts rather than a formal assignment of a Fourier symbol. -/
theorem integral_periodicCosine_derivative_sq (period : ℝ) (hperiod : 0 < period)
    (mode : ℕ) (hmode : 0 < mode) (k : ℕ) :
    (∫ x in (0 : ℝ)..period,
      (iteratedDeriv k (periodicCosine period mode) x) ^ 2) =
      periodicFourierFrequency period mode ^ (2 * k) * (period / 2) := by
  have hibp := integral_periodic_even_derivative period (periodicCosine period mode)
    (periodicCosine_smooth period mode)
    (periodicCosine_periodic period (ne_of_gt hperiod) mode) k
  have heigen : (fun x => periodicCosine period mode x *
      iteratedDeriv (2 * k) (periodicCosine period mode) x) =
      fun x => ((-1 : ℝ) ^ k * periodicFourierFrequency period mode ^ (2 * k)) *
        (periodicCosine period mode x) ^ 2 := by
    funext x
    rw [periodicCosine_even_derivative]
    ring
  rw [heigen, intervalIntegral.integral_const_mul,
    integral_periodicCosine_sq period hperiod mode hmode] at hibp
  apply mul_left_cancel₀ (pow_ne_zero k (by norm_num : (-1 : ℝ) ≠ 0))
  simpa only [mul_assoc] using hibp.symm

theorem integral_topQuadraticDensity_cosine (period : ℝ) (hperiod : 0 < period)
    (M mode k : ℕ) (hmode : 0 < mode) :
    (∫ x in (0 : ℝ)..period, topQuadraticDensity M k (periodicCosine period mode) x) =
      (period / (M : ℝ)) * (-1 : ℝ) ^ (k + 1) *
        (periodicFourierFrequency period mode ^ 2) ^ k := by
  rw [integral_topQuadraticDensity period M k (periodicCosine period mode)
    (periodicCosine_smooth period mode)
    (periodicCosine_periodic period (ne_of_gt hperiod) mode),
    integral_periodicCosine_derivative_sq period hperiod mode hmode]
  rw [pow_mul]
  ring

def periodicCosineSum {N : ℕ} (period : ℝ) (mode : Fin N → ℕ)
    (amplitude : Fin N → ℝ) (x : ℝ) : ℝ :=
  ∑ i, amplitude i * periodicCosine period (mode i) x

theorem periodicCosineSum_smooth {N : ℕ} (period : ℝ) (mode : Fin N → ℕ)
    (amplitude : Fin N → ℝ) : ContDiff ℝ ∞ (periodicCosineSum period mode amplitude) := by
  apply ContDiff.sum
  intro i _
  exact contDiff_const.mul (periodicCosine_smooth period (mode i))

theorem periodicCosineSum_periodic {N : ℕ} (period : ℝ) (hperiod : period ≠ 0)
    (mode : Fin N → ℕ) (amplitude : Fin N → ℝ) :
    Function.Periodic (periodicCosineSum period mode amplitude) period := by
  intro x
  apply Finset.sum_congr rfl
  intro i _
  rw [periodicCosine_periodic period hperiod (mode i) x]

theorem integral_periodicCosineSum_zero {N : ℕ} (period : ℝ) (hperiod : 0 < period)
    (mode : Fin N → ℕ) (hmode : ∀ i, 0 < mode i) (amplitude : Fin N → ℝ) :
    (∫ x in (0 : ℝ)..period, periodicCosineSum period mode amplitude x) = 0 := by
  unfold periodicCosineSum
  rw [intervalIntegral.integral_finsetSum]
  · simp_rw [intervalIntegral.integral_const_mul]
    apply Finset.sum_eq_zero
    intro i _
    rw [integral_periodicCosine_zero period hperiod (mode i) (hmode i), mul_zero]
  · intro i _
    exact (continuous_const.mul (periodicCosine_smooth period (mode i)).continuous).intervalIntegrable
      0 period

/-- Actual finite Fourier orthogonality with arbitrary amplitude vectors. -/
theorem integral_periodicCosineSum_pair {N : ℕ} (period : ℝ) (hperiod : 0 < period)
    (mode : Fin N → ℕ) (hmode : ∀ i, 0 < mode i) (hinjective : Function.Injective mode)
    (a b : Fin N → ℝ) :
    (∫ x in (0 : ℝ)..period,
      periodicCosineSum period mode a x * periodicCosineSum period mode b x) =
      (period / 2) * ∑ i, a i * b i := by
  have hexpand : (fun x => periodicCosineSum period mode a x *
      periodicCosineSum period mode b x) =
      fun x => ∑ i, ∑ j, (a i * b j) *
        (periodicCosine period (mode i) x * periodicCosine period (mode j) x) := by
    funext x
    simp only [periodicCosineSum, Finset.sum_mul, Finset.mul_sum]
    rw [Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro i _
    apply Finset.sum_congr rfl
    intro j _
    ring
  have hinter i j : IntervalIntegrable
      (fun x => (a i * b j) *
        (periodicCosine period (mode i) x * periodicCosine period (mode j) x))
      MeasureTheory.volume 0 period :=
    (continuous_const.mul ((periodicCosine_smooth period (mode i)).continuous.mul
      (periodicCosine_smooth period (mode j)).continuous)).intervalIntegrable 0 period
  have hsingle (i j : Fin N) :
      (∫ x in (0 : ℝ)..period, (a i * b j) *
        (periodicCosine period (mode i) x * periodicCosine period (mode j) x)) =
        if i = j then (a i * b j) * (period / 2) else 0 := by
    rw [intervalIntegral.integral_const_mul,
      integral_periodicCosine_mul period hperiod (mode i) (mode j) (hmode i) (hmode j)]
    simp only [hinjective.eq_iff]
    split_ifs <;> simp
  have hinterOuter (i : Fin N) : IntervalIntegrable
      (fun x => ∑ j, (a i * b j) *
        (periodicCosine period (mode i) x * periodicCosine period (mode j) x))
      MeasureTheory.volume 0 period := by
    have hc : ContDiff ℝ ∞ (fun x => ∑ j, (a i * b j) *
        (periodicCosine period (mode i) x * periodicCosine period (mode j) x)) := by
      apply ContDiff.sum
      intro j _
      exact contDiff_const.mul ((periodicCosine_smooth period (mode i)).mul
        (periodicCosine_smooth period (mode j)))
    exact hc.continuous.intervalIntegrable 0 period
  rw [hexpand, intervalIntegral.integral_finsetSum (fun i _ => hinterOuter i)]
  simp_rw [intervalIntegral.integral_finsetSum (fun j _ => hinter _ j), hsingle]
  simp [Finset.mul_sum, mul_comm, mul_assoc]

theorem periodicCosineSum_even_derivative {N : ℕ} (period : ℝ)
    (mode : Fin N → ℕ) (amplitude : Fin N → ℝ) (k : ℕ) :
    iteratedDeriv (2 * k) (periodicCosineSum period mode amplitude) =
      periodicCosineSum period mode (fun i =>
        amplitude i * (-1 : ℝ) ^ k * periodicFourierFrequency period (mode i) ^ (2 * k)) := by
  funext x
  change iteratedDeriv (2 * k) (fun y =>
    ∑ i, amplitude i * periodicCosine period (mode i) y) x =
      ∑ i, amplitude i * (-1 : ℝ) ^ k *
        periodicFourierFrequency period (mode i) ^ (2 * k) * periodicCosine period (mode i) x
  rw [iteratedDeriv_fun_sum]
  · apply Finset.sum_congr rfl
    intro i _
    rw [iteratedDeriv_const_mul_field, periodicCosine_even_derivative]
    ring
  · intro i _
    exact (contDiff_const.mul
      ((contDiff_infty.mp (periodicCosine_smooth period (mode i))) (2 * k))).contDiffAt

/-- The all-order quadratic candidate on a real, mean-zero finite Fourier
slice, with its lattice and interval normalization computed explicitly. -/
theorem integral_topQuadraticDensity_cosineSum {N : ℕ} (period : ℝ) (hperiod : 0 < period)
    (M k : ℕ) (mode : Fin N → ℕ) (hmode : ∀ i, 0 < mode i)
    (hinjective : Function.Injective mode) (amplitude : Fin N → ℝ) :
    (∫ x in (0 : ℝ)..period,
      topQuadraticDensity M k (periodicCosineSum period mode amplitude) x) =
      (period / (M : ℝ)) * (-1 : ℝ) ^ (k + 1) *
        ∑ i, (amplitude i) ^ 2 * (periodicFourierFrequency period (mode i) ^ 2) ^ k := by
  have hdensity : (fun x => topQuadraticDensity M k
      (periodicCosineSum period mode amplitude) x) =
      fun x => -(2 / (M : ℝ)) * (periodicCosineSum period mode amplitude x *
        iteratedDeriv (2 * k) (periodicCosineSum period mode amplitude) x) := by
    funext x
    simp only [topQuadraticDensity, quadraticResidueNormalForm_eq, iteratedDeriv_zero]
    ring
  rw [hdensity, intervalIntegral.integral_const_mul, periodicCosineSum_even_derivative,
    integral_periodicCosineSum_pair period hperiod mode hmode hinjective]
  simp_rw [pow_mul]
  rw [pow_succ]
  simp_rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro i _
  ring

/-- The actual quadratic Fourier functional in amplitude coordinates. -/
def fourierQuadraticFunctional {N : ℕ} (nodes : Fin N → ℝ)
    (p : Polynomial ℝ) (amplitude : Fin N → ℝ) : ℝ :=
  ∑ j, amplitude j ^ 2 * p.eval (nodes j)

/-- Differentiate the finite quadratic functional on the literal j-th
amplitude line. This supplies the column factors used in the minor. -/
theorem fourierQuadraticFunctional_amplitude_derivative {N : ℕ}
    (nodes : Fin N → ℝ) (p : Polynomial ℝ) (amplitude : Fin N → ℝ) (j : Fin N) :
    HasDerivAt (fun t : ℝ => fourierQuadraticFunctional nodes p
      (fun q => amplitude q + t * (if q = j then 1 else 0)))
      (2 * amplitude j * p.eval (nodes j)) 0 := by
  have hcoord (q : Fin N) : HasDerivAt
      (fun t : ℝ => amplitude q + t * (if q = j then 1 else 0))
      (if q = j then 1 else 0) 0 := by
    simpa using ((hasDerivAt_id (0 : ℝ)).mul_const
      (if q = j then (1 : ℝ) else 0)).const_add (amplitude q)
  have hterm (q : Fin N) := ((hcoord q).pow 2).mul_const (p.eval (nodes q))
  have hsum := HasDerivAt.fun_sum (u := (Finset.univ : Finset (Fin N)))
    (fun q _ => hterm q)
  simpa [fourierQuadraticFunctional] using hsum

def fourierQuadraticJacobian {N : ℕ} (nodes : Fin N → ℝ)
    (polynomials : Fin N → Polynomial ℝ) (amplitude : Fin N → ℝ) :
    Matrix (Fin N) (Fin N) ℝ :=
  fun i j => 2 * amplitude j * (polynomials i).eval (nodes j)

theorem fourierQuadraticJacobian_det {N : ℕ} (nodes : Fin N → ℝ)
    (polynomials : Fin N → Polynomial ℝ) (amplitude : Fin N → ℝ) :
    (fourierQuadraticJacobian nodes polynomials amplitude).det =
      (∏ j, 2 * amplitude j) * (polynomialFrequencyMatrix nodes polynomials).det := by
  exact Matrix.det_mul_row (fun j => 2 * amplitude j)
    (polynomialFrequencyMatrix nodes polynomials)

/-- Exact amplitude factors of the quadratic Jacobian at epsilon*a.
This is the leading nonlinear-minor coefficient once higher field orders
are restored; it is not asserted to be the entire physical Jacobian. -/
theorem fourierQuadraticJacobian_amplitude_scale {N : ℕ} (nodes : Fin N → ℝ)
    (polynomials : Fin N → Polynomial ℝ) (amplitude : Fin N → ℝ) (epsilon : ℝ) :
    (fourierQuadraticJacobian nodes polynomials (fun j => epsilon * amplitude j)).det =
      epsilon ^ N * (∏ j, 2 * amplitude j) *
        (polynomialFrequencyMatrix nodes polynomials).det := by
  rw [fourierQuadraticJacobian_det]
  have hfactor : (∏ j, 2 * (epsilon * amplitude j)) =
      epsilon ^ N * ∏ j, 2 * amplitude j := by
    simp_rw [show ∀ j : Fin N, 2 * (epsilon * amplitude j) =
      epsilon * (2 * amplitude j) from fun j => by ring]
    rw [Finset.prod_mul_distrib]
    simp
  rw [hfactor]

theorem fourierQuadraticJacobian_det_ne_zero {N : ℕ} (nodes : Fin N → ℝ)
    (polynomials : Fin N → Polynomial ℝ) (amplitude : Fin N → ℝ)
    (hnodes : Function.Injective nodes)
    (hdegree : ∀ i, (polynomials i).natDegree ≤ (i : ℕ))
    (hlead : ∀ i, (polynomials i).coeff (i : ℕ) ≠ 0)
    (hamplitude : ∀ j, amplitude j ≠ 0) :
    (fourierQuadraticJacobian nodes polynomials amplitude).det ≠ 0 := by
  rw [fourierQuadraticJacobian_det]
  exact mul_ne_zero (Finset.prod_ne_zero_iff.mpr
    (fun j _ => mul_ne_zero (by norm_num) (hamplitude j)))
    (polynomialFrequencyMatrix_det_ne_zero nodes polynomials hnodes hdegree hlead)

def topFourierPolynomial (period : ℝ) (M k : ℕ) : Polynomial ℝ :=
  Polynomial.C ((period / (M : ℝ)) * (-1 : ℝ) ^ (k + 1)) * Polynomial.X ^ k

theorem topFourierPolynomial_degree (period : ℝ) (M k : ℕ) :
    (topFourierPolynomial period M k).natDegree ≤ k := by
  unfold topFourierPolynomial
  calc
    _ ≤ (Polynomial.C ((period / (M : ℝ)) * (-1 : ℝ) ^ (k + 1))).natDegree +
        (Polynomial.X ^ k : Polynomial ℝ).natDegree := Polynomial.natDegree_mul_le
    _ = k := by simp only [Polynomial.natDegree_C, Polynomial.natDegree_X_pow, zero_add]

theorem topFourierPolynomial_coefficient (period : ℝ) (M k : ℕ) :
    (topFourierPolynomial period M k).coeff k =
      (period / (M : ℝ)) * (-1 : ℝ) ^ (k + 1) := by
  simp only [topFourierPolynomial, Polynomial.coeff_C_mul, Polynomial.coeff_X_pow,
    ite_true, mul_one]

theorem topFourierPolynomial_coefficient_ne_zero (period : ℝ) (hperiod : 0 < period)
    (M : ℕ) (hM : 0 < M) (k : ℕ) :
    (topFourierPolynomial period M k).coeff k ≠ 0 := by
  rw [topFourierPolynomial_coefficient]
  exact mul_ne_zero (div_ne_zero (ne_of_gt hperiod) (Nat.cast_ne_zero.mpr (Nat.ne_of_gt hM)))
    (pow_ne_zero _ (by norm_num))

theorem integral_topQuadraticDensity_cosineSum_eq_polynomial {N : ℕ}
    (period : ℝ) (hperiod : 0 < period) (M k : ℕ) (mode : Fin N → ℕ)
    (hmode : ∀ i, 0 < mode i) (hinjective : Function.Injective mode)
    (amplitude : Fin N → ℝ) :
    (∫ x in (0 : ℝ)..period,
      topQuadraticDensity M k (periodicCosineSum period mode amplitude) x) =
      fourierQuadraticFunctional
        (fun i => periodicFourierFrequency period (mode i) ^ 2)
        (topFourierPolynomial period M k) amplitude := by
  rw [integral_topQuadraticDensity_cosineSum period hperiod M k mode hmode hinjective]
  simp only [fourierQuadraticFunctional, topFourierPolynomial,
    Polynomial.eval_mul, Polynomial.eval_C, Polynomial.eval_pow, Polynomial.eval_X]
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro i _
  ring

/-- Arbitrarily long actual Fourier witnesses for the computed highest
quadratic densities. The identification with the full physical charge
minor remains separate. -/
theorem topFourierJacobian_det_ne_zero {N : ℕ} (period : ℝ) (hperiod : 0 < period)
    (M : ℕ) (hM : 0 < M) (mode : Fin N → ℕ) (hmode : ∀ i, 0 < mode i)
    (hinjective : Function.Injective mode) (amplitude : Fin N → ℝ)
    (hamplitude : ∀ i, amplitude i ≠ 0) :
    (fourierQuadraticJacobian
      (fun i => periodicFourierFrequency period (mode i) ^ 2)
      (fun k => topFourierPolynomial period M (k : ℕ)) amplitude).det ≠ 0 := by
  apply fourierQuadraticJacobian_det_ne_zero _ _ amplitude _ _ _ hamplitude
  · exact positive_frequency_squares_injective
      (fun i => periodicFourierFrequency period (mode i))
      (fun i => periodicFourierFrequency_pos period hperiod (mode i) (hmode i))
      ((periodicFourierFrequency_injective period (ne_of_gt hperiod)).comp hinjective)
  · intro k
    exact topFourierPolynomial_degree period M (k : ℕ)
  · intro k
    exact topFourierPolynomial_coefficient_ne_zero period hperiod M hM (k : ℕ)

def canonicalFourierMode {N : ℕ} (i : Fin N) : ℕ := (i : ℕ) + 1

theorem canonicalFourierMode_pos {N : ℕ} (i : Fin N) : 0 < canonicalFourierMode i :=
  Nat.succ_pos _

theorem canonicalFourierMode_injective {N : ℕ} :
    Function.Injective (@canonicalFourierMode N) := by
  intro i j h
  exact Fin.val_injective (Nat.succ.inj h)

theorem canonical_topFourierJacobian_det_ne_zero (N : ℕ)
    (period : ℝ) (hperiod : 0 < period) (M : ℕ) (hM : 0 < M) :
    (fourierQuadraticJacobian
      (fun i : Fin N => periodicFourierFrequency period (canonicalFourierMode i) ^ 2)
      (fun k => topFourierPolynomial period M (k : ℕ)) (fun _ => 1)).det ≠ 0 :=
  topFourierJacobian_det_ne_zero period hperiod M hM canonicalFourierMode
    canonicalFourierMode_pos canonicalFourierMode_injective (fun _ => 1) (by norm_num)

end FourierWitness

#print axioms AlgebraJet2.second_inverse
#print axioms balancedInverseSum_second
#print axioms zeroEtaNormalized_second
#print axioms zeroEtaNormalized_spectral_second
#print axioms BalancedResolventStart.spectral_second
#print axioms BalancedResolventStart.odd_spectral_second_of_normal_form
#print axioms integral_periodicCosine_derivative_sq
#print axioms integral_topQuadraticDensity_cosine
#print axioms integral_periodicCosineSum_pair
#print axioms integral_topQuadraticDensity_cosineSum
#print axioms fourierQuadraticFunctional_amplitude_derivative
#print axioms fourierQuadraticJacobian_amplitude_scale
#print axioms topFourierJacobian_det_ne_zero
#print axioms canonical_topFourierJacobian_det_ne_zero

end
end DLWLean
