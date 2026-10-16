import BalancedActualCoefficientJet

namespace DLWLean.BalancedPDO
noncomputable section

theorem twoSiteSpatialField_periodic_pointwise {M : ℕ} {Lx : ℝ}
    (d : AlgebraEvolution (PeriodicCoefficient Lx)) (hd : d = periodicSpatialEvolution Lx)
    (plus minus : Fin M) (f : PeriodicCoefficient Lx) (j : Fin M) (r : ℕ) (x : ℝ) :
    (twoSiteSpatialField (R := PeriodicCoefficient Lx) d plus minus f j r : ℝ → ℝ) x =
      twoSiteField plus minus (iteratedDeriv r (f : ℝ → ℝ) x) j := by
  rw [hd]
  unfold twoSiteSpatialField twoSiteField
  split_ifs
  · exact periodicSpatialIterate_eval r f x
  · exact congrArg Neg.neg (periodicSpatialIterate_eval r f x)
  · rfl

theorem balancedOddDensity_actual_quadratic_integral {M : ℕ} {Lx : ℝ}
    {A : Type*} [Ring A] [Algebra ℝ A]
    (model : NormalPDOModel (PeriodicCoefficient Lx) A)
    (spatial : model.d = periodicSpatialEvolution Lx) (tr : CyclicTrace A)
    (trace_eq : ∀ X : A, tr.toLinearMap X =
      periodicCoefficientIntegral Lx (model.coefficients X (-1)))
    (plus minus : Fin M) (hne : plus ≠ minus) (hM : M ≠ 0)
    (f : PeriodicCoefficient Lx) (k : ℕ) :
    (∫ x in (0 : ℝ)..Lx,
      (perturbationPolynomial M (balancedSpectralDensityPolynomial M (2 * k + 1)) 0 0
        (fun j r => twoSiteField plus minus (iteratedDeriv r (f : ℝ → ℝ) x) j)).coeff 2) =
      (2 / (M : ℝ)) * (-1 : ℝ) ^ (k + 1) *
        ∫ x in (0 : ℝ)..Lx, (iteratedDeriv k (f : ℝ → ℝ) x) ^ 2 := by
  let p := balancedSpectralDensityPolynomial M (2 * k + 1)
  let field := twoSiteSpatialField model.d plus minus f
  have hfields (x : ℝ) : (fun j r => (field j r : ℝ → ℝ) x) =
      (fun j r => twoSiteField plus minus (iteratedDeriv r (f : ℝ → ℝ) x) j) := by
    funext j r
    exact twoSiteSpatialField_periodic_pointwise model.d spatial plus minus f j r x
  have hpoint (x : ℝ) : ((actualCoefficientJet M field).second p : ℝ → ℝ) x =
      2 * (perturbationPolynomial M p 0 0
        (fun j r => twoSiteField plus minus (iteratedDeriv r (f : ℝ → ℝ) x) j)).coeff 2 := by
    rw [actualCoefficientJet_second_pointwise, hfields]
  have hleft : (1 / 2 : ℝ) * periodicCoefficientIntegral Lx
      ((twoSiteDifferentialJetEvaluation model plus minus f).jet.second p) =
      ∫ x in (0 : ℝ)..Lx, (perturbationPolynomial M p 0 0
        (fun j r => twoSiteField plus minus (iteratedDeriv r (f : ℝ → ℝ) x) j)).coeff 2 := by
    change (1 / 2 : ℝ) * (∫ x in (0 : ℝ)..Lx,
      ((actualCoefficientJet M field).second p : ℝ → ℝ) x) = _
    simp_rw [hpoint]
    rw [intervalIntegral.integral_const_mul]
    ring
  rw [← hleft, balancedOddDensity_actual_second_trace model tr
    (periodicCoefficientIntegral Lx) trace_eq plus minus hne hM f k, trace_eq]
  have hres := (model.periodicResidueModel spatial).residue_quadratic_integral (2 * k) f f
  change periodicCoefficientIntegral Lx (model.coefficients
    ((model.D : A) ^ (2 * k) *
      (model.coefficient f * (↑model.D⁻¹ : A) * model.coefficient f)) (-1)) = _ at hres
  rw [hres]
  have hcomm : (fun x => iteratedDeriv (2 * k) (f : ℝ → ℝ) x * (f : ℝ → ℝ) x) =
      fun x => (f : ℝ → ℝ) x * iteratedDeriv (2 * k) (f : ℝ → ℝ) x := by
    funext x
    ring
  rw [hcomm, integral_periodic_even_derivative Lx (f : ℝ → ℝ) f.property.1 f.property.2 k,
    pow_succ]
  ring

#print axioms balancedOddDensity_actual_quadratic_integral
end
end DLWLean.BalancedPDO
