import CantrellSupports
import Mathlib.Tactic.FieldSimp

/-! An exact half-angle parameter for the selected support-branch crossing.
This gives an angle and the algebraic crossing side, not a global packing proof. -/
namespace Cantrell37.Angle
noncomputable section

def polynomial (q : ℝ) : ℝ :=
  (4-Real.sqrt 2)*q^4+(12-2*Real.sqrt 2)*q^2-Real.sqrt 2

def lowerQ : ℝ := 3847314469214599/10000000000000000
def upperQ : ℝ := 3847314469214600/10000000000000000
def sqrtLower : ℝ := 14142135623730950488/10000000000000000000
def sqrtUpper : ℝ := 14142135623730950489/10000000000000000000

theorem sqrt_bounds : sqrtLower < Real.sqrt 2 ∧ Real.sqrt 2 < sqrtUpper := by
  have hs : (Real.sqrt 2)^2=2 := Real.sq_sqrt (by norm_num)
  have hn : 0 ≤ Real.sqrt 2 := Real.sqrt_nonneg 2
  have hl : 0 ≤ sqrtLower := by norm_num [sqrtLower]
  have hu : 0 ≤ sqrtUpper := by norm_num [sqrtUpper]
  have hls : sqrtLower^2<2 := by norm_num [sqrtLower]
  have hus : 2<sqrtUpper^2 := by norm_num [sqrtUpper]
  constructor <;> nlinarith

theorem polynomial_expanded (q : ℝ) :
    polynomial q = 4*q^4+12*q^2-Real.sqrt 2*(1+q^2)^2 := by
  unfold polynomial
  ring

theorem lowerQ_sign : polynomial lowerQ < 0 := by
  have hm := mul_le_mul_of_nonneg_right sqrt_bounds.1.le (sq_nonneg (1+lowerQ^2))
  have hc : polynomial lowerQ ≤ 4*lowerQ^4+12*lowerQ^2-sqrtLower*(1+lowerQ^2)^2 := by
    rw [polynomial_expanded]
    linarith
  exact lt_of_le_of_lt hc (by norm_num [lowerQ,sqrtLower])

theorem upperQ_sign : 0 < polynomial upperQ := by
  have hm := mul_le_mul_of_nonneg_right sqrt_bounds.2.le (sq_nonneg (1+upperQ^2))
  have hc : 4*upperQ^4+12*upperQ^2-sqrtUpper*(1+upperQ^2)^2 ≤ polynomial upperQ := by
    rw [polynomial_expanded]
    linarith
  exact lt_of_lt_of_le (by norm_num [upperQ,sqrtUpper]) hc

theorem polynomial_strictMono : StrictMonoOn polynomial (Set.Icc lowerQ upperQ) := by
  intro a ha b hb hab
  have ha0 : 0 ≤ a := le_trans (by norm_num [lowerQ]) ha.1
  have hb0 : 0 ≤ b := ha0.trans hab.le
  have habplus : 0 < b+a := by linarith
  have hp := mul_pos (sub_pos.mpr hab) habplus
  have h2 : a^2 < b^2 := by nlinarith
  have h4 : a^4 ≤ b^4 := pow_le_pow_left₀ ha0 hab.le 4
  have hr : Real.sqrt 2 < 2 := lt_trans sqrt_bounds.2 (by norm_num [sqrtUpper])
  have hc4 : 0 ≤ 4-Real.sqrt 2 := by linarith
  have hc2 : 0 < 12-2*Real.sqrt 2 := by linarith
  have hm4 := mul_le_mul_of_nonneg_left h4 hc4
  have hm2 := mul_lt_mul_of_pos_left h2 hc2
  unfold polynomial
  linarith

