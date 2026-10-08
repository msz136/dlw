import Mathlib.RingTheory.Binomial
import Mathlib.Analysis.Calculus.IteratedDeriv.Defs
import Mathlib.Analysis.Calculus.Deriv.Shift
import Mathlib.MeasureTheory.Integral.IntervalIntegral.IntegrationByParts
import Mathlib.Tactic.Ring

/-!
All-order coefficient and actual periodic integration steps for the top
quadratic Fourier symbol. The finite coefficient below is obtained by
expanding D^n f and then (D^(n-r-1)) f with the standard normal-form
pseudodifferential multiplication rule. This file does not assume the
desired top-symbol formula, and does not yet identify the perturbation of
the physical normalized monodromy L with this quadratic coefficient.
-/
noncomputable section
namespace DLWLean

open scoped BigOperators ContDiff
open Set

theorem residue_shifted_binomial (q : ℕ) :
    Ring.choose ((q : ℤ) - 1) q = if q = 0 then 1 else 0 := by
  cases q with
  | zero => simp
  | succ q =>
    have hcast : ((q + 1 : ℕ) : ℤ) - 1 = (q : ℤ) := by simp
    rw [hcast, Ring.choose_natCast, Nat.choose_eq_zero_of_lt (Nat.lt_succ_self q)]
    simp

/-- Exactly the D^-1 coefficient from the two finite Leibniz expansions
of D^n f D^-1 f. The second binomial has its genuine integer upper index. -/
def quadraticResidueNormalForm {R : Type*} [CommRing R]
    (n : ℕ) (jet : ℕ → R) : R :=
  ∑ r ∈ Finset.range (n + 1),
    (n.choose r : R) *
      ((Ring.choose (((n - r : ℕ) : ℤ) - 1) (n - r) : ℤ) : R) *
      jet r * jet (n - r)

theorem quadraticResidueNormalForm_eq {R : Type*} [CommRing R]
    (n : ℕ) (jet : ℕ → R) :
    quadraticResidueNormalForm n jet = jet n * jet 0 := by
  unfold quadraticResidueNormalForm
  rw [Finset.sum_eq_single n]
  · simp
  · intro r hr hne
    have hle : r ≤ n := Nat.le_of_lt_succ (Finset.mem_range.mp hr)
    have hsub : n - r ≠ 0 := by omega
    simp [residue_shifted_binomial, hsub]
  · intro hnot
    exact (hnot (Finset.mem_range.mpr (Nat.lt_succ_self n))).elim

/-- Periodicity of every derivative follows from translation of the
actual real derivative, including the derivative's total-function convention. -/
theorem periodic_real_deriv {f : ℝ → ℝ} {period : ℝ}
    (hperiodic : Function.Periodic f period) :
    Function.Periodic (deriv f) period := by
  intro x
  have hshift : (fun y => f (y + period)) = f := funext hperiodic
  calc
    deriv f (x + period) = deriv (fun y => f (y + period)) x :=
      (deriv_comp_add_const f period x).symm
    _ = deriv f x := by rw [hshift]

theorem periodic_iteratedDeriv {f : ℝ → ℝ} {period : ℝ}
    (hperiodic : Function.Periodic f period) (n : ℕ) :
    Function.Periodic (iteratedDeriv n f) period := by
  induction n with
  | zero => simpa only [iteratedDeriv_zero] using hperiodic
  | succ n ih =>
    rw [iteratedDeriv_succ]
    exact periodic_real_deriv ih

def derivativePairing (period : ℝ) (f : ℝ → ℝ) (m n : ℕ) : ℝ :=
  ∫ x in (0 : ℝ)..period, iteratedDeriv m f x * iteratedDeriv n f x

