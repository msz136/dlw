import GlobalCenterGeometry
import GlobalOverlapWitness
import Mathlib.Data.Rat.Cast.Order
import Mathlib.Data.Rat.Cast.Lemmas
import Mathlib.Logic.Function.Basic

/-! Finite certificates excluding continuous pose boxes. Splits cover their
closed boundary in both children. Unknown leaves never count as exclusions.
The owner set is Fin n at every node, so recursion cannot silently drop owners.
This module provides soundness, not a complete exclusion certificate for 37. -/
namespace SquarePacking37.GlobalBranchTree
open PackingGeometry

structure Interval where
  lo : ℚ
  hi : ℚ
  deriving DecidableEq

inductive Coordinate where
  | cx | cy | ux | uy
  deriving DecidableEq

structure PoseBox where
  cx : Interval
  cy : Interval
  ux : Interval
  uy : Interval
  deriving DecidableEq

def PoseBox.get (b : PoseBox) : Coordinate → Interval
  | .cx => b.cx | .cy => b.cy | .ux => b.ux | .uy => b.uy

def PoseBox.set (b : PoseBox) (c : Coordinate) (a : Interval) : PoseBox :=
  match c with
  | .cx => {b with cx := a}
  | .cy => {b with cy := a}
  | .ux => {b with ux := a}
  | .uy => {b with uy := a}

def value (s : Square) : Coordinate → ℝ
  | .cx => s.cx | .cy => s.cy | .ux => s.ux | .uy => s.uy

def Interval.Contains (a : Interval) (x : ℝ) : Prop := (a.lo : ℝ) ≤ x ∧ x ≤ a.hi
def Holds (b : PoseBox) (s : Square) : Prop := ∀ c, (b.get c).Contains (value s c)
abbrev State (n : ℕ) := Fin n → PoseBox
def Represents {n : ℕ} (bs : State n) (ss : Fin n → Square) : Prop :=
  ∀ i, Holds (bs i) (ss i)

def Interval.left (a : Interval) (q : ℚ) : Interval := ⟨a.lo, min a.hi q⟩
def Interval.right (a : Interval) (q : ℚ) : Interval := ⟨max a.lo q, a.hi⟩

def splitLeft {n : ℕ} (bs : State n) (i : Fin n) (c : Coordinate) (q : ℚ) : State n :=
  Function.update bs i ((bs i).set c ((bs i).get c |>.left q))
def splitRight {n : ℕ} (bs : State n) (i : Fin n) (c : Coordinate) (q : ℚ) : State n :=
  Function.update bs i ((bs i).set c ((bs i).get c |>.right q))

theorem holds_set (b : PoseBox) (s : Square) (c : Coordinate) (a : Interval)
    (h : Holds b s) (ha : a.Contains (value s c)) : Holds (b.set c a) s := by
  intro d
  by_cases hd : d = c
  · subst d
    cases c <;> simpa [PoseBox.set, PoseBox.get] using ha
  · have hbase := h d
    cases c <;> cases d <;> simp_all [PoseBox.set, PoseBox.get]

theorem split_complete {n : ℕ} (bs : State n) (ss : Fin n → Square)
    (i : Fin n) (c : Coordinate) (q : ℚ) (h : Represents bs ss) :
    Represents (splitLeft bs i c q) ss ∨ Represents (splitRight bs i c q) ss := by
  rcases le_total (value (ss i) c) (q : ℝ) with hl | hr
  · left
    intro j
    by_cases hj : j = i
    · subst j
      simp only [splitLeft, Function.update_self]
      apply holds_set _ _ _ _ (h i)
      have hc := h i c
      exact ⟨hc.1, by simpa [Interval.left, Rat.cast_min] using le_min hc.2 hl⟩
    · simpa [splitLeft, Function.update_of_ne hj] using h j
  · right
    intro j
    by_cases hj : j = i
    · subst j
      simp only [splitRight, Function.update_self]
      apply holds_set _ _ _ _ (h i)
      have hc := h i c
      exact ⟨by simpa [Interval.right, Rat.cast_max] using max_le hc.1 hr, hc.2⟩
    · simpa [splitRight, Function.update_of_ne hj] using h j

