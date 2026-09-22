/-! ## Toolkit: calculus lemmas for the three coordinate derivatives on `XYT`

Everything below is new material added by the final C02 closure. -/

abbrev c02lift (W : XYT) : ℝ × (ℝ × ℝ) → ℝ := fun z => W z.1 z.2.1 z.2.2

/-- The direction vectors, kept as `inl`/`inr` applications so no normalisation is needed. -/
abbrev c02vx : ℝ × (ℝ × ℝ) := ContinuousLinearMap.inl ℝ ℝ (ℝ × ℝ) 1

abbrev c02vy : ℝ × (ℝ × ℝ) :=
  (ContinuousLinearMap.inr ℝ ℝ (ℝ × ℝ)).comp (ContinuousLinearMap.inl ℝ ℝ ℝ) 1

abbrev c02vt : ℝ × (ℝ × ℝ) :=
  (ContinuousLinearMap.inr ℝ ℝ (ℝ × ℝ)).comp (ContinuousLinearMap.inr ℝ ℝ ℝ) 1

/-- `deriv` along the first coordinate is the Fréchet derivative at the lifted point. -/
lemma c02_deriv3_fst (W : XYT) (hW : Smooth3 W) (x y t : ℝ) :
    deriv (fun a : ℝ => W a y t) x = fderiv ℝ (c02lift W) (x, (y, t)) c02vx := by
  have hd : DifferentiableAt ℝ (c02lift W) (x, (y, t)) :=
    (hW.differentiable c02_top_ne_zero) (x, (y, t))
  have hγ : HasFDerivAt (fun a : ℝ => (a, (y, t)))
      (ContinuousLinearMap.inl ℝ ℝ (ℝ × ℝ)) x :=
    hasFDerivAt_prodMk_left x (y, t)
  have h := (hd.hasFDerivAt.comp x hγ).hasDerivAt
  simpa only [c02lift, c02vx, Function.comp_def, ContinuousLinearMap.comp_apply] using h.deriv

lemma c02_deriv3_snd (W : XYT) (hW : Smooth3 W) (x y t : ℝ) :
    deriv (fun b : ℝ => W x b t) y = fderiv ℝ (c02lift W) (x, (y, t)) c02vy := by
  have hd : DifferentiableAt ℝ (c02lift W) (x, (y, t)) :=
    (hW.differentiable c02_top_ne_zero) (x, (y, t))
  have hγ : HasFDerivAt (fun b : ℝ => (x, (b, t)))
      ((ContinuousLinearMap.inr ℝ ℝ (ℝ × ℝ)).comp (ContinuousLinearMap.inl ℝ ℝ ℝ)) y :=
    (hasFDerivAt_prodMk_right x (y, t)).comp y (hasFDerivAt_prodMk_left y t)
  have h := (hd.hasFDerivAt.comp y hγ).hasDerivAt
  simpa only [c02lift, c02vy, Function.comp_def, ContinuousLinearMap.comp_apply] using h.deriv

lemma c02_deriv3_trd (W : XYT) (hW : Smooth3 W) (x y t : ℝ) :
    deriv (W x y) t = fderiv ℝ (c02lift W) (x, (y, t)) c02vt := by
  have hd : DifferentiableAt ℝ (c02lift W) (x, (y, t)) :=
    (hW.differentiable c02_top_ne_zero) (x, (y, t))
  have hγ : HasFDerivAt (fun c : ℝ => (x, (y, c)))
      ((ContinuousLinearMap.inr ℝ ℝ (ℝ × ℝ)).comp (ContinuousLinearMap.inr ℝ ℝ ℝ)) t :=
    (hasFDerivAt_prodMk_right x (y, t)).comp t (hasFDerivAt_prodMk_right y t)
  have h := (hd.hasFDerivAt.comp t hγ).hasDerivAt
  simpa only [c02lift, c02vt, Function.comp_def, ContinuousLinearMap.comp_apply] using h.deriv

/-! ### Smoothness closure -/

@[simp] lemma c02_smooth_add {F G : XYT} (hF : Smooth3 F) (hG : Smooth3 G) :
    Smooth3 (F + G) := by
  have h := hF.add hG
  simpa only [Smooth3, c02lift, Pi.add_apply] using h

