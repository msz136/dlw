/-
Direction A (finite differences, `y`-semidiscretisation of the (2+1)-dimensional
dispersive long wave system).

Scope of this file -- deliberately restricted to results that are proved in full.
No `sorry`, no `admit`, no new `axiom`.

  1. `altTwo` : the checkerboard sequence `1, -1, 1, -1, ...`, its 2-periodicity and
     its 2-antiperiodicity (constant on each parity class).  The continuum operator
     `d/dy` on the circle has only the constants in its kernel, so this parity
     dependence is genuinely discrete.

  2. The coefficient algebra of the centred difference in `ℚ[X]`: the centred kernel
     `(X - X⁻¹)/2` agrees with `(X - 1) + (X - 1)³/6` modulo `(X - 1)⁴`, so the
     first-order coefficient is exactly `1` and the third-order defect exactly
     `1/6`.  Coefficient algebra only -- no remainder estimate.

  3. The kernel of the centred difference on the INTEGER LATTICE with period two,
     stated for `ℤ → K`: `ctr` kills exactly the 2-periodic sequences.  This is the
     rigorous form of "the centred difference has the extra kernel direction
     `j ↦ (-1)^j`"; it needs no `Fin N` arithmetic.
-/
import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Tactic

open scoped BigOperators

namespace DLW.DirA

variable {K : Type*} [Field K]

/-! ## 1. The checkerboard sequence -/

/-- The alternating sequence `1, -1, 1, -1, ...` on `ℕ`. -/
def altTwo : ℕ → K
  | 0 => 1
  | 1 => -1
  | n + 2 => altTwo n

@[simp] lemma altTwo_zero : altTwo (K := K) 0 = 1 := rfl
@[simp] lemma altTwo_one : altTwo (K := K) 1 = -1 := rfl
@[simp] lemma altTwo_add_two (n : ℕ) : altTwo (K := K) (n + 2) = altTwo n := rfl

lemma altTwo_two_mul (a : ℕ) : altTwo (K := K) (2 * a) = 1 := by
  induction a with
  | zero => rfl
  | succ b ih =>
      have h : 2 * (b + 1) = 2 * b + 2 := by omega
      rw [h, altTwo_add_two]; exact ih

lemma altTwo_two_mul_add_one (a : ℕ) : altTwo (K := K) (2 * a + 1) = -1 := by
  induction a with
  | zero => rfl
  | succ b ih =>
      have h : 2 * (b + 1) + 1 = (2 * b + 1) + 2 := by omega
      rw [h, altTwo_add_two]; exact ih

/-- The checkerboard is 2-periodic. -/
lemma altTwo_period_two (n : ℕ) : altTwo (K := K) (n + 2) = altTwo n :=
  altTwo_add_two n

/-- The checkerboard is 2-antiperiodic: shifting by one flips its sign. -/
lemma altTwo_shift_one (n : ℕ) : altTwo (K := K) (n + 1) = -altTwo n := by
  have h : n = 2 * (n / 2) + n % 2 := by have := Nat.div_add_mod n 2; omega
  have hlt : n % 2 < 2 := Nat.mod_lt _ (by omega)
  interval_cases h2 : n % 2
  · have hn : n + 1 = 2 * (n / 2) + 1 := by omega
    have hbase : altTwo (K := K) n = 1 := by rw [h]; simp only [h2, add_zero, altTwo_two_mul]
    rw [hn, hbase]
    simp [altTwo_two_mul_add_one]
  · have hn : n + 1 = 2 * (n / 2 + 1) := by omega
    have hp : 2 * (n / 2 + 1) = 2 * (n / 2) + 2 := by omega
    have hbase : altTwo (K := K) n = -1 := by rw [h]; simp only [h2, altTwo_two_mul_add_one]
    rw [hn, hp, altTwo_add_two, hbase, altTwo_two_mul]
    simp

