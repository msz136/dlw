import TodaFormalization.DLWOneSoliton

/-!
Algebraic core of the determinant-preserving staggered DLW construction.

This file does NOT formalize determinants or the paper's all-N Hirota
identity. It verifies the parameter-shift identity used to reduce BOTH
new lattice equations to that known determinant identity, and the exact
equivalence of the normalized centered equations.
-/

namespace DLWStaggered
open Lean.Grind
variable {K : Type} [Field K] [IsCharP K 0]

def spectralRatio (p q s : K) : K := -(p-s)/(q+s)

def latticeRatio (p q a d : K) : K :=
  ((p-a+d)*(q+a+d))/((p-a-d)*(q+a-d))

theorem shifted_matrix_entry
    (p q a d M : K)
    (hp : p-a-d ≠ 0) (hq : q+a+d ≠ 0) (hqminus : q+a-d ≠ 0) :
    spectralRatio p q (a+d) * (latticeRatio p q a d * M)
    = spectralRatio p q (a-d) * M := by
  simp [spectralRatio, latticeRatio, Field.div_eq_mul_inv]
  grind

-- Uminus=B F.G_j, Uplus=B F.G_(j+1), Vminus=Dx F.G_j,
-- Vplus=Dx F.G_(j+1). The two edge equations are Uminus-h*Vminus=0
-- and Uplus+h*Vplus=0. Sum and divided difference are the meaningful
-- normalized equations for checking the h->0 limit on staggered grids.
theorem centered_equivalence
    (h Uminus Uplus Vminus Vplus : K) (hh : h ≠ 0) :
    (Uminus-h*Vminus=0 ∧ Uplus+h*Vplus=0) ↔
    ((Uminus+Uplus)/2+h*(Vplus-Vminus)/2=0 ∧
     (Uplus-Uminus)/h+Vplus+Vminus=0) := by
  simp [Field.div_eq_mul_inv]
  grind

-- Formal Taylor coefficient checks only; no analytic remainder theorem.
theorem centered_mean_coefficients
    (h b0 b1 b2 b3 d0 d1 d2 : K) :
    ((b0-h/2*b1+h^2/8*b2-h^3/48*b3)
      +(b0+h/2*b1+h^2/8*b2+h^3/48*b3))/2
    + h*((d0+h/2*d1+h^2/8*d2)-(d0-h/2*d1+h^2/8*d2))/2
    = b0+h^2*(b2/8+d1/2) := by
  simp [Field.div_eq_mul_inv]
  grind

theorem centered_difference_coefficients
    (h b0 b1 b2 b3 d0 d1 d2 : K) (hh : h ≠ 0) :
    ((b0+h/2*b1+h^2/8*b2+h^3/48*b3)
      -(b0-h/2*b1+h^2/8*b2-h^3/48*b3))/h
    +(d0+h/2*d1+h^2/8*d2)+(d0-h/2*d1+h^2/8*d2)
    = b1+2*d0+h^2*(b3/24+d2/4) := by
  simp [Field.div_eq_mul_inv]
  grind

end DLWStaggered
