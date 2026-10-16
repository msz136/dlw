import FieldCoordinates
import HamiltonianFamily
import Mathlib.Analysis.Calculus.Deriv.Basic

/-!
Concrete physical starting point and energy functionals. The original
DLW equations below are hypotheses on a trajectory, not a proved Lax
representation. The scalar residue-energy identity in the last theorem
is likewise displayed as its explicit, still required premise.
-/
noncomputable section
open scoped BigOperators
open scoped ContDiff
namespace DLWLean

def previousSite (par : FieldParameters) (j : Fin par.M) : Fin par.M :=
  ⟨(j.val + par.M - 1) % par.M, Nat.mod_lt _ (by have := par.M_ge_two; omega)⟩

def deltaMinus (par : FieldParameters) (f : Fin par.M → ℝ) (j : Fin par.M) : ℝ :=
  (f j - f (previousSite par j)) / par.h

def averageMinus (par : FieldParameters) (f : Fin par.M → ℝ) (j : Fin par.M) : ℝ :=
  (f j + f (previousSite par j)) / 2

def beta (par : FieldParameters) : ℝ := par.h ^ 2 / 32

/-- Exactly the two implicit physical equations in section 2.1, with
pointwise fixed mean closure supplied by FieldCoordinates. -/
def PhysicalDLW (par : FieldParameters) (z : ℝ → FieldCoordinates par) : Prop :=
  ∀ t x j,
    deltaMinus par (fun i =>
      deriv (fun τ => (z τ).U i x) t +
        deriv (fun y => ((z t).U i y) ^ 2 / 2 +
          beta par * ((z t).w i y) ^ 2) x) j +
      deriv (deriv (fun y =>
        deltaMinus par (fun i => (z t).U i y) j +
          averageMinus par (fun i => (z t).w i y) j)) x = 0 ∧
    deriv (fun τ => (z τ).w j x) t +
      deriv (fun y => (z t).U j y * (z t).w j y) x -
        deriv (deriv ((z t).w j)) x = 0

structure StartPoint (par : FieldParameters) where
  trajectory : ℝ → FieldCoordinates par
  joint_smooth_p : ∀ j, ContDiff ℝ ∞
    (fun tx : ℝ × ℝ => (trajectory tx.1).p.value j tx.2)
  joint_smooth_s : ∀ j, ContDiff ℝ ∞
    (fun tx : ℝ × ℝ => (trajectory tx.1).s.value j tx.2)
  physical_equations : PhysicalDLW par trajectory

theorem StartPoint.mean_closure {par : FieldParameters} (start : StartPoint par)
    (t x : ℝ) :
    latticeMean (fun j => (start.trajectory t).w j x) = par.c ∧
      latticeMean (fun j => (start.trajectory t).U j x *
        (start.trajectory t).w j x) = par.gamma :=
  (start.trajectory t).mean_closure x

/-- R is supplied at this stage. Its inverse-difference and skew-adjoint
properties are additional physical construction obligations, not axioms. -/
def physicalEnergy (par : FieldParameters)
    (R : (Fin par.M → ℝ) →ₗ[ℝ] (Fin par.M → ℝ))
    (z : FieldCoordinates par) : ℝ :=
  par.h * ∑ j, ∫ x in (0 : ℝ)..par.Lx,
    (z.U j x) ^ 2 * z.w j x / 2 + beta par * (z.w j x) ^ 3 / 3 +
      z.w j x * deriv (z.U j) x +
        z.w j x * R (fun i => deriv (z.w i) x) j / 2

def physicalK (par : FieldParameters)
    (R : (Fin par.M → ℝ) →ₗ[ℝ] (Fin par.M → ℝ))
    (z : FieldCoordinates par) : ℝ :=
  physicalEnergy par R z - par.gamma * z.physicalUIntegral

def energyConstant (par : FieldParameters) : ℝ :=
  8 * par.G * (par.G ^ 2 / 12 + par.B ^ 2) * par.Lx -
    par.gamma ^ 2 * par.h * (par.M : ℝ) * par.Lx / par.c

/-- Exact K identity once the first physical residue has been computed.
No residue computation is hidden in this premise. -/
theorem physicalK_eq_of_first_residue
    (par : FieldParameters)
    (R : (Fin par.M → ℝ) →ₗ[ℝ] (Fin par.M → ℝ))
    (z : FieldCoordinates par) (C₁ : ℝ)
    (hresidue : C₁ = -physicalEnergy par R z / (8 * par.G) +
      (par.G ^ 2 / 12 + par.B ^ 2) * par.Lx) :
    physicalK par R z = -8 * par.G * C₁ +
      (par.gamma / par.c) * z.physicalMomentum + energyConstant par := by
  unfold physicalK energyConstant
  rw [z.U_integral_identity]
  convert trace_one_energy_to_physical par.G par.B par.gamma par.c par.h
    (par.M : ℝ) par.Lx (physicalEnergy par R z) z.physicalMomentum C₁
    par.c_ne_zero par.G_ne_zero hresidue using 1 <;> ring

#print axioms StartPoint.mean_closure
#print axioms physicalK_eq_of_first_residue

end DLWLean
