import Mathlib.Analysis.Calculus.ContDiff.Operations
import Mathlib.MeasureTheory.Integral.IntervalIntegral.Basic
import Mathlib.Algebra.Ring.Periodic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-!
Concrete periodic field coordinates for the mean closure in section 13.1.
No claim concerning the pseudodifferential Lax operator is made in this module.
-/

noncomputable section

open scoped BigOperators
open scoped ContDiff

namespace DLWLean

/-- Numerical parameters of a fixed finite periodic lattice. -/
structure FieldParameters where
  M : ℕ
  M_ge_two : 2 ≤ M
  Lx : ℝ
  Lx_pos : 0 < Lx
  h : ℝ
  h_pos : 0 < h
  c : ℝ
  c_ne_zero : c ≠ 0
  gamma : ℝ

/-- The finite lattice average, evaluated at one value of the continuous variable. -/
def latticeMean {M : ℕ} (f : Fin M → ℝ) : ℝ :=
  (∑ j, f j) / (M : ℝ)

theorem latticeMean_add {M : ℕ} (f g : Fin M → ℝ) :
    latticeMean (fun j => f j + g j) = latticeMean f + latticeMean g := by
  simp [latticeMean, Finset.sum_add_distrib, add_div]

theorem latticeMean_sub {M : ℕ} (f g : Fin M → ℝ) :
    latticeMean (fun j => f j - g j) = latticeMean f - latticeMean g := by
  simp [latticeMean, Finset.sum_sub_distrib, sub_div]

theorem latticeMean_mul_left {M : ℕ} (a : ℝ) (f : Fin M → ℝ) :
    latticeMean (fun j => a * f j) = a * latticeMean f := by
  unfold latticeMean
  rw [← Finset.mul_sum]
  ring

theorem latticeMean_mul_right {M : ℕ} (f : Fin M → ℝ) (a : ℝ) :
    latticeMean (fun j => f j * a) = latticeMean f * a := by
  unfold latticeMean
  rw [← Finset.sum_mul]
  ring

theorem latticeMean_const {M : ℕ} (hM : M ≠ 0) (a : ℝ) :
    latticeMean (fun _ : Fin M => a) = a := by
  have hMr : (M : ℝ) ≠ 0 := by exact_mod_cast hM
  simp [latticeMean, Finset.sum_const, nsmul_eq_mul, hMr]

theorem FieldParameters.M_ne_zero (par : FieldParameters) : par.M ≠ 0 := by
  exact Nat.ne_of_gt (lt_of_lt_of_le (by decide : 0 < 2) par.M_ge_two)

/-- A smooth field whose continuous argument has the prescribed positive period. -/
structure SmoothPeriodicField (M : ℕ) (Lx : ℝ) where
  value : Fin M → ℝ → ℝ
  smooth : ∀ j, ContDiff ℝ ∞ (value j)
  periodic : ∀ j, Function.Periodic (value j) Lx

/-- Independent coordinates: both fields have zero lattice average pointwise. -/
structure FieldCoordinates (par : FieldParameters) where
  p : SmoothPeriodicField par.M par.Lx
  s : SmoothPeriodicField par.M par.Lx
  p_zero : ∀ x, latticeMean (fun j => p.value j x) = 0
  s_zero : ∀ x, latticeMean (fun j => s.value j x) = 0

def FieldCoordinates.meanPS {par : FieldParameters} (z : FieldCoordinates par)
    (x : ℝ) : ℝ := latticeMean (fun j => z.p.value j x * z.s.value j x)

def FieldCoordinates.commonU {par : FieldParameters} (z : FieldCoordinates par)
    (x : ℝ) : ℝ := (par.gamma - z.meanPS x) / par.c

def FieldCoordinates.U {par : FieldParameters} (z : FieldCoordinates par)
    (j : Fin par.M) (x : ℝ) : ℝ := z.p.value j x + z.commonU x

def FieldCoordinates.w {par : FieldParameters} (z : FieldCoordinates par)
    (j : Fin par.M) (x : ℝ) : ℝ := par.c + z.s.value j x

theorem FieldCoordinates.meanPS_smooth {par : FieldParameters}
    (z : FieldCoordinates par) : ContDiff ℝ ∞ z.meanPS := by
  unfold FieldCoordinates.meanPS latticeMean
  exact (ContDiff.sum fun j _ => (z.p.smooth j).mul (z.s.smooth j)).div_const _

