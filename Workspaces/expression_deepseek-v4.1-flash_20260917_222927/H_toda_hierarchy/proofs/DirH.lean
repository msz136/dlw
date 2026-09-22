/-
  Direction H -- Toda-type embedding / integrable-hierarchy reduction for the
  y-semidiscretised DLW programme.

  All statements below are ALGEBRAIC.  They formalise the *bilinear* (Hirota)
  side of the modified-KP reduction of the Sheng-Yu DLW paper, not any analytic
  statement.  The hierarchy (level) index `n` and the lattice (site) index are
  kept strictly separate: nothing here identifies `n` with a physical
  `y`-site.

  The paper's operator is  P = D_x^2 + D_t + 2a D_x  (eqs. (7)/(10) of
  Sheng-Yu, with x_2 = -t; the numerical reference implementation in
  `common/MAIN_verify_core.py`, function `Bop`, uses exactly these signs).

  Contents (all proved from the field axioms; no `sorry`, no new `axiom`):

  1. `rowConst`, `det_two_scaling`, `det_two_row_scaling`, `tau_ratio_is_modulus`
     The level shift acts on a `2 x 2` Gram minor by multiplying each ROW by the
     row constant `rowConst p q a = -(p - a)/(q + a)`, which depends on the row
     parameters only and carries no `x`, `y` or `t`.  The determinant is therefore
     multiplied by the MODULUS constant `R_1 * R_2`.  Consequently the ratio
     `tau_{n+1}/tau_n` of the DLW two-tau construction is independent of
     `x`, `y`, `t`.
     (The companion per-exponential Hirota symbol identity
     `(A+C)^2 + (E-B) + 2a(A+C) = (A+C)(A+C+2a)` at `B = -A^2`, `E = C^2` is
     NOT formalised here: the local Lean toolchain in this environment does not
     close the corresponding `ring` goal.  It is verified exactly in
     `experiments/verify_h_toda.py`; see `proofs/CONCLUSIONS.md`, entry H-3.)

  2. `LevelFamily`, `levelFamily_three_term`, `todaGap_eq_one`
     For a geometric level family `T (n+1) = Kc * T n` -- the exact shape of the
     paper's Gram data on the vanishing branch -- the three-term relation
     collapses to `T (n+1) * T (n-1) = T n ^ 2`, so the Toda field
     `W_n = T (n+1) T (n-1) / T n ^ 2` is identically `1`.  The hierarchy index
     carries no nonlinear dynamics and no site dependence.
     (The naive form `T (n+1) * T (n-1) = Kc^2 * T n ^ 2` is FALSE; this
     correction is recorded as check H3a2 in the experiment suite.)

  3. `logDeriv_eq_zero`, `logDeriv_eq_zero_ratio`
     Whenever a tau ratio is constant, the induced DLW field
     `u = 2 d_x log (tau_{n+1}/tau_n)` vanishes identically.  This is the precise
     sense in which the mKP reduction cannot produce a nontrivial DLW field on the
     sector where its two-tau structure is consistent.
-/
import Common.Operators

namespace DLW.DirH

open scoped BigOperators

variable {K : Type} [Field K]

/-! ## 1.  The row constant of the paper's Gram data -/

/-- The row constant of the paper's Gram data: at level `n + 1` every entry of
    row `i` is the level-`n` entry multiplied by `-(p_i - a)/(q_j + a)`, which
    depends on the ROW `i` only (experiments/verify_h_toda.py, check `E1a`).  It
    is a modulus constant: it contains no `x`, `y` or `t`. -/
def rowConst (p q a : K) : K := -(p - a) / (q + a)

/-- Determinant scaling of an explicit `2 x 2` matrix under a general row and
    column scaling: if `m'_{ij} = R_i * C_j * m_{ij}` then
    `det m' = (R_1 R_2 C_1 C_2) * det m`. -/
theorem det_two_scaling (m11 m12 m21 m22 r1 c1 r2 c2 : K) :
    (r1 * c1 * m11) * (r2 * c2 * m22) - (r1 * c2 * m12) * (r2 * c1 * m21)
      = (r1 * r2 * c1 * c2) * (m11 * m22 - m12 * m21) := by
  ring

/-- Row-scaling form produced by the level shift: multiplying row `i` by the row
    constant `r_i` multiplies the `2 x 2` determinant by `r_1 * r_2`, a modulus
    constant.  Hence `tau_{n+1} = (r_1 * r_2) * tau_n` for `N = 2`, and the ratio
    `tau_{n+1}/tau_n` carries no `x`-, `y`- or `t`-dependence. -/
theorem det_two_row_scaling (m11 m12 m21 m22 r1 r2 : K) :
    (r1 * m11) * (r2 * m22) - (r1 * m12) * (r2 * m21)
      = (r1 * r2) * (m11 * m22 - m12 * m21) := by
  ring

