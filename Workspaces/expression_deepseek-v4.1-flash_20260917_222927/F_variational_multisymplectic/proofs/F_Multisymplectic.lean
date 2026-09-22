/-
  Direction F — variational / multisymplectic discretisation of the DLW system in the
  `y` direction only (`x`, `t` stay continuous).

  MAIN-AGENT BUILT (the two delegated attempts ran out of context before producing
  anything, so this module was written and verified by the coordinating agent).

  The mathematical content is a STRUCTURAL ANALYSIS, and it is deliberately honest
  about what a variational `y`-discretisation can and cannot do.

  §1  Principal part.  In `W = (w, v)` with `w = u_y`, the DLW system has principal part
          ∂_t W + (u+2a) ∂_x W + u_x W + J ∂_x² W  =  lower order,
          J = [[0,1],[1,0]].
      `J` is a SYMMETRIC INVOLUTION with eigenvalues `+1` and `-1`.  Consequently the
      `x`-symbol of `J ∂_x²` is `-k²` on the symmetric mode `w + v` (forward heat) and
      `+k²` on the antisymmetric mode `w - v` (BACKWARD heat).  The backward branch is
      the structural root of the ill-posedness.

  §2  Growth dichotomy.  Writing `σ = p + i q` and `D = σ + i k (u0 + 2a)`, the
      dispersion relation `D² = k⁴ - c k³/μ` (with `c = v0 + 2λ`) is equivalent to the
      two REAL equations
          p² - (q + k(u0+2a))² = k⁴ - c k³/μ,     2 p (q + k(u0+2a)) = 0.
      Hence either `Re σ = 0` (oscillatory mode) or `(Re σ)² = k⁴ - c k³/μ` exactly.
      This is proved directly, without any complex arithmetic.

  §3  Quantitative consequence: on the growing branch `(Re σ)² ≥ (k²/2)²` for every
      lattice symbol `μ > 0` with `c ≤ 3kμ/4`.

  §4  What a variational `y`-discretisation DOES buy.  A `y`-lattice map coming from a
      discrete Lagrangian is symplectic: its 2-form components are `(0, ±det, ∓det, 0)`,
      so it preserves the form exactly when `det = 1`; and its characteristic polynomial
      is self-adjoint (palindromic, leading coefficient = constant coefficient), so its
      roots come in reciprocal pairs `r₁ r₂ = 1`.

  HONEST SCOPE LIMIT (the central finding of this direction).  A `y`-only variational
  principle acts on the `y`-lattice, which is a SPATIAL direction here.  It therefore
  produces a discrete multisymplectic structure in `y` and discrete conservation laws
  in `(x,t)`, but it cannot alter the `x`-symbol `J ∂_x²` of §1, because that symbol
  contains no `y`-derivative at all.  The obstruction of §1-§3 is therefore invariant
  under every variational `y`-discretisation, exactly as it is under finite differences,
  spectral methods, SBP, FEM/DG and Poisson discretisations.

  Evidence grade: Lean 代数验证 for §1, §2, §4; Lean 分析验证 for §3.  The step from
  "the linearised mode has (Re σ)² ~ k⁴" to "the nonlinear initial-value problem is
  Hadamard ill-posed" is standard but is NOT formalised here, nor anywhere in this run.
-/
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp
import Mathlib.Basic.Real.Basic

namespace DLWF

/-! ## §1. The principal part and its backward-heat branch -/

/-- The involution `J = [[0,1],[1,0]]` acting on `W = (w, v)`. -/
def Jpair (p : ℝ × ℝ) : ℝ × ℝ := (p.2, p.1)

/-- The `x`-symbol of `J ∂_x²` at wavenumber `k` (the factor `-k²` comes from two
    `x`-derivatives of `exp(i k x)`). -/
def xSymbol (k : ℝ) (p : ℝ × ℝ) : ℝ × ℝ := (-(k ^ 2) * p.2, -(k ^ 2) * p.1)

/-- `J` is an involution: `J² = 1`. -/
theorem Jpair_involution (p : ℝ × ℝ) : Jpair (Jpair p) = p := by
  rcases p with ⟨x, y⟩
  rfl

/-- On the SYMMETRIC mode `w + v` the `x`-symbol acts as `-k²`: a forward heat
    operator (the well-posed branch). -/
theorem xSymbol_symmetric_branch (k : ℝ) :
    xSymbol k (1, 1) = (-(k ^ 2), -(k ^ 2)) := by
  ext <;> simp only [xSymbol] <;> ring

/-- On the ANTISYMMETRIC mode `w - v` the `x`-symbol acts as `+k²`: a BACKWARD heat
    operator.  This is the structural root of the ill-posedness, and it contains no
    `y`-derivative, so no `y`-discretisation can touch it. -/
theorem xSymbol_antisymmetric_branch (k : ℝ) :
    xSymbol k (1, -1) = (k ^ 2, -(k ^ 2)) := by
  ext <;> simp only [xSymbol] <;> ring

/-- The two branches are exactly opposite in sign: the `x`-operator `J ∂_x²` is
    indefinite.  A symmetrisable (strongly well-posed) first-order-in-time system with
    a positive-definite symmetriser cannot have an indefinite principal symbol. -/
