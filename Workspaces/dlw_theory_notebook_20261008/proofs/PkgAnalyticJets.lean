import PkgUniformAnalytic
import Mathlib.Analysis.Calculus.Deriv.Shift

noncomputable section
open Set Filter Topology
namespace DLWContract.AnalyticJets
open UniformAnalytic
variable {Z : Type*} [NormedAddCommGroup Z] [NormedSpace ℝ Z]

theorem analytic_partial {f : ℝ × Z → ℝ} {p : ℝ × Z} (hf : AnalyticAt ℝ f p) :
    AnalyticAt ℝ (fun q => deriv (fun s => f (s,q.2)) q.1) p := by
  apply (analytic_dh hf).congr
  filter_upwards [hf.eventually_analyticAt] with q hq
  exact (dh_hasDerivAt q.1 q.2 hq).deriv.symm

theorem even_deriv_zero (f : ℝ → ℝ) (he : ∀ h, f (-h)=f h) : deriv f 0=0 := by
  have hf : (fun h => f (-h))=f := funext he
  have H := deriv_comp_neg (f := f) (x := (0 : ℝ))
  rw [hf,neg_zero] at H
  linarith

theorem odd_second_zero (f : ℝ → ℝ) (ho : ∀ h, f (-h)= -f h) : deriv (deriv f) 0=0 := by
  apply even_deriv_zero
  intro h
  have hf : (fun h => f (-h))=fun h => -f h := funext ho
  have H := deriv_comp_neg (f := f) (x := h)
  rw [hf] at H
  change deriv (-f) h= -deriv f (-h) at H
  rw [deriv.neg] at H
  linarith

theorem dh_eq {f : ℝ × Z → ℝ} {p : ℝ × Z} (hf : AnalyticAt ℝ f p) :
    dh f p=deriv (fun h => f (h,p.2)) p.1 := (dh_hasDerivAt p.1 p.2 hf).deriv.symm

theorem dh_dh_eq {f : ℝ × Z → ℝ} {p : ℝ × Z} (hf : AnalyticAt ℝ f p) :
    dh (dh f) p=deriv (deriv (fun h => f (h,p.2))) p.1 := by
  rw [dh_eq (analytic_dh hf)]
  apply Filter.EventuallyEq.deriv_eq
  have H := hf.eventually_analyticAt
  have hc : ContinuousAt (fun h : ℝ => (h,p.2)) p.1 := by fun_prop
  filter_upwards [hc.preimage_mem_nhds H] with h hh
  exact dh_eq hh

end DLWContract.AnalyticJets
