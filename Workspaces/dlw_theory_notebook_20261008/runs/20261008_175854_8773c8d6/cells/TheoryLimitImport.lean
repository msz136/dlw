import PkgC17
import PkgC18Complete
noncomputable section
open DLWContract

theorem physical_reconstruction_limit : C17 := c17_proved

theorem nonlinear_continuum_limit (a : ℝ) (u v : XYT)
    (hu : Smooth3 u) (hv : Smooth3 v) (x y t : ℝ) :
    PowBound 2 (fun h =>
      n1 a h (localSamples y h u) (localSamples y h v) 0 x t - c1 a u v x (y-h/2) t) ∧
    PowBound 2 (fun h =>
      n2 a h (localSamples y h u) (localSamples y h v) 0 x t - c2 a u v x y t) :=
  c18_proved a u v hu hv x y t

#print C17
#print axioms physical_reconstruction_limit
#print axioms nonlinear_continuum_limit