def far (a b : Interval) : ℚ := max |a.hi-b.lo| |a.lo-b.hi|
def maxCenterDistanceSq (a b : PoseBox) : ℚ := (far a.cx b.cx)^2+(far a.cy b.cy)^2

theorem difference_sq_le (a b : Interval) (x y : ℝ)
    (hx : a.Contains x) (hy : b.Contains y) : (x-y)^2 ≤ ((far a b : ℚ) : ℝ)^2 := by
  have hp : a.hi-b.lo ≤ far a b :=
    (le_abs_self _).trans (le_max_left _ _)
  have hm : -(far a b) ≤ a.lo-b.hi := by
    have h := (neg_abs_le (a.lo-b.hi))
    have hg := le_max_right |a.hi-b.lo| |a.lo-b.hi|
    dsimp [far]
    linarith
  have hp' : (a.hi : ℝ)-(b.lo : ℝ) ≤ (far a b : ℚ) := by exact_mod_cast hp
  have hm' : -((far a b : ℚ) : ℝ) ≤ (a.lo : ℝ)-(b.hi : ℝ) := by exact_mod_cast hm
  have hu : x-y ≤ (far a b : ℚ) := by linarith [hx.2,hy.1]
  have hl : -((far a b : ℚ) : ℝ) ≤ x-y := by linarith [hx.1,hy.2]
  nlinarith [mul_nonneg (sub_nonneg.mpr hu) (by linarith : 0 ≤ ((far a b : ℚ) : ℝ)+(x-y))]

theorem distance_le_box (a b : PoseBox) (s t : Square) (hs : Holds a s) (ht : Holds b t) :
    (s.cx-t.cx)^2+(s.cy-t.cy)^2 ≤ (maxCenterDistanceSq a b : ℝ) := by
  have hx := difference_sq_le a.cx b.cx s.cx t.cx (hs .cx) (ht .cx)
  have hy := difference_sq_le a.cy b.cy s.cy t.cy (hs .cy) (ht .cy)
  have he : (maxCenterDistanceSq a b : ℝ) =
      ((far a.cx b.cx : ℚ) : ℝ)^2+((far a.cy b.cy : ℚ) : ℝ)^2 := by
    simp [maxCenterDistanceSq]
  rw [he]
  linarith

def Interval.Enclosed (a : Interval) (center error : ℚ) : Prop :=
  center-error ≤ a.lo ∧ a.hi ≤ center+error

def Enclosed (b : PoseBox) (w : OverlapWitness.Window) : Prop :=
  b.cx.Enclosed w.cx w.centerError ∧ b.cy.Enclosed w.cy w.centerError ∧
  b.ux.Enclosed w.ux w.directionError ∧ b.uy.Enclosed w.uy w.directionError

instance (a : Interval) (c e : ℚ) : Decidable (a.Enclosed c e) :=
  inferInstanceAs (Decidable (_ ∧ _))
instance (b : PoseBox) (w : OverlapWitness.Window) : Decidable (Enclosed b w) :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ _ ∧ _))
instance (w : OverlapWitness.Window) (px py : ℚ) : Decidable (OverlapWitness.PointCertificate w px py) :=
  inferInstanceAs (Decidable (_ ∧ _))

theorem interval_error (a : Interval) (c e : ℚ) (x : ℝ)
    (he : a.Enclosed c e) (hx : a.Contains x) : |x-(c:ℝ)| ≤ (e:ℝ) := by
  have hlo : (c:ℝ)-(e:ℝ) ≤ (a.lo:ℝ) := by exact_mod_cast he.1
  have hhi : (a.hi:ℝ) ≤ (c:ℝ)+(e:ℝ) := by exact_mod_cast he.2
  apply abs_le.mpr
  constructor <;> linarith [hx.1,hx.2]

