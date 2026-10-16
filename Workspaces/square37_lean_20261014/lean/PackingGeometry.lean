import Mathlib.Basic.Real.Basic
import Mathlib.Data.Rat.Cast.Order
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Push

/-! Rotatable unit-square packings, with an exact rational SAT bridge.
The two basis vectors of each square are (ux,uy) and (-uy,ux).
The coefficient-open square is its geometric interior for a unit basis.
No global lower bound or optimality is assumed here. -/
namespace PackingGeometry
noncomputable section

abbrev Point := ℝ × ℝ

structure Square where
  cx : ℝ
  cy : ℝ
  ux : ℝ
  uy : ℝ

def Square.IsUnit (s : Square) : Prop := s.ux ^ 2 + s.uy ^ 2 = 1

def Square.point (s : Square) (a b : ℝ) : Point :=
  (s.cx + a * s.ux - b * s.uy, s.cy + a * s.uy + b * s.ux)

def Square.closed (s : Square) (p : Point) : Prop :=
  ∃ a b : ℝ, |a| ≤ 1 / 2 ∧ |b| ≤ 1 / 2 ∧ p = s.point a b

def Square.inside (s : Square) (p : Point) : Prop :=
  ∃ a b : ℝ, |a| < 1 / 2 ∧ |b| < 1 / 2 ∧ p = s.point a b

def InContainer (L : ℝ) (p : Point) : Prop :=
  0 ≤ p.1 ∧ p.1 ≤ L ∧ 0 ≤ p.2 ∧ p.2 ≤ L

def IsPacking {n : ℕ} (L : ℝ) (s : Fin n → Square) : Prop :=
  (∀ i, (s i).IsUnit) ∧
  (∀ i p, (s i).closed p → InContainer L p) ∧
  (∀ i j, i < j → ∀ p, ¬ ((s i).inside p ∧ (s j).inside p))

def dot (nx ny x y : ℝ) : ℝ := nx * x + ny * y

def support (s : Square) (nx ny : ℝ) : ℝ :=
  (|nx * s.ux + ny * s.uy| + |-(nx * s.uy) + ny * s.ux|) / 2

theorem linear_bound (a b A B : ℝ) (ha : |a| ≤ 1 / 2) (hb : |b| ≤ 1 / 2) :
    |a * A + b * B| ≤ (|A| + |B|) / 2 := by
  have h₁ := mul_le_mul_of_nonneg_right ha (abs_nonneg A)
  have h₂ := mul_le_mul_of_nonneg_right hb (abs_nonneg B)
  calc
    |a * A + b * B| ≤ |a * A| + |b * B| := abs_add_le _ _
    _ = |a| * |A| + |b| * |B| := by rw [abs_mul, abs_mul]
    _ ≤ (|A| + |B|) / 2 := by linarith

theorem linear_bound_strict (a b A B : ℝ) (ha : |a| < 1 / 2)
    (hb : |b| < 1 / 2) (hne : A ≠ 0 ∨ B ≠ 0) :
    |a * A + b * B| < (|A| + |B|) / 2 := by
  have h₁ := mul_le_mul_of_nonneg_right ha.le (abs_nonneg A)
  have h₂ := mul_le_mul_of_nonneg_right hb.le (abs_nonneg B)
  have hs : |a| * |A| + |b| * |B| < (|A| + |B|) / 2 := by
    rcases hne with hA | hB
    · have := mul_lt_mul_of_pos_right ha (abs_pos.mpr hA)
      linarith
    · have := mul_lt_mul_of_pos_right hb (abs_pos.mpr hB)
      linarith
  calc
    |a * A + b * B| ≤ |a * A| + |b * B| := abs_add_le _ _
    _ = |a| * |A| + |b| * |B| := by rw [abs_mul, abs_mul]
    _ < (|A| + |B|) / 2 := hs

