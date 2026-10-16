import FinalEndpoint

namespace NotebookDLWFrequency
noncomputable section
open DLWLean
open scoped BigOperators ContDiff DLWFieldTopology

theorem degreeBound (par : FieldParameters) (k : ℕ) :
    (actualOddFrequencyPolynomial par k).natDegree ≤ k :=
  actualOddFrequencyPolynomial_degree par k

theorem topCoefficient (par : FieldParameters)
    (foundation : FactorSpectralFoundation par) (k : ℕ) :
    (actualOddFrequencyPolynomial par k).coeff k =
      (par.Lx / (par.M : ℝ)) * (-1 : ℝ) ^ (k + 1) :=
  actualOddFrequencyPolynomial_top par foundation.toActual k

theorem topCoefficientNonzero (par : FieldParameters)
    (foundation : FactorSpectralFoundation par) (k : ℕ) :
    (actualOddFrequencyPolynomial par k).coeff k ≠ 0 :=
  actualOddFrequencyPolynomial_leading_ne_zero par foundation.toActual k

#check degreeBound
#check topCoefficient
#check topCoefficientNonzero
#print axioms topCoefficient

end
end NotebookDLWFrequency
