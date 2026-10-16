import Mathlib.Analysis.Calculus.Deriv.MeanValue
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Topology.Order.IntermediateValue
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.FunProp

namespace Cantrell37
noncomputable section

def poly (s : ℝ) : ℝ :=
  36*s^8 - 2496*s^7 + 59768*s^6 - 733760*s^5 + 5289248*s^4 -
  23462672*s^3 + 63458276*s^2 - 96673872*s + 64068561

def rationalPart (s : ℝ) : ℝ :=
  6*s^4 - 208*s^3 + 2058*s^2 - 7936*s + 11163

def radicalPart (s : ℝ) : ℝ := -64*s^3 + 850*s^2 - 3658*s + 5502

def quartic (s : ℝ) : ℝ := rationalPart s + Real.sqrt 2 * radicalPart s

theorem conjugate_factorization (s r : ℝ) (hr : r^2 = 2) :
    poly s = (rationalPart s + r*radicalPart s) *
      (rationalPart s - r*radicalPart s) := by
  calc
    poly s = (rationalPart s)^2 - 2*(radicalPart s)^2 := by
      unfold poly rationalPart radicalPart
      ring
    _ = (rationalPart s + r*radicalPart s) *
        (rationalPart s - r*radicalPart s) := by
      rw [show (rationalPart s + r*radicalPart s) *
        (rationalPart s - r*radicalPart s) =
        (rationalPart s)^2 - r^2*(radicalPart s)^2 by ring, hr]

theorem quartic_root_is_polynomial_root (s : ℝ) (h : quartic s = 0) :
    poly s = 0 := by
  rw [conjugate_factorization s (Real.sqrt 2) (Real.sq_sqrt (by norm_num))]
  change quartic s * _ = 0
  rw [h, zero_mul]

def lower : ℝ := 659861960924436 / 100000000000000
def upper : ℝ := 659861960924437 / 100000000000000

theorem lower_sign : 0 < poly lower := by norm_num [poly, lower]
theorem upper_sign : poly upper < 0 := by norm_num [poly, upper]

def shifted (y : ℝ) : ℝ :=
  36*y^8 - 624*y^7 - 11212*y^6 - 63740*y^5 - (345729/2)*y^4 -
  231685*y^3 - (557279/4)*y^2 - (192085/4)*y + 405121/64

def shiftedDeriv (y : ℝ) : ℝ :=
  288*y^7 - 4368*y^6 - 67272*y^5 - 318700*y^4 -
  691458*y^3 - 695055*y^2 - (557279/2)*y - 192085/4

theorem shifted_identity (y : ℝ) : poly (13/2+y) = shifted y := by
  unfold poly shifted
  ring

theorem shifted_hasDerivAt (y : ℝ) : HasDerivAt shifted (shiftedDeriv y) y := by
  have h8 := ((hasDerivAt_id y).pow 8).const_mul 36
  have h7 := ((hasDerivAt_id y).pow 7).const_mul 624
  have h6 := ((hasDerivAt_id y).pow 6).const_mul 11212
  have h5 := ((hasDerivAt_id y).pow 5).const_mul 63740
  have h4 := ((hasDerivAt_id y).pow 4).const_mul (345729/2)
  have h3 := ((hasDerivAt_id y).pow 3).const_mul 231685
  have h2 := ((hasDerivAt_id y).pow 2).const_mul (557279/4)
  have h1 := (hasDerivAt_id y).const_mul (192085/4)
  have h := (((((((h8.sub h7).sub h6).sub h5).sub h4).sub h3).sub h2).sub h1).add_const (405121/64)
  convert h using 1
  · funext z
    simp [shifted]
  · norm_num [shiftedDeriv]
    ring

theorem shifted_deriv_negative (y : ℝ) (hy : y ∈ Set.Icc (0:ℝ) 1) :
    shiftedDeriv y < 0 := by
  have h7 : y^7 ≤ 1 := pow_le_one₀ hy.1 hy.2
  have h6 : 0 ≤ y^6 := pow_nonneg hy.1 6
  have h5 : 0 ≤ y^5 := pow_nonneg hy.1 5
  have h4 : 0 ≤ y^4 := pow_nonneg hy.1 4
  have h3 : 0 ≤ y^3 := pow_nonneg hy.1 3
  have h2 : 0 ≤ y^2 := sq_nonneg y
  unfold shiftedDeriv
  nlinarith [hy.1]

theorem shifted_strictAnti : StrictAntiOn shifted (Set.Icc (0:ℝ) 1) := by
  apply strictAntiOn_of_deriv_neg (convex_Icc _ _) (by unfold shifted; fun_prop)
  intro y hy
  rw [(shifted_hasDerivAt y).deriv]
  exact shifted_deriv_negative y (interior_subset hy)