theorem enclosed_fits (b : PoseBox) (w : OverlapWitness.Window) (s : Square)
    (he : Enclosed b w) (hs : Holds b s) : OverlapWitness.Fits w s := by
  exact ⟨interval_error b.cx w.cx w.centerError s.cx he.1 (hs .cx),
    interval_error b.cy w.cy w.centerError s.cy he.2.1 (hs .cy),
    interval_error b.ux w.ux w.directionError s.ux he.2.2.1 (hs .ux),
    interval_error b.uy w.uy w.directionError s.uy he.2.2.2 (hs .uy)⟩

inductive Tree (n : ℕ) where
  | unknown
  | empty (owner : Fin n) (coordinate : Coordinate)
  | collision (first second : Fin n)
  | overlap (first second : Fin n) (firstWindow secondWindow : OverlapWitness.Window) (px py : ℚ)
  | split (owner : Fin n) (coordinate : Coordinate) (cut : ℚ) (left right : Tree n)

def check {n : ℕ} (bs : State n) : Tree n → Bool
  | .unknown => false
  | .empty i c => decide (((bs i).get c).hi < ((bs i).get c).lo)
  | .collision i j => decide (i ≠ j ∧ maxCenterDistanceSq (bs i) (bs j) < 1)
  | .overlap i j wi wj px py => decide (i < j ∧ Enclosed (bs i) wi ∧ Enclosed (bs j) wj ∧
      OverlapWitness.PointCertificate wi px py ∧ OverlapWitness.PointCertificate wj px py)
  | .split i c q l r => check (splitLeft bs i c q) l && check (splitRight bs i c q) r

def unknownCount {n : ℕ} : Tree n → ℕ
  | .unknown => 1
  | .empty _ _ => 0
  | .collision _ _ => 0
  | .overlap _ _ _ _ _ _ => 0
  | .split _ _ _ l r => unknownCount l + unknownCount r

theorem accepted_has_no_unknown {n : ℕ} (t : Tree n) (bs : State n)
    (h : check bs t = true) : unknownCount t = 0 := by
  induction t generalizing bs with
  | unknown => simp [check] at h
  | empty i c => rfl
  | collision i j => rfl
  | overlap i j wi wj px py => rfl
  | split i c q l r ihl ihr =>
      simp only [check, Bool.and_eq_true] at h
      simp [unknownCount, ihl _ h.1, ihr _ h.2]

theorem check_sound {n : ℕ} (t : Tree n) (bs : State n)
    (hcheck : check bs t = true) {L : ℝ} (ss : Fin n → Square)
    (hpacking : IsPacking L ss) (hrep : Represents bs ss) : False := by
  induction t generalizing bs with
  | unknown => simp [check] at hcheck
  | empty i c =>
      have he : ((bs i).get c).hi < ((bs i).get c).lo := by simpa [check] using hcheck
      have he' : (((bs i).get c).hi : ℝ) < (((bs i).get c).lo : ℝ) := by exact_mod_cast he
      have hc := hrep i c
      exact (not_lt_of_ge (hc.1.trans hc.2)) he'
  | collision i j =>
      have hc : i ≠ j ∧ maxCenterDistanceSq (bs i) (bs j) < 1 := by simpa [check] using hcheck
      have hlt : (maxCenterDistanceSq (bs i) (bs j) : ℝ) < 1 := by exact_mod_cast hc.2
      have hbound := distance_le_box (bs i) (bs j) (ss i) (ss j) (hrep i) (hrep j)
      have hge := PackingGeometry.Global.centers_distance_sq hpacking i j hc.1
      linarith
  | overlap i j wi wj px py =>
      have hc : i < j ∧ Enclosed (bs i) wi ∧ Enclosed (bs j) wj ∧
          OverlapWitness.PointCertificate wi px py ∧ OverlapWitness.PointCertificate wj px py := by
        simpa only [check, decide_eq_true_eq] using hcheck
      exact OverlapWitness.rejects_packing_window L ss i j hc.1 wi wj px py
        (enclosed_fits _ _ _ hc.2.1 (hrep i)) (enclosed_fits _ _ _ hc.2.2.1 (hrep j))
        hc.2.2.2.1 hc.2.2.2.2 hpacking
  | split i c q l r ihl ihr =>
      simp only [check, Bool.and_eq_true] at hcheck
      rcases split_complete bs ss i c q hrep with hl | hr
      · exact ihl _ hcheck.1 hl
      · exact ihr _ hcheck.2 hr

