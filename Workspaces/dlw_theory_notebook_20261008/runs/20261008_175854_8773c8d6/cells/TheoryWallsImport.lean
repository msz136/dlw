import PkgC11
noncomputable section
open DLWContract

theorem bilinear_continuum_limit (a : ℝ) (f g : XYT)
    (hf : Smooth3 f) (hg : Smooth3 g) (x y t : ℝ) :
    PowBound 2 (fun h =>
      (wallPlus a h y f g x t + wallMinus a h y f g x t)/2 - cbil a f g x y t) ∧
    PowBound 2 (fun h =>
      (wallPlus a h y f g x t - wallMinus a h y f g x t)/h -
      (cbil a f (sy g) x y t + 2*chx f g x y t)) :=
  c11_proved a f g hf hg x y t

#print PowBound
#print axioms bilinear_continuum_limit
