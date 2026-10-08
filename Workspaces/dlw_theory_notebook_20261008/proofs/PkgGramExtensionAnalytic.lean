import PkgGramExtensionBridge
import PkgAnalyticJets
import PkgC02

noncomputable section
open scoped BigOperators
namespace DLWContract.GramInterpolation
open GramRateExtension AnalyticJets

abbrev Space := ℝ × (ℝ × ℝ)
abbrev Full := ℝ × Space

theorem det_contDiffAt {N : ℕ} {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (M : E → Matrix (Fin N) (Fin N) ℝ) (p : E)
    (hM : ∀ i k, ContDiffAt ℝ ⊤ (fun z => M z i k) p) :
    ContDiffAt ℝ ⊤ (fun z => (M z).det) p := by
  simp only [Matrix.det_apply']
  exact ContDiffAt.sum fun σ _ => contDiffAt_const.mul (contDiffAt_prod fun i _ => hM (σ i) i)

theorem ext_analytic {N : ℕ} (D : Data N) (h0 : ℝ) (hD : PositiveData D h0) (z : Space) :
    AnalyticAt ℝ (fun p : Full => extF D p.1 p.2.1 p.2.2.1 p.2.2.2) (0,z) ∧
    AnalyticAt ℝ (fun p : Full => extG D p.1 p.2.1 p.2.2.1 p.2.2.2) (0,z) := by
  have hr (i : Fin N) : ContDiffAt ℝ ⊤ (fun p : Full => totalRate D i p.1) (0,z) := by
    have hi := data_zero_signs D h0 hD i
    exact (ContDiffAt.comp (0,z) (extendedRate_analytic _ (ne_of_lt hi.1)).contDiffAt contDiffAt_fst).add
      (ContDiffAt.comp (0,z) (extendedRate_analytic _ (ne_of_gt hi.2)).contDiffAt contDiffAt_fst)
  have ha (i : Fin N) : ContDiffAt ℝ ⊤ (fun p : Full =>
      evenLogAmplitude (D.p i-D.a) (D.q i+D.a) p.1) (0,z) := by
    have hi := data_zero_signs D h0 hD i
    exact ContDiffAt.comp (0,z) (amplitude_analytic _ _ (ne_of_lt hi.1) (ne_of_gt hi.2)).contDiffAt contDiffAt_fst
  constructor
  · apply ContDiffAt.analyticAt
    unfold extF rowTau
    apply det_contDiffAt
    intro i k
    exact contDiffAt_const.add (((contDiffAt_const.mul
      (((contDiffAt_snd.snd.fst.mul (hr i)).add (ha i)).exp)).div_const _).mul
        (by fun_prop))
  · apply ContDiffAt.analyticAt
    unfold extG rowTau
    apply det_contDiffAt
    intro i k
    exact contDiffAt_const.add (((contDiffAt_const.mul
      ((contDiffAt_snd.snd.fst.mul (hr i)).exp)).div_const _).mul (by fun_prop))

theorem ext_smooth {N : ℕ} (D : Data N) (h : ℝ) : Smooth3 (extF D h) ∧ Smooth3 (extG D h) := by
  constructor <;> simp only [Smooth3,extF,extG,rowTau] <;>
    apply contDiff_iff_contDiffAt.mpr <;> intro p <;> apply det_contDiffAt <;> intro i k <;> fun_prop

def logF {N : ℕ} (D : Data N) (h : ℝ) : XYT := fun x y t => Real.log (extF D h x y t)
def logG {N : ℕ} (D : Data N) (h : ℝ) : XYT := fun x y t => Real.log (extG D h x y t)
def ax {N : ℕ} (D : Data N) (h : ℝ) := sx (logF D h)
def bx {N : ℕ} (D : Data N) (h : ℝ) := sx (logG D h)

theorem logs_smooth {N : ℕ} (D : Data N) (h0 : ℝ) (hD : PositiveData D h0) (h : ℝ) :
    Smooth3 (logF D h) ∧ Smooth3 (logG D h) :=
  ⟨c02_smooth_log (ext_smooth D h).1 (extF_positive D h0 hD h),
   c02_smooth_log (ext_smooth D h).2 (extG_positive D h0 hD h)⟩

theorem analytic_sx {f : ℝ → XYT} {p : Full}
    (hf : AnalyticAt ℝ (fun q : Full => f q.1 q.2.1 q.2.2.1 q.2.2.2) p) :
    AnalyticAt ℝ (fun q : Full => sx (f q.1) q.2.1 q.2.2.1 q.2.2.2) p := by
  let swap : Full → Full := fun q => (q.2.1,q.1,q.2.2)
  have hs (q : Full) : AnalyticAt ℝ swap q := by
    apply ContDiffAt.analyticAt
    change ContDiffAt ℝ ⊤ swap q
    dsimp [swap]
    fun_prop
  have H := hf.comp (hs (swap p))
  have H' := (analytic_partial H).comp (hs p)
  exact H'

theorem jets_analytic {N : ℕ} (D : Data N) (h0 : ℝ) (hD : PositiveData D h0) (z : Space) :
    AnalyticAt ℝ (fun p : Full => ax D p.1 p.2.1 p.2.2.1 p.2.2.2) (0,z) ∧
    AnalyticAt ℝ (fun p : Full => bx D p.1 p.2.1 p.2.2.1 p.2.2.2) (0,z) := by
  have h := ext_analytic D h0 hD z
  constructor
  · apply analytic_sx
    exact (h.1.contDiffAt.log (ne_of_gt (extF_positive D h0 hD 0 z.1 z.2.1 z.2.2))).analyticAt
  · apply analytic_sx
    exact (h.2.contDiffAt.log (ne_of_gt (extG_positive D h0 hD 0 z.1 z.2.1 z.2.2))).analyticAt

theorem jets_even {N : ℕ} (D : Data N) (h : ℝ) : ax D (-h)=ax D h ∧ bx D (-h)=bx D h := by
  unfold ax bx GramInterpolation.logF GramInterpolation.logG
  rw [(ext_even D h).1,(ext_even D h).2]
  exact ⟨rfl,rfl⟩

#print axioms jets_analytic
end DLWContract.GramInterpolation
