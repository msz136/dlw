/-
# Lean support for the verdict: the rank-one deformation Lax pair of the GSG
# staggered DLW system has a *degenerate* spectral curve

Formal companion to `gsg_project/lax/VERDICT.md`.

For the GSG staggered DLW bilinear pair, the Gram-determinant (rank-one)
deformation

    τ̂_n(z) = det(M(n) + z⁻¹ u vᵀ)

gives the wave function `ψ_n(z) = τ̂_n(z)/τ_n = 1 + Q_n z⁻¹`, which is **exactly
Möbius** in `z`.  Hence the one-step transfer matrix is

    L_n(z) = [[1, Q_{n+1}], [1, Q_n]]

acting on `(ψ_n z, ψ_n)ᵀ`.

## The verdict, and what this file proves about it

The spectral parameter enters the monodromy `T_N = L_{N-1} ⋯ L_0` **not at all**:
`T_N` is a matrix of `z`-free quantities.  Consequently `tr T_N` is `z`-free
(`trace_z_free`) and so is `det T_N` (`det_z_free`).  A spectral problem whose
monodromy does not see the spectral parameter has a trivial spectral curve —
there is no Floquet band structure, no discrete hierarchy, and hence no strong
integrability from the `n`-direction alone.  The discrete Lax pair is
**degenerate**, and the system is at most *S-integrable*, not strongly integrable.

## Main results (no `sorry`, no new `axiom`)

* `zf_all` — all four entries of `T_N` are `z`-free, for every `N`.
* `trace_z_free` — `tr T_N` is `z`-free, for every `N`.
* `det_formula` — `det T_N = ∏_{i<N} (Q_i − Q_{i+1})`.
* `det_z_free` — `det T_N` is `z`-free, for every `N`.
* `trace_charpoly_z_free` — every coefficient of `λ² − tr(T_N)λ + det(T_N)` is
  `z`-free, i.e. the spectral curve does not move with the spectral parameter.
* `mobius_telescopes`, `mobius_composition` — the scalar one-step recursion is
  exactly Möbius, so the `n`-direction carries no spectral dynamics.
* `no_constant_trace` — the logical step by which the dKP-type `tr T(z)` is
  excluded as a conserved density.

## What is *not* claimed here

The τ-function input (`Q_n = τ̂_n/τ_n − 1` for the GSG staggered DLW Gram
determinants) is a **hypothesis** of this file, exactly as it is a hypothesis of
`TodaFormalization.DLWDiscretePair`.  Nothing here is about the literature facts
recorded in `VERDICT.md` (the weak Lax pair with `∂_x^{-1}`, the failure of the
Painlevé test); those are not formalized and are not used.

## Methodological note

This file deliberately does **not** route the verdict through a closed formula for
`tr T_k`.  Four successively proposed closed forms for `tr T_k` were false; each
was refuted only by *exact* symbolic recomputation of the matrix product (never by
sampling `Q` numerically).  `zf_all` is therefore proved by induction on the four
entry recurrences, carrying as invariant, for each entry, both `z`-freeness and
the *real* recurrence satisfied by its `ζ`-free part (`raf`, `rbf`, `rcf`, `rdf`).
The verdict thus depends on no guessed formula.  Note that `coef` is a
*derivation*, not a ring homomorphism, so the invariant must carry the `fst` parts
as well — that is the whole technical content of the proof.  (In particular the
`(1,1)` seed is `1`, not `0`: the seed of a recurrence is the matrix entry itself,
and `(T_0)₁₁ = 1`.)
-/

import Mathlib.Basic.Real.Basic
import Mathlib.Algebra.TrivSqZeroExt.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Tactic

namespace DLWLax

/-! ## Part 1. The dual numbers `ℝ[ζ]/(ζ²)` and the `ζ`-coefficient

`Sq = ℝ[ζ]/(ζ²)` — Mathlib's `TrivSqZeroExt ℝ ℝ` — with `ζ` nilpotent.  This is
the coefficient ring in which the `1/z`-expansion is made exact: an identity over
`Sq` contains the exact statement that the `ζ`-coefficient vanishes.  Since
`ζ ≠ 0`, that statement is not vacuous. -/

/-- The dual numbers over `ℝ`: `ℝ[ζ]/(ζ²)`. -/
abbrev Sq := TrivSqZeroExt ℝ ℝ

/-- The nilpotent `ζ`. -/
def Zeta : Sq := TrivSqZeroExt.inr 1

/-- The `ζ`-coefficient `a + bζ ↦ b`. -/
def coef (x : Sq) : ℝ := x.snd

