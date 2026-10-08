import FinalEndpoint

namespace IntegrabilityNotebookReview
open DLWLean
open scoped DLWFieldTopology
noncomputable section

theorem actualJacobianWitness (par : FieldParameters)
    (foundation : FactorSpectralFoundation par) (N : ℕ)
    (radius : ℝ) (hradius : 0 < radius) :
    ∃ eps : ℝ, 0 < eps ∧ eps < radius ∧
      (covectorMinor (fun i : Fin N => gradientCovector par
        (GlobalPDO.constructedChargeGradient par (2 * i.val + 1)
          (balancedMomentumState par
            (eps • periodicCosineSumCoefficient par (canonicalWitnessMode (N := N))
              (fun _ => 1)))))
        (balancedFourierDirection par (canonicalWitnessMode (N := N)))).det ≠ 0 := by
  exact actualOdd_small_Fourier_minor par foundation.toActual
    canonicalWitnessMode canonicalWitnessMode_pos (canonicalWitnessMode_injective N)
    (fun _ => 1) (fun _ => by norm_num) radius hradius

theorem actualFamilyIndependent (par : FieldParameters)
    (foundation : FactorSpectralFoundation par) (N : ℕ) :
    ∃ S : Set (ClosedPeriodicPair par), IsOpen S ∧ Dense S ∧
      ∀ z ∈ S, LinearIndependent ℝ (fun i : Fin N =>
        gradientCovector par (actualPhysicalFamilyGradient par i.val z)) := by
  exact actualPhysicalFamily_generically_independent par foundation.toActual N

example (par : FieldParameters) (foundation : FactorSpectralFoundation par)
    (start : StartPoint par) (t : ℝ) :
    HasDerivAt (fun τ => actualPhysicalK par (start.closedCurve τ)) 0 t := by
  exact start.actualPhysicalFamily_conserved foundation.toActual 0 t

example (par : FieldParameters) (foundation : FactorSpectralFoundation par)
    (start : StartPoint par) (t : ℝ) :
    HasDerivAt (fun τ => coefficientMomentum par (start.closedCurve τ)) 0 t := by
  exact start.actualPhysicalFamily_conserved foundation.toActual 1 t

#check actualJacobianWitness
#check actualFamilyIndependent
#print axioms actualJacobianWitness
#print axioms actualFamilyIndependent

end
end IntegrabilityNotebookReview
