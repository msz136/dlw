import PkgC02
import PkgContinuous
noncomputable section
open DLWContract

theorem continuous_Hirota_bridge : C01 := c01_proved

theorem continuous_DLW (a : ℝ) (f g : XYT)
    (hf : Smooth3 f) (hg : Smooth3 g)
    (hfp : Positive3 f) (hgp : Positive3 g)
    (hbil : ContinuousPair a f g) :
    c1 a (cu f g) (cv f g) = 0 ∧
    c2 a (cu f g) (cv f g) = 0 :=
  c02_proved a f g hf hg hfp hgp hbil

#print ContinuousPair
#print continuous_DLW
#print axioms continuous_Hirota_bridge
#print axioms continuous_DLW
