import QuadraticSymbol
import QuadraticResolvent

namespace DLWLean
noncomputable section
open scoped ContDiff

theorem derivativePairing_symmetric (period : ℝ) (f : ℝ → ℝ) (m n : ℕ) :
    derivativePairing period f m n = derivativePairing period f n m := by
  unfold derivativePairing
  simp only [mul_comm]

theorem derivativePairing_total_order (period : ℝ) (f : ℝ → ℝ)
    (hsmooth : ContDiff ℝ ∞ f) (hperiodic : Function.Periodic f period)
    (m n : ℕ) :
    derivativePairing period f m n =
      (-1 : ℝ) ^ m * derivativePairing period f 0 (m + n) := by
  have hshift := derivativePairing_shift period f hsmooth hperiodic 0 n m
  simp only [zero_add, Nat.add_comm n m] at hshift
  have hsign : (-1 : ℝ) ^ m * (-1 : ℝ) ^ m = 1 := by
    rw [← mul_pow]
    norm_num
  rw [hshift, ← mul_assoc, hsign, one_mul]

theorem derivativePairing_even_total (period : ℝ) (f : ℝ → ℝ)
    (hsmooth : ContDiff ℝ ∞ f) (hperiodic : Function.Periodic f period)
    (m n k : ℕ) (htotal : m + n = 2 * k) :
    derivativePairing period f m n =
      (-1 : ℝ) ^ (m + k) *
        ∫ x in (0 : ℝ)..period, (iteratedDeriv k f x) ^ 2 := by
  rw [derivativePairing_total_order period f hsmooth hperiodic m n, htotal]
  have hzero : derivativePairing period f 0 (2 * k) =
      (-1 : ℝ) ^ k * ∫ x in (0 : ℝ)..period, (iteratedDeriv k f x) ^ 2 :=
    integral_periodic_even_derivative period f hsmooth hperiodic k
  rw [hzero, ← mul_assoc, ← pow_add]

theorem derivativePairing_odd_total_zero (period : ℝ) (f : ℝ → ℝ)
    (hsmooth : ContDiff ℝ ∞ f) (hperiodic : Function.Periodic f period)
    (m n : ℕ) (hodd : Odd (m + n)) : derivativePairing period f m n = 0 := by
  have hleft := derivativePairing_total_order period f hsmooth hperiodic m n
  have hright := derivativePairing_total_order period f hsmooth hperiodic n m
  rw [derivativePairing_symmetric period f n m, Nat.add_comm n m] at hright
  have hsign : (-1 : ℝ) ^ m * (-1 : ℝ) ^ n = -1 := by
    rw [← pow_add]
    exact hodd.neg_one_pow
  have hsignm : (-1 : ℝ) ^ m * (-1 : ℝ) ^ m = 1 := by
    rw [← mul_pow]
    norm_num
  have hzero : derivativePairing period f 0 (m + n) = 0 := by
    have h1 := congrArg (fun a : ℝ => (-1 : ℝ) ^ m * a) hleft
    have h2 := congrArg (fun a : ℝ => (-1 : ℝ) ^ m * a) hright
    rw [← mul_assoc, hsignm, one_mul] at h1
    rw [← mul_assoc, hsign, neg_one_mul] at h2
    linarith
  rw [hleft, hzero, mul_zero]

#print axioms derivativePairing_even_total
#print axioms derivativePairing_odd_total_zero
end
end DLWLean
