import FieldCoordinates

/-!
Exact local coefficient certificates for the two physical heat intertwiners.
The entries below are independent real jets. `U_t` and `w_t` are defined by
the physical equations, not postulated to satisfy a Riccati conclusion.
These algebraic identities are the local step toward an operator Lax proof;
this module does not define a full pseudodifferential operator algebra.
-/

noncomputable section

namespace DLWLean.DarbouxJets

/-- Values and spatial derivatives at one lattice site and one space-time point. -/
structure Jet where
  U : ℝ
  w : ℝ
  Ux : ℝ
  wx : ℝ
  Uxx : ℝ
  wxx : ℝ
  Rwx : ℝ
  Rwxx : ℝ
  ebar : ℝ
  ebarx : ℝ
  v0 : ℝ

/-- The common scalar term in the physical U equation. -/
def lambda (par : FieldParameters) (z : Jet) : ℝ := 2 * z.ebarx / par.c

def U_t (par : FieldParameters) (z : Jet) : ℝ :=
  -(z.U * z.Ux + par.h ^ 2 / 16 * z.w * z.wx + z.Uxx + z.Rwxx) + lambda par z

def w_t (z : Jet) : ℝ := z.wxx - (z.Ux * z.w + z.U * z.wx)

def alpha (par : FieldParameters) (z : Jet) : ℝ := (z.U + par.h * z.w / 4) / 2
def alpha_x (par : FieldParameters) (z : Jet) : ℝ := (z.Ux + par.h * z.wx / 4) / 2
def alpha_xx (par : FieldParameters) (z : Jet) : ℝ := (z.Uxx + par.h * z.wxx / 4) / 2
def alpha_t (par : FieldParameters) (z : Jet) : ℝ :=
  (U_t par z + par.h * w_t z / 4) / 2

def b (par : FieldParameters) (z : Jet) : ℝ := (z.U - par.h * z.w / 4) / 2
def b_x (par : FieldParameters) (z : Jet) : ℝ := (z.Ux - par.h * z.wx / 4) / 2
def b_xx (par : FieldParameters) (z : Jet) : ℝ := (z.Uxx - par.h * z.wxx / 4) / 2
def b_t (par : FieldParameters) (z : Jet) : ℝ :=
  (U_t par z - par.h * w_t z / 4) / 2

/-- Periodic heat potential specified by the physical mean closure. -/
def V (par : FieldParameters) (z : Jet) : ℝ :=
  z.Rwx / 2 - par.h * z.wx / 4 - z.ebar / par.c + z.v0

def V_x (par : FieldParameters) (z : Jet) : ℝ :=
  z.Rwxx / 2 - par.h * z.wxx / 4 - z.ebarx / par.c

/-- The adjacent lattice potential, using its required discrete difference. -/
def Vplus (par : FieldParameters) (z : Jet) : ℝ := V par z + par.h * z.wx / 2
def Vplus_x (par : FieldParameters) (z : Jet) : ℝ := V_x par z + par.h * z.wxx / 2

def VF (par : FieldParameters) (z : Jet) : ℝ := V par z + 2 * alpha_x par z

theorem potential_difference (par : FieldParameters) (z : Jet) :
    Vplus par z - V par z = par.h * z.wx / 2 := by
  unfold Vplus
  ring

theorem common_intermediate_potential (par : FieldParameters) (z : Jet) :
    VF par z = Vplus par z + 2 * b_x par z := by
  unfold VF Vplus alpha_x b_x
  ring

/-- First physical Darboux Riccati residual vanishes identically. -/
theorem alpha_riccati_residual (par : FieldParameters) (z : Jet) :
    alpha_t par z + alpha_xx par z +
      2 * alpha par z * alpha_x par z + V_x par z = 0 := by
  unfold alpha_t alpha_xx alpha alpha_x U_t w_t lambda V_x
  ring

/-- Second physical Darboux Riccati residual vanishes identically. -/
theorem b_riccati_residual (par : FieldParameters) (z : Jet) :
    b_t par z + b_xx par z + 2 * b par z * b_x par z + Vplus_x par z = 0 := by
  unfold b_t b_xx b b_x U_t w_t lambda Vplus_x V_x
  ring

/-- Arbitrary jets of a test function. There is no special wave-function ansatz. -/
structure TestJet where
  psi : ℝ
  psi_x : ℝ
  psi_xx : ℝ
  psi_xxx : ℝ
  psi_t : ℝ
  psi_xt : ℝ

/-- Expansion of (∂t + D² + Vout)(D-r)ψ. -/
def heatAfterFactor (r rt rx rxx Vout : ℝ) (f : TestJet) : ℝ :=
  f.psi_xt - rt * f.psi - r * f.psi_t +
    f.psi_xxx - r * f.psi_xx - 2 * rx * f.psi_x - rxx * f.psi +
      Vout * (f.psi_x - r * f.psi)

/-- Expansion of (D-r)(∂t + D² + Vin)ψ. -/
def factorAfterHeat (r Vin Vinx : ℝ) (f : TestJet) : ℝ :=
  f.psi_xt + f.psi_xxx + Vinx * f.psi + Vin * f.psi_x -
    r * (f.psi_t + f.psi_xx + Vin * f.psi)

theorem heat_factor_coefficient_identity
    (r rt rx rxx Vin Vinx Vout : ℝ) (f : TestJet) :
    heatAfterFactor r rt rx rxx Vout f - factorAfterHeat r Vin Vinx f =
      (Vout - Vin - 2 * rx) * f.psi_x +
        (-rt - rxx - r * (Vout - Vin) - Vinx) * f.psi := by
  unfold heatAfterFactor factorAfterHeat
  ring

theorem alpha_full_intertwiner (par : FieldParameters) (z : Jet) (f : TestJet) :
    heatAfterFactor (alpha par z) (alpha_t par z) (alpha_x par z)
      (alpha_xx par z) (VF par z) f =
        factorAfterHeat (alpha par z) (V par z) (V_x par z) f := by
  unfold heatAfterFactor factorAfterHeat VF alpha alpha_t alpha_x alpha_xx
    U_t w_t lambda V V_x
  ring

theorem b_full_intertwiner (par : FieldParameters) (z : Jet) (f : TestJet) :
    heatAfterFactor (b par z) (b_t par z) (b_x par z)
      (b_xx par z) (VF par z) f =
        factorAfterHeat (b par z) (Vplus par z) (Vplus_x par z) f := by
  unfold heatAfterFactor factorAfterHeat VF Vplus Vplus_x b b_t b_x b_xx
    alpha_x U_t w_t lambda V V_x
  ring

end DLWLean.DarbouxJets