def rootState (n : ℕ) (target : ℚ) : State n := fun _ =>
  ⟨⟨1/2,target-1/2⟩,⟨1/2,target-1/2⟩,⟨-1,1⟩,⟨-1,1⟩⟩

theorem every_packing_represented {n : ℕ} (target : ℚ) {L : ℝ}
    (ss : Fin n → Square) (hp : IsPacking L ss) (hL : L ≤ (target:ℝ)) :
    Represents (rootState n target) ss := by
  intro i c
  have hb := PackingGeometry.Global.center_bound hp i
  have hu := OverlapWitness.unit_components (ss i) (hp.1 i)
  rcases abs_le.mp hu.1 with ⟨huxlo,huxhi⟩
  rcases abs_le.mp hu.2 with ⟨huylo,huyhi⟩
  cases c <;> dsimp [rootState, PoseBox.get, Interval.Contains, value] <;>
    push_cast <;> constructor <;> linarith [hb.1,hb.2.1,hb.2.2.1,hb.2.2.2]

-- Only a fully checked finite tree proves an exclusion. No such tree near
-- the 37-square endpoint is supplied by this generic assembly theorem.
theorem global_exclusion {n : ℕ} (target : ℚ) (t : Tree n)
    (hcheck : check (rootState n target) t = true) {L : ℝ}
    (hL : L ≤ (target:ℝ)) (ss : Fin n → Square) : ¬ IsPacking L ss := by
  intro hp
  exact check_sound t _ hcheck ss hp (every_packing_represented target ss hp hL)

-- The split is necessary: neither root collision leaf accepts. Both closed
-- child windows are excluded by different owners. An unknown child rejects.
def demoBox (x : Interval) : PoseBox := ⟨x, ⟨0,0⟩, ⟨-1,1⟩, ⟨-1,1⟩⟩
def demoState : State 3 := fun i =>
  if i = 0 then demoBox ⟨0,2⟩ else if i = 1 then demoBox ⟨1/2,1/2⟩ else demoBox ⟨3/2,3/2⟩
def demoTree : Tree 3 := .split 0 .cx 1 (.collision 0 1) (.collision 0 2)

theorem demo_requires_split :
    check demoState (.collision 0 1) = false ∧ check demoState (.collision 0 2) = false := by
  norm_num [check,demoState,demoBox,maxCenterDistanceSq,far]
theorem demo_accepted : check demoState demoTree = true := by
  norm_num [check,demoTree,demoState,demoBox,maxCenterDistanceSq,far,splitLeft,splitRight,
    PoseBox.get,PoseBox.set,Interval.left,Interval.right,Function.update]
theorem demo_unknown_rejected :
    check demoState (.split 0 .cx 1 (.collision 0 1) .unknown) = false := by simp [check]
theorem demo_self_rejected : check demoState (.collision 1 1) = false := by decide
theorem demo_touching_rejected : check demoState (.collision 1 2) = false := by
  norm_num [check,demoState,demoBox,maxCenterDistanceSq,far]
theorem demo_no_packing {L : ℝ} (ss : Fin 3 → Square) :
    ¬ (IsPacking L ss ∧ Represents demoState ss) := by
  intro h
  exact check_sound demoTree demoState demo_accepted ss h.1 h.2

#print axioms split_complete
#print axioms accepted_has_no_unknown
#print axioms check_sound
#print axioms enclosed_fits
#print axioms every_packing_represented
#print axioms global_exclusion
#print axioms demo_accepted
#print axioms demo_no_packing

end SquarePacking37.GlobalBranchTree
