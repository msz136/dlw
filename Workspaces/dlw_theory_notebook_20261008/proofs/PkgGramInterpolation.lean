import PkgGramRateExtension
import PkgC09Complete
import Mathlib.Analysis.Analytic.IsolatedZeros

noncomputable section
open scoped BigOperators Matrix
namespace DLWContract.GramInterpolation
open GramRateExtension

def evenLogAmplitude (P Q h : ℝ) :=
  (Real.log (-P-h/2)+Real.log (-P+h/2)-Real.log (Q-h/2)-Real.log (Q+h/2))/2

theorem amplitude_even (P Q h : ℝ) : evenLogAmplitude P Q (-h)=evenLogAmplitude P Q h := by
  unfold evenLogAmplitude
  rw [show -P-(-h)/2=-P+h/2 by ring,show -P+(-h)/2=-P-h/2 by ring,
    show Q-(-h)/2=Q+h/2 by ring,show Q+(-h)/2=Q-h/2 by ring]
  ring

theorem amplitude_analytic (P Q : ℝ) (hP : P ≠ 0) (hQ : Q ≠ 0) :
    AnalyticAt ℝ (evenLogAmplitude P Q) 0 := by
  have H : ContDiffAt ℝ ⊤ (evenLogAmplitude P Q) 0 := by
    unfold evenLogAmplitude
    have h1 : ContDiffAt ℝ ⊤ (fun h : ℝ => Real.log (-P-h/2)) 0 :=
      (by fun_prop : ContDiffAt ℝ ⊤ (fun h : ℝ => -P-h/2) 0).log (by simpa using hP)
    have h2 : ContDiffAt ℝ ⊤ (fun h : ℝ => Real.log (-P+h/2)) 0 :=
      (by fun_prop : ContDiffAt ℝ ⊤ (fun h : ℝ => -P+h/2) 0).log (by simpa using hP)
    have h3 : ContDiffAt ℝ ⊤ (fun h : ℝ => Real.log (Q-h/2)) 0 :=
      (by fun_prop : ContDiffAt ℝ ⊤ (fun h : ℝ => Q-h/2) 0).log (by simpa using hQ)
    have h4 : ContDiffAt ℝ ⊤ (fun h : ℝ => Real.log (Q+h/2)) 0 :=
      (by fun_prop : ContDiffAt ℝ ⊤ (fun h : ℝ => Q+h/2) 0).log (by simpa using hQ)
    exact ((h1.add h2).sub h3 |>.sub h4).div_const 2
  exact H.analyticAt

theorem amplitude_zero (P Q : ℝ) (hP : P<0) (hQ : 0<Q) :
    Real.exp (evenLogAmplitude P Q 0)=(-P)/Q := by
  have H : evenLogAmplitude P Q 0=Real.log (-P)-Real.log Q := by
    simp only [evenLogAmplitude,zero_div,sub_zero,add_zero]
    ring
  rw [H,Real.exp_sub,Real.exp_log (neg_pos.mpr hP),Real.exp_log hQ]

def rowTau {N : ℕ} (D : Data N) (w : Fin N → ℝ) : XT := fun x t =>
  Matrix.det (fun i k => (if i=k then 1 else 0)+w i/(D.p i+D.q k)*
    Real.exp ((D.p i+D.q k)*x+((D.q k)^2-(D.p i)^2)*t))

theorem rowTau_positive {N : ℕ} (D : Data N) (h : ℝ) (hD : PositiveData D h)
    (w : Fin N → ℝ) (hw : ∀ i, 0<w i) (x t : ℝ) : 0<rowTau D w x t := by
  let E : Data N := {D with rho := w}
  have hE : PositiveData E h := by
    refine ⟨hD.1,hD.2.1,hD.2.2.1,?_⟩
    intro i
    exact ⟨(hD.2.2.2 i).1,(hD.2.2.2 i).2.1,(hD.2.2.2 i).2.2.1,hw i⟩
  have H := (c09_proved N E h hE).2.2.1 0 x t
  simpa only [G,tau,entry,E,zpow_zero,mul_one,rowTau] using H

def totalRate {N : ℕ} (D : Data N) (i : Fin N) (h : ℝ) :=
  extendedRate (D.p i-D.a) h+extendedRate (D.q i+D.a) h

def extG {N : ℕ} (D : Data N) (h : ℝ) : XYT := fun x y t =>
  rowTau D (fun i => D.rho i*Real.exp (y*totalRate D i h)) x t

def extF {N : ℕ} (D : Data N) (h : ℝ) : XYT := fun x y t =>
  rowTau D (fun i => D.rho i*Real.exp
    (y*totalRate D i h+evenLogAmplitude (D.p i-D.a) (D.q i+D.a) h)) x t

theorem extG_positive {N : ℕ} (D : Data N) (h0 : ℝ) (hD : PositiveData D h0)
    (h : ℝ) : Positive3 (extG D h) := by
  intro x y t
  exact rowTau_positive D h0 hD _
    (fun i => mul_pos (hD.2.2.2 i).2.2.2 (Real.exp_pos _)) x t

theorem extF_positive {N : ℕ} (D : Data N) (h0 : ℝ) (hD : PositiveData D h0)
    (h : ℝ) : Positive3 (extF D h) := by
  intro x y t
  exact rowTau_positive D h0 hD _
    (fun i => mul_pos (hD.2.2.2 i).2.2.2 (Real.exp_pos _)) x t

theorem ext_even {N : ℕ} (D : Data N) (h : ℝ) :
    extF D (-h)=extF D h ∧ extG D (-h)=extG D h := by
  constructor <;> funext x y t <;>
    simp [extF,extG,totalRate,extendedRate_even,amplitude_even]

#print axioms ext_even
#print axioms extF_positive
end DLWContract.GramInterpolation
