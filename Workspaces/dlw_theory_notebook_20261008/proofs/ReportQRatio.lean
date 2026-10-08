import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Analysis.SpecialFunctions.Log.Basic

/-! The positive-real centered tau ratio in Report equation (12). -/

namespace DLWContract.ReportQRatio

/-- For positive real tau values, the logarithmic centered exponential
is exactly the quotient by the positive square root. -/
theorem centered_exp_ratio (f g k : ℝ)
    (hf : 0 < f) (hg : 0 < g) (hk : 0 < k) :
    Real.exp (Real.log f - (Real.log g + Real.log k) / 2) =
      f / Real.sqrt (g * k) := by
  rw [Real.exp_sub, Real.exp_log hf, Real.exp_half, Real.exp_add,
    Real.exp_log hg, Real.exp_log hk]

end DLWContract.ReportQRatio

#print axioms DLWContract.ReportQRatio.centered_exp_ratio
