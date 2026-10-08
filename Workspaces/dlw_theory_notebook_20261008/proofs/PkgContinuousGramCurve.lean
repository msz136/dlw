import PkgContinuousGram

noncomputable section
open scoped BigOperators Matrix
namespace DLWContract.ContinuousGram

def family {N : ℕ} (D : Data N) (h y : ℝ) : XYT := fun x e t =>
  tauS D (parameter D.a h e) 1 x y t
def fixed {N : ℕ} (D : Data N) (y : ℝ) : XYT := fun x _ t => tau0 D 0 x y t

theorem family_smooth {N : ℕ} (D : Data N) (h y : ℝ) (hD : PositiveData D h) :
    Smooth3 (family D h y) := by
  unfold Smooth3 family tauS
  apply smooth_det
  intro i k
  simp only [zpow_one,gamma]
  have hp : ContDiff ℝ ⊤ (fun z : ℝ × (ℝ × ℝ) => parameter D.a h z.2.1) :=
    (parameter_smooth D.a h).comp (contDiff_fst.comp contDiff_snd)
  have hq : ∀ z : ℝ × (ℝ × ℝ), D.q k+parameter D.a h z.2.1 ≠ 0 :=
    fun z => (parameter_layer D h hD z.2.1).2 k
  fun_prop

theorem fixed_smooth {N : ℕ} (D : Data N) (y : ℝ) : Smooth3 (fixed D y) := by
  unfold Smooth3 fixed tau0
  apply smooth_det
  intro i k
  fun_prop

theorem family_at_zero {N : ℕ} (D : Data N) (h y : ℝ) :
    slice (family D h y) 0=slice (tau0 D 1) y := by
  funext x t
  simp [family,slice,parameter,tauS,tau0,rate]

theorem fixed_slice {N : ℕ} (D : Data N) (y e : ℝ) :
    slice (fixed D y) e=slice (tau0 D 0) y := rfl

theorem fixed_sy {N : ℕ} (D : Data N) (y : ℝ) : sy (fixed D y)=0 := by
  funext x e t
  simp [sy,fixed]

theorem gamma_parameter_derivative {N : ℕ} (D : Data N) (h : ℝ)
    (hD : PositiveData D h) (i k : Fin N) :
    HasDerivAt (fun e => gamma D (parameter D.a h e) i k)
      (-h*gamma D D.a i k*rate D i k) 0 := by
  have hs := parameter_layer D h hD 0
  have hq : D.q k+D.a ≠ 0 := by simpa [parameter] using hs.2 k
  have hp : D.p i-D.a ≠ 0 := by simpa [parameter] using hs.1 i
  have H := ((parameter_derivative D.a h).sub_const (D.p i)).div
    ((parameter_derivative D.a h).const_add (D.q k)) (by simpa [parameter] using hq)
  convert! H using 1
  · funext e
    simp only [gamma,Pi.div_apply]
    ring
  · simp only [parameter,zero_mul,mul_zero,zero_pow (by decide : 2 ≠ 0),
      add_zero,zero_div,zero_add,gamma,rate]
    field_simp [hp,hq]
    ring

theorem family_sy_at_zero {N : ℕ} (D : Data N) (h y : ℝ) (hD : PositiveData D h) :
    slice (sy (family D h y)) 0=(-h) • slice (sy (tau0 D 1)) y := by
  funext x t
  let A : ℝ → Matrix (Fin N) (Fin N) ℝ := fun Y i k =>
    (if i=k then 1 else 0)+D.rho i/(D.p i+D.q k)*gamma D D.a i k*
      Real.exp ((D.p i+D.q k)*x+((D.q k)^2-(D.p i)^2)*t+Y*rate D i k)
  let B : ℝ → Matrix (Fin N) (Fin N) ℝ := fun e i k =>
    (if i=k then 1 else 0)+D.rho i/(D.p i+D.q k)*gamma D (parameter D.a h e) i k*
      Real.exp ((D.p i+D.q k)*x+((D.q k)^2-(D.p i)^2)*t+y*rate D i k)
  let Y : Matrix (Fin N) (Fin N) ℝ := fun i k =>
    D.rho i/(D.p i+D.q k)*gamma D D.a i k*
      Real.exp ((D.p i+D.q k)*x+((D.q k)^2-(D.p i)^2)*t+y*rate D i k)*rate D i k
  have hA : HasDerivAt A Y y := by
    apply hasDerivAt_pi.mpr
    intro i
    apply hasDerivAt_pi.mpr
    intro k
    have H := (((((hasDerivAt_id y).mul_const (rate D i k)).const_add
      ((D.p i+D.q k)*x+((D.q k)^2-(D.p i)^2)*t)).exp).const_mul
      (D.rho i/(D.p i+D.q k)*gamma D D.a i k)).const_add (if i=k then 1 else 0)
    convert! H using 1 <;> simp only [A,Y,id_eq] <;> ring
  have hB : HasDerivAt B ((-h) • Y) 0 := by
    apply hasDerivAt_pi.mpr
    intro i
    apply hasDerivAt_pi.mpr
    intro k
    change HasDerivAt (fun e => B e i k) ((-h)*Y i k) 0
    have H := (((gamma_parameter_derivative D h hD i k).const_mul
      (D.rho i/(D.p i+D.q k))).mul_const
      (Real.exp ((D.p i+D.q k)*x+((D.q k)^2-(D.p i)^2)*t+y*rate D i k))).const_add
      (if i=k then 1 else 0)
    convert! H using 1 <;> simp only [Matrix.smul_apply,B,Y,Pi.smul_apply,smul_eq_mul] <;> ring
  have hAd := (GramDeterminant.det_derivative A Y y hA).deriv
  have hBd := (GramDeterminant.det_derivative B ((-h) • Y) 0 hB).deriv
  have hBA : B 0=A y := by ext i k; simp [A,B,parameter]
  change deriv (fun Y => (A Y).det) y=GramDeterminant.dDet (A y) Y at hAd
  simp only [slice,sy,Pi.smul_apply,smul_eq_mul,family,tauS,tau0,zpow_one]
  change deriv (fun e => (B e).det) 0=(-h)*deriv (fun Y => (A Y).det) y
  rw [hBd]
  change GramDeterminant.dDet (B 0) ((-h) • Y)=_
  rw [hBA,GramDeterminant.dDet_smul]
  rw [hAd]

end DLWContract.ContinuousGram