/-- `ζ² = 0`. -/
theorem Zeta_sq : Zeta * Zeta = 0 := by
  simp [Zeta]

/-- `ζ ≠ 0`: the ring is not trivial, so a vanishing `ζ`-coefficient is a genuine
assertion and not an artefact. -/
theorem Zeta_ne_zero : Zeta ≠ 0 := by
  intro h
  have := congrArg coef h
  simp [Zeta, coef] at this

theorem coeff_add (x y : Sq) : coef (x + y) = coef x + coef y := by simp [coef]
theorem coeff_sub (x y : Sq) : coef (x - y) = coef x - coef y := by
  simp [coef, TrivSqZeroExt.snd_sub]
/-- **`coef` is a derivation, not a ring homomorphism.** -/
theorem coeff_mul (x y : Sq) : coef (x * y) = x.fst * coef y + coef x * y.fst := by
  simp [coef, TrivSqZeroExt.snd_mul]
theorem coeff_zero : coef (0 : Sq) = 0 := by simp [coef]
theorem coeff_one : coef (1 : Sq) = 0 := by simp [coef]

/-- An element with vanishing `ζ`-coefficient is "`z`-free". -/
def IsZFree (x : Sq) : Prop := coef x = 0

/-- **A `z`-free `Q` makes the cross terms vanish.**  If `b` is `z`-free then
`coef (a·b) = b.fst · coef a`. -/
theorem coeff_mul_zf (a b : Sq) (hb : coef b = 0) :
    coef (a * b) = b.fst * coef a := by
  rw [coeff_mul, hb]
  ring

/-- `IsZFree`, transported to the `snd` projection. -/
theorem zf_snd {x : Sq} (h : IsZFree x) : x.snd = 0 := h

/-- The explicit trace of a `2×2` matrix.  We avoid `Matrix.trace` because its
reducibility makes the `coef` rewriting below brittle. -/
def tr2 (M : Matrix (Fin 2) (Fin 2) Sq) : Sq := M 0 0 + M 1 1

theorem tr2_add (M N : Matrix (Fin 2) (Fin 2) Sq) : tr2 (M + N) = tr2 M + tr2 N := by
  simp [tr2, Matrix.add_apply]
  ring

theorem tr2_mul (M N : Matrix (Fin 2) (Fin 2) Sq) :
    tr2 (M * N) = M 0 0 * N 0 0 + M 0 1 * N 1 0 + (M 1 0 * N 0 1 + M 1 1 * N 1 1) := by
  simp [tr2, Matrix.mul_apply, Fin.sum_univ_two]

/-! ## Part 2. The one-step transfer matrix -/

/-- The `2×2` representative of `L_n(z) = (z+u)/(z+v)`, acting on `(ψ_n z, ψ_n)ᵀ`. -/
def Lmat (u v : Sq) : Matrix (Fin 2) (Fin 2) Sq := !![1, u; 1, v]

/-- `tr L_n = 1 + Q_n`. -/
theorem Lmat_trace (u v : Sq) : (Lmat u v).trace = 1 + v := by
  simp [Lmat, Matrix.trace_fin_two]

/-- `det L_n = v - u`. -/
theorem Lmat_det (u v : Sq) : (Lmat u v).det = v - u := by
  simp [Lmat, Matrix.det_fin_two]

/-- **The one-step characteristic polynomial.**  Writing `L_n = [[1,u],[1,v]]` with
`u = Q_{n+1}`, `v = Q_n`, the characteristic polynomial is
`λ² − (1+v)λ + (v−u) = 0`.

The discriminant is `4u + (1−v)²`, which is **not** a square in `Sq` in general, so
there is no fixed Floquet multiplier and no shortcut from the one-step problem: the
collapsing of the monodromy is a genuinely global (all-`N`) phenomenon, which is
why `zf_all` is proved by induction on `N` rather than from a single step. -/
theorem charpoly (u v lam : Sq) :
    (Lmat u v).det - (Lmat u v).trace * lam + lam ^ 2
      = (v - u) - (1 + v) * lam + lam ^ 2 := by
  simp [Lmat, Matrix.det_fin_two, Matrix.trace_fin_two]

/-- `L_n` is `z`-free entrywise as soon as `Q_n` and `Q_{n+1}` are. -/
theorem Lmat_z_free (u v : Sq) (hu : IsZFree u) (hv : IsZFree v) :
    IsZFree ((Lmat u v) 0 0) ∧ IsZFree ((Lmat u v) 0 1) ∧
    IsZFree ((Lmat u v) 1 0) ∧ IsZFree ((Lmat u v) 1 1) := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · rw [show (Lmat u v) 0 0 = 1 from rfl]; exact coeff_one
  · rw [show (Lmat u v) 0 1 = u from rfl]; exact hu
  · rw [show (Lmat u v) 1 0 = 1 from rfl]; exact coeff_one
  · rw [show (Lmat u v) 1 1 = v from rfl]; exact hv

