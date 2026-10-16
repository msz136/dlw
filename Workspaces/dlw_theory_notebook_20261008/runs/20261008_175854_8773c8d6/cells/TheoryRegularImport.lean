import PkgGramComplete
noncomputable section
open DLWContract

theorem regular_tau (N : ℕ) (D : Data N) (h : ℝ)
    (hD : PositiveData D h) :
    Admissible D h ∧ PositiveL (F D h) ∧ PositiveL (G D h) ∧
    SmoothL (F D h) ∧ SmoothL (G D h) :=
  c09_proved N D h hD

theorem exact_nonlinear_solution (N : ℕ) (D : Data N) (h : ℝ)
    (hD : PositiveData D h) :
    NonlinearPair D.a h (physU (F D h) (G D h)) (physV h (F D h) (G D h)) :=
  c16_proved N D h hD

#print PositiveData
#print axioms regular_tau
#print axioms exact_nonlinear_solution