@[simp] lemma c02_smooth_sub {F G : XYT} (hF : Smooth3 F) (hG : Smooth3 G) :
    Smooth3 (F - G) := by
  have h := hF.sub hG
  simpa only [Smooth3, c02lift, Pi.sub_apply] using h

@[simp] lemma c02_smooth_neg {F : XYT} (hF : Smooth3 F) : Smooth3 (-F) := by
  have h := hF.neg
  simpa only [Smooth3, c02lift, Pi.neg_apply] using h

@[simp] lemma c02_smooth_mul {F G : XYT} (hF : Smooth3 F) (hG : Smooth3 G) :
    Smooth3 (F * G) := by
  have h := hF.mul hG
  simpa only [Smooth3, c02lift, Pi.mul_apply] using h

@[simp] lemma c02_smooth_smul (c : ℝ) {F : XYT} (hF : Smooth3 F) : Smooth3 (c • F) := by
  have h := hF.const_smul c
  simpa only [Smooth3, c02lift, Pi.smul_apply] using h

@[simp] lemma c02_smooth_sx {F : XYT} (hF : Smooth3 F) : Smooth3 (sx F) := by
  have hfd : ContDiff ℝ ⊤ (fun z : ℝ × (ℝ × ℝ) => fderiv ℝ (c02lift F) z c02vx) :=
    (hF.fderiv_right (m := ⊤) le_top).clm_apply
      (contDiff_const : ContDiff ℝ ⊤ (fun _ : ℝ × (ℝ × ℝ) => c02vx))
  have hfun : (fun z : ℝ × (ℝ × ℝ) => sx F z.1 z.2.1 z.2.2)
      = fun z : ℝ × (ℝ × ℝ) => fderiv ℝ (c02lift F) z c02vx := by
    funext z
    show deriv (fun a : ℝ => F a z.2.1 z.2.2) z.1 = fderiv ℝ (c02lift F) z c02vx
    exact c02_deriv3_fst F hF z.1 z.2.1 z.2.2
  show ContDiff ℝ ⊤ (fun z : ℝ × (ℝ × ℝ) => sx F z.1 z.2.1 z.2.2)
  rw [hfun]
  exact hfd

@[simp] lemma c02_smooth_sy {F : XYT} (hF : Smooth3 F) : Smooth3 (sy F) := by
  have hfd : ContDiff ℝ ⊤ (fun z : ℝ × (ℝ × ℝ) => fderiv ℝ (c02lift F) z c02vy) :=
    (hF.fderiv_right (m := ⊤) le_top).clm_apply
      (contDiff_const : ContDiff ℝ ⊤ (fun _ : ℝ × (ℝ × ℝ) => c02vy))
  have hfun : (fun z : ℝ × (ℝ × ℝ) => sy F z.1 z.2.1 z.2.2)
      = fun z : ℝ × (ℝ × ℝ) => fderiv ℝ (c02lift F) z c02vy := by
    funext z
    show deriv (fun b : ℝ => F z.1 b z.2.2) z.2.1 = fderiv ℝ (c02lift F) z c02vy
    exact c02_deriv3_snd F hF z.1 z.2.1 z.2.2
  show ContDiff ℝ ⊤ (fun z : ℝ × (ℝ × ℝ) => sy F z.1 z.2.1 z.2.2)
  rw [hfun]
  exact hfd

@[simp] lemma c02_smooth_st {F : XYT} (hF : Smooth3 F) : Smooth3 (st F) := by
  have hfd : ContDiff ℝ ⊤ (fun z : ℝ × (ℝ × ℝ) => fderiv ℝ (c02lift F) z c02vt) :=
    (hF.fderiv_right (m := ⊤) le_top).clm_apply
      (contDiff_const : ContDiff ℝ ⊤ (fun _ : ℝ × (ℝ × ℝ) => c02vt))
  have hfun : (fun z : ℝ × (ℝ × ℝ) => st F z.1 z.2.1 z.2.2)
      = fun z : ℝ × (ℝ × ℝ) => fderiv ℝ (c02lift F) z c02vt := by
    funext z
    show deriv (F z.1 z.2.1) z.2.2 = fderiv ℝ (c02lift F) z c02vt
    exact c02_deriv3_trd F hF z.1 z.2.1 z.2.2
  show ContDiff ℝ ⊤ (fun z : ℝ × (ℝ × ℝ) => st F z.1 z.2.1 z.2.2)
  rw [hfun]
  exact hfd

