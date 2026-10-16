import GlobalCenterGeometry
import CantrellAlgebra
import Mathlib.Data.Fintype.Prod
import Mathlib.Data.Fintype.Card

/-! A direction-independent, boundary-inclusive 8 by 8 cover of all centers
at or below the public upper side. Each closed cell has diameter squared
98/100 < 1, so at most one packed unit-square center belongs to a cell. -/
namespace PackingGeometry.GlobalGrid
noncomputable section

def cell (k : Fin 8) (x : ℝ) : Prop :=
  1/2+(7/10)*(k.val:ℝ) ≤ x ∧ x ≤ 1/2+(7/10)*((k.val:ℝ)+1)

def belongs (s : Square) (k : Fin 8 × Fin 8) : Prop := cell k.1 s.cx ∧ cell k.2 s.cy

theorem coordinate_cover (x : ℝ) (hl : 1/2 ≤ x) (hu : x ≤ 61/10) :
    ∃ k : Fin 8, cell k x := by
  by_cases h0 : x ≤ 6/5
  · refine ⟨0,?_⟩
    norm_num [cell]
    constructor <;> linarith
  by_cases h1 : x ≤ 19/10
  · refine ⟨1,?_⟩
    norm_num [cell]
    constructor <;> linarith
  by_cases h2 : x ≤ 13/5
  · refine ⟨2,?_⟩
    norm_num [cell]
    constructor <;> linarith
  by_cases h3 : x ≤ 33/10
  · refine ⟨3,?_⟩
    norm_num [cell]
    constructor <;> linarith
  by_cases h4 : x ≤ 4
  · refine ⟨4,?_⟩
    norm_num [cell]
    constructor <;> linarith
  by_cases h5 : x ≤ 47/10
  · refine ⟨5,?_⟩
    norm_num [cell]
    constructor <;> linarith
  by_cases h6 : x ≤ 27/5
  · refine ⟨6,?_⟩
    norm_num [cell]
    constructor <;> linarith
  · refine ⟨7,?_⟩
    norm_num [cell]
    constructor <;> linarith

theorem same_cell_sq_le (k : Fin 8) (x y : ℝ) (hx : cell k x) (hy : cell k y) :
    (x-y)^2 ≤ 49/100 := by
  obtain ⟨hxL,hxU⟩ := hx
  obtain ⟨hyL,hyU⟩ := hy
  have hlo : -(7/10:ℝ) ≤ x-y := by linarith
  have hhi : x-y ≤ (7/10:ℝ) := by linarith
  have hp := mul_nonneg (show 0 ≤ (7/10:ℝ)-(x-y) by linarith)
    (show 0 ≤ (7/10:ℝ)+(x-y) by linarith)
  nlinarith

theorem grid_cover {n : ℕ} {L : ℝ} {squares : Fin n → Square}
    (h : IsPacking L squares) (hL : L ≤ Cantrell37.upper) :
    ∀ i, ∃ k : Fin 8 × Fin 8, belongs (squares i) k := by
  intro i
  obtain ⟨hxL,hxU,hyL,hyU⟩ := Global.center_bound h i
  have hu : Cantrell37.upper ≤ (33/5:ℝ) := by norm_num [Cantrell37.upper]
  obtain ⟨kx,hkx⟩ := coordinate_cover (squares i).cx hxL (by linarith)
  obtain ⟨ky,hky⟩ := coordinate_cover (squares i).cy hyL (by linarith)
  exact ⟨(kx,ky),hkx,hky⟩

theorem grid_capacity {n : ℕ} {L : ℝ} {squares : Fin n → Square}
    (h : IsPacking L squares) (i j : Fin n) (hij : i ≠ j)
    (k : Fin 8 × Fin 8) : ¬ (belongs (squares i) k ∧ belongs (squares j) k) := by
  rintro ⟨hi,hj⟩
  have hx := same_cell_sq_le k.1 (squares i).cx (squares j).cx hi.1 hj.1
  have hy := same_cell_sq_le k.2 (squares i).cy (squares j).cy hi.2 hj.2
  have hd := Global.centers_distance_sq h i j hij
  linarith

theorem grid_injection {n : ℕ} {L : ℝ} {squares : Fin n → Square}
    (h : IsPacking L squares) (hL : L ≤ Cantrell37.upper) :
    ∃ assigned : Fin n → Fin 8 × Fin 8, Function.Injective assigned ∧
      ∀ i, belongs (squares i) (assigned i) := by
  classical
  choose assigned ha using grid_cover h hL
  refine ⟨assigned,?_,ha⟩
  intro i j heq
  by_contra hne
  apply grid_capacity h i j hne (assigned i)
  refine ⟨ha i,?_⟩
  simpa [heq] using ha j

theorem packing_card_le_64 {n : ℕ} {L : ℝ} {squares : Fin n → Square}
    (h : IsPacking L squares) (hL : L ≤ Cantrell37.upper) : n ≤ 64 := by
  obtain ⟨assigned,hinj,_⟩ := grid_injection h hL
  have hc := Fintype.card_le_of_injective assigned hinj
  simpa using hc

#print axioms coordinate_cover
#print axioms grid_cover
#print axioms grid_capacity
#print axioms grid_injection
#print axioms packing_card_le_64

end
end PackingGeometry.GlobalGrid