theorem derivativePairing_step (period : ℝ) (f : ℝ → ℝ)
    (hsmooth : ContDiff ℝ ∞ f) (hperiodic : Function.Periodic f period)
    (m n : ℕ) :
    derivativePairing period f m (n + 1) =
      -derivativePairing period f (m + 1) n := by
  have hcont (k : ℕ) : Continuous (iteratedDeriv k f) :=
    hsmooth.continuous_iteratedDeriv k (by simp)
  have hdiff (k : ℕ) (x : ℝ) :
      HasDerivAt (iteratedDeriv k f) (iteratedDeriv (k + 1) f x) x := by
    rw [iteratedDeriv_succ]
    exact (ContDiff.differentiable_iteratedDeriv' k
      ((contDiff_infty.mp hsmooth) (k + 1)) x).hasDerivAt
  have hboundary (k : ℕ) : iteratedDeriv k f period = iteratedDeriv k f 0 := by
    simpa using periodic_iteratedDeriv hperiodic k 0
  have hibp := intervalIntegral.integral_mul_deriv_eq_deriv_mul_of_hasDerivAt
    (a := (0 : ℝ)) (b := period)
    (u := iteratedDeriv m f) (v := iteratedDeriv n f)
    (u' := iteratedDeriv (m + 1) f) (v' := iteratedDeriv (n + 1) f)
    (hcont m).continuousOn (hcont n).continuousOn
    (fun x _ => hdiff m x) (fun x _ => hdiff n x)
    ((hcont (m + 1)).intervalIntegrable 0 period)
    ((hcont (n + 1)).intervalIntegrable 0 period)
  simpa [derivativePairing, hboundary m, hboundary n] using hibp

theorem derivativePairing_shift (period : ℝ) (f : ℝ → ℝ)
    (hsmooth : ContDiff ℝ ∞ f) (hperiodic : Function.Periodic f period)
    (m n k : ℕ) :
    derivativePairing period f m (n + k) =
      (-1 : ℝ) ^ k * derivativePairing period f (m + k) n := by
  induction k generalizing m with
  | zero => simp
  | succ k ih =>
    have hidx : m + 1 + k = m + (k + 1) := by omega
    calc
      derivativePairing period f m (n + (k + 1)) =
          -derivativePairing period f (m + 1) (n + k) := by
        rw [Nat.add_succ]
        exact derivativePairing_step period f hsmooth hperiodic m (n + k)
      _ = -((-1 : ℝ) ^ k * derivativePairing period f (m + 1 + k) n) :=
        congrArg Neg.neg (ih (m + 1))
      _ = (-1 : ℝ) ^ (k + 1) * derivativePairing period f (m + (k + 1)) n := by
        rw [hidx, pow_succ]
        ring

/-- Actual Lebesgue interval integration and all-order integration by
parts, for every smooth real periodic function. -/
theorem integral_periodic_even_derivative (period : ℝ) (f : ℝ → ℝ)
    (hsmooth : ContDiff ℝ ∞ f) (hperiodic : Function.Periodic f period)
    (k : ℕ) :
    (∫ x in (0 : ℝ)..period, f x * iteratedDeriv (2 * k) f x) =
      (-1 : ℝ) ^ k * ∫ x in (0 : ℝ)..period, (iteratedDeriv k f x) ^ 2 := by
  have hshift := derivativePairing_shift period f hsmooth hperiodic 0 k k
  simpa [derivativePairing, iteratedDeriv_zero, two_mul, pow_two] using hshift

/-- The finite-coefficient candidate supplied by the eta=B=0 quadratic
resolvent expansion, with the physical lattice normalization 2/M. -/
def topQuadraticDensity (M k : ℕ) (f : ℝ → ℝ) (x : ℝ) : ℝ :=
  -(2 / (M : ℝ)) * quadraticResidueNormalForm (2 * k)
    (fun r => iteratedDeriv r f x)

theorem integral_topQuadraticDensity (period : ℝ) (M k : ℕ) (f : ℝ → ℝ)
    (hsmooth : ContDiff ℝ ∞ f) (hperiodic : Function.Periodic f period) :
    (∫ x in (0 : ℝ)..period, topQuadraticDensity M k f x) =
      (2 / (M : ℝ)) * (-1 : ℝ) ^ (k + 1) *
        ∫ x in (0 : ℝ)..period, (iteratedDeriv k f x) ^ 2 := by
  have hdensity : topQuadraticDensity M k f =
      fun x => -(2 / (M : ℝ)) * (f x * iteratedDeriv (2 * k) f x) := by
    ext x
    rw [topQuadraticDensity, quadraticResidueNormalForm_eq]
    simp only [iteratedDeriv_zero]
    ring
  rw [hdensity, intervalIntegral.integral_const_mul,
    integral_periodic_even_derivative period f hsmooth hperiodic k, pow_succ]
  ring

#print axioms quadraticResidueNormalForm_eq
#print axioms integral_periodic_even_derivative
#print axioms integral_topQuadraticDensity

end DLWLean