/-- `log` of a positive `XYT`, pointwise. -/
def c02log (f : XYT) : XYT := fun x y t => Real.log (f x y t)

/-- `c02log` unfolded to the raw `Real.log` lambda. -/
lemma c02log_eq (F : XYT) : c02log F = fun x y t => Real.log (F x y t) := rfl

@[simp] lemma c02_smooth_log {F : XYT} (hF : Smooth3 F) (hpos : Positive3 F) :
    Smooth3 (c02log F) := by
  have h : ContDiff ℝ ⊤ (fun z : ℝ × (ℝ × ℝ) => F z.1 z.2.1 z.2.2) := hF
  have h' := h.log (fun z => ne_of_gt (hpos z.1 z.2.1 z.2.2))
  simpa only [c02log, Smooth3, c02lift] using h'

/-! ### Differentiability of the coordinate slices -/

lemma c02_diff_x (F : XYT) (hF : Smooth3 F) (x y t : ℝ) :
    DifferentiableAt ℝ (fun a : ℝ => F a y t) x := by
  have hd : HasFDerivAt (c02lift F) (fderiv ℝ (c02lift F) (x, (y, t))) (x, (y, t)) :=
    ((hF.differentiable c02_top_ne_zero) (x, (y, t))).hasFDerivAt
  have hγ : HasFDerivAt (fun a : ℝ => (a, (y, t)))
      (ContinuousLinearMap.inl ℝ ℝ (ℝ × ℝ)) x := hasFDerivAt_prodMk_left x (y, t)
  have h3 := (hd.comp x hγ).differentiableAt
  simpa only [c02lift, Function.comp_def] using h3

lemma c02_diff_y (F : XYT) (hF : Smooth3 F) (x y t : ℝ) :
    DifferentiableAt ℝ (fun b : ℝ => F x b t) y := by
  have hd : HasFDerivAt (c02lift F) (fderiv ℝ (c02lift F) (x, (y, t))) (x, (y, t)) :=
    ((hF.differentiable c02_top_ne_zero) (x, (y, t))).hasFDerivAt
  have hγ : HasFDerivAt (fun b : ℝ => (x, (b, t)))
      ((ContinuousLinearMap.inr ℝ ℝ (ℝ × ℝ)).comp (ContinuousLinearMap.inl ℝ ℝ ℝ)) y :=
    (hasFDerivAt_prodMk_right x (y, t)).comp y (hasFDerivAt_prodMk_left y t)
  have h3 := (hd.comp y hγ).differentiableAt
  simpa only [c02lift, Function.comp_def] using h3

lemma c02_diff_t (F : XYT) (hF : Smooth3 F) (x y t : ℝ) :
    DifferentiableAt ℝ (F x y) t := by
  have hd : HasFDerivAt (c02lift F) (fderiv ℝ (c02lift F) (x, (y, t))) (x, (y, t)) :=
    ((hF.differentiable c02_top_ne_zero) (x, (y, t))).hasFDerivAt
  have hγ : HasFDerivAt (fun c : ℝ => (x, (y, c)))
      ((ContinuousLinearMap.inr ℝ ℝ (ℝ × ℝ)).comp (ContinuousLinearMap.inr ℝ ℝ ℝ)) t :=
    (hasFDerivAt_prodMk_right x (y, t)).comp t (hasFDerivAt_prodMk_right y t)
  have h3 := (hd.comp t hγ).differentiableAt
  simpa only [c02lift, Function.comp_def] using h3

/-! ### Linearity over `+`, `-`, scalar multiples, and the product rule -/

lemma c02_sx_add (F G : XYT) (hF : Smooth3 F) (hG : Smooth3 G) :
    sx (F + G) = sx F + sx G := by
  funext x y t
  simp only [sx, Pi.add_apply]
  exact deriv_add (c02_diff_x F hF x y t) (c02_diff_x G hG x y t)

lemma c02_sx_sub (F G : XYT) (hF : Smooth3 F) (hG : Smooth3 G) :
    sx (F - G) = sx F - sx G := by
  funext x y t
  simp only [sx, Pi.sub_apply]
  exact deriv_sub (c02_diff_x F hF x y t) (c02_diff_x G hG x y t)