theorem root_exists_unique : ∃! q : ℝ, q ∈ Set.Icc lowerQ upperQ ∧ polynomial q = 0 := by
  have hlu : lowerQ ≤ upperQ := by norm_num [lowerQ,upperQ]
  have hc : ContinuousOn polynomial (Set.Icc lowerQ upperQ) := by unfold polynomial; fun_prop
  obtain ⟨q,hq,hp⟩ := intermediate_value_Icc hlu hc
    (show (0:ℝ) ∈ Set.Icc (polynomial lowerQ) (polynomial upperQ) from
      ⟨lowerQ_sign.le,upperQ_sign.le⟩)
  refine ⟨q,⟨hq,hp⟩,?_⟩
  intro p hp'
  exact polynomial_strictMono.injOn hp'.1 hq (hp'.2.trans hp.symm)

def root : ℝ := Classical.choose root_exists_unique

theorem root_spec : root ∈ Set.Icc lowerQ upperQ ∧ polynomial root = 0 :=
  (Classical.choose_spec root_exists_unique).1

theorem root_strict_interval : lowerQ < root ∧ root < upperQ := by
  have hs := root_spec
  constructor
  · rcases hs.1.1.eq_or_lt with he | hl
    · have hz : polynomial lowerQ=0 := he.symm ▸ hs.2
      linarith [lowerQ_sign]
    · exact hl
  · rcases hs.1.2.eq_or_lt with he | hl
    · have hz : polynomial upperQ=0 := he ▸ hs.2
      linarith [upperQ_sign]
    · exact hl

def cosQ (q : ℝ) : ℝ := (1-q^2)/(1+q^2)
def sinQ (q : ℝ) : ℝ := 2*q/(1+q^2)
def denominator (q : ℝ) : ℝ := 1+2*q-q^2
def numerator (q : ℝ) : ℝ := 7+10*q-q^2
def sideQ (q : ℝ) : ℝ := numerator q / denominator q

theorem half_angle_unit (q : ℝ) : (cosQ q)^2+(sinQ q)^2=1 := by
  have hn : 1+q^2 ≠ 0 := ne_of_gt (by positivity)
  unfold cosQ sinQ
  field_simp
  <;> nlinarith [sq_nonneg q]

theorem denominator_positive (q : ℝ) (hq0 : 0 ≤ q) (hq1 : q ≤ 1) :
    0 < denominator q := by
  have hm := mul_nonneg hq0 (sub_nonneg.mpr hq1)
  unfold denominator
  nlinarith

theorem sideQ_mono (p q : ℝ) (hp : 3/8 ≤ p) (hpq : p ≤ q) (hq : q ≤ 1) :
    sideQ p ≤ sideQ q := by
  have hp0 : 0 ≤ p := le_trans (by norm_num) hp
  have hq0 : 0 ≤ q := hp0.trans hpq
  have hDp := denominator_positive p hp0 (hpq.trans hq)
  have hDq := denominator_positive q hq0 hq
  have hpq0 : 0 ≤ p*q := mul_nonneg hp0 hq0
  have hfac : 0 ≤ 4*p*q+3*p+3*q-2 := by nlinarith
  have hmul := mul_nonneg (sub_nonneg.mpr hpq) hfac
  unfold sideQ
  apply (div_le_div_iff₀ hDp hDq).mpr
  have hid : numerator q*denominator p-numerator p*denominator q =
      2*(q-p)*(4*p*q+3*p+3*q-2) := by unfold numerator denominator; ring
  nlinarith

theorem side_root_interval : sideQ root ∈ Set.Icc lower upper := by
  have hleft := sideQ_mono lowerQ root (by norm_num [lowerQ]) root_spec.1.1
    (le_trans root_spec.1.2 (by norm_num [upperQ]))
  have hright := sideQ_mono root upperQ
    (le_trans (by norm_num [lowerQ]) root_spec.1.1) root_spec.1.2 (by norm_num [upperQ])
  constructor
  · exact le_trans (by norm_num [lower,sideQ,numerator,denominator,lowerQ]) hleft
  · exact le_trans hright (by norm_num [upper,sideQ,numerator,denominator,upperQ])

