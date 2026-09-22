import Contracts
import Mathlib.Analysis.Calculus.Deriv.Prod
import Mathlib.Topology.Instances.Matrix
import Mathlib.Tactic

noncomputable section
open scoped BigOperators Matrix
namespace DLWContract.GramActual

def K {N : ℕ} (D : Data N) (h s : ℝ) (n j : ℤ) (x t : ℝ)
    (i k : Fin N) : ℝ :=
  D.rho i/(D.p i+D.q k)*(gamma D s i k)^n*(chi D h i k)^j*
    Real.exp ((D.p i+D.q k)*x+((D.q k)^2-(D.p i)^2)*t)

def M {N : ℕ} (D : Data N) (h s : ℝ) (n j : ℤ) (x t : ℝ) :
    Matrix (Fin N) (Fin N) ℝ := fun i k => entry D h s n j i k x t
def V {N : ℕ} (D : Data N) (h s : ℝ) (n j : ℤ) (x t : ℝ) :
    Matrix (Fin N) (Fin N) ℝ := fun i k => (D.p i+D.q k)*K D h s n j x t i k
def W {N : ℕ} (D : Data N) (h s : ℝ) (n j : ℤ) (x t : ℝ) :
    Matrix (Fin N) (Fin N) ℝ := fun i k => (D.p i+D.q k)^2*K D h s n j x t i k
def T {N : ℕ} (D : Data N) (h s : ℝ) (n j : ℤ) (x t : ℝ) :
    Matrix (Fin N) (Fin N) ℝ := fun i k => ((D.q k)^2-(D.p i)^2)*K D h s n j x t i k

def r {N : ℕ} (D : Data N) (h s : ℝ) (n j : ℤ) (x t : ℝ) (i : Fin N) : ℝ :=
  D.rho i*(s-D.p i)^n*(lam h (D.p i-D.a))^j*Real.exp (D.p i*x-(D.p i)^2*t)
def c {N : ℕ} (D : Data N) (h s : ℝ) (n j : ℤ) (x t : ℝ) (k : Fin N) : ℝ :=
  ((D.q k+s)^n)⁻¹*(lam h (D.q k+D.a))^j*Real.exp (D.q k*x+(D.q k)^2*t)
def b {N : ℕ} (D : Data N) (h s : ℝ) (n j : ℤ) (x t : ℝ) (k : Fin N) : ℝ :=
  c D h s n j x t k/(D.q k+s)
def u {N : ℕ} (D : Data N) (h s : ℝ) (n j : ℤ) (x t : ℝ) (i : Fin N) : ℝ :=
  (s-D.p i)*r D h s n j x t i

theorem kernel_x {N : ℕ} (D : Data N) (h s : ℝ) (n j : ℤ) (x t : ℝ) (i k : Fin N) :
    HasDerivAt (fun z => K D h s n j z t i k)
      ((D.p i+D.q k)*K D h s n j x t i k) x := by
  have H := ((((hasDerivAt_id x).const_mul (D.p i+D.q k)).add_const
    (((D.q k)^2-(D.p i)^2)*t)).exp).const_mul
    (D.rho i/(D.p i+D.q k)*(gamma D s i k)^n*(chi D h i k)^j)
  convert! H using 1 <;> simp only [K,id_eq] <;> ring

theorem kernel_t {N : ℕ} (D : Data N) (h s : ℝ) (n j : ℤ) (x t : ℝ) (i k : Fin N) :
    HasDerivAt (fun z => K D h s n j x z i k)
      (((D.q k)^2-(D.p i)^2)*K D h s n j x t i k) t := by
  have H := ((((hasDerivAt_id t).const_mul ((D.q k)^2-(D.p i)^2)).const_add
    ((D.p i+D.q k)*x)).exp).const_mul
    (D.rho i/(D.p i+D.q k)*(gamma D s i k)^n*(chi D h i k)^j)
  convert! H using 1 <;> simp only [K,id_eq] <;> ring

theorem matrix_x {N : ℕ} (D : Data N) (h s : ℝ) (n j : ℤ) (x t : ℝ) :
    HasDerivAt (fun z => M D h s n j z t) (V D h s n j x t) x := by
  apply hasDerivAt_pi.mpr
  intro i
  apply hasDerivAt_pi.mpr
  intro k
  exact (kernel_x D h s n j x t i k).const_add (if i=k then 1 else 0)

