import PkgNumeric
import Mathlib.Analysis.Calculus.IteratedDeriv.FaaDiBruno
import Mathlib.Analysis.Calculus.IteratedDeriv.Lemmas
import Mathlib.Tactic

noncomputable section
open scoped BigOperators
namespace DLWContract
namespace RK4Proof
variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]

def autoStep (F : E → E) (h : ℝ) (z : E) : E :=
  let k₁ := F z
  let k₂ := F (z+(h/2) • k₁)
  let k₃ := F (z+(h/2) • k₂)
  let k₄ := F (z+h • k₃)
  z+(h/6) • (k₁+2 • k₂+2 • k₃+k₄)

theorem jet_hsmul (g : ℝ → E) (hg : ContDiff ℝ ⊤ g) (c : ℝ)
    (n : ℕ) (hn : n ≤ 3) :
    iteratedDeriv (n+1) (fun h : ℝ => (c*h) • g h) 0 =
      (((n+1 : ℕ) : ℝ) * c) • iteratedDeriv n g 0 := by
  rw [← iteratedDerivWithin_univ]
  change iteratedDerivWithin (n+1) ((fun h : ℝ => c*h) • g) Set.univ 0 = _
  rw [iteratedDerivWithin_smul (f := fun h : ℝ => c*h) (g := g)
    (Set.mem_univ 0) uniqueDiffOn_univ
    (by fun_prop) (hg.of_le le_top).contDiffWithinAt]
  simp only [iteratedDerivWithin_univ]
  have linear (k : ℕ) : iteratedDeriv k (fun h : ℝ => c*h) 0 =
      c * (if k = 1 then 1 else 0) := by
    rw [iteratedDeriv_const_mul_field c (fun h : ℝ => h)]
    rw [iteratedDeriv_fun_id_zero]
  interval_cases n <;>
    simp [Finset.sum_range_succ, linear, iteratedDeriv_zero] <;> norm_num <;> module

theorem jet_path (g : ℝ → E) (hg : ContDiff ℝ ⊤ g) (z : E) (c : ℝ)
    (n : ℕ) (hn : n ≤ 3) :
    iteratedDeriv (n+1) (fun h : ℝ => z+(c*h) • g h) 0 =
      (((n+1 : ℕ) : ℝ)*c) • iteratedDeriv n g 0 := by
  rw [iteratedDeriv_const_add (Nat.succ_pos n)]
  exact jet_hsmul g hg c n hn

theorem comp_one (F : E → E) (q : ℝ → E) (hF : ContDiff ℝ ⊤ F)
    (hq : ContDiff ℝ ⊤ q) :
    deriv (fun h => F (q h)) 0 = fderiv ℝ F (q 0) (deriv q 0) := by
  exact (((hF.differentiable (by simp)) (q 0)).hasFDerivAt.comp_hasDerivAt 0
    (((hq.differentiable (by simp)) 0).hasDerivAt)).deriv

theorem comp_two (F : E → E) (q : ℝ → E) (hF : ContDiff ℝ ⊤ F)
    (hq : ContDiff ℝ ⊤ q) :
    iteratedDeriv 2 (fun h => F (q h)) 0 =
      iteratedFDeriv ℝ 2 F (q 0) (fun _ => deriv q 0) +
        fderiv ℝ F (q 0) (iteratedDeriv 2 q 0) := by
  exact iteratedDeriv_vcomp_two (hF.of_le (by simp)).contDiffAt (hq.of_le (by simp)).contDiffAt

theorem comp_three (F : E → E) (q : ℝ → E) (hF : ContDiff ℝ ⊤ F)
    (hq : ContDiff ℝ ⊤ q) :
    iteratedDeriv 3 (fun h => F (q h)) 0 =
      iteratedFDeriv ℝ 3 F (q 0) (fun _ => deriv q 0) +
      iteratedFDeriv ℝ 2 F (q 0) ![iteratedDeriv 2 q 0, deriv q 0] +
      2 • iteratedFDeriv ℝ 2 F (q 0) ![deriv q 0, iteratedDeriv 2 q 0] +
      fderiv ℝ F (q 0) (iteratedDeriv 3 q 0) := by
  exact iteratedDeriv_vcomp_three (hF.of_le (by simp)).contDiffAt (hq.of_le (by simp)).contDiffAt

/-- Exact fourth-degree polynomial for a continuous linear autonomous RHS.
This does not certify the nonlinear order condition in N01. -/
theorem autoStep_linear (A : E →L[ℝ] E) (h : ℝ) (z : E) :
    autoStep A h z = z + h • A z + (h^2/2) • A (A z) +
      (h^3/6) • A (A (A z)) + (h^4/24) • A (A (A (A z))) := by
  simp only [autoStep, map_add, map_smul, map_nsmul]
  module

/-- For the growing scalar test equation RK4 amplifies, just as the exact flow does. -/
theorem rk4_growth_polynomial (g h : ℝ) (hg : 0 < g) (hh : 0 < h) :
    1 < 1 + h*g + (h*g)^2/2 + (h*g)^3/6 + (h*g)^4/24 := by
  have hp : 0 < h*g := mul_pos hh hg
  have h2 : 0 ≤ (h*g)^2/2 := by positivity
  have h3 : 0 ≤ (h*g)^3/6 := by positivity
  have h4 : 0 ≤ (h*g)^4/24 := by positivity
  linarith

end RK4Proof

#print axioms RK4Proof.jet_hsmul
#print axioms RK4Proof.jet_path
#print axioms RK4Proof.comp_one
#print axioms RK4Proof.comp_two
#print axioms RK4Proof.comp_three
#print axioms RK4Proof.autoStep_linear
#print axioms RK4Proof.rk4_growth_polynomial
end DLWContract
