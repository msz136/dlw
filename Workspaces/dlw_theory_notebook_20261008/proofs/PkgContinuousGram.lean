import PkgC07Complete
import PkgC02
import PkgC09Complete

noncomputable section
open scoped BigOperators Matrix
namespace DLWContract.ContinuousGram

def rate {N : ℕ} (D : Data N) (i k : Fin N) :=
  1/(D.p i-D.a)+1/(D.q k+D.a)

def tauS {N : ℕ} (D : Data N) (s : ℝ) (n : ℤ) : XYT := fun x y t =>
  Matrix.det (fun i k => (if i=k then 1 else 0)+D.rho i/(D.p i+D.q k)*
    (gamma D s i k)^n*Real.exp ((D.p i+D.q k)*x+
      ((D.q k)^2-(D.p i)^2)*t+y*rate D i k))

def yData {N : ℕ} (D : Data N) (y : ℝ) : Data N :=
  { D with rho := fun i => D.rho i*Real.exp (y/(D.p i-D.a))*Real.exp (y/(D.q i+D.a)) }

theorem tauS_eq_tau {N : ℕ} (D : Data N) (h s : ℝ) (n : ℤ) (y : ℝ) :
    slice (tauS D s n) y=tau (yData D y) h s n 0 := by
  funext x t
  let E : Matrix (Fin N) (Fin N) ℝ := fun i k => D.rho i/(D.p i+D.q k)*
    (gamma D s i k)^n*Real.exp ((D.p i+D.q k)*x+((D.q k)^2-(D.p i)^2)*t)
  let L : Matrix (Fin N) (Fin N) ℝ := Matrix.diagonal (fun i => Real.exp (y/(D.p i-D.a)))
  let R : Matrix (Fin N) (Fin N) ℝ := Matrix.diagonal (fun k => Real.exp (y/(D.q k+D.a)))
  have hLE (i k : Fin N) : (L*E) i k=Real.exp (y/(D.p i-D.a))*E i k :=
    Matrix.diagonal_mul _ E i k
  have hleft : slice (tauS D s n) y x t=(1+(L*E)*R).det := by
    unfold slice tauS
    apply congrArg Matrix.det
    ext i k
    simp only [Matrix.add_apply,Matrix.one_apply,R,Matrix.mul_diagonal]
    rw [hLE]
    dsimp only [E]
    have he : (D.p i+D.q k)*x+((D.q k)^2-(D.p i)^2)*t+y*rate D i k=
      ((D.p i+D.q k)*x+((D.q k)^2-(D.p i)^2)*t)+
        y/(D.p i-D.a)+y/(D.q k+D.a) := by unfold rate; ring
    rw [he,Real.exp_add,Real.exp_add]
    ring
  have hright : tau (yData D y) h s n 0 x t=(1+R*(L*E)).det := by
    unfold tau
    apply congrArg Matrix.det
    ext i k
    simp only [Matrix.add_apply,Matrix.one_apply,R,Matrix.diagonal_mul]
    rw [hLE]
    simp only [entry,yData,E,zpow_zero,mul_one,gamma]
    ring
  rw [hleft,hright,Matrix.det_one_add_mul_comm]

theorem tauS_at_a {N : ℕ} (D : Data N) (n : ℤ) : tauS D D.a n=tau0 D n := rfl

theorem tauS_zero {N : ℕ} (D : Data N) (s : ℝ) : tauS D s 0=tau0 D 0 := by
  funext x y t
  simp [tauS,tau0,rate]

theorem tauS_bilinear {N : ℕ} (D : Data N) (h s : ℝ)
    (hD : Admissible D h) (hs : LayerOK D s) (y : ℝ) :
    bil s (slice (tauS D s 1) y) (slice (tau0 D 0) y)=0 := by
  rw [← tauS_zero D s,tauS_eq_tau D h s 1 y,tauS_eq_tau D h s 0 y]
  exact c07_proved N (yData D y) h s hD hs 0 0

theorem continuous_first {N : ℕ} (D : Data N) (h : ℝ) (hD : PositiveData D h) :
    cbil D.a (tau0 D 1) (tau0 D 0)=0 := by
  have had := c09_admissible_proved D h hD
  have hs : LayerOK D D.a := by
    constructor
    · intro i
      have hi := hD.2.2.2 i
      have hh := hD.1
      linarith
    · intro k
      have hk := hD.2.2.2 k
      have hh := hD.1
      linarith
  funext x y t
  exact congrFun (congrFun (tauS_bilinear D h D.a had hs y) x) t

theorem smooth_det {N : ℕ} {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (M : E → Matrix (Fin N) (Fin N) ℝ)
    (hM : ∀ i k, ContDiff ℝ ⊤ (fun z => M z i k)) :
    ContDiff ℝ ⊤ (fun z => (M z).det) := by
  simp only [Matrix.det_apply']
  exact ContDiff.sum fun σ _ => contDiff_const.mul (contDiff_prod fun i _ => hM (σ i) i)

theorem smooth_tau0 {N : ℕ} (D : Data N) (n : ℤ) : Smooth3 (tau0 D n) := by
  unfold Smooth3 tau0
  apply smooth_det
  intro i k
  fun_prop

def parameter (a d e : ℝ) := a+d*e/(1+e^2)

theorem parameter_bound (a d e : ℝ) (hd : 0<d) :
    a-d/2 ≤ parameter a d e ∧ parameter a d e ≤ a+d/2 := by
  have he : 0<1+e^2 := by positivity
  have h1 := sq_nonneg (e-1)
  have h2 := sq_nonneg (e+1)
  unfold parameter
  constructor
  · have H : -d/2 ≤ d*e/(1+e^2) :=
      (le_div_iff₀ he).mpr (by nlinarith [mul_nonneg hd.le h2])
    linarith
  · have H : d*e/(1+e^2) ≤ d/2 :=
      (div_le_iff₀ he).mpr (by nlinarith [mul_nonneg hd.le h1])
    linarith

theorem parameter_smooth (a d : ℝ) : ContDiff ℝ ⊤ (parameter a d) := by
  unfold parameter
  fun_prop (disch := intro e; positivity)

theorem parameter_derivative (a d : ℝ) : HasDerivAt (parameter a d) d 0 := by
  have H := (((hasDerivAt_id (0 : ℝ)).const_mul d).div
    (((hasDerivAt_id (0 : ℝ)).pow 2).const_add 1) (by norm_num)).const_add a
  convert! H using 1 <;> simp [parameter]

theorem parameter_layer {N : ℕ} (D : Data N) (h : ℝ) (hD : PositiveData D h) (e : ℝ) :
    LayerOK D (parameter D.a h e) := by
  have hb := parameter_bound D.a h e hD.1
  constructor
  · intro i
    have hi := hD.2.2.2 i
    linarith
  · intro k
    have hk := hD.2.2.2 k
    linarith [hD.1]

end DLWContract.ContinuousGram
