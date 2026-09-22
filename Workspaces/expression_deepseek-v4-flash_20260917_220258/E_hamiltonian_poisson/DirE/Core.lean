/-
DLW y-discretization study: shared algebraic core.

Everything here is purely algebraic over an arbitrary field `K`. There is no
analysis: no `Real.exp`, no limits, no differentiability, no integrals.
Derivative data is supplied pointwise through the `Jet` structure; bridging
that data to actual smooth functions is an explicit step taken outside this
file and must be reported as an unformalized bridge wherever it is used.

Reference: H.-H. Sheng, G.-F. Yu, "Solitons, breathers and rational solutions
for a (2+1)-dimensional dispersive long wave system", Physica D 432 (2022)
133140, DOI 10.1016/j.physd.2021.133140, equations (1)-(8).

Maintained by the integrating agent. Directions may copy this file into their
own project; changes must be proposed back to the integrating agent instead of
being made here.

Builds with the core Lean 4.34 toolchain only (no Mathlib):
  import Init.Grind.Ring.Field    -- provides Field, IsCharP and ring reasoning
  import Init.GrindInstances.Ring.Rat
  open Lean.Grind                 -- the `grind` tactic
-/
import Init.Grind.Ring.Field
import Init.GrindInstances.Ring.Rat

open Lean.Grind

namespace DLWLean

universe u

variable {K : Type u} [Field K]

/-- Pointwise derivative data of a tau function: value, ∂x, ∂x², ∂t.
The `y` direction is deliberately absent: it is the direction that gets
discretized, so its derivatives never appear as pointwise data. -/
structure Jet (K : Type u) where
  val : K
  dx : K
  dxx : K
  dt : K

/-- The jet of the constant function 1. -/
def Jet.one : Jet K := ⟨1, 0, 0, 0⟩

/-- The jet of a constant function c. -/
def Jet.const (c : K) : Jet K := ⟨c, 0, 0, 0⟩

/-- Hirota operator: D_x f·g = f_x g - f g_x. -/
def Dx (F G : Jet K) : K := F.dx * G.val - F.val * G.dx

/-- Hirota operator: D_t f·g = f_t g - f g_t. -/
def Dt (F G : Jet K) : K := F.dt * G.val - F.val * G.dt

/-- Hirota operator: D_x² f·g = f_xx g - 2 f_x g_x + f g_xx. -/
def Dxx (F G : Jet K) : K := F.dxx * G.val - 2 * (F.dx * G.dx) + F.val * G.dxx

/-- The paper's operator B = D_x² + D_t + 2a D_x. -/
def B (a : K) (F G : Jet K) : K := Dxx F G + Dt F G + 2 * a * Dx F G

/-- D_x is antisymmetric. -/
theorem Dx_antisymm (F G : Jet K) : Dx F G = -Dx G F := by
  simp only [Dx]
  grind

/-- D_t is antisymmetric. -/
theorem Dt_antisymm (F G : Jet K) : Dt F G = -Dt G F := by
  simp only [Dt]
  grind

/-- D_x² is symmetric. -/
theorem Dxx_symm (F G : Jet K) : Dxx F G = Dxx G F := by
  simp only [Dxx]
  grind

/-- Only the even part of `B` survives symmetrization: the `D_t` and `2a D_x`
terms cancel. This is the algebraic reason why `B f·g = 0` is *not* a symmetric
condition, and why a second, independent equation is needed. -/
theorem B_add_swap (a : K) (F G : Jet K) : B a F G + B a G F = 2 * Dxx F G := by
  simp only [B, Dx, Dt, Dxx]
  grind

/-- On the diagonal, `B` reduces to `D_x²`: for a single tau function the
`D_t` and `D_x` parts of `B` vanish identically. -/
theorem B_self (a : K) (F : Jet K) : B a F F = Dxx F F := by
  simp only [B, Dx, Dt]
  grind

/-- With `g = 1` the bilinear equation `B f·g = 0` is the linear equation
`f_xx + f_t + 2a f_x = 0`. -/
theorem B_one_right (a : K) (F : Jet K) :
    B a F Jet.one = F.dxx + F.dt + 2 * a * F.dx := by
  simp only [B, Dxx, Dt, Dx, Jet.one]
  grind

/-- With `f = 1` the bilinear equation `B f·g = 0` is the linear equation
`g_xx - g_t - 2a g_x = 0` (note the signs: `D_x`, `D_t` are antisymmetric but
`D_x²` is symmetric, so `D_x² 1·g = +g_xx`). -/
theorem B_one_left (a : K) (G : Jet K) :
    B a Jet.one G = G.dxx - G.dt - 2 * a * G.dx := by
  simp only [B, Dxx, Dt, Dx, Jet.one]
  grind

/-! ### The variable transformation on pointwise data

`u = 2 (ln(f/g))_x = 2 (f_x/f - g_x/g)`. Over a field this needs `f ≠ 0`,
`g ≠ 0`; the definition below is total, and *every* theorem about it must
carry the nonzero hypotheses explicitly. There is no `log` here: this is the
logarithmic derivative written rationally, which is exactly the form in which
a discrete VT can be inverted without formalizing `log`. -/

/-- Rational form of the VT for `u`: `2 (f_x/f - g_x/g)`. -/
def uFromJets (F G : Jet K) : K := 2 * (F.dx / F.val - G.dx / G.val)

/-- `uFromJets` agrees with `2 D_x f·g / (f g)` whenever `f g ≠ 0`. -/
theorem uFromJets_eq (F G : Jet K) (hF : F.val ≠ 0) (hG : G.val ≠ 0) :
    uFromJets F G = 2 * Dx F G / (F.val * G.val) := by
  simp only [uFromJets, Dx, Field.div_eq_mul_inv]
  grind

/-! ### Lattice objects shared by all directions

`Seq K` is a bi-infinite family of tau jets indexed by the y-lattice. All
directions must use these same definitions when they discuss the staggered
pair, so that results can be compared. -/

/-- A bi-infinite family of tau jets indexed by the y-lattice. -/
abbrev Seq (K : Type u) : Type u := Int → Jet K

/-- Forward shift in the y-index. -/
def shift (F : Seq K) : Seq K := fun j => F (j + 1)

/-- `n`-fold forward shift. -/
def shiftN : Nat → Seq K → Seq K
  | 0, F => F
  | n + 1, F => shift (shiftN n F)

/-- The staggered edge equation `(B - h D_x) F_j·G_j = 0`, as a residual
(so that statements can say "this vanishes" rather than assume it). -/
def edgeMinus (a h : K) (F G : Seq K) (j : Int) : K :=
  B a (F j) (G j) - h * Dx (F j) (G j)

/-- The staggered edge equation `(B + h D_x) F_j·G_{j+1} = 0`, as a residual. -/
def edgePlus (a h : K) (F G : Seq K) (j : Int) : K :=
  B a (F j) (G (j + 1)) + h * Dx (F j) (G (j + 1))

/-- The earlier *centered same-point* candidate, kept only for comparison. Its
continuous two-soliton ansatz is refuted (see `lean-toda`, `DLWSemidiscrete.lean`
and `check_dlw_candidate.py`); it is recorded here so that directions A and G can
refer to the same object. -/
def centeredEdge (a lam h : K) (F G : Seq K) (j : Int) : K :=
  (B a (F (j + 1)) (G j) - B a (F j) (G (j + 1))) / h
    + lam * (Dx (F (j + 1)) (G j) + Dx (F j) (G (j + 1)))

end DLWLean
