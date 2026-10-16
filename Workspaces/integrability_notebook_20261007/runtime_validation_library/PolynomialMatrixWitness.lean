import Genericity
import Mathlib.Algebra.Polynomial.Div
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic

namespace DLWLean
noncomputable section
open scoped BigOperators

/-- A polynomial amplitude Jacobian whose entries vanish at zero has
its first possible determinant coefficient equal to the determinant of
the actual linear-entry coefficients. This is proved by literal divX
factorization of every entry. -/
theorem polynomialMatrixDet_lowest_coefficient {N : ℕ}
    (p : Matrix (Fin N) (Fin N) (Polynomial ℝ))
    (hzero : ∀ i j, (p i j).coeff 0 = 0) :
    p.det.coeff N = Matrix.det (fun i j => (p i j).coeff 1) := by
  let q : Matrix (Fin N) (Fin N) (Polynomial ℝ) := fun i j => (p i j).divX
  have hfactor : p = (Polynomial.X : Polynomial ℝ) • q := by
    apply Matrix.ext
    intro i j
    change p i j = Polynomial.X * (p i j).divX
    have h := Polynomial.X_mul_divX_add (p i j)
    simpa only [hzero i j, Polynomial.C_0, add_zero] using h.symm
  have hdet : p.det = Polynomial.X ^ N * q.det := by
    rw [hfactor, Matrix.det_smul]
    simp
  rw [hdet]
  have hcoeff : (Polynomial.X ^ N * q.det).coeff N = q.det.coeff 0 := by
    simpa using Polynomial.coeff_X_pow_mul q.det N 0
  rw [hcoeff, Polynomial.coeff_zero_eq_eval_zero]
  have hmap := (Polynomial.evalRingHom (0 : ℝ)).map_det q
  simp only [RingHom.mapMatrix_apply, Polynomial.coe_evalRingHom] at hmap
  rw [hmap]
  congr 1
  ext i j
  change Polynomial.eval 0 ((p i j).divX) = (p i j).coeff 1
  rw [← Polynomial.coeff_zero_eq_eval_zero, Polynomial.coeff_divX]

theorem polynomialMatrixDet_small_positive_witness {N : ℕ}
    (p : Matrix (Fin N) (Fin N) (Polynomial ℝ))
    (hzero : ∀ i j, (p i j).coeff 0 = 0)
    (hlinear : Matrix.det (fun i j => (p i j).coeff 1) ≠ 0)
    (radius : ℝ) (hradius : 0 < radius) :
    ∃ amplitude : ℝ, 0 < amplitude ∧ amplitude < radius ∧
      Matrix.det (fun i j => (p i j).eval amplitude) ≠ 0 := by
  have hcoefficient : p.det.coeff N ≠ 0 := by
    rwa [polynomialMatrixDet_lowest_coefficient p hzero]
  obtain ⟨amplitude, ha0, har, hdet⟩ :=
    polynomial_nonzero_at_small_positive_amplitude p.det N hcoefficient radius hradius
  refine ⟨amplitude, ha0, har, ?_⟩
  have hmap := (Polynomial.evalRingHom amplitude).map_det p
  simp only [RingHom.mapMatrix_apply, Polynomial.coe_evalRingHom] at hmap
  rw [hmap] at hdet
  exact hdet

#print axioms polynomialMatrixDet_lowest_coefficient
#print axioms polynomialMatrixDet_small_positive_witness
end
end DLWLean