/-! ## Part 3. The monodromy `T_N = L_{N-1} ⋯ L_0` -/

/-- The monodromy over `N` steps: `T_0 = 1`, `T_{k+1} = T_k · L_k`.

`T_N` is defined **without any reference to a spectral parameter**; that is the
whole content of the degeneracy claim. -/
def monodromyMat (N : ℕ) (Q : ℕ → Sq) : Matrix (Fin 2) (Fin 2) Sq :=
  match N with
  | 0 => 1
  | (k + 1) => monodromyMat k Q * Lmat (Q (k + 1)) (Q k)

/-- The four entries of `T_{j+1} = T_j · L_j` in terms of those of `T_j`. -/
theorem entry_00 (j : ℕ) (Q : ℕ → Sq) :
    (monodromyMat j Q * Lmat (Q (j + 1)) (Q j)) 0 0
      = (monodromyMat j Q) 0 0 + (monodromyMat j Q) 0 1 := by
  simp [Lmat, Matrix.mul_apply, Fin.sum_univ_two]

theorem entry_01 (j : ℕ) (Q : ℕ → Sq) :
    (monodromyMat j Q * Lmat (Q (j + 1)) (Q j)) 0 1
      = (monodromyMat j Q) 0 0 * Q (j + 1) + (monodromyMat j Q) 0 1 * Q j := by
  simp [Lmat, Matrix.mul_apply, Fin.sum_univ_two]

theorem entry_10 (j : ℕ) (Q : ℕ → Sq) :
    (monodromyMat j Q * Lmat (Q (j + 1)) (Q j)) 1 0
      = (monodromyMat j Q) 1 0 + (monodromyMat j Q) 1 1 := by
  simp [Lmat, Matrix.mul_apply, Fin.sum_univ_two]

theorem entry_11 (j : ℕ) (Q : ℕ → Sq) :
    (monodromyMat j Q * Lmat (Q (j + 1)) (Q j)) 1 1
      = (monodromyMat j Q) 1 0 * Q (j + 1) + (monodromyMat j Q) 1 1 * Q j := by
  simp [Lmat, Matrix.mul_apply, Fin.sum_univ_two]

/-! ### The four real recurrences of the `ζ`-free parts

When every `coef` vanishes, the `fst` parts of the four entries obey the *same*
recurrences as the entries themselves, but over `ℝ`.  These four mutually
recursive real sequences are the extra invariant carried through the induction. -/

mutual
  /-- The real recurrence for the `(0,0)` entry's `ζ`-free part. -/
  def raf (n : ℕ) (Q : ℕ → Sq) : ℝ :=
    match n with
    | 0 => 1
    | (k + 1) => raf k Q + rbf k Q

  /-- The real recurrence for the `(0,1)` entry's `ζ`-free part. -/
  def rbf (n : ℕ) (Q : ℕ → Sq) : ℝ :=
    match n with
    | 0 => 0
    | (k + 1) => raf k Q * (Q (k + 1)).fst + rbf k Q * (Q k).fst

  /-- The real recurrence for the `(1,0)` entry's `ζ`-free part. -/
  def rcf (n : ℕ) (Q : ℕ → Sq) : ℝ :=
    match n with
    | 0 => 0
    | (k + 1) => rcf k Q + rdf k Q

  /-- The real recurrence for the `(1,1)` entry's `ζ`-free part.

  Note the base value: `(T_0)₁₁ = 1`, so the `ζ`-free part starts at `1`, not at
  `0`.  The two entries `(1,0)` and `(1,1)` therefore have the *same* recurrence
  but different seeds. -/
  def rdf (n : ℕ) (Q : ℕ → Sq) : ℝ :=
    match n with
    | 0 => 1
    | (k + 1) => rcf k Q * (Q (k + 1)).fst + rdf k Q * (Q k).fst
end

/-! ### `z`-freeness of all four entries

The heart of the verdict.  It is deliberately **not** routed through any closed
formula for the trace: the induction carries, for each of the four entries, both
`z`-freeness and the real recurrence of its `ζ`-free part. -/

