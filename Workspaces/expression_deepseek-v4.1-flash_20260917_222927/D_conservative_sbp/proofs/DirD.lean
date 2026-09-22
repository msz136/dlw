/-
  Direction D -- Conservative differences / SBP.
  Discrete calculus and the discrete conservation law for the y-semidiscretised
  dispersive long wave (DLW) system.

  Only the y-direction is discretised; `x` and `t` stay continuous.  With
  `w = u_y` and the lattice operators

      D f j   = (f (j+1) - f j) / h        (forward difference, divided form)
      avg f j = (f j + f (j+1)) / 2        (lattice average)

  the candidate semidiscrete pair (lam = -2, a arbitrary) is

    (E1)  D_t u_j + D_x F_j = 0 ,   F_j = v_{x,j} + (avg(u)_j + 2a) D u_j
    (E2)  D_t v_j + D_x[ (avg(u)_j + 2a) v_j + D_x(D u_j) + 2 lam u_j ] = 0

  What is proved here is exactly the DISCRETE CALCULUS that the conservation
  argument needs: the product rule forced by the forward difference, the SBP
  boundary identity for the averaged nonlinearity, the skew-adjointness of `D`,
  and the telescoping boundary balance.  The analytic consequences (continuum
  limit, ill-posedness of the linearisation) are NOT formalised here and are
  reported as 实验验证 in proofs/CONCLUSIONS.md.

  Coefficient field: `Q`.  The identities are algebraic and hold over any field of
  characteristic different from two; `Q` lets `ring` normalise the numeral `2` of
  the lattice average without an extra `CharZero` hypothesis.

  Verified with:
    & 'C:\Users\msz\学术内容\_lean_shared\Check-Lean.ps1' `
        -Root <this proofs dir> -File <this file> -TimeoutSeconds 300
-/
import Common.Operators
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Algebra.BigOperators.Group.Finset.Lemmas
import Mathlib.Algebra.BigOperators.Ring.Finset

namespace DLW.DirD

open scoped BigOperators

/-- Forward difference in `y`, divided form.  Same object as `DLW.Common.fwd`,
    restated on `Int` for the local development. -/
def D (f : Int → ℚ) (h : ℚ) : Int → ℚ := fun j => (f (j + 1) - f j) / h

/-- Lattice average `(f j + f (j+1))/2`.  This is the averaging the discrete product
    rule FORCES; it is not the identity at finite `h`. -/
def avg (f : Int → ℚ) : Int → ℚ := fun j => (f j + f (j + 1)) / 2

/-! ## The discrete product rule -/

/-- **Symmetric product rule.** `D(x*y) j = (avg x j) * (D y j) + (avg y j) * (D x j)`.
    No correction term.  This is precisely the form that makes the averaged
    nonlinearity `avg u * D u` an exact lattice difference. -/
theorem d_avg_mul (x y : Int → ℚ) (h : ℚ) (hh : h ≠ 0) (j : Int) :
    D (fun i => x i * y i) h j = avg x j * D y h j + avg y j * D x h j := by
  unfold D avg
  field_simp
  ring

/-! ## Summation by parts for the averaged nonlinearity -/

/-- **SBP boundary identity for the averaged nonlinearity.**
    `sum_{j<N} (u_j + u_{j+1})(u_{j+1} - u_j) = u_N^2 - u_0^2`.
    The right side is a PURE BOUNDARY TERM, so over a full period
    (`u_0 = u_N`) the nonlinear term contributes zero net flux.  This is the exact
    discrete conservation of the nonlinear term, and the naive product
    `u_j * D u_j` does NOT have this property. -/
theorem avg_sbp (u : Nat → ℚ) (N : Nat) :
    (∑ j ∈ Finset.range N, (u j + u (j + 1)) * (u (j + 1) - u j))
      = u N ^ 2 - u 0 ^ 2 := by
  have hpt : ∀ j : Nat,
      (u j + u (j + 1)) * (u (j + 1) - u j) = u (j + 1) ^ 2 - u j ^ 2 := by
    intro j; ring
  calc (∑ j ∈ Finset.range N, (u j + u (j + 1)) * (u (j + 1) - u j))
      = ∑ j ∈ Finset.range N, (u (j + 1) ^ 2 - u j ^ 2) :=
        Finset.sum_congr rfl (fun j _ => hpt j)
    _ = u N ^ 2 - u 0 ^ 2 := by
        have htel := DLW.Common.telescoping u u N
        have hconv : (∑ j ∈ Finset.range N, (u (j + 1) ^ 2 - u j ^ 2))
            = ∑ j ∈ Finset.range N, (u (j + 1) * u (j + 1) - u j * u j) := by
          apply Finset.sum_congr rfl
          intro j _
          ring
        rw [hconv, htel]
        ring

/-- The same identity with the divided operators:
    `sum_j (avg u_j) * (D u_j) * (2h) = u_N^2 - u_0^2`. -/
theorem avg_sbp_divided (u : Nat → ℚ) (h : ℚ) (hh : h ≠ 0) (N : Nat) :
    (∑ j ∈ Finset.range N,
        (((u j + u (j + 1)) / 2) * ((u (j + 1) - u j) / h))) * (2 * h)
      = u N ^ 2 - u 0 ^ 2 := by
  have h1 : (∑ j ∈ Finset.range N,
        (((u j + u (j + 1)) / 2) * ((u (j + 1) - u j) / h))) * (2 * h)
      = ∑ j ∈ Finset.range N, (u j + u (j + 1)) * (u (j + 1) - u j) := by
    rw [Finset.sum_mul]
    apply Finset.sum_congr rfl
    intro j _
    field_simp
  rw [h1]
  exact avg_sbp u N

/-! ## Skew-adjointness of the forward difference -/

/-- **SBP / skew-adjointness of `D` on a periodic lattice.**
    `sum_j (x_{j+1}-x_j) y_j + sum_j x_{j+1} (y_{j+1}-y_j) = 0` when the boundary
    contributions vanish.  For periodic data the pairing with any sequence is
    antisymmetric: the discrete analogue of `int (d_y f) g = - int f (d_y g)`. -/
theorem d_skew_adjoint (x y : Nat → ℚ) (N : Nat) (hx : x N = x 0) (hy : y 0 = y N) :
    (∑ j ∈ Finset.range N, (x (j + 1) - x j) * y j)
      + (∑ j ∈ Finset.range N, x (j + 1) * (y (j + 1) - y j)) = 0 := by
  rw [DLW.Common.sbp_fwd_undivided x y N]
  rw [hx, hy]
  ring

/-- Divided form of the skew-adjointness identity. -/
theorem d_skew_adjoint_divided (x y : Nat → ℚ) (h : ℚ) (hh : h ≠ 0) (N : Nat)
    (hx : x N = x 0) (hy : y 0 = y N) :
    ((∑ j ∈ Finset.range N, ((x (j + 1) - x j) / h) * y j)
      + (∑ j ∈ Finset.range N, x (j + 1) * ((y (j + 1) - y j) / h))) * h = 0 := by
  have h1 : (∑ j ∈ Finset.range N, ((x (j + 1) - x j) / h) * y j) * h
      = ∑ j ∈ Finset.range N, (x (j + 1) - x j) * y j := by
    rw [Finset.sum_mul]
    apply Finset.sum_congr rfl
    intro j _
    field_simp
  have h2 : (∑ j ∈ Finset.range N, x (j + 1) * ((y (j + 1) - y j) / h)) * h
      = ∑ j ∈ Finset.range N, x (j + 1) * (y (j + 1) - y j) := by
    rw [Finset.sum_mul]
    apply Finset.sum_congr rfl
    intro j _
    field_simp
  have h3 : ((∑ j ∈ Finset.range N, ((x (j + 1) - x j) / h) * y j)
      + (∑ j ∈ Finset.range N, x (j + 1) * ((y (j + 1) - y j) / h))) * h
      = (∑ j ∈ Finset.range N, ((x (j + 1) - x j) / h) * y j) * h
        + (∑ j ∈ Finset.range N, x (j + 1) * ((y (j + 1) - y j) / h)) * h := by
    ring
  rw [h3, h1, h2]
  exact d_skew_adjoint x y N hx hy

/-! ## The discrete conservation / boundary balance -/

/-- **Exact discrete boundary balance (the discrete conservation law).**
    If the lattice source satisfies the flux form `F_{j+1} - F_j = -(h * s_j)` for
    all `j < N`, then the total source over the period is EXACTLY the boundary jump:
    `(sum_{j<N} s_j) * h = F_0 - F_N`.

    Applied to `(E1)` with `w_j := D u_j` and `s_j := (D_t w)_j` this says the
    conserved quantity `sum_j w_j` changes at the rate `(F_0 - F_N)/h`: it is
    conserved **iff** the boundary flux vanishes.  The boundary term is retained
    explicitly and never dropped. -/
theorem constraint_sbp_balance (F s : Nat → ℚ) (h : ℚ) (N : Nat)
    (hflow : ∀ j : Nat, j < N → F (j + 1) - F j = -(h * s j)) :
    (∑ j ∈ Finset.range N, s j) * h = F 0 - F N := by
  have key : ∀ j : Nat, j < N → s j * h = F j - F (j + 1) := by
    intro j hj
    have h1 := hflow j hj
    have h2 : h * s j = F j - F (j + 1) := by
      calc h * s j = -(F (j + 1) - F j) := by rw [h1]; ring
        _ = F j - F (j + 1) := by ring
    calc s j * h = h * s j := by ring
      _ = F j - F (j + 1) := h2
  have hcongr : (∑ j ∈ Finset.range N, s j * h)
      = ∑ j ∈ Finset.range N, (F j - F (j + 1)) := by
    apply Finset.sum_congr rfl
    intro j hj
    exact key j (Finset.mem_range.mp hj)
  have ht : (∑ j ∈ Finset.range N, (F j - F (j + 1))) = F 0 - F N := by
    have hsum : (∑ j ∈ Finset.range N, (F (j + 1) - F j)) = F N - F 0 := by
      have h := DLW.Common.telescoping F (fun _ : Nat => (1 : ℚ)) N
      simp only [mul_one] at h
      exact h
    calc (∑ j ∈ Finset.range N, (F j - F (j + 1)))
        = -(∑ j ∈ Finset.range N, (F (j + 1) - F j)) := by
          rw [← Finset.sum_neg_distrib]
          apply Finset.sum_congr rfl
          intro j _
          ring
      _ = -(F N - F 0) := by rw [hsum]
      _ = F 0 - F N := by ring
  rw [Finset.sum_mul, hcongr, ht]

/-- `D` commutes with the lattice shift: the discrete counterpart of
    `[d/dy, d/dx] = 0`, and the reason the flux form of `(E1)` preserves the
    constraint `w = D u` exactly. -/
theorem D_shift_comm (x : Int → ℚ) (h : ℚ) (j : Int) :
    D x h (j + 1) = (x (j + 2) - x (j + 1)) / h := by
  have hidx : j + 1 + 1 = j + 2 := by ring
  simp only [D]
  rw [hidx]

/-- `avg` commutes with the lattice shift. -/
theorem avg_shift_comm (x : Int → ℚ) (j : Int) :
    avg x (j + 1) = (x (j + 1) + x (j + 2)) / 2 := by
  have hidx : j + 1 + 1 = j + 2 := by ring
  simp only [avg]
  rw [hidx]

/-! ## What the conserved quantity is NOT -/

/-- **The conserved functional has a kernel, so it has no definite sign.**
    Every constant sequence is annihilated by `D`, so shifting `u` by any constant
    `c` changes the `L^2` norm by an arbitrary amount while leaving every lattice
    derivative `D u_j` -- and hence the conserved functional `sum_j D u_j` --
    unchanged.  Therefore that functional can never control `sum_j u_j^2`:
    **conservation implies no stability.**  Formal counterpart of the shared-spec
    warning that a conservation statement is not a stability statement. -/
theorem constraint_kernel (w : Int → ℚ) (h : ℚ) (c : ℚ) :
    (∀ j, w j = c) → ∀ j, D w h j = 0 := by
  intro hw j
  have h1 : w (j + 1) = c := hw (j + 1)
  have h2 : w j = c := hw j
  simp [D, h1, h2]

/-- The conserved density vanishes on the entire `y`-independent (zero-mode) sector:
    `u_j = u_{j+1}` for all `j` implies `D u_j = 0`. -/
theorem conserved_density_trivial_on_constants (u : Int → ℚ) (h : ℚ)
    (hu : ∀ j, u j = u (j + 1)) : ∀ j, D u h j = 0 := by
  intro j
  have h := hu j
  simp [D, h]

/-! ## Axiom audit for the headline theorems -/

#print axioms DLW.DirD.d_avg_mul
#print axioms DLW.DirD.avg_sbp
#print axioms DLW.DirD.avg_sbp_divided
#print axioms DLW.DirD.d_skew_adjoint
#print axioms DLW.DirD.d_skew_adjoint_divided
#print axioms DLW.DirD.constraint_sbp_balance
#print axioms DLW.DirD.constraint_kernel

end DLW.DirD