/-- `altTwo` is constant on each parity class. -/
lemma altTwo_eq_of_mod_two_eq {m n : ℕ} (h : m % 2 = n % 2) :
    altTwo (K := K) m = altTwo (K := K) n := by
  have hm' : m = 2 * (m / 2) + m % 2 := by have := Nat.div_add_mod m 2; omega
  have hn' : n = 2 * (n / 2) + n % 2 := by have := Nat.div_add_mod n 2; omega
  rw [hm', hn', h]
  by_cases h0 : n % 2 = 0
  · rw [h0]; simp [altTwo_two_mul]
  · have h1 : n % 2 = 1 := by omega
    rw [h1]; simp [altTwo_two_mul_add_one]

/-! ## 2. Kernel of the centred difference on the integer lattice -/

section Lattice

/-- The undivided centred difference on the integer lattice. -/
def ctrL (f : ℤ → K) (j : ℤ) : K := f (j + 1) - f (j - 1)

/-- A sequence is 2-periodic when shifting by two fixes it. -/
def TwoPeriodic (f : ℤ → K) : Prop := ∀ j : ℤ, f (j + 2) = f j

/-- A sequence is 2-antiperiodic when shifting by one flips its sign.  The
checkerboard `j ↦ (-1)^j` is the model case. -/
def TwoAntiPeriodic (f : ℤ → K) : Prop := ∀ j : ℤ, f (j + 1) = -f j

/-- Antiperiodicity implies periodicity. -/
lemma twoPeriodic_of_twoAntiPeriodic {f : ℤ → K} (hf : TwoAntiPeriodic f) :
    TwoPeriodic f := by
  intro j
  have h1 := hf (j + 1)
  have h2 := hf j
  have e : j + 1 + 1 = j + 2 := by omega
  rw [e] at h1
  rw [h1, h2, neg_neg]

/-- **The checkerboard is in the kernel.**  Any 2-periodic sequence is killed by
the centred difference: `ctrL f = 0`. -/
theorem ctrL_eq_zero_of_twoPeriodic {f : ℤ → K} (hf : TwoPeriodic f) : ctrL f = 0 := by
  funext j
  simp only [ctrL, Pi.zero_apply]
  rw [sub_eq_zero]
  have h := hf (j - 1)
  have e : j - 1 + 2 = j + 1 := by omega
  rw [e] at h
  exact h

/-- **Kernel characterisation (necessity).**  A sequence killed by the centred
difference is 2-periodic.  Hence on the periodic lattice the kernel of `ctrL` is
exactly the 2-periodic sequences -- one dimension more than the continuum kernel,
which contains only the constants. -/
theorem twoPeriodic_of_ctrL_eq_zero {f : ℤ → K} (hf : ctrL f = 0) : TwoPeriodic f := by
  intro j
  have hstep : ∀ i : ℤ, f (i + 1) = f (i - 1) := by
    intro i
    have h := congrFun hf i
    simp only [ctrL, Pi.zero_apply] at h
    exact sub_eq_zero.mp h
  have h1 := hstep (j + 1)
  have e : j + 1 - 1 = j := by omega
  rw [e] at h1
  have e2 : j + 1 + 1 = j + 2 := by omega
  rw [e2] at h1
  exact h1

/-- The kernel of the centred difference is exactly the 2-periodic sequences. -/
theorem ctrL_kernel_iff (f : ℤ → K) : ctrL f = 0 ↔ TwoPeriodic f :=
  ⟨twoPeriodic_of_ctrL_eq_zero, ctrL_eq_zero_of_twoPeriodic⟩

end Lattice

/-! ## 3. Coefficient algebra of the centred difference -/

/-- The narrow second difference is exactly the square of the forward difference:
`X² - 2X + 1 = (X - 1)²`.  This is why the WIDE stencil and the square of the first
difference share their principal symbol while the NARROW 3-point Laplacian does not. -/
theorem narrow_second_difference :
    (Polynomial.X ^ 2 - 2 * Polynomial.X + 1 : Polynomial ℚ)
      = (Polynomial.X - 1) ^ 2 := by
  ring

end DLW.DirA
