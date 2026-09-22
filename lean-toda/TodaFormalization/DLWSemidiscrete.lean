import Init.Grind.Ring.Field
import Init.GrindInstances.Ring.Rat

/-!
Algebraic checkpoints for a candidate y-semidiscretization of the DLW
bilinear equations. These are identities over Rat, not formalizations of
smooth functions, Taylor remainder estimates, or integrability.

Write B = Dx^2 + Dt + 2*a*Dx. The proposed edge equation is
 (B f[j+1].g[j] - B f[j].g[j+1])/h
 + lambda*Dx(f[j+1].g[j] + f[j].g[j+1]) = 0.
-/

namespace DLWSemidiscrete
open Lean.Grind

-- b_i and d_i stand for the formal coefficients Dy^i B and Dy^i Dx.
def bPlus (h b0 b1 b2 b3 : Rat) : Rat :=
  b0 + h/2*b1 + h^2/8*b2 + h^3/48*b3
def bMinus (h b0 b1 b2 b3 : Rat) : Rat :=
  b0 - h/2*b1 + h^2/8*b2 - h^3/48*b3
def dPlus (h d0 d1 d2 : Rat) : Rat :=
  d0 + h/2*d1 + h^2/8*d2
def dMinus (h d0 d1 d2 : Rat) : Rat :=
  d0 - h/2*d1 + h^2/8*d2

theorem formal_midpoint_coefficients
    (h lam b0 b1 b2 b3 d0 d1 d2 : Rat) (hh : h ≠ 0) :
    (bPlus h b0 b1 b2 b3 - bMinus h b0 b1 b2 b3)/h
      + lam*(dPlus h d0 d1 d2 + dMinus h d0 d1 d2)
    = b1 + 2*lam*d0 + h^2*(b3/24 + lam*d2/4) := by
  simp [bPlus, bMinus, dPlus, dMinus, Field.div_eq_mul_inv]
  grind

def cayley (h ell : Rat) : Rat := (2+h*ell)/(2-h*ell)

theorem cayley_dispersion (h ell : Rat) (hd : 2-h*ell ≠ 0) :
    2*(cayley h ell - 1) = h*ell*(cayley h ell + 1) := by
  simp [cayley, Field.div_eq_mul_inv]
  grind

-- T = A*(k^2+w+2*a*k) = -C*(k^2-w-2*a*k).
-- J = k*(A-C). This is the coefficient of the one exponential.
theorem one_exponential_edge
    (h ell R T lam J : Rat)
    (hh : h ≠ 0)
    (hcont : T*ell + lam*J = 0)
    (hdisp : 2*(R-1) = h*ell*(R+1)) :
    2*T*(R-1)/h + lam*J*(R+1) = 0 := by
  simp [Field.div_eq_mul_inv]
  grind

def edgeCoefficient (h lam a k w rm rn : Rat) : Rat :=
  (k^2+w+2*a*k)*(rm-rn)/h + lam*k*(rm+rn)

-- a=2, lambda=-2, h=1/10, (p1,q1)=(1,2), (p2,q2)=(0,3).
-- The coefficient of E1*E2 is nonzero when the continuous interaction
-- coefficient is retained. This is a counterexample to that ansatz,
-- NOT a proof that every possible integrable construction is impossible.
theorem unchanged_two_soliton_residual :
    let R1 : Rat := 77/83
    let R2 : Rat := 197/203
    (-1/72)*edgeCoefficient (1/10) (-2) 2 (-6) (-12) 1 (R1*R2)
    + (1/36)*edgeCoefficient (1/10) (-2) 2 0 (-6) R1 R2
    + (2/45)*edgeCoefficient (1/10) (-2) 2 0 6 R2 R1
    + (-1/720)*edgeCoefficient (1/10) (-2) 2 6 12 (R1*R2) 1
    = -27/168490 := by
  simp [edgeCoefficient, Field.div_eq_mul_inv]
  grind

-- For the same two waves, keep the constant and single-wave coefficients
-- fixed but replace the two interaction coefficients by X and Y.
-- Two coefficients of B f.g are 72*X+1/10 and 10*X-Y.
-- Thus the unchanged first bilinear equation already fixes both unknowns.
theorem interaction_coefficients_forced
    (X Y : Rat) (h11 : 72*X+1/10=0) (h21 : 10*X-Y=0) :
    X = -1/720 ∧ Y = -1/72 := by
  simp [Field.div_eq_mul_inv] at *
  grind

end DLWSemidiscrete