lemma c02_sx_smul (c : ℝ) (F : XYT) : sx (c • F) = c • sx F := by
  funext x y t
  simp only [sx, Pi.smul_apply, smul_eq_mul]
  exact deriv_const_mul_field c

lemma c02_sx_mul (F G : XYT) (hF : Smooth3 F) (hG : Smooth3 G) :
    sx (F * G) = sx F * G + F * sx G := by
  funext x y t
  simp only [sx, Pi.mul_apply]
  exact deriv_mul (c02_diff_x F hF x y t) (c02_diff_x G hG x y t)

lemma c02_sy_add (F G : XYT) (hF : Smooth3 F) (hG : Smooth3 G) :
    sy (F + G) = sy F + sy G := by
  funext x y t
  simp only [sy, Pi.add_apply]
  exact deriv_add (c02_diff_y F hF x y t) (c02_diff_y G hG x y t)

lemma c02_sy_sub (F G : XYT) (hF : Smooth3 F) (hG : Smooth3 G) :
    sy (F - G) = sy F - sy G := by
  funext x y t
  simp only [sy, Pi.sub_apply]
  exact deriv_sub (c02_diff_y F hF x y t) (c02_diff_y G hG x y t)

lemma c02_sy_smul (c : ℝ) (F : XYT) : sy (c • F) = c • sy F := by
  funext x y t
  simp only [sy, Pi.smul_apply, smul_eq_mul]
  exact deriv_const_mul_field c

lemma c02_sy_mul (F G : XYT) (hF : Smooth3 F) (hG : Smooth3 G) :
    sy (F * G) = sy F * G + F * sy G := by
  funext x y t
  simp only [sy, Pi.mul_apply]
  exact deriv_mul (c02_diff_y F hF x y t) (c02_diff_y G hG x y t)

lemma c02_st_add (F G : XYT) (hF : Smooth3 F) (hG : Smooth3 G) :
    st (F + G) = st F + st G := by
  funext x y t
  simp only [st, Pi.add_apply]
  exact deriv_add (c02_diff_t F hF x y t) (c02_diff_t G hG x y t)

lemma c02_st_sub (F G : XYT) (hF : Smooth3 F) (hG : Smooth3 G) :
    st (F - G) = st F - st G := by
  funext x y t
  simp only [st, Pi.sub_apply]
  exact deriv_sub (c02_diff_t F hF x y t) (c02_diff_t G hG x y t)

lemma c02_st_smul (c : ℝ) (F : XYT) : st (c • F) = c • st F := by
  funext x y t
  simp only [st, Pi.smul_apply, smul_eq_mul]
  exact deriv_const_mul_field c

lemma c02_st_mul (F G : XYT) (hF : Smooth3 F) (hG : Smooth3 G) :
    st (F * G) = st F * G + F * st G := by
  funext x y t
  simp only [st, Pi.mul_apply]
  exact deriv_mul (c02_diff_t F hF x y t) (c02_diff_t G hG x y t)

/-! ### Clairaut swaps (normal form: `st` outermost, then `sx`, then `sy`) -/

lemma c02_sy_sx (W : XYT) (hW : Smooth3 W) : sy (sx W) = sx (sy W) := by
  funext x y t
  exact c02_clairaut (c02_smooth_fixed_t W hW t) x y

lemma c02_sy_st (W : XYT) (hW : Smooth3 W) : sy (st W) = st (sy W) := by
  funext x y t
  exact (c02_clairaut (c02_smooth_fixed_x W hW x) y t).symm

lemma c02_sx_st (W : XYT) (hW : Smooth3 W) : sx (st W) = st (sx W) := by
  funext x y t
  exact (c02_clairaut (c02_smooth_fixed_y W hW y) x t).symm

/-! ### Derivatives of the zero function -/

@[simp] lemma c02_sx_zero : sx (0 : XYT) = 0 := by
  funext x y t
  simp [sx]

@[simp] lemma c02_sy_zero : sy (0 : XYT) = 0 := by
  funext x y t
  simp [sy]

@[simp] lemma c02_st_zero : st (0 : XYT) = 0 := by
  funext x y t
  simp [st]