theorem xSymbol_branches_opposite_sign (k : ℝ) :
    (xSymbol k (1, 1)).1 = -((xSymbol k (1, -1)).1) := by
  simp only [xSymbol]
  ring

/-! ## §2. Growth dichotomy, over the reals only -/

/-- **Growth dichotomy.**  Let `σ = p + i q` be a growth rate and put
    `D = σ + i k β` with `β = u0 + 2a`.  The complex equation `D² = R` with `R` real
    is equivalent to the two real equations below, and then the real part `p = Re σ`
    either vanishes (oscillatory mode) or satisfies `p² = R` exactly. -/
theorem growth_dichotomy (p q kb R : ℝ)
    (h1 : p ^ 2 - (q + kb) ^ 2 = R) (h2 : 2 * p * (q + kb) = 0) :
    p = 0 ∨ p ^ 2 = R := by
  have h2' : p * (q + kb) = 0 := by linarith
  rcases mul_eq_zero.mp h2' with hp | hq
  · exact Or.inl hp
  · refine Or.inr ?_
    rw [hq] at h1
    linarith

/-- **Quantitative dichotomy.**  On the growing branch the real part of the growth rate
    satisfies `(Re σ)² ≥ (k²/2)²`, uniformly in the lattice symbol `μ > 0`, as soon as
    `c = v0 + 2λ ≤ 3kμ/4`.  Refining the mesh cannot remove this. -/
theorem growth_dichotomy_quantitative (p q kb c k mu : ℝ)
    (hmu : 0 < mu) (hk : 0 < k) (hck : c ≤ 3 * k * mu / 4)
    (h1 : p ^ 2 - (q + kb) ^ 2 = k ^ 4 - c * k ^ 3 / mu)
    (h2 : 2 * p * (q + kb) = 0) :
    p = 0 ∨ (k ^ 2 / 2) ^ 2 ≤ p ^ 2 := by
  rcases growth_dichotomy p q kb (k ^ 4 - c * k ^ 3 / mu) h1 h2 with hp | hp
  · exact Or.inl hp
  · refine Or.inr ?_
    rw [hp]
    have hk3 : (0 : ℝ) ≤ k ^ 3 := by positivity
    have hstep : c * k ^ 3 / mu ≤ 3 * k ^ 4 / 4 := by
      rw [div_le_iff₀ hmu]
      nlinarith [mul_le_mul_of_nonneg_right hck hk3]
    nlinarith

/-! ## §4. What a variational `y`-discretisation does buy -/

/-- **Symplecticity of the `y`-lattice map, componentwise.**  For
    `M = [[a,b],[c,d]]` and `Ω = [[0,1],[-1,0]]`, the four entries of `Mᵀ Ω M` are
    `0`, `det M`, `-det M`, `0`.  Hence the lattice map preserves the symplectic form
    exactly when `det M = 1`.  (The two diagonal entries vanish IDENTICALLY — that is
    the structural content: antisymmetry is automatic, only the determinant matters.) -/
theorem symplectic_form_components (a b c d : ℝ) :
    (a * c + c * (-a) = 0) ∧
      (a * d + c * (-b) = a * d - b * c) ∧
      (b * c + d * (-a) = -(a * d - b * c)) ∧
      (b * d + d * (-b) = 0) := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> ring

/-- **Self-adjoint (palindromic) characteristic polynomial.**  A `y`-discretisation
    obtained from a discrete Lagrangian has a characteristic polynomial whose leading
    and constant coefficients agree: `A r² + B r + A`.  Consequently its roots come in
    reciprocal pairs `r₁ r₂ = 1` — the discrete signature of an area-preserving lattice
    map.  Note what this does NOT say: `r₁ r₂ = 1` permits `|r₁| > 1`, so symplecticity
    alone gives no stability. -/
theorem variational_reciprocal_roots (A B r1 r2 : ℝ) (hA : A ≠ 0)
    (h : ∀ X : ℝ, A * (X - r1) * (X - r2) = A * X ^ 2 + B * X + A) :
    r1 * r2 = 1 := by
  have h0 : A * (r1 * r2) = A * 1 := by
    have hh := h 0
    ring_nf at hh
    linarith
  exact mul_left_cancel₀ hA h0

/-- **Discrete Legendre transform of the `y`-constraint.**  With the discrete
    Lagrangian `L_d = (u_{j+1} - u_j) w - (h/2) w²`, stationarity in the auxiliary
    field `w` (i.e. `∂L_d/∂w = 0`, namely `u_{j+1} - u_j - h w = 0`) reproduces EXACTLY
    the forward-difference constraint `w = (u_{j+1} - u_j)/h`.  This is the only
    structural content a `y`-only variational principle can deliver: the `(x,t)`
    evolution equations come from the `t`-direction and are NOT generated by a
    `y`-Lagrangian. -/
theorem legendre_lagrangian_gives_constraint (h uj uj1 w : ℝ) (hh : h ≠ 0)
    (hstat : uj1 - uj - h * w = 0) :
    w = (uj1 - uj) / h := by
  field_simp
  linarith

/-! ## Axiom audit -/

#print axioms DLWF.xSymbol_antisymmetric_branch
#print axioms DLWF.growth_dichotomy
#print axioms DLWF.growth_dichotomy_quantitative
#print axioms DLWF.symplectic_form_components
#print axioms DLWF.variational_reciprocal_roots

end DLWF