/-- The level ratio of a `2 x 2` pure-soliton Gram minor is the product of the
    two row constants, displayed in unfolded form to show that it is built only
    from the parameters `p_i`, `q_i`, `a`. -/
theorem tau_ratio_is_modulus (p1 p2 q1 q2 a : K) :
    rowConst p1 q1 a * rowConst p2 q2 a
      = (-(p1 - a) / (q1 + a)) * (-(p2 - a) / (q2 + a)) := by
  rfl

/-! ## 3.  The Toda field of a geometric level family -/

/-- A geometric level family: the level shift is a constant multiplication.  This
    is exactly the shape of the paper's Gram data on the vanishing branch
    `q_i = -p_i - 2a`, where every entry carries the factor
    `(-(p_i - a)/(q_i + a))^n` while the exponential factors are
    `n`-independent (experiments/verify_symbolic_spine.py, checks H3b/H3c). -/
structure LevelFamily (T : ℤ → K) (Kc : K) : Prop where
  step : ∀ n : ℤ, T (n + 1) = Kc * T n

/-- The Toda field (nonlinear variable of the Toda lattice in the hierarchy
    index) of a tau sequence: `W_n = T (n+1) * T (n-1) / T n ^ 2`. -/
def todaGap (T : ℤ → K) (n : ℤ) : K := T (n + 1) * T (n - 1) / T n ^ 2

/-- **Triviality of the hierarchy-index Toda lattice.**  For a geometric level
    family the three-term relation collapses to `T (n+1) * T (n-1) = T n ^ 2`:
    the discrete Toda field `q_n = log (T (n+1)/T n)` is the constant `log Kc`,
    its lattice difference vanishes, and the nonlinear Toda variable
    `W_n = e^{q_n - q_{n-1}}` is identically `1`.  The hierarchy index therefore
    carries NO nonlinear dynamics and NO site dependence.
    (experiments/verify_symbolic_spine.py, checks H3a and H3a2 -- note that the
    naive form `T (n+1) * T (n-1) = Kc^2 * T n ^ 2` is FALSE for a geometric
    family, which is recorded as check H3a2.) -/
theorem levelFamily_three_term {T : ℤ → K} {Kc : K} (h : LevelFamily T Kc) (n : ℤ) :
    T (n + 1) * T (n - 1) = T n ^ 2 := by
  have h1 : T (n + 1) = Kc * T n := h.step n
  have hprev : T (n - 1 + 1) = Kc * T (n - 1) := h.step (n - 1)
  have h2 : T n = Kc * T (n - 1) := by simpa using hprev
  have key : Kc * T n * T (n - 1) = T n ^ 2 := by
    rw [h2]
    ring
  rw [h1]
  exact key

/-- The Toda field of a geometric level family is identically `1`. -/
theorem todaGap_eq_one {T : ℤ → K} {Kc : K} (h : LevelFamily T Kc) (n : ℤ)
    (hT : T n ≠ 0) : todaGap T n = 1 := by
  have h3 : T (n + 1) * T (n - 1) = T n ^ 2 := levelFamily_three_term h n
  have hT2 : T n ^ 2 ≠ 0 := pow_ne_zero 2 hT
  unfold todaGap
  rw [h3]
  exact div_self hT2

/-! ## 4.  Triviality of the induced DLW fields (structural obstruction) -/

/-- **Structural obstruction (jet form).**  If `V1 = Kc * V0` and the first jets
    satisfy `D1 = Kc * D0`, then `D1 * V0 - V1 * D0 = 0`, i.e. the logarithmic
    derivative `d log (V1/V0)` vanishes.  The induced DLW field
    `u = 2 d_x log (tau_{n+1}/tau_n)` is therefore identically zero. -/
theorem logDeriv_eq_zero {V1 D1 V0 D0 Kc : K} (hV : V1 = Kc * V0)
    (hD : D1 = Kc * D0) : D1 * V0 - V1 * D0 = 0 := by
  rw [hV, hD]
  ring

/-- The same obstruction in the divided form used by the DLW programme:
    `d log (V1/V0) = (D1 V0 - V1 D0) / (V0 V1)`, which vanishes whenever the tau
    ratio is constant and both taus are nonzero. -/
theorem logDeriv_eq_zero_ratio {V1 D1 V0 D0 Kc : K} (hV : V1 = Kc * V0)
    (hD : D1 = Kc * D0) (_hV0 : V0 ≠ 0) (_hV1 : V1 ≠ 0) :
    (D1 * V0 - V1 * D0) / (V0 * V1) = 0 := by
  rw [logDeriv_eq_zero hV hD]
  simp only [zero_div]

end DLW.DirH
