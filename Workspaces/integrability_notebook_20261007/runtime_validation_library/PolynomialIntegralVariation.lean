import Mathlib.Algebra.Polynomial.Coeff
import Mathlib.Algebra.Algebra.Hom
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Tactic

namespace DLWLean
noncomputable section
open Polynomial

/-- A coefficient algebra need not carry a norm: integration of a finite
coefficient polynomial is an ordinary real polynomial, and its derivative
is the integral of its linear coefficient. -/
theorem linear_polynomial_evaluation_hasDerivAt_zero
    {R : Type*} [CommRing R] [Algebra ℝ R]
    (I : R →ₗ[ℝ] ℝ) (P : Polynomial R) :
    HasDerivAt (fun ε : ℝ => I (P.eval (algebraMap ℝ R ε))) (I (P.coeff 1)) 0 := by
  induction P using Polynomial.induction_on' with
  | add P Q hP hQ =>
    have hfun : (fun ε : ℝ => I ((P + Q).eval (algebraMap ℝ R ε))) =
        fun ε => I (P.eval (algebraMap ℝ R ε)) + I (Q.eval (algebraMap ℝ R ε)) := by
      funext ε
      rw [Polynomial.eval_add, map_add]
    rw [hfun, Polynomial.coeff_add, map_add]
    exact hP.add hQ
  | monomial n a =>
    have hfun : (fun ε : ℝ => I ((Polynomial.monomial n a).eval (algebraMap ℝ R ε))) =
        fun ε => ε ^ n * I a := by
      funext ε
      rw [Polynomial.eval_monomial]
      have hm : a * (algebraMap ℝ R ε) ^ n = ε ^ n • a := by
        rw [Algebra.smul_def, map_pow]
        exact mul_comm _ _
      rw [hm, map_smul, smul_eq_mul]
    rw [hfun]
    have h := ((hasDerivAt_id (0 : ℝ)).pow n).mul_const (I a)
    by_cases hn0 : n = 0
    · subst n
      simpa using h
    · by_cases hn1 : n = 1
      · subst n
        simpa using h
      · have hsub : n - 1 ≠ 0 := by omega
        simpa [Polynomial.coeff_monomial, hn1, hsub, zero_pow] using h

#print axioms linear_polynomial_evaluation_hasDerivAt_zero
end
end DLWLean
