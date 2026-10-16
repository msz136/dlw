import PkgGramEntry
noncomputable section
open DLWContract

theorem two_soliton_expansion (D : Data 2) (h s : ℝ)
    (hD : Admissible D h) (hs : LayerOK D s) (n j : ℤ) (x t : ℝ) :
    let e₀ := entry D h s n j 0 0 x t - 1
    let e₁ := entry D h s n j 1 1 x t - 1
    tau D h s n j x t = 1 + e₀ + e₁ +
      interaction (D.p 0) (D.p 1) (D.q 0) (D.q 1)*e₀*e₁ :=
  c10_proved D h s hD hs n j x t

#print tau
#print interaction
#print axioms two_soliton_expansion
