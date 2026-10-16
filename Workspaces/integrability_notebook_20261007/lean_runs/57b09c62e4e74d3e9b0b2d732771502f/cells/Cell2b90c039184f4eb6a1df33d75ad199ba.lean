import FinalEndpoint

namespace NotebookDLWJacobian
noncomputable section
open DLWLean
open scoped BigOperators ContDiff DLWFieldTopology

#print DLWLean.covectorMinor

theorem nonzeroJacobian (par : FieldParameters)
    (foundation : FactorSpectralFoundation par)
    (N : ℕ) (radius : ℝ) (hradius : 0 < radius) :
    ∃ eps : ℝ, 0 < eps ∧ eps < radius ∧
      (covectorMinor (fun i : Fin N => gradientCovector par
        (GlobalPDO.constructedChargeGradient par (2 * i.val + 1)
          (balancedMomentumState par
            (eps • periodicCosineSumCoefficient par
              (canonicalWitnessMode (N := N)) (fun _ => 1)))))
        (balancedFourierDirection par (canonicalWitnessMode (N := N)))).det ≠ 0 := by
  exact actualOdd_small_Fourier_minor par foundation.toActual
    canonicalWitnessMode canonicalWitnessMode_pos
    (canonicalWitnessMode_injective N) (fun _ => 1)
    (fun _ => by norm_num) radius hradius

#check nonzeroJacobian
#print axioms nonzeroJacobian

end
end NotebookDLWJacobian
