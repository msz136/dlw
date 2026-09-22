import PkgUniformTaylor
import Mathlib.Analysis.Calculus.FDeriv.Analytic
import Mathlib.Analysis.Analytic.Constructions
import Mathlib.Analysis.Calculus.Deriv.Prod

noncomputable section
open Set Filter Topology
namespace DLWContract.UniformAnalytic

variable {Z : Type*} [NormedAddCommGroup Z] [NormedSpace ℝ Z]

def dh (f : ℝ × Z → ℝ) (p : ℝ × Z) := fderiv ℝ f p (1,0)

theorem analytic_dh {f : ℝ × Z → ℝ} {p : ℝ × Z} (hf : AnalyticAt ℝ f p) :
    AnalyticAt ℝ (dh f) p :=
  ((ContinuousLinearMap.apply ℝ ℝ ((1,0) : ℝ × Z)).analyticAt _).comp hf.fderiv

theorem dh_hasDerivAt {f : ℝ × Z → ℝ} (h : ℝ) (z : Z) (hf : AnalyticAt ℝ f (h,z)) :
    HasDerivAt (fun s => f (s,z)) (dh f (h,z)) h := by
  have H := hf.differentiableAt.hasFDerivAt.comp_hasDerivAt h
    ((hasDerivAt_id h).prodMk (hasDerivAt_const h z))
  convert! H using 1

/-- A compact set of analytic germs admits a common step-size neighborhood. -/
theorem common_analytic_interval (f : ℝ × Z → ℝ) (K : Set Z) (hK : IsCompact K)
    (hf : ∀ z ∈ K, AnalyticAt ℝ f (0,z)) :
    ∃ d : ℝ, 0<d ∧ ∀ h ∈ Icc 0 d, ∀ z ∈ K, AnalyticAt ℝ f (h,z) := by
  obtain ⟨U,V,hU,hV,h0,hKV,hUV⟩ := generalized_tube_lemma
    (isCompact_singleton (x := (0 : ℝ))) hK (isOpen_analyticAt ℝ f)
    (by
      rintro ⟨h,z⟩ ⟨hh,hz⟩
      have hh0 : h=0 := mem_singleton_iff.mp hh
      subst h
      exact hf z hz)
  obtain ⟨e,he,heU⟩ := Metric.mem_nhds_iff.mp (hU.mem_nhds (h0 (mem_singleton 0)))
  refine ⟨e/2,half_pos he,?_⟩
  intro h hh z hz
  apply hUV
  refine ⟨heU ?_,hKV hz⟩
  rw [Metric.mem_ball,Real.dist_eq,sub_zero,abs_of_nonneg hh.1]
  linarith [hh.2]

theorem uniform_second_order (f : ℝ × Z → ℝ) (K : Set Z) (hK : IsCompact K)
    (hf : ∀ z ∈ K, AnalyticAt ℝ f (0,z))
    (hzero : ∀ z ∈ K, dh f (0,z)=0) :
    ∃ C : ℝ, 0≤C ∧ ∃ d : ℝ, 0<d ∧ ∀ h ∈ Icc 0 d, ∀ z ∈ K,
      |f (h,z)-f (0,z)|≤C*h^2 := by
  obtain ⟨d,hd,hfD⟩ := common_analytic_interval f K hK hf
  obtain ⟨C,hC,hbound⟩ := UniformTaylor.second_order_on_compact K hK d
    (fun h z => f (h,z)) (fun h z => dh f (h,z)) (fun h z => dh (dh f) (h,z))
    (fun z hz h hh => dh_hasDerivAt h z (hfD h hh z hz))
    (fun z hz h hh => dh_hasDerivAt h z (analytic_dh (hfD h hh z hz))) hzero
    (by
      intro p hp
      exact (analytic_dh (analytic_dh (hfD p.1 hp.1 p.2 hp.2))).continuousAt.continuousWithinAt)
  exact ⟨C,hC,d,hd,fun h hh z hz => hbound z hz h hh⟩

theorem uniform_third_order (f : ℝ × Z → ℝ) (K : Set Z) (hK : IsCompact K)
    (hf : ∀ z ∈ K, AnalyticAt ℝ f (0,z))
    (hz1 : ∀ z ∈ K, dh f (0,z)=0) (hz2 : ∀ z ∈ K, dh (dh f) (0,z)=0) :
    ∃ C : ℝ, 0≤C ∧ ∃ d : ℝ, 0<d ∧ ∀ h ∈ Icc 0 d, ∀ z ∈ K,
      |f (h,z)-f (0,z)|≤C*h^3 := by
  obtain ⟨d,hd,hfD⟩ := common_analytic_interval f K hK hf
  obtain ⟨C,hC,hbound⟩ := UniformTaylor.third_order_on_compact K hK d
    (fun h z => f (h,z)) (fun h z => dh f (h,z)) (fun h z => dh (dh f) (h,z))
    (fun h z => dh (dh (dh f)) (h,z))
    (fun z hz h hh => dh_hasDerivAt h z (hfD h hh z hz))
    (fun z hz h hh => dh_hasDerivAt h z (analytic_dh (hfD h hh z hz)))
    (fun z hz h hh => dh_hasDerivAt h z (analytic_dh (analytic_dh (hfD h hh z hz)))) hz1 hz2
    (by
      intro p hp
      exact (analytic_dh (analytic_dh (analytic_dh
        (hfD p.1 hp.1 p.2 hp.2)))).continuousAt.continuousWithinAt)
  exact ⟨C,hC,d,hd,fun h hh z hz => hbound z hz h hh⟩

#print axioms uniform_second_order
#print axioms uniform_third_order
end DLWContract.UniformAnalytic