theorem matrix_t {N : ℕ} (D : Data N) (h s : ℝ) (n j : ℤ) (x t : ℝ) :
    HasDerivAt (M D h s n j x) (T D h s n j x t) t := by
  apply hasDerivAt_pi.mpr
  intro i
  apply hasDerivAt_pi.mpr
  intro k
  exact (kernel_t D h s n j x t i k).const_add (if i=k then 1 else 0)

theorem matrix_xx {N : ℕ} (D : Data N) (h s : ℝ) (n j : ℤ) (x t : ℝ) :
    HasDerivAt (fun z => V D h s n j z t) (W D h s n j x t) x := by
  apply hasDerivAt_pi.mpr
  intro i
  apply hasDerivAt_pi.mpr
  intro k
  convert! (kernel_x D h s n j x t i k).const_mul (D.p i+D.q k) using 1 <;>
    simp only [V,W] <;> ring

theorem rank_one {N : ℕ} (D : Data N) (h s : ℝ) (n j : ℤ)
    (hD : Admissible D h) (x t : ℝ) :
    V D h s n j x t=Matrix.vecMulVec (r D h s n j x t) (c D h s n j x t) := by
  ext i k
  have hg : gamma D s i k=(s-D.p i)/(D.q k+s) := by simp [gamma,neg_sub,neg_div]
  have he : (D.p i+D.q k)*x+((D.q k)^2-(D.p i)^2)*t=
      (D.p i*x-(D.p i)^2*t)+(D.q k*x+(D.q k)^2*t) := by ring
  simp only [V,K,Matrix.vecMulVec_apply,r,c,hg,chi,div_zpow,mul_zpow,he,Real.exp_add]
  field_simp [hD.2.1 i k]
  <;> ring

theorem kernel_shift {N : ℕ} (D : Data N) (h s : ℝ) (n j : ℤ)
    (hs : LayerOK D s) (x t : ℝ) (i k : Fin N) :
    K D h s (n+1) j x t i k=gamma D s i k*K D h s n j x t i k := by
  have hg : gamma D s i k ≠ 0 := by
    exact div_ne_zero (neg_ne_zero.mpr (hs.1 i)) (hs.2 k)
  simp only [K,zpow_add_one₀ hg n]
  ring

theorem matrix_shift {N : ℕ} (D : Data N) (h s : ℝ) (n j : ℤ)
    (hD : Admissible D h) (hs : LayerOK D s) (x t : ℝ) :
    M D h s (n+1) j x t=M D h s n j x t-
      Matrix.vecMulVec (r D h s n j x t) (b D h s n j x t) := by
  have hr := rank_one D h s n j hD x t
  ext i k
  have hv := congrFun (congrFun hr i) k
  change (D.p i+D.q k)*K D h s n j x t i k=
    r D h s n j x t i*c D h s n j x t k at hv
  change (if i=k then 1 else 0)+K D h s (n+1) j x t i k=
    (if i=k then 1 else 0)+K D h s n j x t i k-
      r D h s n j x t i*(c D h s n j x t k/(D.q k+s))
  rw [kernel_shift D h s n j hs]
  simp only [gamma]
  field_simp [hs.2 k]
  linear_combination -hv

theorem next_rank_one {N : ℕ} (D : Data N) (h s : ℝ) (n j : ℤ)
    (hD : Admissible D h) (hs : LayerOK D s) (x t : ℝ) :
    V D h s (n+1) j x t=Matrix.vecMulVec (u D h s n j x t) (b D h s n j x t) := by
  have hr := rank_one D h s n j hD x t
  ext i k
  have hv := congrFun (congrFun hr i) k
  change (D.p i+D.q k)*K D h s n j x t i k=
    r D h s n j x t i*c D h s n j x t k at hv
  change (D.p i+D.q k)*K D h s (n+1) j x t i k=
    (s-D.p i)*r D h s n j x t i*(c D h s n j x t k/(D.q k+s))
  rw [kernel_shift D h s n j hs]
  simp only [gamma]
  field_simp [hs.2 k]
  linear_combination (s-D.p i)*hv

end DLWContract.GramActual