theorem first_support_equality (q : ℝ) (hd : denominator q ≠ 0) :
    3+4*cosQ q+5*sinQ q=(cosQ q+sinQ q)*sideQ q := by
  have hh : 1+q^2 ≠ 0 := ne_of_gt (by positivity)
  unfold cosQ sinQ sideQ numerator denominator at *
  field_simp [hh,hd]
  have hd' : 1+q*2-q^2 ≠ 0 := by simpa [mul_comm] using hd
  field_simp [hd']
  <;> ring

theorem second_support_residual (q : ℝ) (hd : denominator q ≠ 0) :
    2*(1+sinQ q*(cosQ q-sinQ q))*sideQ q -
      (6+8*cosQ q+10*sinQ q*(cosQ q-sinQ q)+Real.sqrt 2) =
      polynomial q/(1+q^2)^2 := by
  have hh : 1+q^2 ≠ 0 := ne_of_gt (by positivity)
  unfold cosQ sinQ sideQ numerator denominator polynomial at *
  field_simp
  <;> ring

theorem support_equalities_root :
    3+4*cosQ root+5*sinQ root=(cosQ root+sinQ root)*sideQ root ∧
    6+8*cosQ root+10*sinQ root*(cosQ root-sinQ root)+Real.sqrt 2 =
      2*(1+sinQ root*(cosQ root-sinQ root))*sideQ root := by
  have hq0 : 0 ≤ root := le_trans (by norm_num [lowerQ]) root_spec.1.1
  have hq1 : root ≤ 1 := le_trans root_spec.1.2 (by norm_num [upperQ])
  have hd : denominator root ≠ 0 := ne_of_gt (denominator_positive root hq0 hq1)
  constructor
  · exact first_support_equality root hd
  · have hres := second_support_residual root hd
    rw [root_spec.2,zero_div] at hres
    linarith

theorem side_root_eq_candidate : sideQ root = candidateSide :=
  support_equalities_identify_candidate (sideQ root) (cosQ root) (sinQ root)
    side_root_interval (half_angle_unit root) support_equalities_root.1 support_equalities_root.2

/-- Every unit direction in the first octant has the indicated half-angle
parameter. Thus subsequent one-variable bounds cover the whole stated octant. -/
theorem half_angle_representation (c s : ℝ) (hs : 0 ≤ s) (hsc : s ≤ c)
    (hu : c^2+s^2=1) :
    ∃ q : ℝ, 0 ≤ q ∧ q ≤ Real.sqrt 2-1 ∧ cosQ q=c ∧ sinQ q=s := by
  have hc : 0 ≤ c := hs.trans hsc
  have hd : 0 < 1+c := by linarith
  have hdne : 1+c ≠ 0 := ne_of_gt hd
  let q := s/(1+c)
  have hq0 : 0 ≤ q := div_nonneg hs hd.le
  have hss : s^2=(1-c)*(1+c) := by nlinarith [hu]
  have hqsq : q^2=(1-c)/(1+c) := by
    dsimp [q]
    rw [div_pow,hss]
    field_simp [hdne]
    <;> ring
  have hcos : cosQ q=c := by
    unfold cosQ
    rw [hqsq]
    field_simp [hdne]
    <;> ring
  have hsin : sinQ q=s := by
    unfold sinQ
    rw [hqsq]
    dsimp [q]
    field_simp [hdne]
    <;> ring
  have hrel : q^2+2*q=(1-c+2*s)/(1+c) := by
    rw [hqsq]
    dsimp [q]
    ring
  have hineq : q^2+2*q ≤ 1 := by
    rw [hrel]
    apply (div_le_one hd).mpr
    linarith
  have hqhi : q ≤ Real.sqrt 2-1 := by
    by_contra hn
    have hlt : Real.sqrt 2-1<q := lt_of_not_ge hn
    have hroot : (Real.sqrt 2)^2=2 := Real.sq_sqrt (by norm_num)
    have hroot0 : 0 ≤ Real.sqrt 2 := Real.sqrt_nonneg 2
    have hp := mul_pos (sub_pos.mpr hlt)
      (show 0<q+(Real.sqrt 2-1)+2 by linarith)
    nlinarith
  exact ⟨q,hq0,hqhi,hcos,hsin⟩

#print axioms root_exists_unique
#print axioms half_angle_unit
#print axioms support_equalities_root
#print axioms side_root_eq_candidate
#print axioms half_angle_representation

end
end Cantrell37.Angle