/-! ## The certificate -/

/-- Numerals in `XYT` are constant functions. -/
@[simp] lemma c02_ofNat_apply (n : ℕ) (x y t : ℝ) :
    ((OfNat.ofNat n : XYT) x y t) = (OfNat.ofNat n : ℝ) := rfl

/-- Numerals in `XT` are constant functions. -/
@[simp] lemma c02_ofNat_apply_XT (n : ℕ) (x t : ℝ) :
    ((OfNat.ofNat n : XT) x t) = (OfNat.ofNat n : ℝ) := rfl

/-- The `y`-slice at `x` is `F x y`. -/
lemma c02_slice_fun (F : XYT) (y x : ℝ) : slice F y x = F x y := rfl

/-! ## Unfolding `cbil` and `chx` on `XYT`

`cbil`/`chx` are defined through `y`-slices; these rewrites put them in `(x,t)`
derivative notation directly on `XYT`. -/

lemma c02_cbil_unfold (a : ℝ) (F G : XYT) :
    cbil a F G
      = sx (sx F) * G - ((2 : XYT) * sx F) * sx G + F * sx (sx G)
        + st F * G - F * st G + (2*a) • (sx F * G - F * sx G) := by
  funext x y t
  simp only [cbil, bil, slice, dx, dt, xx, hx, sx, st, Pi.mul_apply, Pi.sub_apply,
    Pi.add_apply, Pi.smul_apply, c02_ofNat_apply, c02_ofNat_apply_XT, c02_slice_fun]

lemma c02_chx_unfold (F G : XYT) : chx F G = sx F * G - F * sx G := by
  funext x y t
  simp only [chx, hx, slice, dx, sx, Pi.mul_apply, Pi.sub_apply]

/-! ## Log-jet rewrites for `XYT` -/

lemma c02_log_sx' (F : XYT) (hF : Smooth3 F) (hpos : Positive3 F) :
    sx F = F * sx (c02log F) := by
  have h := c02_log_sx F hF (fun x y t => hpos x y t)
  simpa only [c02log_eq] using h

lemma c02_log_sy' (F : XYT) (hF : Smooth3 F) (hpos : Positive3 F) :
    sy F = F * sy (c02log F) := by
  have h := c02_log_sy F hF (fun x y t => hpos x y t)
  simpa only [c02log_eq] using h

lemma c02_log_st' (F : XYT) (hF : Smooth3 F) (hpos : Positive3 F) :
    st F = F * st (c02log F) := by
  have h := c02_log_st F hF (fun x y t => hpos x y t)
  simpa only [c02log_eq] using h

lemma c02_log_sxx' (F : XYT) (hF : Smooth3 F) (hpos : Positive3 F) :
    sx (sx F) = F * (sx (sx (c02log F)) + (sx (c02log F)) ^ 2) := by
  have h := c02_log_sxx F hF (fun x y t => hpos x y t)
  simpa only [c02log_eq] using h