theorem isolated_root_exists_unique :
    ∃! s : ℝ, s ∈ Set.Icc lower upper ∧ poly s = 0 := by
  have hlu : lower ≤ upper := by norm_num [lower, upper]
  have hc : ContinuousOn poly (Set.Icc lower upper) := by unfold poly; fun_prop
  obtain ⟨s, hs, hp⟩ := intermediate_value_Icc' hlu hc
    (show (0:ℝ) ∈ Set.Icc (poly upper) (poly lower) from
      ⟨le_of_lt upper_sign, le_of_lt lower_sign⟩)
  refine ⟨s, ⟨hs, hp⟩, ?_⟩
  intro t ht
  have sy : s-13/2 ∈ Set.Icc (0:ℝ) 1 := by
    rcases hs with ⟨hl, hu⟩
    constructor <;> norm_num [lower, upper] at * <;> linarith
  have ty : t-13/2 ∈ Set.Icc (0:ℝ) 1 := by
    rcases ht.1 with ⟨hl, hu⟩
    constructor <;> norm_num [lower, upper] at * <;> linarith
  have eqv : shifted (t-13/2) = shifted (s-13/2) := by
    rw [← shifted_identity, ← shifted_identity]
    convert ht.2.trans hp.symm using 1 <;> congr 1 <;> ring
  have := shifted_strictAnti.injOn ty sy eqv
  linarith

noncomputable def candidateSide : ℝ := Classical.choose isolated_root_exists_unique

theorem candidateSide_spec : candidateSide ∈ Set.Icc lower upper ∧
    poly candidateSide = 0 := (Classical.choose_spec isolated_root_exists_unique).1

theorem candidateSide_strict_interval : lower < candidateSide ∧ candidateSide < upper := by
  have hs := candidateSide_spec
  constructor
  · rcases hs.1.1.eq_or_lt with heq | hlt
    · have hz : poly lower = 0 := heq.symm ▸ hs.2
      linarith [lower_sign]
    · exact hlt
  · rcases hs.1.2.eq_or_lt with heq | hlt
    · have hz : poly upper = 0 := heq ▸ hs.2
      linarith [upper_sign]
    · exact hlt

theorem rationalPart_shifted (y : ℝ) :
    rationalPart (13/2+y) = 6*y^4 - 52*y^3 - 477*y^2 - 955*y + 943/8 := by
  unfold rationalPart
  ring

theorem radicalPart_shifted (y : ℝ) :
    radicalPart (13/2+y) = -64*y^3 - 398*y^2 - 720*y + 123/2 := by
  unfold radicalPart
  ring

/-- Squaring the radical equation adds a conjugate factor. It is strictly
positive throughout the isolating interval, so it contributes no root there. -/
theorem conjugate_positive_on_interval (s : ℝ) (hs : s ∈ Set.Icc lower upper) :
    0 < rationalPart s - Real.sqrt 2 * radicalPart s := by
  let y := s - 13/2
  have hy : y ∈ Set.Icc (9/100 : ℝ) (1/10 : ℝ) := by
    dsimp [y]
    rcases hs with ⟨hlo, hhi⟩
    constructor <;> norm_num [lower, upper] at * <;> linarith
  have hy0 : 0 ≤ y := le_trans (by norm_num) hy.1
  have hy2 : y^2 ≤ (1/10 : ℝ)^2 := pow_le_pow_left₀ hy0 hy.2 2
  have hy3 : y^3 ≤ (1/10 : ℝ)^3 := pow_le_pow_left₀ hy0 hy.2 3
  have hy2nonneg : 0 ≤ y^2 := sq_nonneg y
  have hy3nonneg : 0 ≤ y^3 := pow_nonneg hy0 3
  have hy4nonneg : 0 ≤ y^4 := pow_nonneg hy0 4
  have hsid : s = 13/2+y := by dsimp [y]; ring
  have hA : 0 < rationalPart s := by
    rw [hsid, rationalPart_shifted]
    nlinarith [hy.2]
  have hB : radicalPart s < 0 := by
    rw [hsid, radicalPart_shifted]
    nlinarith [hy.1]
  have hmul : Real.sqrt 2 * radicalPart s < 0 :=
    mul_neg_of_pos_of_neg (by positivity) hB
  linarith

theorem candidateSide_quartic : quartic candidateSide = 0 := by
  have hp : quartic candidateSide *
      (rationalPart candidateSide - Real.sqrt 2 * radicalPart candidateSide) = 0 := by
    change (rationalPart candidateSide + Real.sqrt 2 * radicalPart candidateSide) *
      (rationalPart candidateSide - Real.sqrt 2 * radicalPart candidateSide) = 0
    rw [← conjugate_factorization candidateSide (Real.sqrt 2)
      (Real.sq_sqrt (by norm_num))]
    exact candidateSide_spec.2
  exact (mul_eq_zero.mp hp).resolve_right
    (ne_of_gt (conjugate_positive_on_interval candidateSide candidateSide_spec.1))

theorem quartic_root_unique_in_interval (s : ℝ)
    (hs : s ∈ Set.Icc lower upper) (hq : quartic s = 0) : s = candidateSide := by
  exact (Classical.choose_spec isolated_root_exists_unique).2 s
    ⟨hs, quartic_root_is_polynomial_root s hq⟩

-- This identifies an algebraic endpoint. It does not assert any global packing bound.
#print axioms Cantrell37.conjugate_factorization
#print axioms Cantrell37.isolated_root_exists_unique
#print axioms Cantrell37.candidateSide_strict_interval
#print axioms Cantrell37.conjugate_positive_on_interval
#print axioms Cantrell37.candidateSide_quartic
#print axioms Cantrell37.quartic_root_unique_in_interval

end
end Cantrell37
