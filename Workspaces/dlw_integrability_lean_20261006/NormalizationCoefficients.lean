import HeatIntertwiner
import Mathlib.RingTheory.Binomial
import Mathlib.Tactic.FieldSimp

/-!
The exact left-normal pseudo-differential product through D^-3.
The one-site coefficients include g_x and g_xx; omitting them would not
represent (D-b)^-1(D-alpha). All recurrences below are derived identities.
-/

namespace DLWLean

noncomputable section
open scoped BigOperators

variable {R : Type*} [CommRing R] [Algebra ℝ R]

/-- Coefficients of 1+a1 D^-1+a2 D^-2+a3 D^-3 modulo order <= -4. -/
@[ext] structure PDO3 (R : Type*) where
  first : R
  second : R
  third : R

namespace PDO3

def one : PDO3 R := ⟨0, 0, 0⟩

/-- The only nonzero derivative correction at this truncation is
binom(-1,1)*a1*D(b1)=-a1*D(b1). -/
def mul (d : AlgebraEvolution R) (a b : PDO3 R) : PDO3 R :=
  ⟨a.first + b.first,
   a.second + b.second + a.first * b.first,
   a.third + b.third + a.first * b.second + a.second * b.first -
     a.first * d.toLinearMap b.first⟩

theorem binomial_derivative_correction (a b : R) :
    (((Ring.choose (-1 : ℤ) 1 : ℤ) : R) * a * b) = -a * b := by
  simp [Ring.choose_one_right]

theorem one_mul (d : AlgebraEvolution R) (a : PDO3 R) : mul d one a = a := by
  ext <;> simp [mul, one]

theorem mul_one (d : AlgebraEvolution R) (a : PDO3 R) : mul d a one = a := by
  ext <;> simp [mul, one]

/-- Associativity uses the spatial derivation Leibniz rule and proves that
these are actual truncated differential-operator multiplication laws. -/
theorem mul_assoc (d : AlgebraEvolution R) (a b c : PDO3 R) :
    mul d (mul d a b) c = mul d a (mul d b c) := by
  ext <;> simp only [mul, map_add, d.leibniz] <;> ring

end PDO3

def transferBeta (U g : R) : R := halfCoefficient * (U - g)

theorem two_mul_transferBeta (U g : R) : 2 * transferBeta U g = U - g := by
  unfold transferBeta
  rw [← mul_assoc, two_mul_halfCoefficient, one_mul]

/-- Exact coefficients from s1=-g, s_(k+1)=b*s_k-D(s_k). -/
def transferCoefficients3 (d : AlgebraEvolution R) (U g : R) : PDO3 R :=
  let b := transferBeta U g
  ⟨-g, d.toLinearMap g - b * g,
    -d.toLinearMap (d.toLinearMap g) + 2 * b * d.toLinearMap g +
      (d.toLinearMap b - b ^ 2) * g⟩

theorem transfer_first_coefficient (d : AlgebraEvolution R) (U g : R) :
    (transferCoefficients3 d U g).first = -g := rfl

/-- These are precisely the D^-1 and D^-2 coefficients of
(D-b)T=(D-alpha), establishing the inverse-factor recurrence. -/
theorem transfer_second_coefficient_equation (d : AlgebraEvolution R) (U g : R) :
    d.toLinearMap (transferCoefficients3 d U g).first +
      (transferCoefficients3 d U g).second -
        transferBeta U g * (transferCoefficients3 d U g).first = 0 := by
  simp only [transferCoefficients3, map_neg]
  ring

theorem transfer_third_coefficient_equation (d : AlgebraEvolution R) (U g : R) :
    d.toLinearMap (transferCoefficients3 d U g).second +
      (transferCoefficients3 d U g).third -
        transferBeta U g * (transferCoefficients3 d U g).second = 0 := by
  simp only [transferCoefficients3, map_sub, d.leibniz]
  ring

/-- Ordered product S_(n-1)...S_0 with genuine PDO3 multiplication. -/
def monodromyCoefficients3 (d : AlgebraEvolution R) (U g : ℕ → R) : ℕ → PDO3 R
  | 0 => PDO3.one
  | n + 1 => PDO3.mul d (transferCoefficients3 d (U n) (g n))
      (monodromyCoefficients3 d U g n)

theorem monodromy_first_recurrence (d : AlgebraEvolution R)
    (U g : ℕ → R) (n : ℕ) :
    (monodromyCoefficients3 d U g (n + 1)).first =
      -g n + (monodromyCoefficients3 d U g n).first := rfl

theorem monodromy_second_recurrence (d : AlgebraEvolution R)
    (U g : ℕ → R) (n : ℕ) :
    (monodromyCoefficients3 d U g (n + 1)).second =
      d.toLinearMap (g n) - transferBeta (U n) (g n) * g n +
        (monodromyCoefficients3 d U g n).second -
        g n * (monodromyCoefficients3 d U g n).first := by
  simp only [monodromyCoefficients3, PDO3.mul, transferCoefficients3]
  ring

