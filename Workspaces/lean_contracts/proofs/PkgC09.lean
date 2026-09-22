/-
Package: C09 — admissibility, positivity and smoothness of the DLW Gram determinants
`F D h = tau D h (D.a - h/2) 1` and `G D h = tau D h D.a 0`.

Contents
* `c09_admissible_proved`  — `PositiveData D h → Admissible D h`               (part (a))
* `c09_smooth_proved`      — `SmoothL (F D h) ∧ SmoothL (G D h)`               (part (b))
* `det_cauchy_submatrix_pos` and friends — positivity of Cauchy minors         (part (c))

All statements of `Contracts.lean` are used verbatim.
-/
import Contracts
import Mathlib.LinearAlgebra.Matrix.SchurComplement
import Mathlib.LinearAlgebra.Matrix.Charpoly.Coeff
import Mathlib.Tactic

set_option linter.unusedSimpArgs false
set_option linter.unusedTactic false
set_option linter.unreachableTactic false

noncomputable section
open scoped BigOperators
namespace DLWContract

/-! ## Part (a): positive data is admissible -/

theorem c09_admissible_proved {N : ℕ} (D : Data N) (h : ℝ) (hD : PositiveData D h) :
    Admissible D h := by
  obtain ⟨hh, hp, hq, hdata⟩ := hD
  refine ⟨ne_of_gt hh, ?_, ?_, ?_⟩
  · intro i k
    have h1 : 0 < D.p i := (hdata i).1
    have h2 : 0 < D.q k := (hdata k).2.2.1
    linarith
  · intro i
    have h1 : D.p i < D.a - h / 2 := (hdata i).2.1
    constructor <;> linarith
  · intro k
    have h1 : 0 < D.p k := (hdata k).1
    have h2 : D.p k < D.a - h / 2 := (hdata k).2.1
    have h3 : 0 < D.q k := (hdata k).2.2.1
    constructor <;> linarith

/-! ## Part (b): smoothness of `tau` -/

private lemma contDiff_det {N : ℕ} {M : Fin N → Fin N → (ℝ × ℝ) → ℝ}
    (hM : ∀ i k, ContDiff ℝ ⊤ (M i k)) :
    ContDiff ℝ ⊤ (fun z : ℝ × ℝ => Matrix.det (Matrix.of (fun i k => M i k z))) := by
  have hsum : (fun z : ℝ × ℝ => Matrix.det (Matrix.of (fun i k => M i k z)))
      = fun z : ℝ × ℝ =>
          ∑ σ : Equiv.Perm (Fin N), ((Equiv.Perm.sign σ : ℤ) : ℝ) * ∏ i, M (σ i) i z := by
    funext z
    simpa using Matrix.det_apply' (Matrix.of (fun i k => M i k z))
  rw [hsum]
  refine ContDiff.sum fun σ _ => ?_
  exact contDiff_const.mul (contDiff_prod fun i _ => hM (σ i) i)

private lemma contDiff_entry {N : ℕ} (D : Data N) (h s : ℝ) (n j : ℤ) (i k : Fin N) :
    ContDiff ℝ ⊤ (fun z : ℝ × ℝ => entry D h s n j i k z.1 z.2) := by
  unfold entry
  fun_prop

private theorem smoothXT_tau {N : ℕ} (D : Data N) (h s : ℝ) (n j : ℤ) :
    SmoothXT (tau D h s n j) := by
  simp only [SmoothXT, tau]
  exact contDiff_det (fun i k => contDiff_entry D h s n j i k)

private theorem smoothL_tau {N : ℕ} (D : Data N) (h s : ℝ) (n : ℤ) :
    SmoothL (tau D h s n) := fun j => smoothXT_tau D h s n j

theorem c09_smooth_proved {N : ℕ} (D : Data N) (h : ℝ) :
    SmoothL (F D h) ∧ SmoothL (G D h) :=
  ⟨smoothL_tau D h (D.a - h / 2) 1, smoothL_tau D h D.a 0⟩

/-! ## Part (c): positivity of Cauchy principal minors -/

private lemma inv_sub_inv_left {a b c : ℝ} (ha : a + c ≠ 0) (hb : b + c ≠ 0) :
    (a + c)⁻¹ - (b + c)⁻¹ = (b - a) * ((a + c) * (b + c))⁻¹ := by
  have h : (a + c) * (b + c) ≠ 0 := mul_ne_zero ha hb
  field_simp
  ring

private lemma inv_sub_inv_right {a c d : ℝ} (hc : a + c ≠ 0) (hd : a + d ≠ 0) :
    (a + c)⁻¹ - (a + d)⁻¹ = (d - c) * ((a + c) * (a + d))⁻¹ := by
  have h : (a + c) * (a + d) ≠ 0 := mul_ne_zero hc hd
  field_simp
  ring

private lemma fin_succ_strictMono {n : ℕ} : StrictMono (Fin.succ : Fin n → Fin (n+1)) := by
  intro a b hab
  rw [Fin.lt_def] at hab ⊢
  simp only [Fin.val_succ]
  omega

private lemma neg_one_pow_mul_self (n : ℕ) : (-1:ℝ)^n * (-1)^n = 1 := by
  rw [← pow_add, show n + n = 2 * n from by ring, pow_mul]
  simp

/-- Elimination matrix for row ops: `E i l = δ_il - (if l=0 ∧ i≠0 then 1 else 0)`.
    Lower unitriangular, hence `det E = 1`. -/
private def rowElim (n : ℕ) : Matrix (Fin (n+1)) (Fin (n+1)) ℝ :=
  Matrix.of fun i l => (if i = l then (1:ℝ) else 0) -
    (if l = 0 then (if i = 0 then (0:ℝ) else 1) else 0)

/-- Elimination matrix for column ops: `F l j = δ_lj - (if l=0 ∧ j≠0 then 1 else 0)`.
    Upper unitriangular, hence `det F = 1`. -/