theorem contained_of_bounds (s : Square) (L : ℝ)
    (hx₀ : (|s.ux| + |s.uy|) / 2 ≤ s.cx)
    (hx₁ : s.cx + (|s.ux| + |s.uy|) / 2 ≤ L)
    (hy₀ : (|s.ux| + |s.uy|) / 2 ≤ s.cy)
    (hy₁ : s.cy + (|s.ux| + |s.uy|) / 2 ≤ L) :
    ∀ p, s.closed p → InContainer L p := by
  rintro p ⟨a, b, ha, hb, rfl⟩
  have hx := linear_bound a b s.ux (-s.uy) ha hb
  have hy := linear_bound a b s.uy s.ux ha hb
  rw [abs_neg] at hx
  rcases abs_le.mp hx with ⟨hxlo, hxhi⟩
  rcases abs_le.mp hy with ⟨hylo, hyhi⟩
  unfold InContainer Square.point
  dsimp
  constructor
  · linarith
  constructor
  · linarith
  constructor <;> linarith

theorem inside_projection_strict (s : Square) (hs : s.IsUnit)
    (nx ny : ℝ) (hn : nx ^ 2 + ny ^ 2 = 1) (p : Point) (hp : s.inside p) :
    |dot nx ny (p.1 - s.cx) (p.2 - s.cy)| < support s nx ny := by
  rcases hp with ⟨a, b, ha, hb, rfl⟩
  have hne : nx * s.ux + ny * s.uy ≠ 0 ∨ -(nx * s.uy) + ny * s.ux ≠ 0 := by
    by_contra h
    push Not at h
    rcases h with ⟨h₁, h₂⟩
    have ident : (nx * s.ux + ny * s.uy)^2 + (-(nx * s.uy) + ny * s.ux)^2 =
        (nx^2 + ny^2) * (s.ux^2 + s.uy^2) := by ring
    rw [h₁, h₂, hn, hs] at ident
    norm_num at ident
  have h := linear_bound_strict a b (nx * s.ux + ny * s.uy)
    (-(nx * s.uy) + ny * s.ux) ha hb hne
  unfold support
  convert h using 1 <;> unfold dot Square.point <;> congr 1 <;> ring

theorem disjoint_of_separation (s t : Square) (hs : s.IsUnit) (ht : t.IsUnit)
    (nx ny : ℝ) (hn : nx ^ 2 + ny ^ 2 = 1)
    (hsep : support s nx ny + support t nx ny ≤ dot nx ny (t.cx-s.cx) (t.cy-s.cy)) :
    ∀ p, ¬ (s.inside p ∧ t.inside p) := by
  rintro p ⟨hp, hq⟩
  have h₁ := abs_lt.mp (inside_projection_strict s hs nx ny hn p hp)
  have h₂ := abs_lt.mp (inside_projection_strict t ht nx ny hn p hq)
  have hid : dot nx ny (t.cx-s.cx) (t.cy-s.cy) =
      dot nx ny (p.1-s.cx) (p.2-s.cy) - dot nx ny (p.1-t.cx) (p.2-t.cy) := by
    unfold dot
    ring
  linarith

theorem closed_projection_bound (s : Square) (nx ny : ℝ) (p : Point)
    (hp : s.closed p) :
    |dot nx ny (p.1 - s.cx) (p.2 - s.cy)| ≤ support s nx ny := by
  rcases hp with ⟨a, b, ha, hb, rfl⟩
  have h := linear_bound a b (nx * s.ux + ny * s.uy)
    (-(nx * s.uy) + ny * s.ux) ha hb
  unfold support
  convert h using 1 <;> unfold dot Square.point <;> congr 1 <;> ring

theorem closed_disjoint_of_strict_separation (s t : Square) (nx ny : ℝ)
    (hsep : support s nx ny + support t nx ny < dot nx ny (t.cx-s.cx) (t.cy-s.cy)) :
    ∀ p, ¬ (s.closed p ∧ t.closed p) := by
  rintro p ⟨hp, hq⟩
  have h₁ := abs_le.mp (closed_projection_bound s nx ny p hp)
  have h₂ := abs_le.mp (closed_projection_bound t nx ny p hq)
  have hid : dot nx ny (t.cx-s.cx) (t.cy-s.cy) =
      dot nx ny (p.1-s.cx) (p.2-s.cy) - dot nx ny (p.1-t.cx) (p.2-t.cy) := by
    unfold dot
    ring
  linarith

structure QSquare where
  cx : ℚ
  cy : ℚ
  ux : ℚ
  uy : ℚ
  deriving DecidableEq

def QSquare.real (q : QSquare) : Square := ⟨q.cx, q.cy, q.ux, q.uy⟩

def QSquare.unit (q : QSquare) : Prop := q.ux ^ 2 + q.uy ^ 2 = 1