theorem FieldCoordinates.meanPS_periodic {par : FieldParameters}
    (z : FieldCoordinates par) : Function.Periodic z.meanPS par.Lx := by
  intro x
  unfold FieldCoordinates.meanPS latticeMean
  congr 1
  apply Finset.sum_congr rfl
  intro j _
  change z.p.value j (x + par.Lx) * z.s.value j (x + par.Lx) =
    z.p.value j x * z.s.value j x
  rw [z.p.periodic j x, z.s.periodic j x]

theorem FieldCoordinates.commonU_smooth {par : FieldParameters}
    (z : FieldCoordinates par) : ContDiff ℝ ∞ z.commonU := by
  exact (contDiff_const.sub z.meanPS_smooth).div_const _

theorem FieldCoordinates.commonU_periodic {par : FieldParameters}
    (z : FieldCoordinates par) : Function.Periodic z.commonU par.Lx := by
  intro x
  unfold FieldCoordinates.commonU
  rw [z.meanPS_periodic x]

theorem FieldCoordinates.U_smooth {par : FieldParameters}
    (z : FieldCoordinates par) (j : Fin par.M) : ContDiff ℝ ∞ (z.U j) := by
  exact (z.p.smooth j).add z.commonU_smooth

theorem FieldCoordinates.U_periodic {par : FieldParameters}
    (z : FieldCoordinates par) (j : Fin par.M) : Function.Periodic (z.U j) par.Lx := by
  intro x
  unfold FieldCoordinates.U
  rw [z.p.periodic j x, z.commonU_periodic x]

theorem FieldCoordinates.w_smooth {par : FieldParameters}
    (z : FieldCoordinates par) (j : Fin par.M) : ContDiff ℝ ∞ (z.w j) := by
  exact contDiff_const.add (z.s.smooth j)

theorem FieldCoordinates.w_periodic {par : FieldParameters}
    (z : FieldCoordinates par) (j : Fin par.M) : Function.Periodic (z.w j) par.Lx := by
  intro x
  unfold FieldCoordinates.w
  rw [z.s.periodic j x]

theorem FieldCoordinates.mean_w {par : FieldParameters} (z : FieldCoordinates par)
    (x : ℝ) : latticeMean (fun j => z.w j x) = par.c := by
  simp only [FieldCoordinates.w, latticeMean_add,
    latticeMean_const par.M_ne_zero, z.s_zero, add_zero]

theorem FieldCoordinates.mean_U {par : FieldParameters} (z : FieldCoordinates par)
    (x : ℝ) : latticeMean (fun j => z.U j x) = z.commonU x := by
  simp only [FieldCoordinates.U, latticeMean_add, z.p_zero,
    latticeMean_const par.M_ne_zero, zero_add]

theorem FieldCoordinates.mean_Uw {par : FieldParameters} (z : FieldCoordinates par)
    (x : ℝ) : latticeMean (fun j => z.U j x * z.w j x) = par.gamma := by
  have expand : (fun j => z.U j x * z.w j x) =
      (fun j => z.p.value j x * z.s.value j x +
        z.p.value j x * par.c +
        z.commonU x * z.s.value j x + z.commonU x * par.c) := by
    funext j
    simp only [FieldCoordinates.U, FieldCoordinates.w]
    ring
  rw [expand]
  simp only [latticeMean_add, latticeMean_mul_right, latticeMean_mul_left,
    z.p_zero, z.s_zero, latticeMean_const par.M_ne_zero, zero_mul, mul_zero,
    add_zero, FieldCoordinates.commonU, FieldCoordinates.meanPS]
  rw [div_mul_cancel₀ _ par.c_ne_zero]
  ring

theorem FieldCoordinates.mean_closure {par : FieldParameters}
    (z : FieldCoordinates par) (x : ℝ) :
    latticeMean (fun j => z.w j x) = par.c ∧
      latticeMean (fun j => z.U j x * z.w j x) = par.gamma :=
  ⟨z.mean_w x, z.mean_Uw x⟩

/-- The projector onto the zero lattice average component. -/
def latticeP0 {M : ℕ} (f : Fin M → ℝ) (j : Fin M) : ℝ :=
  f j - latticeMean f

theorem FieldCoordinates.recover_p {par : FieldParameters}
    (z : FieldCoordinates par) (j : Fin par.M) (x : ℝ) :
    latticeP0 (fun i => z.U i x) j = z.p.value j x := by
  change z.U j x - latticeMean (fun i => z.U i x) = z.p.value j x
  rw [z.mean_U x]
  unfold FieldCoordinates.U
  ring

theorem FieldCoordinates.recover_s {par : FieldParameters}
    (z : FieldCoordinates par) (j : Fin par.M) (x : ℝ) :
    z.w j x - par.c = z.s.value j x := by
  simp only [FieldCoordinates.w]
  ring

