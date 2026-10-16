import PkgC22Complete
import PkgC23Complete
import PkgQuotientRate
noncomputable section
open DLWContract

theorem lattice_phase_limit : C12 := c12_proved
theorem exact_lattice_interpolation : C24 := c24_proved

theorem continuous_Gram_pair (N : ℕ) (D : Data N) (h₀ : ℝ)
    (hD : PositiveData D h₀) :
    ContinuousPair D.a (tau0 D 1) (tau0 D 0) :=
  c23_proved N D h₀ hD

theorem exact_solution_limit (N : ℕ) (D : Data N) (h₀ : ℝ)
    (hD : PositiveData D h₀) :
    UniformBoxO2 (fun h =>
      interpU h (tauI D h (D.a-h/2) 1 (1/2)) (tauI D h D.a 0 0) -
      cu (tau0 D 1) (tau0 D 0)) ∧
    UniformBoxO2 (fun h =>
      interpV h (tauI D h (D.a-h/2) 1 (1/2)) (tauI D h D.a 0 0) -
      cv (tau0 D 1) (tau0 D 0)) :=
  c22_proved N D h₀ hD

#print UniformBoxO2
#print axioms lattice_phase_limit
#print axioms exact_lattice_interpolation
#print axioms continuous_Gram_pair
#print axioms exact_solution_limit