private def colElim (n : ℕ) : Matrix (Fin (n+1)) (Fin (n+1)) ℝ :=
  Matrix.of fun l j => (if l = j then (1:ℝ) else 0) -
    (if l = 0 then (if j = 0 then (0:ℝ) else 1) else 0)

private lemma rowElim_det (n : ℕ) : (rowElim n).det = 1 := by
  rw [Matrix.det_of_isLowerTriangular]
  · refine Finset.prod_eq_one fun i _ => ?_
    simp only [rowElim, Matrix.of_apply]
    by_cases hi : i = 0
    · subst hi; simp
    · simp only [if_neg hi]
      rw [if_pos (by simp)]
      simp [hi]
  · intro i j hij
    -- hij : toDual j < toDual i  ↔  i < j
    have hlt : i < j := OrderDual.toDual_lt_toDual.mp hij
    simp only [rowElim, Matrix.of_apply]
    have hj0 : j ≠ 0 := by
      rintro rfl
      simp only [Fin.lt_def, Fin.val_zero] at hlt
      omega
    simp only [if_neg (ne_of_lt hlt), if_neg hj0]
    simp

private lemma colElim_det (n : ℕ) : (colElim n).det = 1 := by
  rw [Matrix.det_of_isUpperTriangular]
  · refine Finset.prod_eq_one fun j _ => ?_
    simp only [colElim, Matrix.of_apply]
    by_cases hj : j = 0
    · subst hj; simp
    · simp only [if_neg hj]
      rw [if_pos (by simp)]
      simp [hj]
  · intro l j hlj
    -- hlj : j < l
    have hlt : j < l := hlj
    simp only [colElim, Matrix.of_apply]
    have hl0 : l ≠ 0 := by
      rintro rfl
      simp only [Fin.lt_def, Fin.val_zero] at hlt
      omega
    simp only [if_neg hlt.ne', if_neg hl0]
    simp

/-- The classical elimination recurrence for the Cauchy determinant. -/
private lemma cauchy_det_recurrence (n : ℕ) (x y : Fin (n+1) → ℝ)
    (hxy : ∀ i j, x i + y j ≠ 0) :
    (Matrix.of (fun i j : Fin (n+1) => (x i + y j)⁻¹)).det =
      (∏ i : Fin n, (x 0 - x i.succ)) *
      ((x 0 + y 0)⁻¹ * (∏ j : Fin n, (x 0 + y j.succ)⁻¹)) *
      (∏ i : Fin n, (x i.succ + y 0)⁻¹) *
      (∏ j : Fin n, (y 0 - y j.succ)) *
      (Matrix.of (fun i j : Fin n => (x i.succ + y j.succ)⁻¹)).det := by
  -- ### stage 1: row operation `row i ← row i - row 0`, then row/column scaling
  have hstep1 : (Matrix.of (fun i j : Fin (n+1) => (x i + y j)⁻¹)).det =
      (∏ i : Fin (n+1), (if i = 0 then (1:ℝ) else x 0 - x i)) *
      (∏ j : Fin (n+1), (x 0 + y j)⁻¹) *
      (Matrix.of (fun i j : Fin (n+1) => if i = 0 then (1:ℝ) else (x i + y j)⁻¹)).det := by
    have hEdet : (rowElim n).det = 1 := rowElim_det n
    have hmul : rowElim n * Matrix.of (fun i j : Fin (n+1) => (x i + y j)⁻¹) =
        Matrix.of (fun i j : Fin (n+1) =>
          (if i = 0 then (1:ℝ) else x 0 - x i) *
          ((x 0 + y j)⁻¹ * (if i = 0 then (1:ℝ) else (x i + y j)⁻¹))) := by
      ext i j
      rw [Matrix.mul_apply]
      simp only [rowElim, Matrix.of_apply]
      by_cases hi : i = 0
      · subst hi
        rw [Finset.sum_eq_single (0 : Fin (n+1))]
        · simp
        · intro l _ hl
          have h0l : ¬ ((0:Fin (n+1)) = l) := fun h => hl h.symm
          simp only [if_neg h0l, if_neg hl]
          ring
        · intro h; exact absurd (Finset.mem_univ _) h
      · have hpt : ∀ l : Fin (n+1),
            ((if i = l then (1:ℝ) else 0) -
              (if l = 0 then (if i = 0 then (0:ℝ) else 1) else 0)) * (x l + y j)⁻¹
            = (if i = l then (x l + y j)⁻¹ else 0) - (if l = 0 then (x l + y j)⁻¹ else 0) := by
          intro l
          rcases eq_or_ne l 0 with h0 | hl
          · subst h0
            simp only [if_neg hi, if_pos rfl]
            simp only [ite_true]
            ring
          · rcases eq_or_ne i l with hil | hil
            · subst hil
              simp only [if_neg hi, if_pos rfl]
              simp only [ite_true]
              ring
            · simp only [if_neg hil, if_neg hl]
              ring
        rw [Finset.sum_congr rfl (fun l _ => hpt l), Finset.sum_sub_distrib]
        simp only [Finset.sum_ite_eq, Finset.sum_ite_eq', Finset.mem_univ, ite_true, if_neg hi]
        rw [inv_sub_inv_left (hxy i j) (hxy 0 j), mul_inv_rev]
    have hdet1 : (Matrix.of (fun i j : Fin (n+1) => (x i + y j)⁻¹)).det
        = (rowElim n * Matrix.of (fun i j : Fin (n+1) => (x i + y j)⁻¹)).det := by
      rw [Matrix.det_mul, hEdet, one_mul]
    have hs1 : (Matrix.of (fun i j : Fin (n+1) =>
          (if i = 0 then (1:ℝ) else x 0 - x i) *
            ((x 0 + y j)⁻¹ * (if i = 0 then (1:ℝ) else (x i + y j)⁻¹)))).det
        = (∏ i : Fin (n+1), (if i = 0 then (1:ℝ) else x 0 - x i)) *
          (Matrix.of (fun i j : Fin (n+1) =>
            (x 0 + y j)⁻¹ * (if i = 0 then (1:ℝ) else (x i + y j)⁻¹))).det :=
      Matrix.det_mul_column (fun i : Fin (n+1) => if i = 0 then (1:ℝ) else x 0 - x i)
        (Matrix.of (fun i j : Fin (n+1) =>
          (x 0 + y j)⁻¹ * (if i = 0 then (1:ℝ) else (x i + y j)⁻¹)))
    have hs2 : (Matrix.of (fun i j : Fin (n+1) =>
            (x 0 + y j)⁻¹ * (if i = 0 then (1:ℝ) else (x i + y j)⁻¹))).det
        = (∏ j : Fin (n+1), (x 0 + y j)⁻¹) *
          (Matrix.of (fun i j : Fin (n+1) => if i = 0 then (1:ℝ) else (x i + y j)⁻¹)).det :=
      Matrix.det_mul_row (fun j : Fin (n+1) => (x 0 + y j)⁻¹)
        (Matrix.of (fun i j : Fin (n+1) => if i = 0 then (1:ℝ) else (x i + y j)⁻¹))
    rw [hdet1, hmul, hs1, hs2]
    ring
  -- ### stage 2: column operation `col j ← col j - col 0`, then row/column scaling
  have hstep2 : (Matrix.of (fun i j : Fin (n+1) => if i = 0 then (1:ℝ) else (x i + y j)⁻¹)).det =
      (∏ i : Fin (n+1), (if i = 0 then (1:ℝ) else (x i + y 0)⁻¹)) *
      (∏ j : Fin (n+1), (if j = 0 then (1:ℝ) else y 0 - y j)) *
      (Matrix.of (fun i j : Fin (n+1) =>
        if i = 0 then (if j = 0 then (1:ℝ) else 0)
        else (if j = 0 then (1:ℝ) else (x i + y j)⁻¹))).det := by
    have hFdet : (colElim n).det = 1 := colElim_det n
    have hmul : Matrix.of (fun i j : Fin (n+1) => if i = 0 then (1:ℝ) else (x i + y j)⁻¹) *
          colElim n =
        Matrix.of (fun i j : Fin (n+1) =>
          (if i = 0 then (1:ℝ) else (x i + y 0)⁻¹) *
          ((if j = 0 then (1:ℝ) else y 0 - y j) *
            (if i = 0 then (if j = 0 then (1:ℝ) else 0)
             else (if j = 0 then (1:ℝ) else (x i + y j)⁻¹)))) := by
      ext i j
      rw [Matrix.mul_apply]
      simp only [colElim, Matrix.of_apply]
      by_cases hj : j = 0
      · subst hj
        rw [Finset.sum_eq_single (0 : Fin (n+1))]
        · by_cases hi : i = 0
          · subst hi; simp
          · simp only [if_neg hi, if_pos rfl]
            simp only [ite_true]
            ring
        · intro l _ hl
          simp only [if_neg hl]
          ring
        · intro h; exact absurd (Finset.mem_univ _) h
      · have hpt : ∀ l : Fin (n+1),
            (if i = 0 then (1:ℝ) else (x i + y l)⁻¹) *
              ((if l = j then (1:ℝ) else 0) -
                (if l = 0 then (if j = 0 then (0:ℝ) else 1) else 0))
            = (if i = 0 then (1:ℝ) else (x i + y j)⁻¹) * (if l = j then (1:ℝ) else 0)
              - (if i = 0 then (1:ℝ) else (x i + y 0)⁻¹) * (if l = 0 then (1:ℝ) else 0) := by
          intro l
          rcases eq_or_ne l 0 with h0 | hl
          · subst h0
            have h0j : ¬ ((0:Fin (n+1)) = j) := fun h => hj h.symm
            simp only [if_neg h0j, if_neg hj, if_pos rfl]
            simp only [ite_true]
            ring
          · rcases eq_or_ne l j with hlj | hlj
            · subst hlj
              simp only [if_neg hj, if_pos rfl]
              simp only [ite_true]
              ring
            · simp only [if_neg hlj, if_neg hl]
              ring
        rw [Finset.sum_congr rfl (fun l _ => hpt l), Finset.sum_sub_distrib]
        simp only [mul_ite, mul_one, mul_zero, Finset.sum_ite_eq', Finset.mem_univ, ite_true]
        by_cases hi : i = 0
        · subst hi
          simp only [if_pos rfl, if_neg hj]
          simp only [ite_true]
          ring
        · simp only [if_neg hi, if_neg hj]
          exact (inv_sub_inv_right (hxy i j) (hxy i 0)).trans (by rw [mul_inv_rev]; ring)
    have hdet2 : (Matrix.of (fun i j : Fin (n+1) => if i = 0 then (1:ℝ) else (x i + y j)⁻¹)).det
        = (Matrix.of (fun i j : Fin (n+1) => if i = 0 then (1:ℝ) else (x i + y j)⁻¹) * colElim n).det := by
      rw [Matrix.det_mul, hFdet, mul_one]
    have hs1 : (Matrix.of (fun i j : Fin (n+1) =>
          (if i = 0 then (1:ℝ) else (x i + y 0)⁻¹) *
            ((if j = 0 then (1:ℝ) else y 0 - y j) *
              (if i = 0 then (if j = 0 then (1:ℝ) else 0)
               else (if j = 0 then (1:ℝ) else (x i + y j)⁻¹))))).det
        = (∏ i : Fin (n+1), (if i = 0 then (1:ℝ) else (x i + y 0)⁻¹)) *
          (Matrix.of (fun i j : Fin (n+1) =>
            (if j = 0 then (1:ℝ) else y 0 - y j) *
              (if i = 0 then (if j = 0 then (1:ℝ) else 0)
               else (if j = 0 then (1:ℝ) else (x i + y j)⁻¹)))).det :=
      Matrix.det_mul_column (fun i : Fin (n+1) => if i = 0 then (1:ℝ) else (x i + y 0)⁻¹)
        (Matrix.of (fun i j : Fin (n+1) =>
          (if j = 0 then (1:ℝ) else y 0 - y j) *
            (if i = 0 then (if j = 0 then (1:ℝ) else 0)
             else (if j = 0 then (1:ℝ) else (x i + y j)⁻¹))))
    have hs2 : (Matrix.of (fun i j : Fin (n+1) =>
            (if j = 0 then (1:ℝ) else y 0 - y j) *
              (if i = 0 then (if j = 0 then (1:ℝ) else 0)
               else (if j = 0 then (1:ℝ) else (x i + y j)⁻¹)))).det
        = (∏ j : Fin (n+1), (if j = 0 then (1:ℝ) else y 0 - y j)) *
          (Matrix.of (fun i j : Fin (n+1) =>
            if i = 0 then (if j = 0 then (1:ℝ) else 0)
            else (if j = 0 then (1:ℝ) else (x i + y j)⁻¹))).det :=
      Matrix.det_mul_row (fun j : Fin (n+1) => if j = 0 then (1:ℝ) else y 0 - y j)
        (Matrix.of (fun i j : Fin (n+1) =>
          if i = 0 then (if j = 0 then (1:ℝ) else 0)
          else (if j = 0 then (1:ℝ) else (x i + y j)⁻¹)))
    rw [hdet2, hmul, hs1, hs2]
    ring
  -- ### stage 3: Laplace expansion along row 0
  have hstep3 : (Matrix.of (fun i j : Fin (n+1) =>
        if i = 0 then (if j = 0 then (1:ℝ) else 0)
        else (if j = 0 then (1:ℝ) else (x i + y j)⁻¹))).det =
      (Matrix.of (fun i j : Fin n => (x i.succ + y j.succ)⁻¹)).det := by
    set E' : Matrix (Fin (n+1)) (Fin (n+1)) ℝ :=
      Matrix.of (fun i j => if i = 0 then (if j = 0 then (1:ℝ) else 0)
        else (if j = 0 then (1:ℝ) else (x i + y j)⁻¹)) with hE'
    have hsub : E'.submatrix Fin.succ Fin.succ
        = Matrix.of (fun i j : Fin n => (x i.succ + y j.succ)⁻¹) := by
      ext i j
      rw [Matrix.submatrix_apply, hE', Matrix.of_apply]
      simp [Fin.succ_ne_zero]
    have h00 : E' 0 0 = 1 := by simp [hE']
    rw [Matrix.det_succ_row_zero]
    rw [Finset.sum_eq_single (0 : Fin (n+1))]
    · rw [h00, Fin.succAbove_zero, hsub]
      simp
    · intro j _ hj
      have h0 : E' 0 j = 0 := by simp [hE', hj]
      rw [h0]
      ring
    · intro h
      exact absurd (Finset.mem_univ (0 : Fin (n+1))) h
  -- ### combine
  rw [hstep1, hstep2, hstep3]
  rw [Fin.prod_univ_succ (f := fun i : Fin (n+1) => if i = 0 then (1:ℝ) else x 0 - x i),
    Fin.prod_univ_succ (f := fun j : Fin (n+1) => (x 0 + y j)⁻¹),
    Fin.prod_univ_succ (f := fun i : Fin (n+1) => if i = 0 then (1:ℝ) else (x i + y 0)⁻¹),
    Fin.prod_univ_succ (f := fun j : Fin (n+1) => if j = 0 then (1:ℝ) else y 0 - y j)]
  simp only [Fin.succ_ne_zero, Fin.isValue, Fin.val_zero, ite_false, ite_true, one_mul, mul_one,
    zero_mul]
  ring

/-- Cauchy determinants with positive strictly monotone data are positive. -/
private lemma cauchy_det_pos : ∀ (n : ℕ) (x y : Fin n → ℝ),
    (∀ i, 0 < x i) → (∀ j, 0 < y j) → StrictMono x → StrictMono y →
    0 < (Matrix.of (fun i j : Fin n => (x i + y j)⁻¹)).det := by
  intro n
  induction n with
  | zero => intro x y _ _ _ _; simp
  | succ n ih =>
    intro x y hx hy hxs hys
    have hN1 : (∏ i : Fin n, (x 0 - x i.succ))
        = (-1:ℝ)^n * ∏ i : Fin n, (x i.succ - x 0) := by
      rw [show (∏ i : Fin n, (x 0 - x i.succ))
            = ∏ i : Fin n, ((-1:ℝ) * (x i.succ - x 0)) from
        Finset.prod_congr rfl fun i _ => by ring]
      rw [Finset.prod_mul_distrib]
      simp [Finset.prod_const]
    have hN2 : (∏ j : Fin n, (y 0 - y j.succ))
        = (-1:ℝ)^n * ∏ j : Fin n, (y j.succ - y 0) := by
      rw [show (∏ j : Fin n, (y 0 - y j.succ))
            = ∏ j : Fin n, ((-1:ℝ) * (y j.succ - y 0)) from
        Finset.prod_congr rfl fun j _ => by ring]
      rw [Finset.prod_mul_distrib]
      simp [Finset.prod_const]
    rw [cauchy_det_recurrence n x y (fun i j => ne_of_gt (add_pos (hx i) (hy j)))]
    rw [hN1, hN2]
    set Q1 : ℝ := ∏ i : Fin n, (x i.succ - x 0) with hQ1def
    set Q2 : ℝ := ∏ j : Fin n, (y j.succ - y 0) with hQ2def
    set P1 : ℝ := (x 0 + y 0)⁻¹ * ∏ j : Fin n, (x 0 + y j.succ)⁻¹ with hP1def
    set P2 : ℝ := ∏ i : Fin n, (x i.succ + y 0)⁻¹ with hP2def
    set D : ℝ := (Matrix.of (fun i j : Fin n => (x i.succ + y j.succ)⁻¹)).det with hDdef
    have hQ1 : 0 < Q1 := by
      rw [hQ1def]
      exact Finset.prod_pos fun i _ => sub_pos.mpr (hxs (Fin.succ_pos i))
    have hQ2 : 0 < Q2 := by
      rw [hQ2def]
      exact Finset.prod_pos fun j _ => sub_pos.mpr (hys (Fin.succ_pos j))
    have hP1 : 0 < P1 := by
      rw [hP1def]
      exact mul_pos (inv_pos.mpr (add_pos (hx 0) (hy 0)))
        (Finset.prod_pos fun j _ => inv_pos.mpr (add_pos (hx 0) (hy j.succ)))
    have hP2 : 0 < P2 := by
      rw [hP2def]
      exact Finset.prod_pos fun i _ => inv_pos.mpr (add_pos (hx i.succ) (hy 0))
    have hD : 0 < D := by
      rw [hDdef]
      exact ih (fun i => x i.succ) (fun j => y j.succ) (fun i => hx i.succ) (fun j => hy j.succ)
        (hxs.comp fin_succ_strictMono) (hys.comp fin_succ_strictMono)
    rw [show ((-1:ℝ)^n * Q1) * P1 * P2 * ((-1:ℝ)^n * Q2) * D
        = (Q1 * Q2) * (P1 * P2 * D) by
      rw [show ((-1:ℝ)^n * Q1) * P1 * P2 * ((-1:ℝ)^n * Q2) * D
            = ((-1:ℝ)^n * (-1:ℝ)^n) * ((Q1 * Q2) * (P1 * P2 * D)) by ring,
        neg_one_pow_mul_self n, one_mul]]
    exact mul_pos (mul_pos hQ1 hQ2) (mul_pos (mul_pos hP1 hP2) hD)

/-- Positivity of Cauchy minors indexed by a strictly monotone family. -/
theorem det_cauchy_submatrix_pos {m : ℕ} (p q : Fin m → ℝ)
    (hp : ∀ i, 0 < p i) (hq : ∀ j, 0 < q j)
    (hps : StrictMono p) (hqs : StrictMono q)
    {M : ℕ} (v : Fin M → Fin m) (hv : StrictMono v) :
    0 < (Matrix.of (fun i j : Fin M => (p (v i) + q (v j))⁻¹)).det :=
  cauchy_det_pos M (fun i => p (v i)) (fun j => q (v j))
    (fun i => hp (v i)) (fun j => hq (v j)) (hps.comp hv) (hqs.comp hv)

/-! ## Rank-one factorization of `entry` and `PositiveL` -/

private def rfacA {N : ℕ} (D : Data N) (h s : ℝ) (n j : ℤ) (x t : ℝ) (i : Fin N) : ℝ :=
  D.rho i * (-(D.p i - s))^n * (lam h (D.p i - D.a))^j *
    Real.exp (D.p i * x - (D.p i)^2 * t)

private def rfacB {N : ℕ} (D : Data N) (h s : ℝ) (n j : ℤ) (x t : ℝ) (k : Fin N) : ℝ :=
  (D.q k + s)^(-n) * (lam h (D.q k + D.a))^j *
    Real.exp (D.q k * x + (D.q k)^2 * t)

private lemma zpow_div {a b : ℝ} (n : ℤ) :
    (a / b)^n = a^n * b^(-n) := by
  rw [div_eq_mul_inv, mul_zpow, inv_zpow, zpow_neg]

private lemma exp_split {p q x t : ℝ} :
    Real.exp ((p + q) * x + (q^2 - p^2) * t) =
      Real.exp (p * x - p^2 * t) * Real.exp (q * x + q^2 * t) := by
  rw [← Real.exp_add]
  congr 1
  ring

private lemma entry_rank_one {N : ℕ} (D : Data N) (h s : ℝ) (n j : ℤ)
    (i k : Fin N) (x t : ℝ) :
    entry D h s n j i k x t =
      (if i = k then (1:ℝ) else 0) +
        rfacA D h s n j x t i * rfacB D h s n j x t k * (D.p i + D.q k)⁻¹ := by
  unfold entry rfacA rfacB gamma chi lam
  simp only [div_eq_mul_inv]
  rw [mul_zpow, inv_zpow, zpow_neg, mul_zpow, exp_split]
  ring

private lemma tau_eq_det_one_add {N : ℕ} (D : Data N) (h s : ℝ) (n j : ℤ) (x t : ℝ) :
    tau D h s n j x t =
      Matrix.det ((1 : Matrix (Fin N) (Fin N) ℝ) +
        Matrix.diagonal (fun i : Fin N => rfacA D h s n j x t i) *
          Matrix.of (fun i k : Fin N => (D.p i + D.q k)⁻¹) *
          Matrix.diagonal (fun k : Fin N => rfacB D h s n j x t k)) := by
  simp only [tau]
  refine congr_arg Matrix.det ?_
  funext i k
  rw [entry_rank_one]
  simp only [Matrix.add_apply, Matrix.one_apply, Matrix.mul_apply,
    Matrix.diagonal_apply, Matrix.of_apply]
  rw [Finset.sum_eq_single k]
  · simp only [if_pos rfl, mul_assoc]
    ring
  · intro l _ hl
    simp only [hl, if_false, mul_zero]
  · intro h
    exact absurd (Finset.mem_univ k) h

private lemma det_one_add_comm_diag {N : ℕ} (A B : Fin N → ℝ)
    (K : Matrix (Fin N) (Fin N) ℝ) :
    Matrix.det ((1 : Matrix (Fin N) (Fin N) ℝ) +
        Matrix.diagonal A * K * Matrix.diagonal B) =
      Matrix.det ((1 : Matrix (Fin N) (Fin N) ℝ) +
        K * Matrix.diagonal (fun i => B i * A i)) := by
  have hassoc : Matrix.diagonal A * K * Matrix.diagonal B =
      Matrix.diagonal A * (K * Matrix.diagonal B) := mul_assoc _ _ _
  rw [hassoc, Matrix.det_one_add_mul_comm]
  have hassoc2 : (K * Matrix.diagonal B) * Matrix.diagonal A =
      K * (Matrix.diagonal B * Matrix.diagonal A) := mul_assoc _ _ _
  rw [hassoc2, Matrix.diagonal_mul_diagonal]

/-- `det (1 + M)` equals the sum of all principal minors of `M`. -/
private lemma det_one_add_eq_sum_minors {N : ℕ} (M : Matrix (Fin N) (Fin N) ℝ) :
    Matrix.det (1 + M) =
      ∑ s ∈ (Finset.univ : Finset (Fin N)).powerset,
        (M.submatrix Subtype.val Subtype.val).det := by
  classical
  set P : ℝ[X] := Matrix.det (1 + (Polynomial.X : ℝ[X]) • M.map (algebraMap ℝ ℝ[X])) with hP
  set g : ℕ → ℝ := fun k =>
    ∑ s ∈ (Finset.univ : Finset (Fin N)).powersetCard k,
      (M.submatrix Subtype.val Subtype.val).det with hgdef
  have hcoeff : ∀ k : ℕ, P.coeff k = g k := by
    intro k
  rw [hgdef, hP]
  simpa only using Matrix.coeff_det_one_add_X_smul_eq_sum_minors M k
  have heval : P.eval (1:ℝ) = Matrix.det (1 + M) := by
    rw [hP, ← RingHom.map_det (Polynomial.evalRingHom (1:ℝ))]
    congr 1
    ext i j
    simp only [Matrix.map_apply, Matrix.add_apply, Matrix.one_apply, smul_apply,
      Algebra.smul_def, RingHom.id_apply, Polynomial.eval_mul, Polynomial.eval_C,
      Polynomial.eval_X, mul_one]
    split_ifs <;> rfl
  have h1 : P.eval (1:ℝ) =
      ∑ k ∈ Finset.range (P.natDegree + 1), g k := by
    rw [Polynomial.eval_eq_sum_range]
    simp only [mul_one]
    exact Finset.sum_congr rfl (fun k _ => hcoeff k).symm
  have hempty : ∀ k : ℕ, N < k →
      (Finset.univ : Finset (Fin N)).powersetCard k = ∅ := by
    intro k hk
    ext s
    simp only [Finset.mem_powersetCard, Finset.mem_univ, true_and, Finset.mem_empty_iff_false,
      not_and, Classical.not_imp]
    intro _hs
    have hle : s.card ≤ N := Finset.card_le_card (Finset.subset_univ s)
    omega
  have hg_big : ∀ k, N < k → g k = 0 := by
    intro k hk
    rw [hgdef, hempty k hk]
    simp
  have hg_nat : ∀ k, k ∉ Finset.range (P.natDegree + 1) → g k = 0 := by
    intro k hk
    rw [← hcoeff k]
    exact Polynomial.coeff_eq_zero_of_natDegree_lt (by
      simpa [Finset.mem_range] using hk)
  have hg_card : ∀ k, k ∉ Finset.range (N + 1) → g k = 0 := by
    intro k hk
    exact hg_big k (by simpa [Finset.mem_range] using hk)
  have h2 : ∑ k ∈ Finset.range (P.natDegree + 1), g k
      = ∑ k ∈ Finset.range (N + 1), g k := by
    set R := max (P.natDegree + 1) (N + 1)
    have hs1 : Finset.range (P.natDegree + 1) ⊆ Finset.range R := by
      intro k hk
      simp only [Finset.mem_range] at hk ⊢
      exact lt_of_lt_of_le hk (le_max_left _ _)
    have hs2 : Finset.range (N + 1) ⊆ Finset.range R := by
      intro k hk
      simp only [Finset.mem_range] at hk ⊢
      exact lt_of_lt_of_le hk (le_max_right _ _)
    exact (Finset.sum_subset hs1 (fun k _ hns => hg_nat k hns)).trans
      (Finset.sum_subset hs2 (fun k _ hns => hg_card k hns)).symm
  have h3 : ∑ k ∈ Finset.range (N + 1), g k
      = ∑ s ∈ (Finset.univ : Finset (Fin N)).powerset,
        (M.submatrix Subtype.val Subtype.val).det := by
    rw [← Finset.sum_sigma]
    refine Finset.sum_bij (fun x _ => x.2) ?_ ?_ ?_ ?_
    · intro x hx
      exact Finset.mem_powerset.2 (Finset.subset_univ _)
    · intro x1 hx1 x2 hx2 heq
      obtain ⟨k1, s1⟩ := x1
      obtain ⟨k2, s2⟩ := x2
      simp only at heq
      subst heq
      obtain ⟨_, hs1⟩ := Finset.mem_sigma.mp hx1
      obtain ⟨_, hs2⟩ := Finset.mem_sigma.mp hx2
      rw [Finset.mem_powersetCard_univ] at hs1 hs2
      simp only
      omega
    · intro s hs
      refine ⟨(s.card, s), ?_, rfl⟩
      refine Finset.mem_sigma.mpr ⟨?_, ?_⟩
      · simp only [Finset.mem_range]
        exact Finset.card_le_card (Finset.subset_univ s)
      · exact Finset.mem_powersetCard_univ.2 rfl
    · intro x hx
      exact Finset.mem_sigma.2 ⟨Finset.mem_range.2 (le_of_lt (Finset.mem_range.1 hx.1)),
        hx.2⟩
  rw [← heval, h1, h2, h3]

private lemma lam_p_lt_zero {N : ℕ} (D : Data N) (h : ℝ) (hD : PositiveData D h)
    (i : Fin N) :
    D.p i - D.a + h / 2 < 0 ∧ D.p i - D.a - h / 2 < 0 := by
  obtain ⟨hh, _, _, hdata⟩ := hD
  have hlt : D.p i < D.a - h / 2 := (hdata i).2.1
  constructor <;> linarith

private lemma lam_q_pos {N : ℕ} (D : Data N) (h : ℝ) (hD : PositiveData D h)
    (k : Fin N) :
    0 < D.q k + D.a + h / 2 ∧ 0 < D.q k + D.a - h / 2 := by
  obtain ⟨hh, _, _, hdata⟩ := hD
  have hp : 0 < D.p k := (hdata k).1
  have hlt : D.p k < D.a - h / 2 := (hdata k).2.1
  have hq : 0 < D.q k := (hdata k).2.2.1
  have hah : 0 < D.a - h / 2 := lt_of_lt_of_le hp (le_of_lt hlt)
  constructor <;> linarith

private lemma lam_p_neg' {N : ℕ} (D : Data N) (h : ℝ) (hD : PositiveData D h)
    (i : Fin N) : 0 < lam h (D.p i - D.a) := by
  obtain ⟨h1, h2⟩ := lam_p_lt_zero D h hD i
  unfold lam
  exact div_pos_of_neg_of_neg h1 h2

private lemma lam_q_pos' {N : ℕ} (D : Data N) (h : ℝ) (hD : PositiveData D h)
    (k : Fin N) : 0 < lam h (D.q k + D.a) := by
  obtain ⟨h1, h2⟩ := lam_q_pos D h hD k
  unfold lam
  exact div_pos (by linarith) (by linarith)

private lemma pos_p {N : ℕ} {D : Data N} {h : ℝ} (hD : PositiveData D h) (i : Fin N) :
    0 < D.p i := (hD.2.2.2 i).1

private lemma pos_q {N : ℕ} {D : Data N} {h : ℝ} (hD : PositiveData D h) (k : Fin N) :
    0 < D.q k := (hD.2.2.2 k).2.2.1

private lemma pos_rho {N : ℕ} {D : Data N} {h : ℝ} (hD : PositiveData D h) (i : Fin N) :
    0 < D.rho i := (hD.2.2.2 i).2.2.2

private lemma ah_half_pos {N : ℕ} {D : Data N} {h : ℝ} (hD : PositiveData D h)
    (k : Fin N) : 0 < D.a - h / 2 := by
  have hp : 0 < D.p k := pos_p hD k
  have hlt : D.p k < D.a - h / 2 := (hD.2.2.2 k).2.1
  linarith

/-- Positivity of the rank-one factors on the `F` layer (`s = a − h/2`, `n = 1`). -/
private lemma rfac_F_pos {N : ℕ} (D : Data N) (h : ℝ) (hD : PositiveData D h)
    (j : ℤ) (x t : ℝ) :
    (∀ i, 0 < rfacA D h (D.a - h / 2) 1 j x t i) ∧
    (∀ k, 0 < rfacB D h (D.a - h / 2) 1 j x t k) := by
  constructor
  · intro i
    unfold rfacA
    have hrho : 0 < D.rho i := pos_rho hD i
    have hp : 0 < D.p i := pos_p hD i
    have hlt : D.p i < D.a - h / 2 := (hD.2.2.2 i).2.1
    have hbase : 0 < -(D.p i - (D.a - h / 2)) := by linarith
    have hz : (-(D.p i - (D.a - h / 2)))^((1:ℤ)) = -(D.p i - (D.a - h / 2)) := by simp
    have hlam : 0 < lam h (D.p i - D.a) := lam_p_neg' D h hD i
    have hexp : 0 < Real.exp (D.p i * x - (D.p i)^2 * t) := Real.exp_pos _
    rw [hz]
    simp only [zpow_one]
    refine mul_pos (mul_pos (mul_pos hrho hbase) (zpow_pos hlam j)) hexp
  · intro k
    unfold rfacB
    have hq : 0 < D.q k := pos_q hD k
    have hah : 0 < D.a - h / 2 := ah_half_pos hD k
    have hden : 0 < D.q k + (D.a - h / 2) := add_pos hq hah
    have hz : (D.q k + (D.a - h / 2))^(-(1:ℤ)) = (D.q k + (D.a - h / 2))⁻¹ := by simp
    have hlam : 0 < lam h (D.q k + D.a) := lam_q_pos' D h hD k
    have hexp : 0 < Real.exp (D.q k * x + (D.q k)^2 * t) := Real.exp_pos _
    rw [hz]
    exact mul_pos (mul_pos (inv_pos.mpr hden) (zpow_pos hlam j)) hexp

/-- Positivity of the rank-one factors on the `G` layer (`s = a`, `n = 0`). -/
private lemma rfac_G_pos {N : ℕ} (D : Data N) (h : ℝ) (hD : PositiveData D h)
    (j : ℤ) (x t : ℝ) :
    (∀ i, 0 < rfacA D h D.a 0 j x t i) ∧ (∀ k, 0 < rfacB D h D.a 0 j x t k) := by
  constructor
  · intro i
    unfold rfacA
    have hrho : 0 < D.rho i := pos_rho hD i
    have hlam : 0 < lam h (D.p i - D.a) := lam_p_neg' D h hD i
    have hexp : 0 < Real.exp (D.p i * x - (D.p i)^2 * t) := Real.exp_pos _
    have hz : (-(D.p i - D.a))^((0:ℤ)) = (1:ℝ) := by simp
    rw [hz]
    simp only [mul_one]
    exact mul_pos (mul_pos hrho (zpow_pos hlam j)) hexp
  · intro k
    unfold rfacB
    have hlam : 0 < lam h (D.q k + D.a) := lam_q_pos' D h hD k
    have hexp : 0 < Real.exp (D.q k * x + (D.q k)^2 * t) := Real.exp_pos _
    have hz : (D.q k + D.a)^(-(0:ℤ)) = (1:ℝ) := by simp
    rw [hz]
    simp only [mul_one]
    exact mul_pos (zpow_pos hlam j) hexp

private lemma mul_diagonal_submatrix {N : ℕ}
    (K : Matrix (Fin N) (Fin N) ℝ) (c : Fin N → ℝ)
    (s : Finset (Fin N)) :
    (K * Matrix.diagonal c).submatrix Subtype.val Subtype.val
      = K.submatrix Subtype.val Subtype.val *
          Matrix.diagonal (fun i : s => c i.val) := by
  ext a b
  simp only [Matrix.submatrix_apply, Matrix.mul_apply, Matrix.diagonal_apply]
  rw [Finset.sum_eq_single b.val]
  · simp only [if_pos rfl]
    rw [Finset.sum_eq_single b]
    · simp
    · intro l _ hl
      rw [if_neg hl, mul_zero]
    · intro h
      exact absurd (Finset.mem_univ b) h
  · intro l _ hl
    rw [if_neg hl, mul_zero]
  · intro h
    exact absurd (Finset.mem_univ b.val) h

/-- Positivity of a Cauchy principal minor, reindexed along `Finset.orderIsoOfFin`. -/
private lemma cauchy_finset_minor_pos {N : ℕ} (D : Data N) (hD : PositiveData D h)
    (s : Finset (Fin N)) :
    0 < (Matrix.of (fun i j : s =>
        (D.p (i : Fin N) + D.q (j : Fin N))⁻¹)).det := by
  classical
  let e : Fin s.card ≃o s := s.orderIsoOfFin rfl
  have hv : StrictMono (fun i : Fin s.card => ((e i : s) : Fin N)) :=
    fun a b hab => e.strictMono hab
  have heq : (Matrix.of (fun i j : s =>
        (D.p (i : Fin N) + D.q (j : Fin N))⁻¹)).submatrix e.toEquiv e.toEquiv =
      Matrix.of (fun i j : Fin s.card =>
        (D.p ((e i : s) : Fin N) + D.q ((e j : s) : Fin N))⁻¹) := by
    ext i j
    simp [Matrix.submatrix_apply]
  rw [← Matrix.det_submatrix_equiv_self (OrderIso.toEquiv e), heq]
  exact det_cauchy_submatrix_pos D.p D.q (fun i => pos_p hD i) (fun k => pos_q hD k)
    hD.2.1 hD.2.2.1 _ hv

private lemma submatrix_K_eq_of {N : ℕ} (D : Data N)
    (s : Finset (Fin N)) :
    (Matrix.of (fun i k : Fin N => (D.p i + D.q k)⁻¹)).submatrix Subtype.val Subtype.val
      = Matrix.of (fun i j : s => (D.p i.val + D.q j.val)⁻¹) := by
  ext i j
  simp [Matrix.submatrix_apply]

private lemma minor_term_pos {N : ℕ} (D : Data N) (h : ℝ) (hD : PositiveData D h)
    (c : Fin N → ℝ) (hc : ∀ i, 0 < c i) (s : Finset (Fin N)) :
    0 < (((Matrix.of (fun i k : Fin N => (D.p i + D.q k)⁻¹) *
        Matrix.diagonal c).submatrix Subtype.val Subtype.val).det) := by
  have hK := submatrix_K_eq_of D s
  have hmul := mul_diagonal_submatrix
    (Matrix.of (fun i k : Fin N => (D.p i + D.q k)⁻¹)) c s
  rw [hmul, Matrix.det_mul, hK, Matrix.det_diagonal]
  exact mul_pos (cauchy_finset_minor_pos D hD s)
    (Finset.prod_pos fun i _ => hc i)

private lemma det_one_add_K_diag_pos {N : ℕ} (D : Data N) (h : ℝ)
    (hD : PositiveData D h) (c : Fin N → ℝ) (hc : ∀ i, 0 < c i) :
    0 < Matrix.det ((1 : Matrix (Fin N) (Fin N) ℝ) +
      Matrix.of (fun i k : Fin N => (D.p i + D.q k)⁻¹) * Matrix.diagonal c) := by
  classical
  rw [det_one_add_eq_sum_minors]
  refine Finset.sum_pos (fun s _ => ?_) ⟨∅, Finset.mem_univ _⟩
  exact minor_term_pos D h hD c hc s

private lemma c09_positive_F {N : ℕ} (D : Data N) (h : ℝ) (hD : PositiveData D h) :
    PositiveL (F D h) := by
  intro j x t
  obtain ⟨hA, hB⟩ := rfac_F_pos D h hD j x t
  have htr : F D h j x t =
      Matrix.det ((1 : Matrix (Fin N) (Fin N) ℝ) +
        Matrix.of (fun i k : Fin N => (D.p i + D.q k)⁻¹) *
          Matrix.diagonal (fun i => rfacB D h (D.a - h / 2) 1 j x t i *
            rfacA D h (D.a - h / 2) 1 j x t i)) := by
    simp only [F]
    rw [tau_eq_det_one_add, det_one_add_comm_diag]
  rw [htr]
  exact det_one_add_K_diag_pos D h hD _ (fun i => mul_pos (hB i) (hA i))

private lemma c09_positive_G {N : ℕ} (D : Data N) (h : ℝ) (hD : PositiveData D h) :
    PositiveL (G D h) := by
  intro j x t
  obtain ⟨hA, hB⟩ := rfac_G_pos D h hD j x t
  have htr : G D h j x t =
      Matrix.det ((1 : Matrix (Fin N) (Fin N) ℝ) +
        Matrix.of (fun i k : Fin N => (D.p i + D.q k)⁻¹) *
          Matrix.diagonal (fun i => rfacB D h D.a 0 j x t i *
            rfacA D h D.a 0 j x t i)) := by
    simp only [G]
    rw [tau_eq_det_one_add, det_one_add_comm_diag]
  rw [htr]
  exact det_one_add_K_diag_pos D h hD _ (fun i => mul_pos (hB i) (hA i))

/-- Full `C09`: admissibility, positivity and smoothness of `F` and `G`. -/
theorem c09_proved : C09 := by
  intro N D h hD
  refine ⟨c09_admissible_proved D h hD, c09_positive_F D h hD,
    c09_positive_G D h hD, ?_, ?_⟩
  · exact (c09_smooth_proved D h).1
  · exact (c09_smooth_proved D h).2

end DLWContract