theorem sum_eq_card_mul_latticeMean {M : ℕ} (hM : M ≠ 0) (f : Fin M → ℝ) :
    (∑ j, f j) = (M : ℝ) * latticeMean f := by
  have hMr : (M : ℝ) ≠ 0 := by exact_mod_cast hM
  unfold latticeMean
  field_simp

theorem FieldCoordinates.sum_U {par : FieldParameters}
    (z : FieldCoordinates par) (x : ℝ) :
    (∑ j, z.U j x) = (par.M : ℝ) * par.gamma / par.c -
      (∑ j, z.p.value j x * z.s.value j x) / par.c := by
  rw [sum_eq_card_mul_latticeMean par.M_ne_zero, z.mean_U]
  unfold FieldCoordinates.commonU FieldCoordinates.meanPS latticeMean
  have hMr : (par.M : ℝ) ≠ 0 := by exact_mod_cast par.M_ne_zero
  field_simp

/-- The actual spatial translation momentum, with the h-weighted pairing. -/
def FieldCoordinates.physicalMomentum {par : FieldParameters}
    (z : FieldCoordinates par) : ℝ :=
  par.h * ∑ j, ∫ x in (0 : ℝ)..par.Lx, z.p.value j x * z.s.value j x

def FieldCoordinates.physicalUIntegral {par : FieldParameters}
    (z : FieldCoordinates par) : ℝ :=
  par.h * ∑ j, ∫ x in (0 : ℝ)..par.Lx, z.U j x

theorem FieldCoordinates.U_integral_identity {par : FieldParameters}
    (z : FieldCoordinates par) :
    z.physicalUIntegral =
      par.h * (par.M : ℝ) * par.Lx * par.gamma / par.c -
        z.physicalMomentum / par.c := by
  have hintU : (∫ x in (0 : ℝ)..par.Lx, ∑ j, z.U j x) =
      ∑ j, ∫ x in (0 : ℝ)..par.Lx, z.U j x :=
    intervalIntegral.integral_finsetSum fun j _ =>
      (z.U_smooth j).continuous.intervalIntegrable _ _
  have hPScont : Continuous (fun x => ∑ j, z.p.value j x * z.s.value j x) :=
    continuous_finsetSum _ fun j _ => (z.p.smooth j).continuous.mul (z.s.smooth j).continuous
  have hintPS : (∫ x in (0 : ℝ)..par.Lx, ∑ j, z.p.value j x * z.s.value j x) =
      ∑ j, ∫ x in (0 : ℝ)..par.Lx, z.p.value j x * z.s.value j x :=
    intervalIntegral.integral_finsetSum fun j _ =>
      ((z.p.smooth j).continuous.mul (z.s.smooth j).continuous).intervalIntegrable _ _
  unfold FieldCoordinates.physicalUIntegral FieldCoordinates.physicalMomentum
  rw [← hintU]
  simp_rw [z.sum_U]
  rw [intervalIntegral.integral_sub
    (continuous_const.intervalIntegrable _ _)
    ((hPScont.div_const par.c).intervalIntegrable _ _)]
  rw [intervalIntegral.integral_const, intervalIntegral.integral_div, hintPS]
  simp only [sub_zero, smul_eq_mul]
  ring

/-- Normalizing constant occurring in the proposed scalar Lax operator. -/
def FieldParameters.G (par : FieldParameters) : ℝ :=
  par.h * (par.M : ℝ) * par.c / 4

def FieldParameters.B (par : FieldParameters) : ℝ := par.gamma / (2 * par.c)

theorem FieldParameters.G_ne_zero (par : FieldParameters) : par.G ≠ 0 := by
  have hMr : (par.M : ℝ) ≠ 0 := by exact_mod_cast par.M_ne_zero
  exact div_ne_zero (mul_ne_zero (mul_ne_zero (ne_of_gt par.h_pos) hMr)
    par.c_ne_zero) (by norm_num)

theorem latticeMean_P0 {M : ℕ} (hM : M ≠ 0) (f : Fin M → ℝ) :
    latticeMean (latticeP0 f) = 0 := by
  unfold latticeP0
  rw [latticeMean_sub, latticeMean_const hM]
  ring

theorem SmoothPeriodicField.mean_smooth {M : ℕ} {Lx : ℝ}
    (f : SmoothPeriodicField M Lx) :
    ContDiff ℝ ∞ (fun x => latticeMean (fun j => f.value j x)) := by
  unfold latticeMean
  exact (ContDiff.sum fun j _ => f.smooth j).div_const _

