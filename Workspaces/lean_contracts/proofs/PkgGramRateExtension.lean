import Contracts
import Mathlib.Analysis.Analytic.IsolatedZeros
import Mathlib.Tactic

noncomputable section
namespace DLWContract.GramRateExtension

def logDifference (P h : ℝ) := Real.log (P+h/2)-Real.log (P-h/2)
def extendedRate (P : ℝ) : ℝ → ℝ := dslope (logDifference P) 0

theorem logDifference_derivative (P : ℝ) (hP : P ≠ 0) :
    HasDerivAt (logDifference P) (1/P) 0 := by
  have hp := (((hasDerivAt_id (0 : ℝ)).div_const 2).const_add P).log (by simpa using hP)
  have hm := (((hasDerivAt_id (0 : ℝ)).div_const 2).const_sub P).log (by simpa using hP)
  convert! hp.sub hm using 1 <;> norm_num <;> ring

theorem extendedRate_zero (P : ℝ) (hP : P ≠ 0) : extendedRate P 0=1/P := by
  exact (dslope_same _ _).trans (logDifference_derivative P hP).deriv

theorem extendedRate_eq (P h : ℝ) (hh : h ≠ 0)
    (hp : P+h/2 ≠ 0) (hm : P-h/2 ≠ 0) :
    extendedRate P h=Real.log (lam h P)/h := by
  rw [extendedRate,dslope_of_ne _ hh]
  simp only [slope,logDifference,sub_zero,zero_div,add_zero,sub_self,
    vsub_eq_sub,smul_eq_mul,lam,Real.log_div hp hm]
  ring

theorem extendedRate_analytic (P : ℝ) (hP : P ≠ 0) : AnalyticAt ℝ (extendedRate P) 0 := by
  have H : ContDiffAt ℝ ⊤ (logDifference P) 0 := by
    unfold logDifference
    apply ContDiffAt.sub
    · apply ContDiffAt.log
      · fun_prop
      · simpa using hP
    · apply ContDiffAt.log
      · fun_prop
      · simpa using hP
  obtain ⟨p,hp⟩ := H.analyticAt
  exact ⟨p.fslope,hp.has_fpower_series_dslope_fslope⟩

theorem logDifference_odd (P h : ℝ) : logDifference P (-h) = -logDifference P h := by
  unfold logDifference
  rw [show P+(-h)/2=P-h/2 by ring,show P-(-h)/2=P+h/2 by ring]
  ring

theorem extendedRate_even (P h : ℝ) : extendedRate P (-h)=extendedRate P h := by
  by_cases hh : h=0
  · simp [hh]
  · rw [extendedRate,dslope_of_ne _ (neg_ne_zero.mpr hh),dslope_of_ne _ hh]
    simp only [slope,logDifference_odd,logDifference,zero_div,add_zero,sub_zero,sub_self,
      vsub_eq_sub,smul_eq_mul,neg_inv]
    ring

theorem extendedRate_derivative_zero (P : ℝ) (hP : P ≠ 0) :
    deriv (extendedRate P) 0=0 := by
  have H := (extendedRate_analytic P hP).differentiableAt.hasDerivAt
  have H0 : HasDerivAt (extendedRate P) (deriv (extendedRate P) 0) (-0) := by simpa using H
  have Hn := H0.comp 0 (hasDerivAt_neg (0 : ℝ))
  have he : (fun h => extendedRate P (-h))=extendedRate P := funext (extendedRate_even P)
  simp only [Function.comp_def] at Hn
  rw [he] at Hn
  have hd := Hn.unique H
  nlinarith [hd]

#print axioms extendedRate_analytic
#print axioms extendedRate_derivative_zero
end DLWContract.GramRateExtension