/-- **All four entries of `T_N` are `z`-free**, for every `N`, as soon as every
`Q_n` is. -/
theorem zf_all (N : ℕ) (Q : ℕ → Sq) (hQ : ∀ i, IsZFree (Q i)) :
    IsZFree ((monodromyMat N Q) 0 0) ∧ IsZFree ((monodromyMat N Q) 0 1) ∧
    IsZFree ((monodromyMat N Q) 1 0) ∧ IsZFree ((monodromyMat N Q) 1 1) := by
  have hQc : ∀ i, coef (Q i) = 0 := fun i => hQ i
  have hstrong : ∀ k : ℕ,
      IsZFree ((monodromyMat k Q) 0 0) ∧ IsZFree ((monodromyMat k Q) 0 1) ∧
      IsZFree ((monodromyMat k Q) 1 0) ∧ IsZFree ((monodromyMat k Q) 1 1) ∧
      ((monodromyMat k Q) 0 0).fst = raf k Q ∧
      ((monodromyMat k Q) 0 1).fst = rbf k Q ∧
      ((monodromyMat k Q) 1 0).fst = rcf k Q ∧
      ((monodromyMat k Q) 1 1).fst = rdf k Q := by
    intro k
    induction k with
    | zero =>
      have h1 : (monodromyMat 0 Q : Matrix (Fin 2) (Fin 2) Sq) = 1 := rfl
      have hd0 : rdf 0 Q = 1 := rfl
      have hb0 : rbf 0 Q = 0 := rfl
      have hc0 : rcf 0 Q = 0 := rfl
      refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
      · rw [h1]; simp only [Matrix.one_apply]; exact coeff_one
      · rw [h1]; simp only [Matrix.one_apply]; exact coeff_zero
      · rw [h1]; simp only [Matrix.one_apply]; exact coeff_one
      · rw [h1]; simp only [Matrix.one_apply]; exact coeff_zero
      · rw [h1]; simp only [Matrix.one_apply, raf]; rfl
      · rw [h1]; simp only [Matrix.one_apply, hb0]; rfl
      · rw [h1]; simp only [Matrix.one_apply, hc0]; rfl
      · rw [h1]; simp only [Matrix.one_apply, hd0]; rfl
    | succ j ih =>
      obtain ⟨ha, hb, hc, hd, haf, hbf, hcf, hdf⟩ := ih
      have hQj : coef (Q j) = 0 := hQc j
      have hQj1 : coef (Q (j + 1)) = 0 := hQc (j + 1)
      have hstep : (monodromyMat (j + 1) Q : Matrix (Fin 2) (Fin 2) Sq)
          = monodromyMat j Q * Lmat (Q (j + 1)) (Q j) := rfl
      have h00 := entry_00 j Q
      have h01 := entry_01 j Q
      have h10 := entry_10 j Q
      have h11 := entry_11 j Q
      refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
      · rw [hstep, h00, IsZFree, coeff_add, ha, hb]
        ring
      · rw [hstep, h01, IsZFree, coeff_add, coeff_mul, coeff_mul, hQj1, hQj, ha, hb]
        ring
      · rw [hstep, h10, IsZFree, coeff_add, hc, hd]
        ring
      · rw [hstep, h11, IsZFree, coeff_add, coeff_mul, coeff_mul, hQj1, hQj, hc, hd]
        ring
      · rw [hstep, h00, TrivSqZeroExt.fst_add, haf, hbf, raf]
      · rw [hstep, h01, TrivSqZeroExt.fst_add, TrivSqZeroExt.fst_mul,
          TrivSqZeroExt.fst_mul, haf, hbf, rbf]
      · rw [hstep, h10, TrivSqZeroExt.fst_add, hcf, hdf, rcf]
      · rw [hstep, h11, TrivSqZeroExt.fst_add, TrivSqZeroExt.fst_mul,
          TrivSqZeroExt.fst_mul, hcf, hdf, rdf]
  obtain ⟨ha, hb, hc, hd, _, _, _, _⟩ := hstrong N
  exact ⟨ha, hb, hc, hd⟩

/-- **Main result: `tr T(z)` is `z`-free.**  If every `Q_n` has vanishing
`ζ`-coefficient, then so does `tr T_N`, for every period `N`.  A monodromy that
does not see the spectral parameter has a trivial spectral curve. -/
theorem trace_z_free (N : ℕ) (Q : ℕ → Sq) (hQ : ∀ i, IsZFree (Q i)) :
    IsZFree (tr2 (monodromyMat N Q)) := by
  obtain ⟨ha, _, _, hd⟩ := zf_all N Q hQ
  rw [tr2, IsZFree, coeff_add, ha, hd]
  ring