theorem SmoothPeriodicField.mean_periodic {M : ℕ} {Lx : ℝ}
    (f : SmoothPeriodicField M Lx) :
    Function.Periodic (fun x => latticeMean (fun j => f.value j x)) Lx := by
  intro x
  unfold latticeMean
  change (∑ j, f.value j (x + Lx)) / (M : ℝ) =
    (∑ j, f.value j x) / (M : ℝ)
  apply congrArg (fun a : ℝ => a / (M : ℝ))
  apply Finset.sum_congr rfl
  intro j _
  exact f.periodic j x

def SmoothPeriodicField.zeroMeanPart {M : ℕ} {Lx : ℝ}
    (f : SmoothPeriodicField M Lx) : SmoothPeriodicField M Lx where
  value := fun j x => latticeP0 (fun i => f.value i x) j
  smooth := fun j => (f.smooth j).sub f.mean_smooth
  periodic := fun j x => by
    change f.value j (x + Lx) - latticeMean (fun i => f.value i (x + Lx)) =
      f.value j x - latticeMean (fun i => f.value i x)
    have hmean : latticeMean (fun i => f.value i (x + Lx)) =
        latticeMean (fun i => f.value i x) := f.mean_periodic x
    rw [f.periodic j x, hmean]

def SmoothPeriodicField.subtractConstant {M : ℕ} {Lx : ℝ}
    (f : SmoothPeriodicField M Lx) (a : ℝ) : SmoothPeriodicField M Lx where
  value := fun j x => f.value j x - a
  smooth := fun j => (f.smooth j).sub contDiff_const
  periodic := fun j x => by
    change f.value j (x + Lx) - a = f.value j x - a
    rw [f.periodic j x]

/-- Closed physical fields, with no hidden restrictions beyond smoothness,
periodicity and the two mean constraints. -/
structure PeriodicPhysicalState (par : FieldParameters) where
  U : SmoothPeriodicField par.M par.Lx
  w : SmoothPeriodicField par.M par.Lx
  mean_w : ∀ x, latticeMean (fun j => w.value j x) = par.c
  mean_Uw : ∀ x, latticeMean (fun j => U.value j x * w.value j x) = par.gamma

def PeriodicPhysicalState.toCoordinates {par : FieldParameters}
    (f : PeriodicPhysicalState par) : FieldCoordinates par where
  p := f.U.zeroMeanPart
  s := f.w.subtractConstant par.c
  p_zero := fun x => latticeMean_P0 par.M_ne_zero (fun j => f.U.value j x)
  s_zero := fun x => by
    change latticeMean (fun j => f.w.value j x - par.c) = 0
    rw [latticeMean_sub, f.mean_w x, latticeMean_const par.M_ne_zero]
    ring

theorem PeriodicPhysicalState.projected_product_mean {par : FieldParameters}
    (f : PeriodicPhysicalState par) (x : ℝ) :
    latticeMean (fun j =>
      latticeP0 (fun i => f.U.value i x) j * (f.w.value j x - par.c)) =
        par.gamma - latticeMean (fun j => f.U.value j x) * par.c := by
  have expand : (fun j =>
      latticeP0 (fun i => f.U.value i x) j * (f.w.value j x - par.c)) =
      (fun j => f.U.value j x * f.w.value j x - f.U.value j x * par.c -
        latticeMean (fun i => f.U.value i x) * f.w.value j x +
        latticeMean (fun i => f.U.value i x) * par.c) := by
    funext j
    unfold latticeP0
    ring
  rw [expand]
  simp only [latticeMean_add, latticeMean_sub, latticeMean_mul_right,
    latticeMean_mul_left, f.mean_Uw x, f.mean_w x,
    latticeMean_const par.M_ne_zero]
  ring

theorem PeriodicPhysicalState.reconstruct_U {par : FieldParameters}
    (f : PeriodicPhysicalState par) (j : Fin par.M) (x : ℝ) :
    f.toCoordinates.U j x = f.U.value j x := by
  change latticeP0 (fun i => f.U.value i x) j +
    (par.gamma - latticeMean (fun i =>
      latticeP0 (fun k => f.U.value k x) i * (f.w.value i x - par.c))) / par.c =
      f.U.value j x
  rw [f.projected_product_mean x]
  unfold latticeP0
  field_simp [par.c_ne_zero]
  ring

theorem PeriodicPhysicalState.reconstruct_w {par : FieldParameters}
    (f : PeriodicPhysicalState par) (j : Fin par.M) (x : ℝ) :
    f.toCoordinates.w j x = f.w.value j x := by
  change par.c + (f.w.value j x - par.c) = f.w.value j x
  ring

end DLWLean
