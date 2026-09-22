/-
Common.Operators — shared algebraic core for all eight directions.
Main-agent maintained; directions may extend in their own files but must
not edit this file (coordinate via main agent).
-/

import Mathlib.Tactic.Ring
import Mathlib.Algebra.Group.Basic

namespace DLWCommon

/-- Pointwise derivative data along (x,t) at one lattice point. -/
structure Jet (R : Type*) where
  value : R
  dx : R
  dxx : R
  dt : R

/-- Hirota D_x on jets: F G_x - F_x G. -/
def hirotaX {R : Type*} [CommRing R] (F G : Jet R) : R :=
  F.dx * G.value - F.value * G.dx

/-- Hirota B = D_x^2 + D_t + 2a D_x on jets. -/
def hirotaB {R : Type*} [CommRing R] (a : R) (F G : Jet R) : R :=
  F.dxx * G.value - 2 * F.dx * G.dx + F.value * G.dxx
    + F.dt * G.value - F.value * G.dt + 2 * a * hirotaX F G

/-- Plane-wave jet: E with E_x = k E, E_xx = k^2 E, E_t = w E. -/
def waveJet {R : Type*} [CommRing R] (A k w E : R) : Jet R :=
  ⟨1 + A * E, A * k * E, A * k^2 * E, A * w * E⟩

/-- Staggered edge residual (bilinear, one lattice-step pair), division-free
    form: (B F·G)_next - (B F·G)_cur + h λ (D_x F·G |_next + D_x F·G |_cur).
    The divided-by-h version is this times h⁻¹; directions using division
    should work over a Field (e.g. ℚ or ℝ) or keep this scaled form. -/
def edgeResidual {R : Type*} [CommRing R] (h lam a : R)
    (F G Fnext Gnext : Jet R) : R :=
  hirotaB a Fnext G - hirotaB a F Gnext
    + h * lam * (hirotaX Fnext G + hirotaX F Gnext)

section RingLemmas

variable {R : Type*} [CommRing R]

/-- The DLW "momentum" combination: ∂_x(u·q) = u_x q + u q_x, i.e. the
    product rule for the x-flux u*q appearing in the conservative form
    w_t + ∂_x[v_x + (u+2a)w] = 0 (q := w). Stated here as the bilinear
    algebraic identity used to expand flux products on jets. -/
theorem product_dx_jet (u du q dq : R) :
    du * q + u * dq = (u + q) * (du + dq) - u * du - q * dq := by
  ring

/-- D_x bilinear part of B is antisymmetric under (F,G) swap after
    including the linear terms: this is FALSE for B as a whole (the D_t
    and D_x terms change sign). Recorded as the correct statement:
    B(f,g) = B(g,f) + 2*(2*a*D_x + D_t)(f,g) recombined — so only the
    D_x^2 part is symmetric. Directions must not assume B-symmetry. -/
theorem hirotaX_antisymmetric (F G : Jet R) :
    hirotaX F G = -hirotaX G F := by
  simp only [hirotaX]
  ring

end RingLemmas

end DLWCommon