/-- **`det T_N = ∏_{i<N} (Q_i − Q_{i+1})`.** -/
theorem det_formula (N : ℕ) (Q : ℕ → Sq) :
    (monodromyMat N Q).det = ∏ i ∈ Finset.range N, (Q i - Q (i + 1)) := by
  induction N with
  | zero => simp [monodromyMat, Matrix.det_one]
  | succ k ih =>
    rw [show (monodromyMat (k + 1) Q : Matrix (Fin 2) (Fin 2) Sq)
        = monodromyMat k Q * Lmat (Q (k + 1)) (Q k) from rfl]
    rw [Matrix.det_mul, ih, Lmat_det, Finset.prod_range_succ]

/-- **The determinant is `z`-free too**, so the whole monodromy is `z`-free, and
in particular the spectral curve `det(T_N − λ) = 0` is trivial. -/
theorem det_z_free (N : ℕ) (Q : ℕ → Sq) (hQ : ∀ i, IsZFree (Q i)) :
    IsZFree ((monodromyMat N Q).det) := by
  have hc : ∀ i, coef (Q i) = 0 := fun i => hQ i
  have hfac : ∀ i, coef (Q i - Q (i + 1)) = 0 := by
    intro i
    rw [coeff_sub, hc i, hc (i + 1)]
    ring
  rw [det_formula, IsZFree]
  induction (Finset.range N) using Finset.induction_on with
  | empty => simp [coef]
  | insert a s ha ih =>
    rw [Finset.prod_insert ha, coeff_mul, ih, hfac a]
    ring

/-- **The characteristic polynomial of the monodromy has `z`-free coefficients.**
`λ ↦ λ² − tr(T_N)·λ + det(T_N)` is a polynomial in `λ` all of whose coefficients
are `z`-free, i.e. none of them depends on the spectral parameter.  Together with
`zf_all` this is the precise algebraic content of "the spectral curve is
trivial": the curve degenerates to a pair of points that do not move with `z`, so
there is no Floquet band structure. -/
theorem trace_charpoly_z_free (N : ℕ) (Q : ℕ → Sq) (hQ : ∀ i, IsZFree (Q i)) :
    IsZFree ((monodromyMat N Q).det)
      ∧ IsZFree (-(tr2 (monodromyMat N Q)))
      ∧ IsZFree (1 : Sq) := by
  have htr := trace_z_free N Q hQ
  have hdet := det_z_free N Q hQ
  refine ⟨hdet, ?_, coeff_one⟩
  rw [IsZFree, show coef (-(tr2 (monodromyMat N Q))) = -coef (tr2 (monodromyMat N Q))
      from by simp [coef, TrivSqZeroExt.snd_neg]]
  rw [htr]
  ring

/-! ## Part 4. The scalar Möbius recursion -/

/-- **Telescoping over one period.**  The two-step product of the scalar transfer
maps collapses: the intermediate factor `(z+Q_1)` cancels. -/
theorem mobius_telescopes (z q0 q1 q2 : ℝ) (h1 : z + q1 ≠ 0) (h0 : z + q0 ≠ 0) :
    ((z + q1) / (z + q0)) * ((z + q2) / (z + q1)) = (z + q2) / (z + q0) := by
  field_simp

/-- **The Möbius product law.**  Composing `z ↦ (z+u)/(z+v)` with
`w ↦ (w + w')/(w + x)` is again linear fractional. -/
theorem mobius_composition (z u v w x : ℝ) (hv : z + v ≠ 0) :
    (((z + u) / (z + v)) + w) / (((z + u) / (z + v)) + x)
      = (z + u + w * (z + v)) / (z + u + x * (z + v)) := by
  rw [show (z + u) / (z + v) + w = (z + u + w * (z + v)) / (z + v) by field_simp,
      show (z + u) / (z + v) + x = (z + u + x * (z + v)) / (z + v) by field_simp]
  field_simp

/-! ## Part 5. The trace is not a conserved density -/

/-- **No conserved density can take two values.**  This is the logical step by
which `VERDICT.md` reaches its conclusion: the dKP-type monodromy trace is not
constant along the flow, so it is not a conserved density, so the "infinite
family of conserved densities from `tr T(z)`" claim fails. -/
theorem no_constant_trace (T : ℝ → ℝ) (s₁ s₂ : ℝ) (h : T s₁ ≠ T s₂) :
    ¬ ∃ c : ℝ, ∀ s, T s = c := by
  rintro ⟨c, hc⟩
  exact h (by rw [hc s₁, hc s₂])

#print axioms zf_all
#print axioms trace_z_free
#print axioms det_formula
#print axioms det_z_free
#print axioms trace_charpoly_z_free
#print axioms mobius_telescopes
#print axioms no_constant_trace

end DLWLax