theorem monodromy_third_recurrence (d : AlgebraEvolution R)
    (U g : ℕ → R) (n : ℕ) :
    (monodromyCoefficients3 d U g (n + 1)).third =
      (transferCoefficients3 d (U n) (g n)).third +
        (monodromyCoefficients3 d U g n).third -
        g n * (monodromyCoefficients3 d U g n).second +
        (d.toLinearMap (g n) - transferBeta (U n) (g n) * g n) *
          (monodromyCoefficients3 d U g n).first +
        g n * d.toLinearMap (monodromyCoefficients3 d U g n).first := by
  simp only [monodromyCoefficients3, PDO3.mul, transferCoefficients3]
  ring

theorem monodromy_first_coefficient_sum (d : AlgebraEvolution R)
    (U g : ℕ → R) (n : ℕ) :
    (monodromyCoefficients3 d U g n).first = -∑ j ∈ Finset.range n, g j := by
  induction n with
  | zero => simp [monodromyCoefficients3, PDO3.one]
  | succ n ih =>
    rw [monodromy_first_recurrence, ih, Finset.sum_range_succ]
    ring

/-- The exact second coefficient before imposing fixed mean closure. -/
theorem monodromy_second_coefficient_twice (d : AlgebraEvolution R)
    (U g : ℕ → R) (n : ℕ) :
    2 * (monodromyCoefficients3 d U g n).second =
      (∑ j ∈ Finset.range n, g j) ^ 2 -
        (∑ j ∈ Finset.range n, U j * g j) +
        2 * (∑ j ∈ Finset.range n, d.toLinearMap (g j)) := by
  induction n with
  | zero => simp [monodromyCoefficients3, PDO3.one]
  | succ n ih =>
    rw [monodromy_second_recurrence, monodromy_first_coefficient_sum]
    calc
      _ = 2 * (monodromyCoefficients3 d U g n).second +
          2 * (d.toLinearMap (g n) - transferBeta (U n) (g n) * g n) +
          2 * g n * (∑ j ∈ Finset.range n, g j) := by ring
      _ = (∑ j ∈ Finset.range n, g j) ^ 2 -
          (∑ j ∈ Finset.range n, U j * g j) +
          2 * (∑ j ∈ Finset.range n, d.toLinearMap (g j)) +
          (2 * d.toLinearMap (g n) - (U n - g n) * g n) +
          2 * g n * (∑ j ∈ Finset.range n, g j) := by
        rw [ih]
        congr 2
        rw [mul_sub, ← mul_assoc, two_mul_transferBeta]
      _ = _ := by simp only [Finset.sum_range_succ]; ring

theorem monodromy_second_coefficient_fixed_mean (d : AlgebraEvolution R)
    (U g : ℕ → R) (n : ℕ)
    (hmean : d.toLinearMap (∑ j ∈ Finset.range n, g j) = 0) :
    (monodromyCoefficients3 d U g n).second = halfCoefficient *
      ((∑ j ∈ Finset.range n, g j) ^ 2 -
        (∑ j ∈ Finset.range n, U j * g j)) := by
  have hs : (∑ j ∈ Finset.range n, d.toLinearMap (g j)) = 0 := by
    simpa only [map_sum] using hmean
  have h2 := monodromy_second_coefficient_twice d U g n
  rw [hs, mul_zero, add_zero] at h2
  have hhalf : (halfCoefficient : R) * 2 = 1 :=
    (mul_comm _ _).trans two_mul_halfCoefficient
  have hh := congrArg (fun r : R => halfCoefficient * r) h2
  simpa only [← mul_assoc, hhalf, one_mul] using hh

/-- Low-order inverse coefficients for F=a D^-1+b D^-2+c D^-3,
when a and b are spatial constants. -/
def inverseLeading (a : ℝ) : ℝ := a⁻¹
def inverseConstant (a b : ℝ) : ℝ := -b / a ^ 2
def inverseResidue (a b c : ℝ) : ℝ := b ^ 2 / a ^ 3 - c / a ^ 2

theorem inverse_coefficient_equations (a b c : ℝ) (ha : a ≠ 0) :
    a * inverseLeading a = 1 ∧
    a * inverseConstant a b + b * inverseLeading a = 0 ∧
    a * inverseResidue a b c + b * inverseConstant a b +
      c * inverseLeading a = 0 := by
  unfold inverseLeading inverseConstant inverseResidue
  constructor
  · exact mul_inv_cancel₀ ha
  · constructor <;> field_simp <;> ring

/-- Extracting L=a F^-1+b/a produces the leading coefficient one,
zero constant term, and the claimed exact first residue. -/
theorem normalized_first_residue (a b c : ℝ) (ha : a ≠ 0) :
    a * inverseLeading a = 1 ∧
    a * inverseConstant a b + b / a = 0 ∧
    a * inverseResidue a b c = b ^ 2 / a ^ 2 - c / a := by
  unfold inverseLeading inverseConstant inverseResidue
  constructor
  · exact mul_inv_cancel₀ ha
  · constructor <;> field_simp <;> ring

#print axioms PDO3.mul_assoc
#print axioms transfer_third_coefficient_equation
#print axioms monodromy_second_coefficient_fixed_mean
#print axioms normalized_first_residue

end
end DLWLean
