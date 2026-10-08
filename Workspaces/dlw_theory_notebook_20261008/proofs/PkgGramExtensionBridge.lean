import PkgGramInterpolationBridge

noncomputable section
namespace DLWContract.GramInterpolation
open GramRateExtension

theorem data_signs {N : ℕ} (D : Data N) (h0 h : ℝ) (hD : PositiveData D h0)
    (hh : 0<h) (hh0 : h≤h0) (i : Fin N) :
    D.p i-D.a+h/2<0 ∧ D.p i-D.a-h/2<0 ∧
    0<D.q i+D.a-h/2 ∧ 0<D.q i+D.a+h/2 := by
  have hi := hD.2.2.2 i
  constructor
  · linarith [hi.2.1]
  constructor
  · linarith [hi.2.1]
  constructor <;> linarith [hi.1,hi.2.1,hi.2.2.1]

theorem data_zero_signs {N : ℕ} (D : Data N) (h0 : ℝ) (hD : PositiveData D h0)
    (i : Fin N) : D.p i-D.a<0 ∧ 0<D.q i+D.a := by
  have hi := hD.2.2.2 i
  constructor <;> linarith [hD.1,hi.1,hi.2.1,hi.2.2.1]

theorem extension_zero {N : ℕ} (D : Data N) (h0 : ℝ) (hD : PositiveData D h0) :
    extF D 0=tau0 D 1 ∧ extG D 0=tau0 D 0 := by
  have hr (i : Fin N) : totalRate D i 0=1/(D.p i-D.a)+1/(D.q i+D.a) := by
    have hi := data_zero_signs D h0 hD i
    rw [totalRate,extendedRate_zero _ (ne_of_lt hi.1),extendedRate_zero _ (ne_of_gt hi.2)]
  constructor
  · funext x y t
    rw [tau0_row]
    unfold extF
    congr 1
    funext i
    have hi := data_zero_signs D h0 hD i
    rw [hr,Real.exp_add,amplitude_zero _ _ hi.1 hi.2]
    simp only [zpow_one,gamma]
    ring
  · funext x y t
    rw [tau0_row]
    simp only [extG,hr,zpow_zero,mul_one]

theorem amplitude_bridge (P Q h : ℝ) (hP : P+h/2<0) (hPm : P-h/2<0)
    (hQ : 0<Q-h/2) (hQp : 0<Q+h/2) :
    evenLogAmplitude P Q h=Real.log (-(P+h/2)/(Q-h/2))-
      (Real.log (lam h P)+Real.log (lam h Q))/2 := by
  rw [Real.log_div (ne_of_gt (neg_pos.mpr hP)) (ne_of_gt hQ)]
  rw [lam,lam,Real.log_div (ne_of_lt hP) (ne_of_lt hPm),
    Real.log_div (ne_of_gt hQp) (ne_of_gt hQ)]
  rw [Real.log_neg_eq_log]
  unfold evenLogAmplitude
  rw [show -P-h/2=-(P+h/2) by ring,show -P+h/2=-(P-h/2) by ring,
    Real.log_neg_eq_log,Real.log_neg_eq_log]
  ring

theorem extension_eq {N : ℕ} (D : Data N) (h0 h : ℝ) (hD : PositiveData D h0)
    (hh : 0<h) (hh0 : h≤h0) :
    tauI D h (D.a-h/2) 1 (1/2)=extF D h ∧ tauI D h D.a 0 0=extG D h := by
  have hs := data_signs D h0 h hD hh hh0
  have hp (i : Fin N) : lam h (D.p i-D.a) ≠ 0 :=
    div_ne_zero (ne_of_lt (hs i).1) (ne_of_lt (hs i).2.1)
  have hq (i : Fin N) : lam h (D.q i+D.a) ≠ 0 :=
    div_ne_zero (ne_of_gt (hs i).2.2.2) (ne_of_gt (hs i).2.2.1)
  have hr (i : Fin N) : totalRate D i h=
      (Real.log (lam h (D.p i-D.a))+Real.log (lam h (D.q i+D.a)))/h := by
    rw [totalRate,extendedRate_eq _ _ (ne_of_gt hh) (ne_of_lt (hs i).1)
      (ne_of_lt (hs i).2.1),extendedRate_eq _ _ (ne_of_gt hh)
      (ne_of_gt (hs i).2.2.2) (ne_of_gt (hs i).2.2.1)]
    ring
  constructor
  · funext x y t
    rw [tauI_row D h (D.a-h/2) 1 (1/2) x y t hp hq]
    unfold extF
    congr 1
    funext i
    have hg : gamma D (D.a-h/2) i i= -((D.p i-D.a)+h/2)/((D.q i+D.a)-h/2) := by
      unfold gamma
      congr 1 <;> ring
    have hgp : 0<gamma D (D.a-h/2) i i := by
      rw [hg]
      exact div_pos (neg_pos.mpr (hs i).1) (hs i).2.2.1
    rw [zpow_one,hr,amplitude_bridge _ _ _ (hs i).1 (hs i).2.1
      (hs i).2.2.1 (hs i).2.2.2,← hg]
    rw [show y*((Real.log (lam h (D.p i-D.a))+Real.log (lam h (D.q i+D.a)))/h)+
      (Real.log (gamma D (D.a-h/2) i i)-
      (Real.log (lam h (D.p i-D.a))+Real.log (lam h (D.q i+D.a)))/2)=
      Real.log (gamma D (D.a-h/2) i i)+(y/h-1/2)*
      (Real.log (lam h (D.p i-D.a))+Real.log (lam h (D.q i+D.a))) by ring,
      Real.exp_add,Real.exp_log hgp]
    ring
  · funext x y t
    rw [tauI_row D h D.a 0 0 x y t hp hq]
    unfold extG
    congr 1
    funext i
    rw [hr]
    simp only [zpow_zero,mul_one,sub_zero]
    congr 2
    ring

#print axioms extension_zero
#print axioms extension_eq
end DLWContract.GramInterpolation
