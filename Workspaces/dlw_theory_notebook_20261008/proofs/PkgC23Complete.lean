import PkgContinuousGramCurve

noncomputable section
namespace DLWContract
namespace ContinuousGram

theorem bil_smul_left (a d : ℝ) (f g : XT) : bil a (d • f) g=d • bil a f g := by
  funext x t
  simp only [bil,hx,xx,dx,dt,Pi.add_apply,Pi.sub_apply,Pi.mul_apply,
    Pi.smul_apply,Pi.ofNat_apply,deriv_const_smul_field,smul_eq_mul,deriv_const_mul_field]
  ring

theorem bil_zero_right (a : ℝ) (f : XT) : bil a f 0=0 := by
  funext x t
  simp [bil,hx,xx,dx,dt]

theorem bil_parameter (a s : ℝ) (f g : XT) (x t : ℝ) :
    bil a f g x t=bil s f g x t-2*(s-a)*hx f g x t := by
  simp only [bil,hx,Pi.add_apply,Pi.sub_apply,Pi.mul_apply,Pi.smul_apply,
    Pi.ofNat_apply,smul_eq_mul]
  ring

theorem first_y_identity {N : ℕ} (D : Data N) (h : ℝ) (hD : PositiveData D h)
    (x y t : ℝ) :
    cbil D.a (sy (tau0 D 1)) (tau0 D 0) x y t=2*chx (tau0 D 1) (tau0 D 0) x y t := by
  let F := family D h y
  let G := fixed D y
  have hF := family_smooth D h y hD
  have hG := fixed_smooth D y
  have hf := c02_slice_jets F hF x 0 t
  have hg := c02_slice_jets G hG x 0 t
  have hχ := (hf.2.1.mul hg.1).sub (hf.1.mul hg.2.1)
  have hc := (((parameter_derivative D.a h).sub_const D.a).const_mul 2).neg
  have hp := hc.mul hχ
  have he : (fun e => cbil D.a F G x e t)=
      (fun e => -(2*(parameter D.a h e-D.a))*chx F G x e t) := by
    funext e
    have H := congrFun (congrFun (tauS_bilinear D h (parameter D.a h e)
      (c09_admissible_proved D h hD) (parameter_layer D h hD e) y) x) t
    rw [cbil,bil_parameter D.a (parameter D.a h e)]
    change bil (parameter D.a h e) (slice (tauS D (parameter D.a h e) 1) y)
      (slice (tau0 D 0) y) x t-2*(parameter D.a h e-D.a)*hx (slice F e) (slice G e) x t=_
    rw [H]
    change 0-2*(parameter D.a h e-D.a)*chx F G x e t=_
    ring
  have hp' : HasDerivAt (fun e => -(2*(parameter D.a h e-D.a))*chx F G x e t)
      (-2*h*chx F G x 0 t) 0 := by
    convert! hp using 1 <;>
      simp only [chx,hx,slice,Pi.neg_apply,Pi.sub_apply,Pi.mul_apply,parameter,
        zero_pow (by decide : 2 ≠ 0),mul_zero,zero_div,add_zero,sub_self,zero_mul,
        neg_zero,mul_neg,one_mul] <;> ring
  have hd := c02_deriv_cbil_y D.a F G hF hG x 0 t
  rw [he,hp'.deriv] at hd
  dsimp only [F,G] at hd
  simp only [cbil,fixed_sy,slice,Pi.zero_apply] at hd
  change -2*h*chx (family D h y) (fixed D y) x 0 t=
    bil D.a (slice (sy (family D h y)) 0) (slice (fixed D y) 0) x t+
      bil D.a (slice (family D h y) 0) 0 x t at hd
  rw [family_sy_at_zero D h y hD,fixed_slice,bil_smul_left,bil_zero_right] at hd
  have hχ0 : chx (family D h y) (fixed D y) x 0 t=
      chx (tau0 D 1) (tau0 D 0) x y t := by
    change hx (slice (family D h y) 0) (slice (fixed D y) 0) x t=_
    rw [family_at_zero,fixed_slice]
    rfl
  rw [hχ0] at hd
  change -2*h*chx (tau0 D 1) (tau0 D 0) x y t=
    (-h)*cbil D.a (sy (tau0 D 1)) (tau0 D 0) x y t+0 at hd
  have H : h*(cbil D.a (sy (tau0 D 1)) (tau0 D 0) x y t-
      2*chx (tau0 D 1) (tau0 D 0) x y t)=0 := by nlinarith [hd]
  have := (mul_eq_zero.mp H).resolve_left (ne_of_gt hD.1)
  linarith

end ContinuousGram

theorem c23_proved : C23 := by
  intro N D h hD
  have hfirst := ContinuousGram.continuous_first D h hD
  refine ⟨hfirst,?_⟩
  funext x y t
  have hsum := c02_deriv_cbil_y D.a (tau0 D 1) (tau0 D 0)
    (ContinuousGram.smooth_tau0 D 1) (ContinuousGram.smooth_tau0 D 0) x y t
  rw [hfirst] at hsum
  simp only [Pi.zero_apply,deriv_const] at hsum
  have hy := ContinuousGram.first_y_identity D h hD x y t
  change cbil D.a (sy (tau0 D 1)) (tau0 D 0) x y t-
    cbil D.a (tau0 D 1) (sy (tau0 D 0)) x y t-4*chx (tau0 D 1) (tau0 D 0) x y t=0
  linarith

#print axioms c23_proved
end DLWContract