/-- First `x`-derivative of `sy F`, in log coordinates. -/
lemma c02_sx_sy_log (F : XYT) (hF : Smooth3 F) (hpos : Positive3 F) :
    sx (sy F) = sx F * sy (c02log F) + F * sx (sy (c02log F)) := by
  rw [c02_log_sy' F hF hpos]
  exact c02_sx_mul F (sy (c02log F)) hF (c02_smooth_sy (c02_smooth_log hF hpos))

/-- `t`-derivative of `sy F`, in log coordinates. -/
lemma c02_st_sy_log (F : XYT) (hF : Smooth3 F) (hpos : Positive3 F) :
    st (sy F) = st F * sy (c02log F) + F * st (sy (c02log F)) := by
  rw [c02_log_sy' F hF hpos]
  exact c02_st_mul F (sy (c02log F)) hF (c02_smooth_sy (c02_smooth_log hF hpos))

/-- Second `x`-derivative of `sy F`, in log coordinates. -/
lemma c02_sxx_sy_log (F : XYT) (hF : Smooth3 F) (hpos : Positive3 F) :
    sx (sx (sy F)) = sx (sx F) * sy (c02log F)
      + (2 : XYT) * (sx F * sx (sy (c02log F))) + F * sx (sx (sy (c02log F))) := by
  have hQ : Smooth3 (c02log F) := c02_smooth_log hF hpos
  have hsyQ : Smooth3 (sy (c02log F)) := c02_smooth_sy hQ
  rw [c02_sx_sy_log F hF hpos,
    c02_sx_add (sx F * sy (c02log F)) (F * sx (sy (c02log F)))
      (c02_smooth_mul (c02_smooth_sx hF) hsyQ)
      (c02_smooth_mul hF (c02_smooth_sx hsyQ)),
    c02_sx_mul (sx F) (sy (c02log F)) (c02_smooth_sx hF) hsyQ,
    c02_sx_mul F (sx (sy (c02log F))) hF (c02_smooth_sx hsyQ)]
  ring

/-- `R = A_xx + (B_x)^2 + B_t + 2a B_x` (the C13 quotient in `A`,`B` coordinates). -/
def c02R (a : ℝ) (A B : XYT) : XYT :=
  sx (sx A) + (sx B) * (sx B) + st B + (2*a) • sx B

/-- `S = 2E + 4 B_x` with `E = q_xxy - 2 B_x q_xy - q_yt - 2a q_xy`, `q = (A-B)/2`. -/
def c02S (a : ℝ) (A B : XYT) : XYT :=
  sx (sx (sy A)) - sx (sx (sy B)) - st (sy A) + st (sy B)
    - (2:ℝ) • ((sx B) * (sx (sy A) - sx (sy B)))
    - (2*a) • (sx (sy A) - sx (sy B)) + (4:ℝ) • sx B

/-- `2 * (q_y R + E + 2 B_x)`: twice the honest third-order hypothesis. -/
def c02E2 (a : ℝ) (A B : XYT) : XYT := (sy A - sy B) * c02R a A B + c02S a A B

/-- All the rewriting used to compare `c1`/`c2` with the certificate. -/
macro "c02_simp" "[" es:Lean.Parser.Tactic.simpLemma,* "]" : tactic =>
  `(tactic|
    (simp (config := { maxDischargeDepth := 40 }) only [c1, c2, c02R, c02S, c02E2,
      c02_smooth_add, c02_smooth_sub, c02_smooth_neg, c02_smooth_mul, c02_smooth_smul,
      c02_smooth_sx, c02_smooth_sy, c02_smooth_st,
      c02_sx_add, c02_sx_sub, c02_sx_smul, c02_sx_mul,
      c02_sy_add, c02_sy_sub, c02_sy_smul, c02_sy_mul,
      c02_st_add, c02_st_sub, c02_st_smul, c02_st_mul,
      c02_sy_sx, c02_sy_st, c02_sx_st, $es,*]))

lemma c02_c1_eq (a : ℝ) (A B : XYT) (hA : Smooth3 A) (hB : Smooth3 B) :
    c1 a ((2:ℝ) • sx B) ((2:ℝ) • sx (sy A))
      = (2:ℝ) • sx (sy (c02R a A B)) := by
  c02_simp [hA, hB]
  funext x y t
  simp only [Pi.add_apply, Pi.mul_apply, Pi.smul_apply, smul_eq_mul]
  ring

/-- The second residual identity: `c2 = 2 ∂x∂y R − 2 ∂x S`. -/
lemma c02_c2_eq (a : ℝ) (A B : XYT) (hA : Smooth3 A) (hB : Smooth3 B) :
    c2 a ((2:ℝ) • sx B) ((2:ℝ) • sx (sy A))
      = (2:ℝ) • sx (sy (c02R a A B)) - (2:ℝ) • sx (c02S a A B) := by
  c02_simp [hA, hB]
  funext x y t
  simp only [Pi.add_apply, Pi.sub_apply, Pi.mul_apply, Pi.smul_apply, smul_eq_mul,
    c02_ofNat_apply]
  ring

/-! ## The three bridge identities

With `A = log f + log g`, `B = log f - log g`:

* `cbil a f g = (f*g) * R` where `R = c02R a A B`,
* `chx f g = (f*g) * B_x`,
* `2 * cbil a f (sy g) = (f*g) * (c02E2 a A B - 4 B_x)`. -/

/-- All the rewriting used for the bridge identities. -/
macro "c02_bridge" "[" es:Lean.Parser.Tactic.simpLemma,* "]" : tactic =>
  `(tactic|
    (simp (config := { maxDischargeDepth := 60 }) only [c02R, c02S, c02E2,
      c02_cbil_unfold, c02_chx_unfold,
      c02_log_sx', c02_log_sy', c02_log_st', c02_log_sxx',
      c02_sx_sy_log, c02_st_sy_log, c02_sxx_sy_log,
      c02_smooth_add, c02_smooth_sub, c02_smooth_neg, c02_smooth_mul, c02_smooth_smul,
      c02_smooth_sx, c02_smooth_sy, c02_smooth_st, c02_smooth_log,
      c02_sx_add, c02_sx_sub, c02_sx_smul, c02_sx_mul,
      c02_sy_add, c02_sy_sub, c02_sy_smul, c02_sy_mul,
      c02_st_add, c02_st_sub, c02_st_smul, c02_st_mul,
      c02_sy_sx, c02_sy_st, c02_sx_st, $es,*]))

/-- Bridge 1: the C13 quotient identity in `A`,`B` coordinates. -/
lemma c02_cbil_eq (a : ℝ) (f g : XYT) (hf : Smooth3 f) (hg : Smooth3 g)
    (hfp : Positive3 f) (hgp : Positive3 g) :
    cbil a f g = (f * g) * c02R a (c02log f + c02log g) (c02log f - c02log g) := by
  c02_bridge [hf, hg, hfp, hgp]
  funext x y t
  simp only [Pi.add_apply, Pi.sub_apply, Pi.mul_apply, Pi.smul_apply, smul_eq_mul,
    Pi.pow_apply, c02_ofNat_apply, c02_ofNat_apply_XT]
  ring

/-- Bridge 2: `chx f g = (f*g) * B_x`. -/
lemma c02_chx_eq (f g : XYT) (hf : Smooth3 f) (hg : Smooth3 g)
    (hfp : Positive3 f) (hgp : Positive3 g) :
    chx f g = (f * g) * sx (c02log f - c02log g) := by
  c02_bridge [hf, hg, hfp, hgp]
  funext x y t
  simp only [Pi.add_apply, Pi.sub_apply, Pi.mul_apply, Pi.smul_apply, smul_eq_mul,
    c02_ofNat_apply]
  ring

/-- Bridge 3: the `y`-derivative of `cbil` in `A`,`B` coordinates. -/
lemma c02_cbil_syg_eq (a : ℝ) (f g : XYT) (hf : Smooth3 f) (hg : Smooth3 g)
    (hfp : Positive3 f) (hgp : Positive3 g) :
    (2:ℝ) • cbil a f (sy g)
      = (f * g) * (c02E2 a (c02log f + c02log g) (c02log f - c02log g)
          - (4:ℝ) • sx (c02log f - c02log g)) := by
  c02_bridge [hf, hg, hfp, hgp]
  funext x y t
  simp only [Pi.add_apply, Pi.sub_apply, Pi.mul_apply, Pi.smul_apply, smul_eq_mul,
    Pi.pow_apply, c02_ofNat_apply, c02_ofNat_apply_XT]
  ring


/-! ## `cu`, `cv` in `A`,`B` coordinates -/

lemma c02_log_sub_eq (f g : XYT) :
    (fun x y t => Real.log (f x y t) - Real.log (g x y t)) = c02log f - c02log g := by
  funext x y t
  simp only [Pi.sub_apply, c02log_eq]

lemma c02_log_add_eq (f g : XYT) :
    (fun x y t => Real.log (f x y t) + Real.log (g x y t)) = c02log f + c02log g := by
  funext x y t
  simp only [Pi.add_apply, c02log_eq]

lemma c02_cu_eq (f g : XYT) :
    cu f g = (2:ℝ) • sx (c02log f - c02log g) := by
  funext x y t
  simp only [cu, c02_log_sub_eq, Pi.mul_apply, Pi.smul_apply, smul_eq_mul,
    c02_ofNat_apply]

lemma c02_cv_eq (f g : XYT) :
    cv f g = (2:ℝ) • sx (sy (c02log f + c02log g)) := by
  funext x y t
  simp only [cv, c02_log_add_eq, Pi.mul_apply, Pi.smul_apply, smul_eq_mul,
    c02_ofNat_apply]

/-! ## The target -/

/-- **C02 is proved.**

With `A = log f + log g`, `B = log f - log g`, `R := c02R a A B`, `S := c02S a A B`
and `E2 := (A_y - B_y) * R + S` the certificate is

* `cbil a f g = (f*g) * R` and `chx f g = (f*g) * B_x`,
* `2 * cbil a f (sy g) = (f*g) * (E2 - 4 B_x)`,
* `R = 0` and `E2 = 0` follow from `ContinuousPair`, hence `S = 0`,
* `c1 a (cu f g) (cv f g) = 2 ∂x∂y R` and `c2 a (cu f g) (cv f g) = 2 ∂x∂y R - 2 ∂x S`. -/
theorem c02_proved : C02 := by
  intro a f g hf hg hfp hgp hcont
  obtain ⟨hI, hII⟩ := c02_hyp_from_ContinuousPair a f g hf hg hcont
  set A : XYT := c02log f + c02log g with hAdef
  set B : XYT := c02log f - c02log g with hBdef
  have hA : Smooth3 A := by
    rw [hAdef]
    exact c02_smooth_add (c02_smooth_log hf hfp) (c02_smooth_log hg hgp)
  have hB : Smooth3 B := by
    rw [hBdef]
    exact c02_smooth_sub (c02_smooth_log hf hfp) (c02_smooth_log hg hgp)
  have hb1 : cbil a f g = (f * g) * c02R a A B := by
    rw [hAdef, hBdef]
    exact c02_cbil_eq a f g hf hg hfp hgp
  have hb2 : chx f g = (f * g) * sx B := by
    rw [hBdef]
    exact c02_chx_eq f g hf hg hfp hgp
  have hb3 : (2:ℝ) • cbil a f (sy g)
      = (f * g) * (c02E2 a A B - (4:ℝ) • sx B) := by
    rw [hAdef, hBdef]
    exact c02_cbil_syg_eq a f g hf hg hfp hgp
  have hR : c02R a A B = 0 := by
    funext x y t
    have hzero : (f * g) * c02R a A B = 0 := by rw [← hb1, hI]
    have hpt : (f x y t * g x y t) * c02R a A B x y t = 0 := by
      have hh := congrFun (congrFun (congrFun hzero x) y) t
      simpa [Pi.mul_apply] using hh
    rcases mul_eq_zero.mp hpt with h | h
    · exact absurd h (mul_ne_zero (ne_of_gt (hfp x y t)) (ne_of_gt (hgp x y t)))
    · exact h
  have hE2 : c02E2 a A B = 0 := by
    funext x y t
    have h1 : cbil a f (sy g) x y t + 2 * (chx f g x y t) = 0 := by
      have hh := congrFun (congrFun (congrFun hII x) y) t
      simpa using hh
    have h2 : chx f g x y t = (f x y t * g x y t) * sx B x y t := by
      have hh := congrFun (congrFun (congrFun hb2 x) y) t
      simpa [Pi.mul_apply] using hh
    have h3 : 2 * (cbil a f (sy g) x y t)
        = (f x y t * g x y t) * (c02E2 a A B x y t - 4 * (sx B x y t)) := by
      have hh := congrFun (congrFun (congrFun hb3 x) y) t
      simpa [Pi.mul_apply, Pi.sub_apply, Pi.smul_apply, smul_eq_mul] using hh
    have hpt : (f x y t * g x y t) * c02E2 a A B x y t = 0 := by
      nlinarith [h1, h2, h3]
    rcases mul_eq_zero.mp hpt with h | h
    · exact absurd h (mul_ne_zero (ne_of_gt (hfp x y t)) (ne_of_gt (hgp x y t)))
    · exact h
  have hS : c02S a A B = 0 := by
    have h := hE2
    rw [c02E2, hR] at h
    simpa using h
  have hcu : cu f g = (2:ℝ) • sx B := by
    rw [c02_cu_eq f g, hBdef]
  have hcv : cv f g = (2:ℝ) • sx (sy A) := by
    rw [c02_cv_eq f g, hAdef]
  refine ⟨?_, ?_⟩
  · rw [hcu, hcv, c02_c1_eq a A B hA hB, hR]
    simp
  · rw [hcu, hcv, c02_c2_eq a A B hA hB, hR, hS]
    simp