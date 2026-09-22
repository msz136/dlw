import Mathlib.Basic.Real.Basic
import Mathlib.Tactic.Ring

/-!
# DLW shared operators (main-agent maintained)

Common formal infrastructure for the eight discretization directions.
Derivative data is FORMAL (jets); the bridge to real differentiable functions
is NOT part of this module and must be stated explicitly where used.
-/

namespace DLW

/-- Pointwise derivative data (value, x, xx, t). Formal jet, not a function. -/
structure Jet (K : Type) where
  value : K
  dx : K
  dxx : K
  dt : K

/-- First-order Hirota D_x on jets: F_x G - F G_x. -/
def hirotaX [Field K] (F G : Jet K) : K := F.dx*G.value - F.value*G.dx

/-- Second-order x part: F_xx G - 2 F_x G_x + F G_xx. -/
def hirotaXx [Field K] (F G : Jet K) : K :=
  F.dxx*G.value - 2*F.dx*G.dx + F.value*G.dxx

/-- B_s on jets: Dx^2 + Dt + 2s Dx  (Dt part: F_t G - F G_t). -/
def hirotaB [Field K] (s : K) (F G : Jet K) : K :=
  hirotaXx F G + (F.dt*G.value - F.value*G.dt) + 2*s*hirotaX F G

/-- Lattice function on the integer grid (y = j h, h fixed outside). -/
abbrev LatticeFun (K : Type) := ℤ → K

def shift (u : LatticeFun K) : LatticeFun K := fun j => u (j+1)

def dplus [Sub K] (u : LatticeFun K) : LatticeFun K := fun j => u (j+1) - u j
def dminus [Sub K] (u : LatticeFun K) : LatticeFun K := fun j => u j - u (j-1)
def dcenter [DivisionRing K] (u : LatticeFun K) : LatticeFun K :=
  fun j => (u (j+1) - u (j-1)) / 2
def average [DivisionRing K] (u : LatticeFun K) : LatticeFun K :=
  fun j => (u (j+1) + u j) / 2

theorem shift_dplus [Sub K] (u : LatticeFun K) :
    shift (dplus u) = dplus (shift u) := by
  funext j; rfl

theorem dcenter_shift [DivisionRing K] (u : LatticeFun K) :
    dcenter (shift u) = shift (dcenter u) := by
  funext j; simp [shift, dcenter]

/-- Semidiscrete staggered tau system (S): eq1 at site j, eq2 pairing F_j with G_{j+1}. -/
def stagEq1 [Field K] (a h : K) (F G : ℤ → Jet K) (j : ℤ) : Prop :=
  hirotaB (a - h/2) (F j) (G j) = 0

def stagEq2 [Field K] (a h : K) (F G : ℤ → Jet K) (j : ℤ) : Prop :=
  hirotaB (a + h/2) (F j) (G (j+1)) = 0

/-- Semidiscrete centered (same-site) candidate: eq1 and the divided-difference eq2. -/
def centeredEq1 [Field K] (a : K) (f g : ℤ → Jet K) (j : ℤ) : Prop :=
  hirotaB a (f j) (g j) = 0

def centeredEq2 [Field K] (a lam h : K) (f g : ℤ → Jet K) (j : ℤ) : Prop :=
  (hirotaB a (f (j+1)) (g j) - hirotaB a (f j) (g (j+1))) / h
    + lam * (hirotaX (f (j+1)) (g j) + hirotaX (f j) (g (j+1))) = 0

end DLW
