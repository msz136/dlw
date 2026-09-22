/-
  API probe: which lemmas/notations actually exist in the deployed
  Lean 4.34.0 + Mathlib v4.34.0 (commit 5ed2965).

  Run:
    & 'C:\Users\msz\学术内容\_lean_shared\Check-Lean.ps1' -Root <proofs> -File <...>\Common\ApiProbe.lean

  Every `#check` line is independent; failures are reported but do not stop
  the file. Read build.log for the full list of successes/failures.
-/
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Algebra.BigOperators.Group.Finset.Lemmas
import Mathlib.Algebra.BigOperators.Group.Finset.Interval
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Analysis.Asymptotics.Defs

-- notation check
example (f : Nat → Nat) : (∑ i ∈ Finset.range 3, f i) = f 0 + f 1 + f 2 := by
  simp [Finset.sum_range_succ]

#check @Finset.sum_range_sub'
#check @Finset.sum_range_sub
#check @Finset.sum_range_succ
#check @Finset.sum_add_distrib
#check @Finset.sum_mul
#check @Finset.mul_sum
#check @Finset.sum_congr
#check @Finset.sum_range_succ_sub_sum
#check @Finset.sum_range_zero
#check @Finset.sum_range_add
#check @Finset.sum_apply
#check @Finset.sum_comm
#check @Finset.sum_bij
#check @Finset.sum_image
#check @Finset.sum_Ico_sub
#check @Finset.sum_range_sub_sum_range

-- matrices
#check @Matrix
#check @Matrix.transpose
#check @Matrix.det
#check @Matrix.mulVec
#check @Matrix.dotProduct
#check @Matrix.vecMul
#check @Matrix.det_transpose
#check @Matrix.det_mul

-- real / complex analysis
#check @Real.exp
#check @Complex.exp
#check @HasDerivAt
#check @deriv
#check @HasDerivAt.exp
#check @Real.hasDerivAt_exp
#check @HasDerivAt.const_mul
#check @HasDerivAt.add
#check @HasDerivAt.mul
#check @HasDerivAt.div
#check @HasDerivAt.comp
#check @hasDerivAt_exp
#check @DifferentiableAt
#check @ContDiff

-- asymptotics / Taylor remainder
#check @Asymptotics.IsBigO
#check @Asymptotics.IsLittleO
#check @Asymptotics.isLittleO_iff_tendsto
#check @HasFTaylorSeriesUpTo
#check @taylor
#check @HasStrictFDerivAt

-- limits
#check @Filter.Tendsto
#check @nhds
#check @Continuous

-- matrices over a field, finite sums
#check @Finset.univ
#check @Fintype
#check @Finsupp

-- exponential as a sum / finite sum of exponentials
#check @Finset.sum_range_succ'
#check @Finset.prod_range_succ
#check @Finset.prod_range_div'

-- rational / integer
#check @Rat
#check @Int.toNat_add_one_of_nonneg
#check @Int.toNat_sub_one_of_pos
