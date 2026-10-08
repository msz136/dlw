import PkgGramInterpolation

noncomputable section
open scoped BigOperators Matrix
namespace DLWContract.GramInterpolation

theorem det_row_col {N : ℕ} (E : Matrix (Fin N) (Fin N) ℝ) (a b : Fin N → ℝ) :
    (Matrix.det (fun i k => (if i=k then 1 else 0)+a i*b k*E i k))=
      Matrix.det (fun i k => (if i=k then 1 else 0)+(a i*b i)*E i k) := by
  let L := Matrix.diagonal a
  let R := Matrix.diagonal b
  have hLE (i k : Fin N) : (L*E) i k=a i*E i k := Matrix.diagonal_mul a E i k
  have h1 : (fun i k => (if i=k then 1 else 0)+a i*b k*E i k)=
      (1+(L*E)*R : Matrix (Fin N) (Fin N) ℝ) := by
    ext i k
    simp only [Matrix.add_apply,Matrix.one_apply,R,Matrix.mul_diagonal]
    rw [hLE]
    ring
  have h2 : (fun i k => (if i=k then 1 else 0)+(a i*b i)*E i k)=
      (1+R*(L*E) : Matrix (Fin N) (Fin N) ℝ) := by
    ext i k
    simp only [Matrix.add_apply,Matrix.one_apply,R,Matrix.diagonal_mul]
    rw [hLE]
    ring
  rw [h1,h2,Matrix.det_one_add_mul_comm]

theorem tau0_row {N : ℕ} (D : Data N) (n : ℤ) (x y t : ℝ) :
    tau0 D n x y t=rowTau D (fun i => D.rho i*(gamma D D.a i i)^n*
      Real.exp (y*(1/(D.p i-D.a)+1/(D.q i+D.a)))) x t := by
  let E : Matrix (Fin N) (Fin N) ℝ := fun i k =>
    Real.exp ((D.p i+D.q k)*x+((D.q k)^2-(D.p i)^2)*t)/(D.p i+D.q k)
  let A : Fin N → ℝ := fun i => D.rho i*(D.a-D.p i)^n*Real.exp (y/(D.p i-D.a))
  let B : Fin N → ℝ := fun k => ((D.q k+D.a)^n)⁻¹*Real.exp (y/(D.q k+D.a))
  have hs (i k : Fin N) : D.rho i/(D.p i+D.q k)*(gamma D D.a i k)^n*
      Real.exp ((D.p i+D.q k)*x+((D.q k)^2-(D.p i)^2)*t+
        y*(1/(D.p i-D.a)+1/(D.q k+D.a)))=A i*B k*E i k := by
    have hg : gamma D D.a i k=(D.a-D.p i)/(D.q k+D.a) := by simp [gamma,neg_sub]
    have he : (D.p i+D.q k)*x+((D.q k)^2-(D.p i)^2)*t+
      y*(1/(D.p i-D.a)+1/(D.q k+D.a))=
      ((D.p i+D.q k)*x+((D.q k)^2-(D.p i)^2)*t)+y/(D.p i-D.a)+y/(D.q k+D.a) := by ring
    rw [hg,div_zpow,he,Real.exp_add,Real.exp_add]
    dsimp [A,B,E]
    ring
  have hw (i : Fin N) : D.rho i*(gamma D D.a i i)^n*
      Real.exp (y*(1/(D.p i-D.a)+1/(D.q i+D.a)))=A i*B i := by
    have hg : gamma D D.a i i=(D.a-D.p i)/(D.q i+D.a) := by simp [gamma,neg_sub]
    rw [hg,div_zpow,show y*(1/(D.p i-D.a)+1/(D.q i+D.a))=
      y/(D.p i-D.a)+y/(D.q i+D.a) by ring,Real.exp_add]
    dsimp [A,B]
    ring
  unfold tau0 rowTau
  simp_rw [hs,hw]
  rw [det_row_col E A B]
  apply congrArg Matrix.det
  ext i k
  dsimp [E]
  ring

theorem tauI_row {N : ℕ} (D : Data N) (h s : ℝ) (n : ℤ) (offset x y t : ℝ)
    (hp : ∀ i, lam h (D.p i-D.a) ≠ 0) (hq : ∀ k, lam h (D.q k+D.a) ≠ 0) :
    tauI D h s n offset x y t=rowTau D (fun i => D.rho i*(gamma D s i i)^n*
      Real.exp ((y/h-offset)*(Real.log (lam h (D.p i-D.a))+Real.log (lam h (D.q i+D.a))))) x t := by
  let E : Matrix (Fin N) (Fin N) ℝ := fun i k =>
    Real.exp ((D.p i+D.q k)*x+((D.q k)^2-(D.p i)^2)*t)/(D.p i+D.q k)
  let A : Fin N → ℝ := fun i => D.rho i*(s-D.p i)^n*
    Real.exp ((y/h-offset)*Real.log (lam h (D.p i-D.a)))
  let B : Fin N → ℝ := fun k => ((D.q k+s)^n)⁻¹*
    Real.exp ((y/h-offset)*Real.log (lam h (D.q k+D.a)))
  have hs (i k : Fin N) : D.rho i/(D.p i+D.q k)*(gamma D s i k)^n*
      Real.exp ((D.p i+D.q k)*x+((D.q k)^2-(D.p i)^2)*t+
        (y/h-offset)*Real.log (chi D h i k))=A i*B k*E i k := by
    have hg : gamma D s i k=(s-D.p i)/(D.q k+s) := by simp [gamma,neg_sub]
    rw [hg,div_zpow,chi,Real.log_mul (hp i) (hq k),mul_add]
    dsimp [A,B,E]
    rw [show (D.p i+D.q k)*x+((D.q k)^2-(D.p i)^2)*t+
      ((y/h-offset)*Real.log (lam h (D.p i-D.a))+
      (y/h-offset)*Real.log (lam h (D.q k+D.a))) =
      (((D.p i+D.q k)*x+((D.q k)^2-(D.p i)^2)*t)+
      (y/h-offset)*Real.log (lam h (D.p i-D.a)))+
      (y/h-offset)*Real.log (lam h (D.q k+D.a)) by ring]
    rw [Real.exp_add,Real.exp_add]
    ring
  have hw (i : Fin N) : D.rho i*(gamma D s i i)^n*
      Real.exp ((y/h-offset)*(Real.log (lam h (D.p i-D.a))+Real.log (lam h (D.q i+D.a))))=
      A i*B i := by
    have hg : gamma D s i i=(s-D.p i)/(D.q i+s) := by simp [gamma,neg_sub]
    rw [hg,div_zpow,mul_add,Real.exp_add]
    dsimp [A,B]
    ring
  unfold tauI rowTau
  simp_rw [hs,hw]
  rw [det_row_col E A B]
  apply congrArg Matrix.det
  ext i k
  dsimp [E]
  ring

end DLWContract.GramInterpolation
