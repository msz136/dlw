import NormalResidueBridge

namespace DLWLean
noncomputable section

/-- All-order integration by parts for two independent actual periodic
coefficients. This is the analytic step of the Euler variational rule. -/
theorem periodicCoefficientIntegral_iterated_parts (Lx : ℝ)
    (a b : PeriodicCoefficient Lx) (n : ℕ) :
    periodicCoefficientIntegral Lx (a * periodicSpatialIterate n b) =
      (-1 : ℝ) ^ n * periodicCoefficientIntegral Lx (periodicSpatialIterate n a * b) := by
  induction n generalizing a with
  | zero => simp [periodicSpatialIterate]
  | succ n ih =>
    have hstep : periodicSpatialIterate (n + 1) b =
        (periodicSpatialEvolution Lx).toLinearMap (periodicSpatialIterate n b) := by
      unfold periodicSpatialIterate
      exact Function.iterate_succ_apply' _ n b
    have hstepa : periodicSpatialIterate n ((periodicSpatialEvolution Lx).toLinearMap a) =
        periodicSpatialIterate (n + 1) a := by
      unfold periodicSpatialIterate
      exact (Function.iterate_succ_apply _ n a).symm
    rw [hstep, periodicCoefficientIntegral_parts, ih, hstepa, pow_succ]
    ring

theorem periodicSpatialIterate_add {Lx : ℝ} (n : ℕ)
    (a b : PeriodicCoefficient Lx) :
    periodicSpatialIterate n (a + b) = periodicSpatialIterate n a + periodicSpatialIterate n b := by
  induction n with
  | zero => rfl
  | succ n ih =>
    simp only [periodicSpatialIterate, Function.iterate_succ_apply'] at *
    rw [ih, map_add]

theorem periodicSpatialIterate_smul {Lx : ℝ} (n : ℕ)
    (r : ℝ) (a : PeriodicCoefficient Lx) :
    periodicSpatialIterate n (r • a) = r • periodicSpatialIterate n a := by
  induction n with
  | zero => rfl
  | succ n ih =>
    simp only [periodicSpatialIterate, Function.iterate_succ_apply'] at *
    rw [ih, map_smul]

#print axioms periodicCoefficientIntegral_iterated_parts
end
end DLWLean
