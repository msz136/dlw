/-
  DLW common discrete-operator library.

  Shared by all eight direction subagents.  Nothing here assumes any particular
  discretisation of the DLW system; it provides lattice difference operators,
  their kernels, and discrete summation by parts.

  Verified with the shared entry point:
    & 'C:\Users\msz\学术内容\_lean_shared\Check-Lean.ps1' -Root <proofs> -File <file>
-/
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Algebra.BigOperators.Group.Finset.Lemmas
import Mathlib.Algebra.BigOperators.Ring.Finset

namespace DLW.Common

open scoped BigOperators

variable {K : Type} [Field K]

/-! ## Difference operators on the bi-infinite lattice -/

/-- Forward difference on the bi-infinite lattice. -/
def fwd (u : Int → K) (h : K) : Int → K := fun j => (u (j + 1) - u j) / h

/-- Backward difference on the bi-infinite lattice. -/
def bwd (u : Int → K) (h : K) : Int → K := fun j => (u j - u (j - 1)) / h

/-- Centred difference on the bi-infinite lattice. -/
def ctr (u : Int → K) (h : K) : Int → K := fun j => (u (j + 1) - u (j - 1)) / (2 * h)

/-- Second centred difference on the bi-infinite lattice. -/
def ctr2 (u : Int → K) (h : K) : Int → K :=
  fun j => (u (j + 1) - 2 * u j + u (j - 1)) / h ^ 2

/-- The centred difference annihilates constants: its kernel is non-trivial.
    This is the lattice counterpart of "d_y kills constants" and is exactly why
    the constraint `w = u_y` needs a mean / zero-mode convention. -/
theorem ctr_const (c : K) (h : K) : ctr (fun _ => c) h = fun _ => 0 := by
  funext j
  simp [ctr]

/-- The centred difference annihilates any `y`-independent sequence, not just
    constants.  Hence `ctr` has an infinite-dimensional kernel on
    `periodic` grids, and `w = u_y` cannot be inverted without a convention. -/
theorem ctr_kernel (w : Int → K) (h : K) :
    (∀ j, w (j + 1) = w (j - 1)) → ctr w h = fun _ => 0 := by
  intro hw
  funext j
  simp only [ctr]
  rw [hw j]
  ring

/-! ## Summation by parts on a finite interval -/

section SBP

/-- Telescoping identity for a finite lattice interval. -/
theorem telescoping (u v : Nat → K) (N : Nat) :
    (∑ j ∈ Finset.range N, (u (j + 1) * v (j + 1) - u j * v j))
      = u N * v N - u 0 * v 0 := by
  induction N with
  | zero => simp
  | succ n ih =>
      rw [Finset.sum_range_succ, ih]
      ring

/-- Core summation-by-parts (SBP) identity for the forward difference in
    undivided form.  Exact for every `N`, every `K`, every `u`, `v`.
    The boundary term `u N * v N - u 0 * v 0` is explicit: dropping it is
    precisely the error direction D must not make. -/
theorem sbp_fwd_undivided (u v : Nat → K) (N : Nat) :
    (∑ j ∈ Finset.range N, (u (j + 1) - u j) * v j)
      + (∑ j ∈ Finset.range N, u (j + 1) * (v (j + 1) - v j))
      = u N * v N - u 0 * v 0 := by
  rw [← Finset.sum_add_distrib]
  have h : (∑ j ∈ Finset.range N,
        ((u (j + 1) - u j) * v j + u (j + 1) * (v (j + 1) - v j)))
      = ∑ j ∈ Finset.range N, (u (j + 1) * v (j + 1) - u j * v j) := by
    apply Finset.sum_congr rfl
    intro j _
    ring
  rw [h]
  exact telescoping u v N

/-- Summation by parts for the forward difference in divided form. -/
theorem sbp_fwd (u v : Nat → K) (h : K) (hh : h ≠ 0) (N : Nat) :
    (∑ j ∈ Finset.range N, ((u (j + 1) - u j) / h) * v j) * h
        + (∑ j ∈ Finset.range N, u (j + 1) * ((v (j + 1) - v j) / h)) * h
      = u N * v N - u 0 * v 0 := by
  have h1 : (∑ j ∈ Finset.range N, ((u (j + 1) - u j) / h) * v j) * h
      = ∑ j ∈ Finset.range N, (u (j + 1) - u j) * v j := by
    rw [Finset.sum_mul]
    apply Finset.sum_congr rfl
    intro j _
    field_simp
  have h2 : (∑ j ∈ Finset.range N, u (j + 1) * ((v (j + 1) - v j) / h)) * h
      = ∑ j ∈ Finset.range N, u (j + 1) * (v (j + 1) - v j) := by
    rw [Finset.sum_mul]
    apply Finset.sum_congr rfl
    intro j _
    field_simp
  rw [h1, h2]
  exact sbp_fwd_undivided u v N

/-- The centred difference has zero total sum over a symmetric interval, i.e.
    it lands in the zero-mean subspace.  This is the discrete solvability
    condition needed to invert `ctr` (the "mean condition"). -/
theorem sum_range_ctr (u : Int → K) (N : Nat) :
    (∑ j ∈ Finset.range N, (u ((j : Int) + 1) - u (j : Int)))
      = u (N : Int) - u 0 := by
  have hcast : ∀ j : Nat, ((j : Int) + 1) = ((j + 1 : Nat) : Int) := by
    intro j; push_cast; ring
  rw [show (∑ j ∈ Finset.range N, (u ((j : Int) + 1) - u (j : Int)))
        = ∑ j ∈ Finset.range N,
            (u (((j + 1 : Nat)) : Int) - u ((j : Nat) : Int)) from by
      apply Finset.sum_congr rfl
      intro j _
      rw [hcast j]]
  have h := telescoping (fun j : Nat => u (j : Int)) (fun _ : Nat => (1 : K)) N
  simpa using h

end SBP

end DLW.Common