def QSquare.bounds (q : QSquare) (L : ℚ) : Prop :=
  (|q.ux| + |q.uy|) / 2 ≤ q.cx ∧ q.cx + (|q.ux| + |q.uy|) / 2 ≤ L ∧
  (|q.ux| + |q.uy|) / 2 ≤ q.cy ∧ q.cy + (|q.ux| + |q.uy|) / 2 ≤ L

def qsupport (q : QSquare) (nx ny : ℚ) : ℚ :=
  (|nx * q.ux + ny * q.uy| + |-(nx * q.uy) + ny * q.ux|) / 2

def QSeparated (q r : QSquare) (nx ny : ℚ) : Prop :=
  nx ^ 2 + ny ^ 2 = 1 ∧
  qsupport q nx ny + qsupport r nx ny ≤ nx * (r.cx-q.cx) + ny * (r.cy-q.cy)

def QStrictSeparated (q r : QSquare) (nx ny : ℚ) : Prop :=
  nx ^ 2 + ny ^ 2 = 1 ∧
  qsupport q nx ny + qsupport r nx ny < nx * (r.cx-q.cx) + ny * (r.cy-q.cy)

theorem QStrictSeparated.weak {q r : QSquare} {nx ny : ℚ}
    (h : QStrictSeparated q r nx ny) : QSeparated q r nx ny := ⟨h.1, h.2.le⟩

instance (q : QSquare) : Decidable q.unit := inferInstanceAs (Decidable (_ = _))
instance (q : QSquare) (L : ℚ) : Decidable (q.bounds L) :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ _ ∧ _))
instance (q r : QSquare) (nx ny : ℚ) : Decidable (QSeparated q r nx ny) :=
  inferInstanceAs (Decidable (_ ∧ _))

theorem real_unit (q : QSquare) (hq : q.unit) : q.real.IsUnit := by
  dsimp [Square.IsUnit, QSquare.real]
  unfold QSquare.unit at hq
  simp only [pow_two] at hq ⊢
  exact_mod_cast hq

theorem real_bounds (q : QSquare) (L : ℚ) (hq : q.bounds L) :
    ∀ p, q.real.closed p → InContainer (L : ℝ) p := by
  rcases hq with ⟨hx₀, hx₁, hy₀, hy₁⟩
  apply contained_of_bounds
  all_goals dsimp [QSquare.real]
  · exact_mod_cast hx₀
  · exact_mod_cast hx₁
  · exact_mod_cast hy₀
  · exact_mod_cast hy₁

theorem real_separated (q r : QSquare) (hq : q.unit) (hr : r.unit)
    (nx ny : ℚ) (h : QSeparated q r nx ny) :
    ∀ p, ¬ (q.real.inside p ∧ r.real.inside p) := by
  rcases h with ⟨hn, hs⟩
  apply disjoint_of_separation q.real r.real (real_unit q hq) (real_unit r hr) nx ny
  · simp only [pow_two] at hn ⊢
    exact_mod_cast hn
  · dsimp [support, dot, QSquare.real]
    unfold qsupport at hs
    exact_mod_cast hs

theorem real_closed_separated (q r : QSquare) (nx ny : ℚ)
    (h : QStrictSeparated q r nx ny) :
    ∀ p, ¬ (q.real.closed p ∧ r.real.closed p) := by
  apply closed_disjoint_of_strict_separation q.real r.real nx ny
  have hs := h.2
  dsimp [support, dot, QSquare.real]
  unfold qsupport at hs
  exact_mod_cast hs

theorem packing_of_rational_certificate {n : ℕ} (L : ℚ) (q : Fin n → QSquare)
    (normal : Fin n → Fin n → ℚ × ℚ)
    (hu : ∀ i, (q i).unit) (hb : ∀ i, (q i).bounds L)
    (hsep : ∀ i j, i < j → QSeparated (q i) (q j) (normal i j).1 (normal i j).2) :
    IsPacking (L : ℝ) (fun i => (q i).real) := by
  refine ⟨fun i => real_unit (q i) (hu i), fun i => real_bounds (q i) L (hb i), ?_⟩
  intro i j hij
  exact real_separated (q i) (q j) (hu i) (hu j) _ _ (hsep i j hij)

#print axioms packing_of_rational_certificate

end
end PackingGeometry
