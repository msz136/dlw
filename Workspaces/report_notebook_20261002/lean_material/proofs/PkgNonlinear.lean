/-
Probe: calculus infrastructure for the C14/C15 package (development file, not a target).
-/
import Contracts
import Mathlib.Analysis.Calculus.ContDiff.Operations
import Mathlib.Analysis.Calculus.ContDiff.Deriv
import Mathlib.Analysis.Calculus.ContDiff.Comp
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Analysis.Calculus.Deriv.Inv
import Mathlib.Analysis.Calculus.FDeriv.Symmetric
import Mathlib.Analysis.Calculus.FDeriv.Linear
import Mathlib.Analysis.Calculus.ContDiff.FTaylorSeries
import Mathlib.Analysis.Normed.Operator.Bilinear
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Tactic

noncomputable section
open scoped BigOperators
namespace DLWContract

/-! ## calculus helpers -/

private lemma diffAt_of_contDiff {E G : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    [NormedAddCommGroup G] [NormedSpace ℝ G] {f : E → G} (h : ContDiff ℝ ⊤ f) (x : E) :
    DifferentiableAt ℝ f x :=
  ((h.of_le le_top).differentiable_one).differentiableAt

private lemma slice_cont {f : XT} (hf : SmoothXT f) (t : ℝ) :
    ContDiff ℝ ⊤ (fun x : ℝ => f x t) :=
  hf.comp (contDiff_prodMk_left (f₀ := t))

private lemma slice_cont_t {f : XT} (hf : SmoothXT f) (x : ℝ) :
    ContDiff ℝ ⊤ (fun t : ℝ => f x t) :=
  hf.comp (contDiff_prodMk_right (e₀ := x))

/-- chain rule for the first slice, all arguments explicit. -/
private lemma hasDerivAt_slice_x {G : Type*} [NormedAddCommGroup G] [NormedSpace ℝ G]
    {F : ℝ × ℝ → G} {a b : ℝ}
    (hFd : HasFDerivAt F (fderiv ℝ F (a, b)) (a, b)) :
    HasDerivAt (fun z : ℝ => F (z, b)) ((fderiv ℝ F (a, b)) (1, 0)) a :=
  HasFDerivAt.comp_hasDerivAt (f := fun z : ℝ => (z, b)) (f' := ((1 : ℝ), (0 : ℝ)))
    (x := a) (hl := hFd)
    (hf := (hasDerivAt_id' (x := a)).prodMk (hasDerivAt_const (c := b) (x := a)))

/-- chain rule for the second slice, all arguments explicit. -/
private lemma hasDerivAt_slice_t {G : Type*} [NormedAddCommGroup G] [NormedSpace ℝ G]
    {F : ℝ × ℝ → G} {a b : ℝ}
    (hFd : HasFDerivAt F (fderiv ℝ F (a, b)) (a, b)) :
    HasDerivAt (fun s : ℝ => F (a, s)) ((fderiv ℝ F (a, b)) (0, 1)) b :=
  HasFDerivAt.comp_hasDerivAt (f := fun s : ℝ => (a, s)) (f' := ((0 : ℝ), (1 : ℝ)))
    (x := b) (hl := hFd)
    (hf := (hasDerivAt_const (c := a) (x := b)).prodMk (hasDerivAt_id' (x := b)))

/-- chain rule with the continuous linear map "evaluate at `v`". -/
private lemma hasDerivAt_apply_clm {G : ℝ → (ℝ × ℝ →L[ℝ] ℝ)} {a : ℝ} {g' : ℝ × ℝ →L[ℝ] ℝ}
    (h : HasDerivAt G g' a) (v : ℝ × ℝ) : HasDerivAt (fun z : ℝ => G z v) (g' v) a :=
  HasFDerivAt.comp_hasDerivAt (f := G) (f' := g') (x := a)
    (hl := (ContinuousLinearMap.apply ℝ ℝ v).hasFDerivAt) (hf := h)

/-- `x`-derivative of a smooth two-variable function as a Fréchet derivative. -/
private lemma deriv_slice_eq {F : ℝ × ℝ → ℝ} (hF : ContDiff ℝ ⊤ F) (a b : ℝ) :
    deriv (fun z : ℝ => F (z, b)) a = (fderiv ℝ F (a, b)) (1, 0) :=
  (hasDerivAt_slice_x ((diffAt_of_contDiff hF (a, b)).hasFDerivAt)).deriv

/-- `t`-derivative of a smooth two-variable function as a Fréchet derivative. -/
private lemma deriv_slice_eq' {F : ℝ × ℝ → ℝ} (hF : ContDiff ℝ ⊤ F) (a b : ℝ) :
    deriv (fun s : ℝ => F (a, s)) b = (fderiv ℝ F (a, b)) (0, 1) :=
  (hasDerivAt_slice_t ((diffAt_of_contDiff hF (a, b)).hasFDerivAt)).deriv

/-- The `x`-partial derivative of a smooth function is smooth. -/
private lemma smoothXT_dx {f : XT} (hf : SmoothXT f) : SmoothXT (dx f) := by
  have hfun : (fun p : ℝ × ℝ => dx f p.1 p.2)
      = fun p : ℝ × ℝ => (fderiv ℝ (fun q : ℝ × ℝ => f q.1 q.2) p) (1, 0) := by
    funext p
    obtain ⟨a, b⟩ := p
    simpa only [dx] using deriv_slice_eq hf a b
  have hsm : ContDiff ℝ ⊤
      (fun p : ℝ × ℝ => (fderiv ℝ (fun q : ℝ × ℝ => f q.1 q.2) p) (1, 0)) := by
    have h1 : ContDiff ℝ ⊤ (fun q : (ℝ × ℝ) × (ℝ × ℝ) =>
        (fderiv ℝ (fun r : ℝ × ℝ => f r.1 r.2) q.1) q.2) :=
      hf.contDiff_fderiv_apply (m := ⊤) le_top
    have h2 : ContDiff ℝ ⊤ (fun p : ℝ × ℝ => (p, ((1 : ℝ), (0 : ℝ)))) :=
      contDiff_prodMk_left ((1 : ℝ), (0 : ℝ))
    simpa only [Function.comp_def] using h1.comp h2
  show ContDiff ℝ ⊤ (fun p : ℝ × ℝ => dx f p.1 p.2)
  rw [hfun]
  exact hsm

/-- The `t`-partial derivative of a smooth function is smooth. -/
private lemma smoothXT_dt {f : XT} (hf : SmoothXT f) : SmoothXT (dt f) := by
  have hfun : (fun p : ℝ × ℝ => dt f p.1 p.2)
      = fun p : ℝ × ℝ => (fderiv ℝ (fun q : ℝ × ℝ => f q.1 q.2) p) (0, 1) := by
    funext p
    obtain ⟨a, b⟩ := p
    simpa only [dt] using deriv_slice_eq' hf a b
  have hsm : ContDiff ℝ ⊤
      (fun p : ℝ × ℝ => (fderiv ℝ (fun q : ℝ × ℝ => f q.1 q.2) p) (0, 1)) := by
    have h1 : ContDiff ℝ ⊤ (fun q : (ℝ × ℝ) × (ℝ × ℝ) =>
        (fderiv ℝ (fun r : ℝ × ℝ => f r.1 r.2) q.1) q.2) :=
      hf.contDiff_fderiv_apply (m := ⊤) le_top
    have h2 : ContDiff ℝ ⊤ (fun p : ℝ × ℝ => (p, ((0 : ℝ), (1 : ℝ)))) :=
      contDiff_prodMk_left ((0 : ℝ), (1 : ℝ))
    simpa only [Function.comp_def] using h1.comp h2
  show ContDiff ℝ ⊤ (fun p : ℝ × ℝ => dt f p.1 p.2)
  rw [hfun]
  exact hsm

/-! ## a smoothness predicate on lattices -/

private def Sm (z : Lattice) : Prop := ∀ j, SmoothXT (z j)

private lemma dAtx {z : Lattice} (hz : Sm z) (j : ℤ) (t x : ℝ) :
    DifferentiableAt ℝ (fun x' : ℝ => z j x' t) x :=
  diffAt_of_contDiff (slice_cont (hz j) t) x

private lemma dAtt {z : Lattice} (hz : Sm z) (j : ℤ) (x t : ℝ) :
    DifferentiableAt ℝ (fun t' : ℝ => z j x t') t :=
  diffAt_of_contDiff (slice_cont_t (hz j) x) t

private lemma Sm_add {z w : Lattice} (hz : Sm z) (hw : Sm w) : Sm (z + w) := by
  intro j
  show ContDiff ℝ ⊤ (fun y : ℝ × ℝ => (z + w) j y.1 y.2)
  simpa only [Pi.add_apply] using (hz j).add (hw j)

private lemma Sm_sub {z w : Lattice} (hz : Sm z) (hw : Sm w) : Sm (z - w) := by
  intro j
  show ContDiff ℝ ⊤ (fun y : ℝ × ℝ => (z - w) j y.1 y.2)
  simpa only [Pi.sub_apply] using (hz j).sub (hw j)

private lemma Sm_mul {z w : Lattice} (hz : Sm z) (hw : Sm w) : Sm (z * w) := by
  intro j
  show ContDiff ℝ ⊤ (fun y : ℝ × ℝ => (z * w) j y.1 y.2)
  simpa only [Pi.mul_apply] using (hz j).mul (hw j)

private lemma Sm_pow {z : Lattice} (hz : Sm z) (n : ℕ) : Sm (z ^ n) := by
  intro j
  show ContDiff ℝ ⊤ (fun y : ℝ × ℝ => (z ^ n) j y.1 y.2)
  simpa only [Pi.pow_apply] using (hz j).pow n

private lemma Sm_smul (c : ℝ) {z : Lattice} (hz : Sm z) : Sm (c • z) := by
  intro j
  show ContDiff ℝ ⊤ (fun y : ℝ × ℝ => (c • z) j y.1 y.2)
  simpa only [Pi.smul_apply, smul_eq_mul] using ContDiff.const_smul c (hz j)

private lemma Sm_const (c : ℝ) : Sm (fun _ _ _ => c) := fun _ => contDiff_const

private lemma Sm_lx {z : Lattice} (hz : Sm z) : Sm (lx z) := fun j => smoothXT_dx (hz j)

private lemma Sm_lt {z : Lattice} (hz : Sm z) : Sm (lt z) := fun j => smoothXT_dt (hz j)

private lemma Sm_lxx {z : Lattice} (hz : Sm z) : Sm (lxx z) := Sm_lx (Sm_lx hz)

private lemma Sm_dm (h : ℝ) {z : Lattice} (hz : Sm z) : Sm (dm h z) := by
  intro j
  show ContDiff ℝ ⊤ (fun y : ℝ × ℝ => dm h z j y.1 y.2)
  simpa only [dm, Pi.sub_apply, Pi.smul_apply, smul_eq_mul] using
    ContDiff.const_smul (1 / h) ((hz j).sub (hz (j - 1)))

private lemma Sm_d0 (h : ℝ) {z : Lattice} (hz : Sm z) : Sm (d0 h z) := by
  intro j
  show ContDiff ℝ ⊤ (fun y : ℝ × ℝ => d0 h z j y.1 y.2)
  simpa only [d0, Pi.sub_apply, Pi.smul_apply, smul_eq_mul] using
    ContDiff.const_smul (1 / (2 * h)) ((hz (j + 1)).sub (hz (j - 1)))

private lemma Sm_mm {z : Lattice} (hz : Sm z) : Sm (mm z) := by
  intro j
  show ContDiff ℝ ⊤ (fun y : ℝ × ℝ => mm z j y.1 y.2)
  simpa only [mm, Pi.add_apply, Pi.div_apply, Pi.ofNat_apply] using
    ((hz j).add (hz (j - 1))).div_const 2

private lemma Sm_two_mul {z : Lattice} (hz : Sm z) : Sm (2 * z) := by
  intro j
  show ContDiff ℝ ⊤ (fun y : ℝ × ℝ => (2 * z) j y.1 y.2)
  simpa only [Pi.mul_apply, Pi.ofNat_apply] using
    (contDiff_const (c := (2 : ℝ))).mul (hz j)

private lemma Sm_lap (h : ℝ) {z : Lattice} (hz : Sm z) : Sm (lap h z) := by
  intro j
  have h2 : ContDiff ℝ ⊤ (fun y : ℝ × ℝ => (2 : ℝ) * z j y.1 y.2) :=
    (contDiff_const (c := (2 : ℝ))).mul (hz j)
  have h3 : ContDiff ℝ ⊤ (fun y : ℝ × ℝ =>
      z (j + 1) y.1 y.2 - 2 * z j y.1 y.2 + z (j - 1) y.1 y.2) :=
    ((hz (j + 1)).sub h2).add (hz (j - 1))
  have h4 : ContDiff ℝ ⊤ (fun y : ℝ × ℝ => (1 / h ^ 2) •
      (z (j + 1) y.1 y.2 - 2 * z j y.1 y.2 + z (j - 1) y.1 y.2)) :=
    ContDiff.const_smul (1 / h ^ 2) h3
  show ContDiff ℝ ⊤ (fun y : ℝ × ℝ => lap h z j y.1 y.2)
  simpa only [lap, Pi.add_apply, Pi.sub_apply, Pi.mul_apply, Pi.smul_apply, Pi.ofNat_apply,
    smul_eq_mul] using h4

macro "sm" : tactic => `(tactic| repeat (first
  | assumption
  | apply Sm_add
  | apply Sm_sub
  | apply Sm_mul
  | apply Sm_pow
  | apply Sm_smul
  | apply Sm_lx
  | apply Sm_lt
  | apply Sm_lxx
  | apply Sm_dm
  | apply Sm_d0
  | apply Sm_mm
  | apply Sm_lap
  | exact Sm_const _))

/-! ## linearity of the site operators (pointwise algebra) -/

private lemma dm_add (h : ℝ) (z w : Lattice) : dm h (z + w) = dm h z + dm h w := by
  funext j x t
  simp only [dm, Pi.add_apply, Pi.sub_apply, Pi.smul_apply, smul_eq_mul]
  ring

private lemma dm_sub (h : ℝ) (z w : Lattice) : dm h (z - w) = dm h z - dm h w := by
  funext j x t
  simp only [dm, Pi.sub_apply, Pi.smul_apply, smul_eq_mul]
  ring

private lemma dm_smul (h c : ℝ) (z : Lattice) : dm h (c • z) = c • dm h z := by
  funext j x t
  simp only [dm, Pi.sub_apply, Pi.smul_apply, smul_eq_mul]
  ring

private lemma d0_add (h : ℝ) (z w : Lattice) : d0 h (z + w) = d0 h z + d0 h w := by
  funext j x t
  simp only [d0, Pi.add_apply, Pi.sub_apply, Pi.smul_apply, smul_eq_mul]
  ring

private lemma d0_sub (h : ℝ) (z w : Lattice) : d0 h (z - w) = d0 h z - d0 h w := by
  funext j x t
  simp only [d0, Pi.sub_apply, Pi.smul_apply, smul_eq_mul]
  ring

private lemma d0_smul (h c : ℝ) (z : Lattice) : d0 h (c • z) = c • d0 h z := by
  funext j x t
  simp only [d0, Pi.sub_apply, Pi.smul_apply, smul_eq_mul]
  ring

private lemma mm_add (z w : Lattice) : mm (z + w) = mm z + mm w := by
  funext j x t
  simp only [mm, Pi.add_apply, Pi.div_apply, Pi.ofNat_apply]
  ring

private lemma mm_sub (z w : Lattice) : mm (z - w) = mm z - mm w := by
  funext j x t
  simp only [mm, Pi.add_apply, Pi.sub_apply, Pi.div_apply, Pi.ofNat_apply]
  ring

private lemma mm_smul (c : ℝ) (z : Lattice) : mm (c • z) = c • mm z := by
  funext j x t
  simp only [mm, Pi.add_apply, Pi.div_apply, Pi.smul_apply, Pi.ofNat_apply, smul_eq_mul]
  ring

private lemma lap_add (h : ℝ) (z w : Lattice) : lap h (z + w) = lap h z + lap h w := by
  funext j x t
  simp only [lap, Pi.add_apply, Pi.sub_apply, Pi.mul_apply, Pi.smul_apply, Pi.ofNat_apply,
    smul_eq_mul]
  ring

private lemma lap_sub (h : ℝ) (z w : Lattice) : lap h (z - w) = lap h z - lap h w := by
  funext j x t
  simp only [lap, Pi.add_apply, Pi.sub_apply, Pi.mul_apply, Pi.smul_apply, Pi.ofNat_apply,
    smul_eq_mul]
  ring

private lemma lap_smul (h c : ℝ) (z : Lattice) : lap h (c • z) = c • lap h z := by
  funext j x t
  simp only [lap, Pi.add_apply, Pi.sub_apply, Pi.mul_apply, Pi.smul_apply, Pi.ofNat_apply,
    smul_eq_mul]
  ring

/-! ## linearity of `lx` and `lt` -/

private lemma lx_const (c : ℝ) : lx (fun _ _ _ => c) = 0 := by
  funext j x t
  show deriv (fun _ : ℝ => c) x = 0
  simp

private lemma lx_add {z w : Lattice} (hz : Sm z) (hw : Sm w) : lx (z + w) = lx z + lx w := by
  funext j x t
  have hfun : (fun x' : ℝ => z j x' t + w j x' t)
      = (fun x' : ℝ => z j x' t) + (fun x' : ℝ => w j x' t) := by
    funext x'
    simp only [Pi.add_apply]
  simp only [lx, dx, Pi.add_apply]
  rw [hfun, deriv_add (dAtx hz j t x) (dAtx hw j t x)]

private lemma lx_sub {z w : Lattice} (hz : Sm z) (hw : Sm w) : lx (z - w) = lx z - lx w := by
  funext j x t
  have hfun : (fun x' : ℝ => z j x' t - w j x' t)
      = (fun x' : ℝ => z j x' t) - (fun x' : ℝ => w j x' t) := by
    funext x'
    simp only [Pi.sub_apply]
  simp only [lx, dx, Pi.sub_apply]
  rw [hfun, deriv_sub (dAtx hz j t x) (dAtx hw j t x)]

private lemma lx_smul (c : ℝ) {z : Lattice} (hz : Sm z) : lx (c • z) = c • lx z := by
  funext j x t
  have hfun : (fun x' : ℝ => c * z j x' t)
      = fun x' : ℝ => c * (fun x' : ℝ => z j x' t) x' := by
    funext x'
    rfl
  simp only [lx, dx, Pi.smul_apply, smul_eq_mul]
  rw [hfun, deriv_const_mul c (dAtx hz j t x)]

private lemma lx_mul {z w : Lattice} (hz : Sm z) (hw : Sm w) :
    lx (z * w) = lx z * w + z * lx w := by
  funext j x t
  have hfun : (fun x' : ℝ => z j x' t * w j x' t)
      = (fun x' : ℝ => z j x' t) * (fun x' : ℝ => w j x' t) := by
    funext x'
    simp only [Pi.mul_apply]
  simp only [lx, dx, Pi.add_apply, Pi.mul_apply]
  rw [hfun, deriv_mul (dAtx hz j t x) (dAtx hw j t x)]

private lemma lx_sq {z : Lattice} (hz : Sm z) : lx (z ^ 2) = (2 : ℝ) • (z * lx z) := by
  funext j x t
  have hfun : (fun x' : ℝ => z j x' t ^ 2) = (fun x' : ℝ => z j x' t) ^ 2 := by
    funext x'
    simp only [Pi.pow_apply]
  simp only [lx, dx, Pi.mul_apply, Pi.pow_apply, Pi.smul_apply, smul_eq_mul]
  rw [hfun, deriv_pow (dAtx hz j t x) 2]
  ring

private lemma lt_add {z w : Lattice} (hz : Sm z) (hw : Sm w) : lt (z + w) = lt z + lt w := by
  funext j x t
  simp only [lt, dt, Pi.add_apply]
  rw [deriv_add (dAtt hz j x t) (dAtt hw j x t)]

private lemma lt_sub {z w : Lattice} (hz : Sm z) (hw : Sm w) : lt (z - w) = lt z - lt w := by
  funext j x t
  simp only [lt, dt, Pi.sub_apply]
  rw [deriv_sub (dAtt hz j x t) (dAtt hw j x t)]

private lemma lt_smul (c : ℝ) {z : Lattice} (hz : Sm z) : lt (c • z) = c • lt z := by
  funext j x t
  have hfun : (c • (z j x) : ℝ → ℝ) = fun t' : ℝ => c * z j x t' := by
    funext t'
    simp only [Pi.smul_apply, smul_eq_mul]
  simp only [lt, dt, Pi.smul_apply, smul_eq_mul]
  rw [hfun, deriv_const_mul c (dAtt hz j x t)]

/-! ## shifts -/

private lemma lx_shift_p (z : Lattice) : lx (fun j => z (j + 1)) = fun j => lx z (j + 1) := by
  funext j x t
  rfl

private lemma lx_shift_m (z : Lattice) : lx (fun j => z (j - 1)) = fun j => lx z (j - 1) := by
  funext j x t
  rfl

private lemma lt_shift_p (z : Lattice) : lt (fun j => z (j + 1)) = fun j => lt z (j + 1) := by
  funext j x t
  rfl

private lemma lt_shift_m (z : Lattice) : lt (fun j => z (j - 1)) = fun j => lt z (j - 1) := by
  funext j x t
  rfl

/-! ## definitional normal forms of the site operators -/

private lemma dm_eq (h : ℝ) (z : Lattice) : dm h z = (1 / h) • (z - fun j => z (j - 1)) := by
  funext j x t
  simp only [dm, Pi.sub_apply, Pi.smul_apply, smul_eq_mul]

private lemma d0_eq (h : ℝ) (z : Lattice) :
    d0 h z = (1 / (2 * h)) • ((fun j => z (j + 1)) - fun j => z (j - 1)) := by
  funext j x t
  simp only [d0, Pi.sub_apply, Pi.smul_apply, smul_eq_mul]

private lemma mm_eq (z : Lattice) : mm z = (z + fun j => z (j - 1)) / 2 := by
  funext j x t
  simp only [mm, Pi.add_apply, Pi.div_apply, Pi.ofNat_apply]

private lemma lap_eq (h : ℝ) (z : Lattice) :
    lap h z = (1 / h ^ 2) • ((fun j => z (j + 1)) - (2 : ℝ) • z + fun j => z (j - 1)) := by
  funext j x t
  simp only [lap, Pi.add_apply, Pi.sub_apply, Pi.mul_apply, Pi.smul_apply, Pi.ofNat_apply,
    smul_eq_mul]

private lemma div_two_eq (z : Lattice) : z / 2 = (1 / 2 : ℝ) • z := by
  funext j x t
  simp only [Pi.div_apply, Pi.ofNat_apply, Pi.smul_apply, smul_eq_mul]
  ring

/-! ## commutation of `lx` and `lt` with the site operators -/

private lemma lx_dm (h : ℝ) {z : Lattice} (hz : Sm z) : lx (dm h z) = dm h (lx z) := by
  have hm : Sm (fun j => z (j - 1)) := fun j => hz (j - 1)
  rw [dm_eq, dm_eq, lx_smul (1 / h) (Sm_sub hz hm), lx_sub hz hm, lx_shift_m]

private lemma lx_d0 (h : ℝ) {z : Lattice} (hz : Sm z) : lx (d0 h z) = d0 h (lx z) := by
  have hp : Sm (fun j => z (j + 1)) := fun j => hz (j + 1)
  have hm : Sm (fun j => z (j - 1)) := fun j => hz (j - 1)
  rw [d0_eq, d0_eq, lx_smul (1 / (2 * h)) (Sm_sub hp hm), lx_sub hp hm, lx_shift_p, lx_shift_m]

private lemma lx_mm {z : Lattice} (hz : Sm z) : lx (mm z) = mm (lx z) := by
  have hm : Sm (fun j => z (j - 1)) := fun j => hz (j - 1)
  rw [mm_eq, mm_eq, div_two_eq, div_two_eq, lx_smul (1 / 2) (Sm_add hz hm), lx_add hz hm,
    lx_shift_m]

private lemma lx_lap (h : ℝ) {z : Lattice} (hz : Sm z) : lx (lap h z) = lap h (lx z) := by
  have hp : Sm (fun j => z (j + 1)) := fun j => hz (j + 1)
  have hm : Sm (fun j => z (j - 1)) := fun j => hz (j - 1)
  have h2 : Sm ((fun j => z (j + 1)) - (2 : ℝ) • z + fun j => z (j - 1)) :=
    Sm_add (Sm_sub hp (Sm_smul 2 hz)) hm
  rw [lap_eq, lap_eq, lx_smul (1 / h ^ 2) h2, lx_add (Sm_sub hp (Sm_smul 2 hz)) hm,
    lx_sub hp (Sm_smul 2 hz), lx_smul 2 hz, lx_shift_p, lx_shift_m]

private lemma lt_dm (h : ℝ) {z : Lattice} (hz : Sm z) : lt (dm h z) = dm h (lt z) := by
  have hm : Sm (fun j => z (j - 1)) := fun j => hz (j - 1)
  rw [dm_eq, dm_eq, lt_smul (1 / h) (Sm_sub hz hm), lt_sub hz hm, lt_shift_m]

private lemma lt_d0 (h : ℝ) {z : Lattice} (hz : Sm z) : lt (d0 h z) = d0 h (lt z) := by
  have hp : Sm (fun j => z (j + 1)) := fun j => hz (j + 1)
  have hm : Sm (fun j => z (j - 1)) := fun j => hz (j - 1)
  rw [d0_eq, d0_eq, lt_smul (1 / (2 * h)) (Sm_sub hp hm), lt_sub hp hm, lt_shift_p, lt_shift_m]

private lemma lt_mm {z : Lattice} (hz : Sm z) : lt (mm z) = mm (lt z) := by
  have hm : Sm (fun j => z (j - 1)) := fun j => hz (j - 1)
  rw [mm_eq, mm_eq, div_two_eq, div_two_eq, lt_smul (1 / 2) (Sm_add hz hm), lt_add hz hm,
    lt_shift_m]

private lemma lt_lap (h : ℝ) {z : Lattice} (hz : Sm z) : lt (lap h z) = lap h (lt z) := by
  have hp : Sm (fun j => z (j + 1)) := fun j => hz (j + 1)
  have hm : Sm (fun j => z (j - 1)) := fun j => hz (j - 1)
  have h2 : Sm ((fun j => z (j + 1)) - (2 : ℝ) • z + fun j => z (j - 1)) :=
    Sm_add (Sm_sub hp (Sm_smul 2 hz)) hm
  rw [lap_eq, lap_eq, lt_smul (1 / h ^ 2) h2, lt_add (Sm_sub hp (Sm_smul 2 hz)) hm,
    lt_sub hp (Sm_smul 2 hz), lt_smul 2 hz, lt_shift_p, lt_shift_m]

/-! ## Clairaut: mixed partial derivatives commute -/

private lemma lt_lx {z : Lattice} (hz : Sm z) : lt (lx z) = lx (lt z) := by
  funext j x t
  set F : ℝ × ℝ → ℝ := fun p => z j p.1 p.2 with hF
  have hFd : ContDiff ℝ ⊤ F := by rw [hF]; exact hz j
  have hsymm : IsSymmSndFDerivAt ℝ F (x, t) := hFd.contDiffAt.isSymmSndFDerivAt le_top
  have hfd : HasFDerivAt (fun p : ℝ × ℝ => fderiv ℝ F p)
      (fderiv ℝ (fun p : ℝ × ℝ => fderiv ℝ F p) (x, t)) (x, t) :=
    (diffAt_of_contDiff (hFd.fderiv_right (m := ⊤) le_top) (x, t)).hasFDerivAt
  have h1 : HasDerivAt (fun z' : ℝ => fderiv ℝ F (z', t))
      ((fderiv ℝ (fun p : ℝ × ℝ => fderiv ℝ F p) (x, t)) (1, 0)) x :=
    hasDerivAt_slice_x (F := fun p : ℝ × ℝ => fderiv ℝ F p) (a := x) (b := t) hfd
  have hA : deriv (fun z' : ℝ => (fderiv ℝ F (z', t)) (0, 1)) x
      = (fderiv ℝ (fun p : ℝ × ℝ => fderiv ℝ F p) (x, t) (1, 0)) (0, 1) :=
    (hasDerivAt_apply_clm h1 ((0 : ℝ), (1 : ℝ))).deriv
  have h2 : HasDerivAt (fun s : ℝ => fderiv ℝ F (x, s))
      ((fderiv ℝ (fun p : ℝ × ℝ => fderiv ℝ F p) (x, t)) (0, 1)) t :=
    hasDerivAt_slice_t (F := fun p : ℝ × ℝ => fderiv ℝ F p) (a := x) (b := t) hfd
  have hB : deriv (fun s : ℝ => (fderiv ℝ F (x, s)) (1, 0)) t
      = (fderiv ℝ (fun p : ℝ × ℝ => fderiv ℝ F p) (x, t) (0, 1)) (1, 0) :=
    (hasDerivAt_apply_clm h2 ((1 : ℝ), (0 : ℝ))).deriv
  have hsym : (fderiv ℝ (fun p : ℝ × ℝ => fderiv ℝ F p) (x, t) (1, 0)) (0, 1)
      = (fderiv ℝ (fun p : ℝ × ℝ => fderiv ℝ F p) (x, t) (0, 1)) (1, 0) :=
    hsymm.eq ((1 : ℝ), (0 : ℝ)) ((0 : ℝ), (1 : ℝ))
  have hLHS : lt (lx z) j x t
      = (fderiv ℝ (fun p : ℝ × ℝ => fderiv ℝ F p) (x, t) (0, 1)) (1, 0) := by
    have hfun : (fun s : ℝ => deriv (fun x' : ℝ => z j x' s) x)
        = (fun s : ℝ => (fderiv ℝ F (x, s)) (1, 0)) := by
      funext s
      simpa only [hF] using deriv_slice_eq hFd x s
    show deriv (fun s : ℝ => deriv (fun x' : ℝ => z j x' s) x) t = _
    rw [hfun, hB]
  have hRHS : lx (lt z) j x t
      = (fderiv ℝ (fun p : ℝ × ℝ => fderiv ℝ F p) (x, t) (1, 0)) (0, 1) := by
    have hfun : (fun x' : ℝ => deriv (fun t' : ℝ => z j x' t') t)
        = (fun x' : ℝ => (fderiv ℝ F (x', t)) (0, 1)) := by
      funext x'
      simpa only [hF] using deriv_slice_eq' hFd x' t
    show deriv (fun x' : ℝ => deriv (fun t' : ℝ => z j x' t') t) x = _
    rw [hfun, hA]
  rw [hLHS, hRHS, hsym]

/-! ## `XT`-level linearity of `dx`, `dt`, `xx` -/

private lemma dx_add {z w : XT} (hz : SmoothXT z) (hw : SmoothXT w) :
    dx (z + w) = dx z + dx w := by
  funext x t
  have h1 : DifferentiableAt ℝ (fun x' : ℝ => z x' t) x :=
    diffAt_of_contDiff (slice_cont hz t) x
  have h2 : DifferentiableAt ℝ (fun x' : ℝ => w x' t) x :=
    diffAt_of_contDiff (slice_cont hw t) x
  have hf : (fun x' : ℝ => (z + w) x' t)
      = ((fun x' : ℝ => z x' t) + fun x' : ℝ => w x' t) := by
    funext x'
    simp only [Pi.add_apply]
  show deriv (fun x' : ℝ => (z + w) x' t) x
      = deriv (fun x' : ℝ => z x' t) x + deriv (fun x' : ℝ => w x' t) x
  rw [hf]
  exact deriv_add h1 h2

private lemma dx_sub {z w : XT} (hz : SmoothXT z) (hw : SmoothXT w) :
    dx (z - w) = dx z - dx w := by
  funext x t
  have h1 : DifferentiableAt ℝ (fun x' : ℝ => z x' t) x :=
    diffAt_of_contDiff (slice_cont hz t) x
  have h2 : DifferentiableAt ℝ (fun x' : ℝ => w x' t) x :=
    diffAt_of_contDiff (slice_cont hw t) x
  have hf : (fun x' : ℝ => (z - w) x' t)
      = ((fun x' : ℝ => z x' t) - fun x' : ℝ => w x' t) := by
    funext x'
    simp only [Pi.sub_apply]
  show deriv (fun x' : ℝ => (z - w) x' t) x
      = deriv (fun x' : ℝ => z x' t) x - deriv (fun x' : ℝ => w x' t) x
  rw [hf]
  exact deriv_sub h1 h2

private lemma dx_smul (c : ℝ) {z : XT} (hz : SmoothXT z) : dx (c • z) = c • dx z := by
  funext x t
  have h1 : DifferentiableAt ℝ (fun x' : ℝ => z x' t) x :=
    diffAt_of_contDiff (slice_cont hz t) x
  have hf : (fun x' : ℝ => (c • z) x' t)
      = fun x' : ℝ => c * (fun x' : ℝ => z x' t) x' := by
    funext x'
    simp only [Pi.smul_apply, smul_eq_mul]
  show deriv (fun x' : ℝ => (c • z) x' t) x = c * deriv (fun x' : ℝ => z x' t) x
  rw [hf]
  exact deriv_const_mul c h1

private lemma dt_add {z w : XT} (hz : SmoothXT z) (hw : SmoothXT w) :
    dt (z + w) = dt z + dt w := by
  funext x t
  have h1 : DifferentiableAt ℝ (fun t' : ℝ => z x t') t :=
    diffAt_of_contDiff (slice_cont_t hz x) t
  have h2 : DifferentiableAt ℝ (fun t' : ℝ => w x t') t :=
    diffAt_of_contDiff (slice_cont_t hw x) t
  have hf : ((z + w) x) = ((z x) + fun t' : ℝ => w x t') := by
    funext t'
    simp only [Pi.add_apply]
  show deriv ((z + w) x) t = deriv (z x) t + deriv (w x) t
  rw [hf]
  exact deriv_add h1 h2

private lemma dt_sub {z w : XT} (hz : SmoothXT z) (hw : SmoothXT w) :
    dt (z - w) = dt z - dt w := by
  funext x t
  have h1 : DifferentiableAt ℝ (fun t' : ℝ => z x t') t :=
    diffAt_of_contDiff (slice_cont_t hz x) t
  have h2 : DifferentiableAt ℝ (fun t' : ℝ => w x t') t :=
    diffAt_of_contDiff (slice_cont_t hw x) t
  have hf : ((z - w) x) = ((z x) - fun t' : ℝ => w x t') := by
    funext t'
    simp only [Pi.sub_apply]
  show deriv ((z - w) x) t = deriv (z x) t - deriv (w x) t
  rw [hf]
  exact deriv_sub h1 h2

private lemma dt_smul (c : ℝ) {z : XT} (hz : SmoothXT z) : dt (c • z) = c • dt z := by
  funext x t
  have h1 : DifferentiableAt ℝ (fun t' : ℝ => z x t') t :=
    diffAt_of_contDiff (slice_cont_t hz x) t
  have hf : ((c • z) x) = fun t' : ℝ => c * (fun t' : ℝ => z x t') t' := by
    funext t'
    simp only [Pi.smul_apply, smul_eq_mul]
  show deriv ((c • z) x) t = c * deriv (z x) t
  rw [hf]
  exact deriv_const_mul c h1

private lemma xx_add {z w : XT} (hz : SmoothXT z) (hw : SmoothXT w) :
    xx (z + w) = xx z + xx w := by
  show dx (dx (z + w)) = dx (dx z) + dx (dx w)
  rw [dx_add hz hw, dx_add (smoothXT_dx hz) (smoothXT_dx hw)]

private lemma xx_sub {z w : XT} (hz : SmoothXT z) (hw : SmoothXT w) :
    xx (z - w) = xx z - xx w := by
  show dx (dx (z - w)) = dx (dx z) - dx (dx w)
  rw [dx_sub hz hw, dx_sub (smoothXT_dx hz) (smoothXT_dx hw)]

private lemma xx_smul (c : ℝ) {z : XT} (hz : SmoothXT z) : xx (c • z) = c • xx z := by
  show dx (dx (c • z)) = c • dx (dx z)
  rw [dx_smul c hz, dx_smul c (smoothXT_dx hz)]

/-! ## `lxx`: linearity and commutation with the site operators -/

private lemma lxx_add {z w : Lattice} (hz : Sm z) (hw : Sm w) : lxx (z + w) = lxx z + lxx w := by
  show lx (lx (z + w)) = lx (lx z) + lx (lx w)
  rw [lx_add hz hw, lx_add (Sm_lx hz) (Sm_lx hw)]

private lemma lxx_sub {z w : Lattice} (hz : Sm z) (hw : Sm w) : lxx (z - w) = lxx z - lxx w := by
  show lx (lx (z - w)) = lx (lx z) - lx (lx w)
  rw [lx_sub hz hw, lx_sub (Sm_lx hz) (Sm_lx hw)]

private lemma lxx_smul (c : ℝ) {z : Lattice} (hz : Sm z) : lxx (c • z) = c • lxx z := by
  show lx (lx (c • z)) = c • lx (lx z)
  rw [lx_smul c hz, lx_smul c (Sm_lx hz)]

private lemma lxx_dm (h : ℝ) {z : Lattice} (hz : Sm z) : lxx (dm h z) = dm h (lxx z) := by
  show lx (lx (dm h z)) = dm h (lx (lx z))
  rw [lx_dm h hz, lx_dm h (Sm_lx hz)]

private lemma lxx_d0 (h : ℝ) {z : Lattice} (hz : Sm z) : lxx (d0 h z) = d0 h (lxx z) := by
  show lx (lx (d0 h z)) = d0 h (lx (lx z))
  rw [lx_d0 h hz, lx_d0 h (Sm_lx hz)]

private lemma lxx_mm {z : Lattice} (hz : Sm z) : lxx (mm z) = mm (lxx z) := by
  show lx (lx (mm z)) = mm (lx (lx z))
  rw [lx_mm hz, lx_mm (Sm_lx hz)]

private lemma lxx_lap (h : ℝ) {z : Lattice} (hz : Sm z) : lxx (lap h z) = lap h (lxx z) := by
  show lx (lx (lap h z)) = lap h (lx (lx z))
  rw [lx_lap h hz, lx_lap h (Sm_lx hz)]

private lemma lxx_lx (z : Lattice) : lxx (lx z) = lx (lxx z) := rfl

private lemma lxx_shift_p (z : Lattice) : lxx (fun j => z (j + 1)) = fun j => lxx z (j + 1) := by
  funext j x t
  rfl

private lemma lxx_shift_m (z : Lattice) : lxx (fun j => z (j - 1)) = fun j => lxx z (j - 1) := by
  funext j x t
  rfl

/-! ## two abstract linear lattice identities in third `x`-derivatives -/

private lemma d3_ident4 (h : ℝ) (hne : h ≠ 0) (A B : Lattice) :
    mm ((4 / h) • ((fun j => B (j + 1)) - B) + d0 h ((2 : ℝ) • A - B - fun j => B (j + 1)))
      - (h ^ 2 / 4) • lap h (dm h ((2 : ℝ) • A - B - fun j => B (j + 1)))
    = dm h ((2 : ℝ) • A + B + fun j => B (j + 1)) := by
  funext j x t
  simp only [mm, d0, dm, lap, Pi.add_apply, Pi.sub_apply, Pi.mul_apply, Pi.smul_apply,
    Pi.ofNat_apply, Pi.div_apply, smul_eq_mul]
  field_simp
  ring_nf

private lemma d3_ident5 (h : ℝ) (hne : h ≠ 0) (A B : Lattice) :
    d0 h ((2 : ℝ) • A - B - fun j => B (j + 1)) + h • lap h ((fun j => B (j + 1)) - B)
    = d0 h ((2 : ℝ) • A + B + fun j => B (j + 1)) - (4 / h) • ((fun j => B (j + 1)) - B) := by
  funext j x t
  simp only [d0, lap, Pi.add_apply, Pi.sub_apply, Pi.mul_apply, Pi.smul_apply,
    Pi.ofNat_apply, smul_eq_mul]
  field_simp
  ring_nf

/-! ## a local copy of the normalized Hirota quotient identity (C13) -/

private lemma C13_local (a : ℝ) (f g : XT) (hf : SmoothXT f) (hg : SmoothXT g)
    (hpos : ∀ x t, 0 < f x t ∧ 0 < g x t) :
    let α : XT := fun x t => Real.log (f x t)
    let β : XT := fun x t => Real.log (g x t)
    bil a f g / (f * g) = xx (α + β) + (dx (α - β)) ^ 2 + dt (α - β) + (2 * a) • dx (α - β) := by
  dsimp only
  set α : XT := fun x t => Real.log (f x t) with hα
  set β : XT := fun x t => Real.log (g x t) with hβ
  have hfT : ∀ t, ContDiff ℝ ⊤ (fun x : ℝ => f x t) := fun t => slice_cont hf t
  have hgT : ∀ t, ContDiff ℝ ⊤ (fun x : ℝ => g x t) := fun t => slice_cont hg t
  have hft : ∀ x, ContDiff ℝ ⊤ (fun t : ℝ => f x t) := fun x => slice_cont_t hf x
  have hgt : ∀ x, ContDiff ℝ ⊤ (fun t : ℝ => g x t) := fun x => slice_cont_t hg x
  have hαx : ∀ t, ContDiff ℝ ⊤ (fun x : ℝ => α x t) := by
    intro t
    have h : ContDiff ℝ ⊤ (fun x : ℝ => Real.log (f x t)) :=
      (hfT t).log (fun x => ne_of_gt (hpos x t).1)
    simpa [hα] using h
  have hβx : ∀ t, ContDiff ℝ ⊤ (fun x : ℝ => β x t) := by
    intro t
    have h : ContDiff ℝ ⊤ (fun x : ℝ => Real.log (g x t)) :=
      (hgT t).log (fun x => ne_of_gt (hpos x t).2)
    simpa [hβ] using h
  have hαt : ∀ x, ContDiff ℝ ⊤ (fun t : ℝ => α x t) := by
    intro x
    have h : ContDiff ℝ ⊤ (fun t : ℝ => Real.log (f x t)) :=
      (hft x).log (fun t => ne_of_gt (hpos x t).1)
    simpa [hα] using h
  have hβt : ∀ x, ContDiff ℝ ⊤ (fun t : ℝ => β x t) := by
    intro x
    have h : ContDiff ℝ ⊤ (fun t : ℝ => Real.log (g x t)) :=
      (hgt x).log (fun t => ne_of_gt (hpos x t).2)
    simpa [hβ] using h
  have hαxD : ∀ t, ContDiff ℝ ⊤ (deriv (fun x : ℝ => α x t)) := fun t =>
    ContDiff.deriv' (n := ⊤) (show ContDiff ℝ (⊤ + 1) (fun x : ℝ => α x t) from hαx t)
  have hβxD : ∀ t, ContDiff ℝ ⊤ (deriv (fun x : ℝ => β x t)) := fun t =>
    ContDiff.deriv' (n := ⊤) (show ContDiff ℝ (⊤ + 1) (fun x : ℝ => β x t) from hβx t)
  have hdxf : ∀ x t, dx f x t = f x t * dx α x t := by
    intro x t
    have hfne : f x t ≠ 0 := ne_of_gt (hpos x t).1
    have h1 : HasDerivAt (fun z : ℝ => Real.log (f z t))
        (deriv (fun z : ℝ => f z t) x / f x t) x :=
      (diffAt_of_contDiff (hfT t) x).hasDerivAt.log hfne
    simp only [dx, hα]
    rw [h1.deriv]
    field_simp
  have hdxg : ∀ x t, dx g x t = g x t * dx β x t := by
    intro x t
    have hgne : g x t ≠ 0 := ne_of_gt (hpos x t).2
    have h1 : HasDerivAt (fun z : ℝ => Real.log (g z t))
        (deriv (fun z : ℝ => g z t) x / g x t) x :=
      (diffAt_of_contDiff (hgT t) x).hasDerivAt.log hgne
    simp only [dx, hβ]
    rw [h1.deriv]
    field_simp
  have hdtf : ∀ x t, dt f x t = f x t * dt α x t := by
    intro x t
    have hfne : f x t ≠ 0 := ne_of_gt (hpos x t).1
    have h1 : HasDerivAt (fun z : ℝ => Real.log (f x z))
        (deriv (f x) t / f x t) t :=
      (diffAt_of_contDiff (hft x) t).hasDerivAt.log hfne
    simp only [dt, hα]
    rw [h1.deriv]
    field_simp
  have hdtg : ∀ x t, dt g x t = g x t * dt β x t := by
    intro x t
    have hgne : g x t ≠ 0 := ne_of_gt (hpos x t).2
    have h1 : HasDerivAt (fun z : ℝ => Real.log (g x z))
        (deriv (g x) t / g x t) t :=
      (diffAt_of_contDiff (hgt x) t).hasDerivAt.log hgne
    simp only [dt, hβ]
    rw [h1.deriv]
    field_simp
  have hxxf : ∀ x t, xx f x t = f x t * (xx α x t + (dx α x t) ^ 2) := by
    intro x t
    have hfun : (fun z : ℝ => dx f z t) = ((fun z : ℝ => f z t) * (fun z : ℝ => dx α z t)) := by
      funext z
      simp only [Pi.mul_apply]
      exact hdxf z t
    have hd1 : DifferentiableAt ℝ (fun z : ℝ => f z t) x := diffAt_of_contDiff (hfT t) x
    have hd2 : DifferentiableAt ℝ (fun z : ℝ => dx α z t) x :=
      diffAt_of_contDiff (hαxD t) x
    have hmul : deriv ((fun z : ℝ => f z t) * (fun z : ℝ => dx α z t)) x
        = dx f x t * dx α x t + f x t * xx α x t := by
      have h := deriv_mul hd1 hd2
      simpa only [dx, xx] using h
    calc xx f x t = deriv (fun z : ℝ => dx f z t) x := rfl
      _ = deriv ((fun z : ℝ => f z t) * (fun z : ℝ => dx α z t)) x := by rw [hfun]
      _ = dx f x t * dx α x t + f x t * xx α x t := hmul
      _ = f x t * (xx α x t + (dx α x t) ^ 2) := by
            rw [hdxf x t]
            ring
  have hxxg : ∀ x t, xx g x t = g x t * (xx β x t + (dx β x t) ^ 2) := by
    intro x t
    have hfun : (fun z : ℝ => dx g z t) = ((fun z : ℝ => g z t) * (fun z : ℝ => dx β z t)) := by
      funext z
      simp only [Pi.mul_apply]
      exact hdxg z t
    have hd1 : DifferentiableAt ℝ (fun z : ℝ => g z t) x := diffAt_of_contDiff (hgT t) x
    have hd2 : DifferentiableAt ℝ (fun z : ℝ => dx β z t) x :=
      diffAt_of_contDiff (hβxD t) x
    have hmul : deriv ((fun z : ℝ => g z t) * (fun z : ℝ => dx β z t)) x
        = dx g x t * dx β x t + g x t * xx β x t := by
      have h := deriv_mul hd1 hd2
      simpa only [dx, xx] using h
    calc xx g x t = deriv (fun z : ℝ => dx g z t) x := rfl
      _ = deriv ((fun z : ℝ => g z t) * (fun z : ℝ => dx β z t)) x := by rw [hfun]
      _ = dx g x t * dx β x t + g x t * xx β x t := hmul
      _ = g x t * (xx β x t + (dx β x t) ^ 2) := by
            rw [hdxg x t]
            ring
  have hdxadd : dx (α + β) = dx α + dx β := by
    funext x t
    simp only [dx, Pi.add_apply]
    exact deriv_add (diffAt_of_contDiff (hαx t) x) (diffAt_of_contDiff (hβx t) x)
  have hdxsub : dx (α - β) = dx α - dx β := by
    funext x t
    simp only [dx, Pi.sub_apply]
    exact deriv_sub (diffAt_of_contDiff (hαx t) x) (diffAt_of_contDiff (hβx t) x)
  have hdtsub : dt (α - β) = dt α - dt β := by
    funext x t
    simp only [dt, Pi.sub_apply]
    exact deriv_sub (diffAt_of_contDiff (hαt x) t) (diffAt_of_contDiff (hβt x) t)
  have hxxadd : xx (α + β) = xx α + xx β := by
    funext x t
    have h1 : (fun z : ℝ => deriv (fun w : ℝ => α w t + β w t) z)
        = (fun z : ℝ => deriv (fun w : ℝ => α w t) z + deriv (fun w : ℝ => β w t) z) := by
      funext z
      exact deriv_add (diffAt_of_contDiff (hαx t) z) (diffAt_of_contDiff (hβx t) z)
    simp only [xx, dx, Pi.add_apply]
    rw [h1]
    exact deriv_add (diffAt_of_contDiff (hαxD t) x) (diffAt_of_contDiff (hβxD t) x)
  funext x t
  have e1 : xx (α + β) x t = xx α x t + xx β x t := by simp only [hxxadd, Pi.add_apply]
  have e2 : dx (α - β) x t = dx α x t - dx β x t := by simp only [hdxsub, Pi.sub_apply]
  have e3 : dt (α - β) x t = dt α x t - dt β x t := by simp only [hdtsub, Pi.sub_apply]
  simp only [bil, hx, Pi.div_apply, Pi.mul_apply, Pi.sub_apply, Pi.add_apply, Pi.pow_apply,
    Pi.smul_apply, Pi.ofNat_apply, smul_eq_mul]
  rw [e1, e2, e3, hxxf x t, hxxg x t, hdxf x t, hdxg x t, hdtf x t, hdtg x t]
  rw [div_eq_iff (ne_of_gt (mul_pos (hpos x t).1 (hpos x t).2))]
  ring

/-! ## smoothness closure for `XT` -/

private lemma SmXT_add {z w : XT} (hz : SmoothXT z) (hw : SmoothXT w) : SmoothXT (z + w) :=
  show ContDiff ℝ ⊤ (fun p : ℝ × ℝ => (z + w) p.1 p.2) from hz.add hw

private lemma SmXT_sub {z w : XT} (hz : SmoothXT z) (hw : SmoothXT w) : SmoothXT (z - w) :=
  show ContDiff ℝ ⊤ (fun p : ℝ × ℝ => (z - w) p.1 p.2) from hz.sub hw

private lemma SmXT_smul (c : ℝ) {z : XT} (hz : SmoothXT z) : SmoothXT (c • z) :=
  show ContDiff ℝ ⊤ (fun p : ℝ × ℝ => (c • z) p.1 p.2) from ContDiff.const_smul c hz

private lemma SmXT_mul {z w : XT} (hz : SmoothXT z) (hw : SmoothXT w) : SmoothXT (z * w) :=
  show ContDiff ℝ ⊤ (fun p : ℝ × ℝ => (z * w) p.1 p.2) from hz.mul hw

private lemma Sm_logL (F : Lattice) (hF : Sm F) (hFp : PositiveL F) : Sm (logL F) := by
  intro j
  show ContDiff ℝ ⊤ (fun p : ℝ × ℝ => Real.log (F j p.1 p.2))
  exact (hF j).log (fun p => ne_of_gt (hFp j p.1 p.2))

/-! ## the logarithmic jet combinations `U`, `V`, `Z` -/

private abbrev UX (α β γ : XT) : XT := (2 : ℝ) • α - β - γ
private abbrev VX (α β γ : XT) : XT := γ - β
private abbrev ZX (α β γ : XT) : XT := (2 : ℝ) • α + β + γ
private abbrev ΦX (a h : ℝ) (α β γ : XT) : XT :=
  dt (UX α β γ) + (1 / 2 : ℝ) • (dx (UX α β γ)) ^ 2 + (1 / 2 : ℝ) • (dx (VX α β γ)) ^ 2
    + (2 * a) • dx (UX α β γ) - h • dx (VX α β γ)

private lemma dx_UX (α β γ : XT) (hα : SmoothXT α) (hβ : SmoothXT β) (hγ : SmoothXT γ) :
    dx (UX α β γ) = (2 : ℝ) • dx α - dx β - dx γ := by
  show dx ((2 : ℝ) • α - β - γ) = (2 : ℝ) • dx α - dx β - dx γ
  rw [dx_sub (SmXT_sub (SmXT_smul 2 hα) hβ) hγ, dx_sub (SmXT_smul 2 hα) hβ, dx_smul 2 hα]

private lemma dt_UX (α β γ : XT) (hα : SmoothXT α) (hβ : SmoothXT β) (hγ : SmoothXT γ) :
    dt (UX α β γ) = (2 : ℝ) • dt α - dt β - dt γ := by
  show dt ((2 : ℝ) • α - β - γ) = (2 : ℝ) • dt α - dt β - dt γ
  rw [dt_sub (SmXT_sub (SmXT_smul 2 hα) hβ) hγ, dt_sub (SmXT_smul 2 hα) hβ, dt_smul 2 hα]

private lemma dx_VX (α β γ : XT) (hα : SmoothXT α) (hβ : SmoothXT β) (hγ : SmoothXT γ) :
    dx (VX α β γ) = dx γ - dx β := by
  show dx (γ - β) = dx γ - dx β
  rw [dx_sub hγ hβ]

private lemma dt_VX (α β γ : XT) (hα : SmoothXT α) (hβ : SmoothXT β) (hγ : SmoothXT γ) :
    dt (VX α β γ) = dt γ - dt β := by
  show dt (γ - β) = dt γ - dt β
  rw [dt_sub hγ hβ]

private lemma xx_VX (α β γ : XT) (hα : SmoothXT α) (hβ : SmoothXT β) (hγ : SmoothXT γ) :
    xx (VX α β γ) = xx γ - xx β := by
  show xx (γ - β) = xx γ - xx β
  rw [xx_sub hγ hβ]

private lemma xx_ZX (α β γ : XT) (hα : SmoothXT α) (hβ : SmoothXT β) (hγ : SmoothXT γ) :
    xx (ZX α β γ) = (2 : ℝ) • xx α + xx β + xx γ := by
  show xx ((2 : ℝ) • α + β + γ) = (2 : ℝ) • xx α + xx β + xx γ
  rw [xx_add (SmXT_add (SmXT_smul 2 hα) hβ) hγ, xx_add (SmXT_smul 2 hα) hβ, xx_smul 2 hα]

/-- identity (1): `normA + normC` in logarithmic jets. -/
private lemma sumXT (a h : ℝ) (α β γ : XT) (hα : SmoothXT α) (hβ : SmoothXT β)
    (hγ : SmoothXT γ) :
    (xx (α + β) + (dx (α - β)) ^ 2 + dt (α - β) + (2 * (a - h / 2)) • dx (α - β))
      + (xx (α + γ) + (dx (α - γ)) ^ 2 + dt (α - γ) + (2 * (a + h / 2)) • dx (α - γ))
    = ΦX a h α β γ + xx (ZX α β γ) := by
  show (xx (α + β) + (dx (α - β)) ^ 2 + dt (α - β) + (2 * (a - h / 2)) • dx (α - β))
      + (xx (α + γ) + (dx (α - γ)) ^ 2 + dt (α - γ) + (2 * (a + h / 2)) • dx (α - γ))
    = dt (UX α β γ) + (1 / 2 : ℝ) • (dx (UX α β γ)) ^ 2
      + (1 / 2 : ℝ) • (dx (VX α β γ)) ^ 2 + (2 * a) • dx (UX α β γ) - h • dx (VX α β γ)
      + xx (ZX α β γ)
  rw [xx_add hα hβ, xx_add hα hγ, dt_sub hα hβ, dt_sub hα hγ, dx_sub hα hβ, dx_sub hα hγ,
    dt_UX α β γ hα hβ hγ, dx_UX α β γ hα hβ hγ, dx_VX α β γ hα hβ hγ,
    xx_ZX α β γ hα hβ hγ]
  funext x t
  simp only [Pi.add_apply, Pi.sub_apply, Pi.mul_apply, Pi.pow_apply, Pi.smul_apply,
    Pi.ofNat_apply, smul_eq_mul]
  ring

/-- identity (2): `normA - normC` in logarithmic jets. -/
private lemma sumXT2 (a h : ℝ) (α β γ : XT) (hα : SmoothXT α) (hβ : SmoothXT β)
    (hγ : SmoothXT γ) :
    (xx (α + β) + (dx (α - β)) ^ 2 + dt (α - β) + (2 * (a - h / 2)) • dx (α - β))
      - (xx (α + γ) + (dx (α - γ)) ^ 2 + dt (α - γ) + (2 * (a + h / 2)) • dx (α - γ))
    = - xx (VX α β γ) + dx (UX α β γ) * dx (VX α β γ) + dt (VX α β γ)
      + (2 * a) • dx (VX α β γ) - h • dx (UX α β γ) := by
  show (xx (α + β) + (dx (α - β)) ^ 2 + dt (α - β) + (2 * (a - h / 2)) • dx (α - β))
      - (xx (α + γ) + (dx (α - γ)) ^ 2 + dt (α - γ) + (2 * (a + h / 2)) • dx (α - γ))
    = - xx (VX α β γ) + dx (UX α β γ) * dx (VX α β γ) + dt (VX α β γ)
      + (2 * a) • dx (VX α β γ) - h • dx (UX α β γ)
  rw [xx_add hα hβ, xx_add hα hγ, dt_sub hα hβ, dt_sub hα hγ, dx_sub hα hβ, dx_sub hα hγ,
    dx_UX α β γ hα hβ hγ, dx_VX α β γ hα hβ hγ,
    dt_VX α β γ hα hβ hγ, xx_VX α β γ hα hβ hγ]
  funext x t
  simp only [Pi.add_apply, Pi.sub_apply, Pi.mul_apply, Pi.pow_apply, Pi.smul_apply,
    Pi.neg_apply, smul_eq_mul]
  ring

/-! ## `normA` and `normC` rewritten through `C13` -/

private lemma normA_eq (a h : ℝ) (F G : Lattice) (hF : Sm F) (hG : Sm G)
    (hFp : PositiveL F) (hGp : PositiveL G) :
    normA a h F G = fun j =>
      xx (logL F j + logL G j) + (dx (logL F j - logL G j)) ^ 2
        + dt (logL F j - logL G j) + (2 * (a - h / 2)) • dx (logL F j - logL G j) := by
  funext j
  show bil (a - h / 2) (F j) (G j) / (F j * G j) = _
  have h := C13_local (a - h / 2) (F j) (G j) (hF j) (hG j)
    (fun x t => ⟨hFp j x t, hGp j x t⟩)
  dsimp only [logL] at h ⊢
  exact h

private lemma normC_eq (a h : ℝ) (F G : Lattice) (hF : Sm F) (hG : Sm G)
    (hFp : PositiveL F) (hGp : PositiveL G) :
    normC a h F G = fun j =>
      xx (logL F j + logL G (j + 1)) + (dx (logL F j - logL G (j + 1))) ^ 2
        + dt (logL F j - logL G (j + 1))
        + (2 * (a + h / 2)) • dx (logL F j - logL G (j + 1)) := by
  funext j
  show bil (a + h / 2) (F j) (G (j + 1)) / (F j * G (j + 1)) = _
  have h := C13_local (a + h / 2) (F j) (G (j + 1)) (hF j) (hG (j + 1))
    (fun x t => ⟨hFp j x t, hGp (j + 1) x t⟩)
  dsimp only [logL] at h ⊢
  exact h

/-! ## the lattice-level objects appearing in C14 -/

private abbrev UL (F G : Lattice) : Lattice := fun j => UX (logL F j) (logL G j) (logL G (j + 1))
private abbrev VL (F G : Lattice) : Lattice := fun j => VX (logL F j) (logL G j) (logL G (j + 1))
private abbrev ZL (F G : Lattice) : Lattice := fun j => ZX (logL F j) (logL G j) (logL G (j + 1))
private abbrev ΦL (a h : ℝ) (F G : Lattice) : Lattice :=
  lt (UL F G) + (1 / 2 : ℝ) • (lx (UL F G)) ^ 2 + (1 / 2 : ℝ) • (lx (VL F G)) ^ 2
    + (2 * a) • lx (UL F G) - h • lx (VL F G)

private lemma norm_sum_eq (a h : ℝ) (F G : Lattice) (hF : Sm F) (hG : Sm G)
    (hFp : PositiveL F) (hGp : PositiveL G) :
    normA a h F G + normC a h F G = ΦL a h F G + lxx (ZL F G) := by
  show normA a h F G + normC a h F G
    = fun j => ΦX a h (logL F j) (logL G j) (logL G (j + 1))
        + xx (ZX (logL F j) (logL G j) (logL G (j + 1)))
  rw [normA_eq a h F G hF hG hFp hGp, normC_eq a h F G hF hG hFp hGp]
  funext j
  exact sumXT a h (logL F j) (logL G j) (logL G (j + 1))
    (Sm_logL F hF hFp j) (Sm_logL G hG hGp j) (Sm_logL G hG hGp (j + 1))

private lemma norm_diff_eq (a h : ℝ) (F G : Lattice) (hF : Sm F) (hG : Sm G)
    (hFp : PositiveL F) (hGp : PositiveL G) :
    normA a h F G - normC a h F G =
      - lxx (VL F G) + lx (UL F G) * lx (VL F G) + lt (VL F G)
        + (2 * a) • lx (VL F G) - h • lx (UL F G) := by
  show normA a h F G - normC a h F G
    = fun j => - xx (VX (logL F j) (logL G j) (logL G (j + 1)))
        + dx (UX (logL F j) (logL G j) (logL G (j + 1)))
            * dx (VX (logL F j) (logL G j) (logL G (j + 1)))
        + dt (VX (logL F j) (logL G j) (logL G (j + 1)))
        + (2 * a) • dx (VX (logL F j) (logL G j) (logL G (j + 1)))
        - h • dx (UX (logL F j) (logL G j) (logL G (j + 1)))
  rw [normA_eq a h F G hF hG hFp hGp, normC_eq a h F G hF hG hFp hGp]
  funext j
  exact sumXT2 a h (logL F j) (logL G j) (logL G (j + 1))
    (Sm_logL F hF hFp j) (Sm_logL G hG hGp j) (Sm_logL G hG hGp (j + 1))

/-! ## `physU`, `physV` and `W` in terms of `U`, `V` -/

private lemma two_mul_eq_smul (z : Lattice) : (2 : Lattice) * z = (2 : ℝ) • z := by
  funext j x t
  simp only [Pi.mul_apply, Pi.smul_apply, Pi.ofNat_apply, smul_eq_mul]

private lemma physU_eq (F G : Lattice) : physU F G = lx (UL F G) := by
  show lx ((2 : Lattice) * logL F - logL G - (fun j => logL G (j + 1))) = lx (UL F G)
  congr 1

private lemma physV_eq (h : ℝ) (F G : Lattice) :
    physV h F G = (4 / h) • lx (VL F G) + d0 h (lx (UL F G)) := by
  have h1 : ((fun j => logL G (j + 1)) - logL G) = VL F G := by
    funext j x t
    simp only [VL, VX, Pi.sub_apply]
  show (4 / h) • lx ((fun j => logL G (j + 1)) - logL G) + d0 h (physU F G) = _
  rw [h1, physU_eq]

private lemma W_eq (h : ℝ) (F G : Lattice) :
    W h (physU F G) (physV h F G) = (4 / h) • lx (VL F G) := by
  show physV h F G - d0 h (physU F G) = _
  rw [physV_eq, physU_eq, add_sub_cancel_right]

/-! ## expanding `H` when `W = (4/h) • y` -/

private lemma H_expand (a h : ℝ) (hne : h ≠ 0) (u y : Lattice) :
    H a h u ((4 / h) • y + d0 h u)
      = (1 / 2 : ℝ) • (u ^ 2) + (1 / 2 : ℝ) • (y ^ 2) + (2 * a) • u - h • y := by
  have hW : W h u ((4 / h) • y + d0 h u) = (4 / h) • y := by
    show ((4 / h) • y + d0 h u) - d0 h u = (4 / h) • y
    rw [add_sub_cancel_right]
  show u ^ 2 / 2 + (2 * a) • u
      + h ^ 2 • ((W h u ((4 / h) • y + d0 h u)) ^ 2 / 32
          - W h u ((4 / h) • y + d0 h u) / 4)
    = (1 / 2 : ℝ) • (u ^ 2) + (1 / 2 : ℝ) • (y ^ 2) + (2 * a) • u - h • y
  rw [hW]
  funext j x t
  simp only [Pi.add_apply, Pi.sub_apply, Pi.mul_apply, Pi.pow_apply, Pi.smul_apply,
    Pi.ofNat_apply, Pi.div_apply, smul_eq_mul]
  field_simp
  ring

/-! ## smoothness of the compound expressions -/

private lemma Sm_tail (a h : ℝ) (u y : Lattice) (hu : Sm u) (hy : Sm y) :
    Sm ((1 / 2 : ℝ) • (u ^ 2) + (1 / 2 : ℝ) • (y ^ 2) + (2 * a) • u - h • y) :=
  Sm_sub (Sm_add (Sm_add (Sm_smul _ (Sm_pow hu 2)) (Sm_smul _ (Sm_pow hy 2))) (Sm_smul _ hu))
    (Sm_smul h hy)

private lemma Sm_tail3 (a h : ℝ) (U y : Lattice) (hU : Sm U) (hy : Sm y) :
    Sm (lt U + (1 / 2 : ℝ) • (lx U) ^ 2 + (1 / 2 : ℝ) • (y ^ 2) + (2 * a) • lx U - h • y) :=
  Sm_sub (Sm_add (Sm_add (Sm_add (Sm_lt hU) (Sm_smul _ (Sm_pow (Sm_lx hU) 2)))
    (Sm_smul _ (Sm_pow hy 2))) (Sm_smul _ (Sm_lx hU))) (Sm_smul h hy)

/-! ## identity (3): `lt u + lx (H a h u v) = lx Φ` -/

private lemma id3 (a h : ℝ) (hne : h ≠ 0) (U y : Lattice) (hU : Sm U) (hy : Sm y) :
    lt (lx U) + lx (H a h (lx U) ((4 / h) • y + d0 h (lx U)))
      = lx (lt U + (1 / 2 : ℝ) • (lx U) ^ 2 + (1 / 2 : ℝ) • (y ^ 2)
          + (2 * a) • lx U - h • y) := by
  have hu : Sm (lx U) := Sm_lx hU
  have hA : Sm ((1 / 2 : ℝ) • ((lx U) ^ 2)) := Sm_smul _ (Sm_pow hu 2)
  have hB : Sm ((1 / 2 : ℝ) • (y ^ 2)) := Sm_smul _ (Sm_pow hy 2)
  have hC : Sm ((2 * a) • (lx U)) := Sm_smul _ hu
  have hD : Sm (h • y) := Sm_smul h hy
  have hE : Sm (lt U) := Sm_lt hU
  rw [H_expand a h hne (lx U) y]
  have eL : lx ((1 / 2 : ℝ) • ((lx U) ^ 2) + (1 / 2 : ℝ) • (y ^ 2) + (2 * a) • (lx U) - h • y)
      = (lx U) * lx (lx U) + y * lx y + (2 * a) • lx (lx U) - h • lx y := by
    rw [lx_sub (Sm_add (Sm_add hA hB) hC) hD, lx_add (Sm_add hA hB) hC, lx_add hA hB,
      lx_smul (1 / 2) (Sm_pow hu 2), lx_smul (1 / 2) (Sm_pow hy 2), lx_smul (2 * a) hu,
      lx_smul h hy, lx_sq hu, lx_sq hy]
    funext j x t
    simp only [Pi.add_apply, Pi.sub_apply, Pi.mul_apply, Pi.smul_apply, smul_eq_mul]
    ring
  have eR : lx (lt U + (1 / 2 : ℝ) • (lx U) ^ 2 + (1 / 2 : ℝ) • (y ^ 2)
        + (2 * a) • lx U - h • y)
      = lt (lx U) + (lx U) * lx (lx U) + y * lx y + (2 * a) • lx (lx U) - h • lx y := by
    rw [lx_sub (Sm_add (Sm_add (Sm_add hE hA) hB) hC) hD,
      lx_add (Sm_add (Sm_add hE hA) hB) hC, lx_add (Sm_add hE hA) hB, lx_add hE hA,
      lx_smul (1 / 2) (Sm_pow hu 2), lx_smul (1 / 2) (Sm_pow hy 2), lx_smul (2 * a) hu,
      lx_smul h hy, lx_sq hu, lx_sq hy, ← lt_lx hU]
    funext j x t
    simp only [Pi.add_apply, Pi.sub_apply, Pi.mul_apply, Pi.smul_apply, smul_eq_mul]
    ring
  rw [eL, eR]
  funext j x t
  simp only [Pi.add_apply, Pi.sub_apply, Pi.mul_apply, Pi.smul_apply, smul_eq_mul]
  ring

/-! ## smoothness of `UL`, `VL`, `ZL`, `ΦL` -/

private lemma Sm_UL (F G : Lattice) (hF : Sm F) (hG : Sm G) (hFp : PositiveL F)
    (hGp : PositiveL G) : Sm (UL F G) := by
  intro j
  simpa only [UL, UX] using
    SmXT_sub (SmXT_sub (SmXT_smul 2 (Sm_logL F hF hFp j)) (Sm_logL G hG hGp j))
      (Sm_logL G hG hGp (j + 1))

private lemma Sm_VL (F G : Lattice) (hF : Sm F) (hG : Sm G) (hFp : PositiveL F)
    (hGp : PositiveL G) : Sm (VL F G) := by
  intro j
  simpa only [VL, VX] using SmXT_sub (Sm_logL G hG hGp (j + 1)) (Sm_logL G hG hGp j)

private lemma Sm_ZL (F G : Lattice) (hF : Sm F) (hG : Sm G) (hFp : PositiveL F)
    (hGp : PositiveL G) : Sm (ZL F G) := by
  intro j
  simpa only [ZL, ZX] using
    SmXT_add (SmXT_add (SmXT_smul 2 (Sm_logL F hF hFp j)) (Sm_logL G hG hGp j))
      (Sm_logL G hG hGp (j + 1))

private lemma Sm_ΦL (a h : ℝ) (F G : Lattice) (hF : Sm F) (hG : Sm G) (hFp : PositiveL F)
    (hGp : PositiveL G) : Sm (ΦL a h F G) := by
  have hU := Sm_UL F G hF hG hFp hGp
  have hV := Sm_VL F G hF hG hFp hGp
  simpa only [ΦL] using
    Sm_sub (Sm_add (Sm_add (Sm_add (Sm_lt hU) (Sm_smul (1 / 2 : ℝ) (Sm_pow (Sm_lx hU) 2)))
      (Sm_smul (1 / 2 : ℝ) (Sm_pow (Sm_lx hV) 2))) (Sm_smul (2 * a) (Sm_lx hU)))
      (Sm_smul h (Sm_lx hV))

/-! ## third `x`-derivatives of the logarithmic combinations -/

private abbrev A3 (F : Lattice) : Lattice := lxx (lx (logL F))
private abbrev B3 (G : Lattice) : Lattice := lxx (lx (logL G))
private abbrev SB (G : Lattice) : Lattice := fun j => B3 G (j + 1)

private lemma lxx_UL (F G : Lattice) (hF : Sm F) (hG : Sm G) (hFp : PositiveL F)
    (hGp : PositiveL G) :
    lxx (UL F G) = (2 : ℝ) • lxx (logL F) - lxx (logL G) - lxx (fun j => logL G (j + 1)) := by
  have hp := Sm_logL F hF hFp
  have hq := Sm_logL G hG hGp
  have hq1 : Sm (fun j => logL G (j + 1)) := fun j => hq (j + 1)
  have hEq : UL F G = (2 : ℝ) • logL F - logL G - (fun j => logL G (j + 1)) := by
    funext j x t
    simp only [UL, UX, Pi.sub_apply, Pi.smul_apply, smul_eq_mul]
  rw [hEq, lxx_sub (Sm_sub (Sm_smul (2 : ℝ) hp) hq) hq1,
    lxx_sub (Sm_smul (2 : ℝ) hp) hq, lxx_smul (2 : ℝ) hp]

private lemma lxx_VL (F G : Lattice) (hF : Sm F) (hG : Sm G) (hFp : PositiveL F)
    (hGp : PositiveL G) :
    lxx (VL F G) = (fun j => lxx (logL G) (j + 1)) - lxx (logL G) := by
  have hq := Sm_logL G hG hGp
  have hq1 : Sm (fun j => logL G (j + 1)) := fun j => hq (j + 1)
  have hEq : VL F G = (fun j => logL G (j + 1)) - logL G := by
    funext j x t
    simp only [VL, VX, Pi.sub_apply]
  rw [hEq, lxx_sub hq1 hq, lxx_shift_p (logL G)]

private lemma lxx_ZL (F G : Lattice) (hF : Sm F) (hG : Sm G) (hFp : PositiveL F)
    (hGp : PositiveL G) :
    lxx (ZL F G) = (2 : ℝ) • lxx (logL F) + lxx (logL G) + lxx (fun j => logL G (j + 1)) := by
  have hp := Sm_logL F hF hFp
  have hq := Sm_logL G hG hGp
  have hq1 : Sm (fun j => logL G (j + 1)) := fun j => hq (j + 1)
  have hEq : ZL F G = (2 : ℝ) • logL F + logL G + (fun j => logL G (j + 1)) := by
    funext j x t
    simp only [ZL, ZX, Pi.add_apply, Pi.smul_apply, smul_eq_mul]
  rw [hEq, lxx_add (Sm_add (Sm_smul (2 : ℝ) hp) hq) hq1,
    lxx_add (Sm_smul (2 : ℝ) hp) hq, lxx_smul (2 : ℝ) hp]

private lemma lxx_physU (F G : Lattice) (hF : Sm F) (hG : Sm G) (hFp : PositiveL F)
    (hGp : PositiveL G) : lxx (physU F G) = (2 : ℝ) • A3 F - B3 G - SB G := by
  have hp := Sm_logL F hF hFp
  have hq := Sm_logL G hG hGp
  have hq1 : Sm (fun j => logL G (j + 1)) := fun j => hq (j + 1)
  rw [physU_eq]
  show lx (lxx (UL F G)) = _
  rw [lxx_UL F G hF hG hFp hGp,
    lx_sub (Sm_sub (Sm_smul (2 : ℝ) (Sm_lxx hp)) (Sm_lxx hq)) (Sm_lxx hq1),
    lx_sub (Sm_smul (2 : ℝ) (Sm_lxx hp)) (Sm_lxx hq), lx_smul (2 : ℝ) (Sm_lxx hp),
    lxx_shift_p (logL G), lx_shift_p (lxx (logL G))]
  rfl

private lemma lxx_lxVL (F G : Lattice) (hF : Sm F) (hG : Sm G) (hFp : PositiveL F)
    (hGp : PositiveL G) : lxx (lx (VL F G)) = SB G - B3 G := by
  have hq := Sm_logL G hG hGp
  have hq1 : Sm (fun j => logL G (j + 1)) := fun j => hq (j + 1)
  show lx (lxx (VL F G)) = _
  rw [lxx_VL F G hF hG hFp hGp, lx_sub (fun j => Sm_lxx hq (j + 1)) (Sm_lxx hq),
    lx_shift_p (lxx (logL G))]
  rfl

private lemma lx_lxx_VL (F G : Lattice) (hF : Sm F) (hG : Sm G) (hFp : PositiveL F)
    (hGp : PositiveL G) : lx (lxx (VL F G)) = SB G - B3 G :=
  lxx_lxVL F G hF hG hFp hGp

private lemma lxx_lxZL (F G : Lattice) (hF : Sm F) (hG : Sm G) (hFp : PositiveL F)
    (hGp : PositiveL G) : lx (lxx (ZL F G)) = (2 : ℝ) • A3 F + B3 G + SB G := by
  have hp := Sm_logL F hF hFp
  have hq := Sm_logL G hG hGp
  have hq1 : Sm (fun j => logL G (j + 1)) := fun j => hq (j + 1)
  show lx (lxx (ZL F G)) = _
  rw [lxx_ZL F G hF hG hFp hGp,
    lx_add (Sm_add (Sm_smul (2 : ℝ) (Sm_lxx hp)) (Sm_lxx hq)) (Sm_lxx hq1),
    lx_add (Sm_smul (2 : ℝ) (Sm_lxx hp)) (Sm_lxx hq), lx_smul (2 : ℝ) (Sm_lxx hp),
    lxx_shift_p (logL G), lx_shift_p (lxx (logL G))]
  rfl

private lemma lxx_physV (h : ℝ) (F G : Lattice) (hF : Sm F) (hG : Sm G) (hFp : PositiveL F)
    (hGp : PositiveL G) :
    lxx (physV h F G) = (4 / h) • lxx (lx (VL F G)) + d0 h (lxx (physU F G)) := by
  have hU' := Sm_UL F G hF hG hFp hGp
  have hV' := Sm_VL F G hF hG hFp hGp
  have hlxU : Sm (lx (UL F G)) := Sm_lx hU'
  rw [physV_eq, physU_eq]
  rw [lxx_add (Sm_smul (4 / h) (Sm_lx hV')) (Sm_d0 h hlxU),
    lxx_smul (4 / h) (Sm_lx hV'), lxx_d0 h hlxU]

/-- `(h²/4) • lap h ((4/h) • X) = h • lap h X` for `h ≠ 0`. -/
private lemma quarter_lap (h : ℝ) (hne : h ≠ 0) (X : Lattice) :
    (h ^ 2 / 4) • lap h ((4 / h) • X) = h • lap h X := by
  rw [lap_smul h (4 / h) X]
  funext j x t
  simp only [Pi.smul_apply, smul_eq_mul]
  field_simp

/-! ## identities (4) and (5) -/

private lemma id4 (h : ℝ) (hne : h ≠ 0) (F G : Lattice) (hF : Sm F) (hG : Sm G)
    (hFp : PositiveL F) (hGp : PositiveL G) :
    lxx (mm (physV h F G) - (h ^ 2 / 4) • lap h (dm h (physU F G)))
      = dm h (lx (lxx (ZL F G))) := by
  have hU' := Sm_UL F G hF hG hFp hGp
  have hV' := Sm_VL F G hF hG hFp hGp
  have hu : Sm (physU F G) := by rw [physU_eq]; exact Sm_lx hU'
  have hv : Sm (physV h F G) := by
    rw [physV_eq]
    exact Sm_add (Sm_smul (4 / h) (Sm_lx hV')) (Sm_d0 h (Sm_lx hU'))
  have e1 : lxx (mm (physV h F G) - (h ^ 2 / 4) • lap h (dm h (physU F G)))
      = mm (lxx (physV h F G))
        - (h ^ 2 / 4) • lap h (dm h (lxx (physU F G))) := by
    rw [lxx_sub (Sm_mm hv) (Sm_smul (h ^ 2 / 4) (Sm_lap h (Sm_dm h hu))),
      lxx_smul (h ^ 2 / 4) (Sm_lap h (Sm_dm h hu)), lxx_mm hv,
      lxx_lap h (Sm_dm h hu), lxx_dm h hu]
  rw [e1, lxx_physV h F G hF hG hFp hGp, lxx_physU F G hF hG hFp hGp,
    lxx_lxVL F G hF hG hFp hGp, lxx_lxZL F G hF hG hFp hGp]
  exact d3_ident4 h hne (A3 F) (B3 G)

private lemma id5 (h : ℝ) (hne : h ≠ 0) (F G : Lattice) (hF : Sm F) (hG : Sm G)
    (hFp : PositiveL F) (hGp : PositiveL G) :
    lxx (d0 h (physU F G) + (h ^ 2 / 4) • lap h (W h (physU F G) (physV h F G)))
      = d0 h (lx (lxx (ZL F G))) - (4 / h) • lx (lxx (VL F G)) := by
  have hU' := Sm_UL F G hF hG hFp hGp
  have hV' := Sm_VL F G hF hG hFp hGp
  have hu : Sm (physU F G) := by rw [physU_eq]; exact Sm_lx hU'
  have hlxV : Sm (lx (VL F G)) := Sm_lx hV'
  have e1 : lxx (d0 h (physU F G) + (h ^ 2 / 4) • lap h (W h (physU F G) (physV h F G)))
      = d0 h (lxx (physU F G)) + h • lap h (lxx (lx (VL F G))) := by
    rw [W_eq h F G,
      lxx_add (Sm_d0 h hu) (Sm_smul (h ^ 2 / 4) (Sm_lap h (Sm_smul (4 / h) hlxV))),
      lxx_d0 h hu, lxx_smul (h ^ 2 / 4) (Sm_lap h (Sm_smul (4 / h) hlxV)),
      lxx_lap h (Sm_smul (4 / h) hlxV), lxx_smul (4 / h) hlxV,
      quarter_lap h hne (lxx (lx (VL F G)))]
  rw [e1, lxx_physU F G hF hG hFp hGp, lxx_lxVL F G hF hG hFp hGp,
    lx_lxx_VL F G hF hG hFp hGp, lxx_lxZL F G hF hG hFp hGp]
  exact d3_ident5 h hne (A3 F) (B3 G)

private lemma Sm_neg {z : Lattice} (hz : Sm z) : Sm (-z) := by
  intro j
  show ContDiff ℝ ⊤ (fun p : ℝ × ℝ => (-z) j p.1 p.2)
  simpa only [Pi.neg_apply] using (hz j).neg

private lemma Sm_div (c : ℝ) {z : Lattice} (hz : Sm z) : Sm (z / (fun _ _ _ => c : Lattice)) := by
  intro j
  show ContDiff ℝ ⊤ (fun p : ℝ × ℝ => (z / (fun _ _ _ => c : Lattice)) j p.1 p.2)
  simpa only [Pi.div_apply] using (hz j).div_const c

private lemma Sm_W (h : ℝ) {u v : Lattice} (hu : Sm u) (hv : Sm v) : Sm (W h u v) := by
  show Sm (v - d0 h u)
  exact Sm_sub hv (Sm_d0 h hu)

private lemma Sm_H (a h : ℝ) {u v : Lattice} (hu : Sm u) (hv : Sm v) : Sm (H a h u v) := by
  have hW : Sm (W h u v) := Sm_W h hu hv
  show Sm (u ^ 2 / 2 + (2 * a) • u + h ^ 2 • ((W h u v) ^ 2 / 32 - W h u v / 4))
  exact Sm_add (Sm_add (Sm_div 2 (Sm_pow hu 2)) (Sm_smul (2 * a) hu))
    (Sm_smul (h ^ 2) (Sm_sub (Sm_div 32 (Sm_pow hW 2)) (Sm_div 4 hW)))

private lemma lx_neg {z : Lattice} (hz : Sm z) : lx (-z) = - lx z := by
  have h : -z = (-1 : ℝ) • z := by
    funext j x t
    simp only [Pi.neg_apply, Pi.smul_apply, smul_eq_mul, neg_one_mul]
  rw [h, lx_smul (-1) hz, neg_one_smul]

private lemma lt_physV (h : ℝ) (F G : Lattice) (hF : Sm F) (hG : Sm G) (hFp : PositiveL F)
    (hGp : PositiveL G) :
    lt (physV h F G) = (4 / h) • lt (lx (VL F G)) + d0 h (lt (physU F G)) := by
  have hU' := Sm_UL F G hF hG hFp hGp
  have hV' := Sm_VL F G hF hG hFp hGp
  rw [physV_eq, physU_eq]
  rw [lt_add (Sm_smul (4 / h) (Sm_lx hV')) (Sm_d0 h (Sm_lx hU')),
    lt_smul (4 / h) (Sm_lx hV'), lt_d0 h (Sm_lx hU')]

private lemma lx_HW (a h : ℝ) (F G : Lattice) (hF : Sm F) (hG : Sm G) (hFp : PositiveL F)
    (hGp : PositiveL G) :
    lx (d0 h (H a h (physU F G) (physV h F G))
        + (physU F G + (fun _ _ _ => 2 * a)) * W h (physU F G) (physV h F G)
        - 4 * physU F G)
      = d0 h (lx (H a h (physU F G) (physV h F G)))
        + lx (physU F G) * W h (physU F G) (physV h F G)
        + (physU F G + (fun _ _ _ => 2 * a)) * lx (W h (physU F G) (physV h F G))
        - 4 * lx (physU F G) := by
  have hU' := Sm_UL F G hF hG hFp hGp
  have hV' := Sm_VL F G hF hG hFp hGp
  have hu : Sm (physU F G) := by rw [physU_eq]; exact Sm_lx hU'
  have hv : Sm (physV h F G) := by
    rw [physV_eq]; exact Sm_add (Sm_smul (4 / h) (Sm_lx hV')) (Sm_d0 h (Sm_lx hU'))
  have hun : Sm (physU F G + (fun _ _ _ => 2 * a)) := Sm_add hu (Sm_const (2 * a))
  have hH : Sm (H a h (physU F G) (physV h F G)) := Sm_H a h hu hv
  have hW : Sm (W h (physU F G) (physV h F G)) := Sm_W h hu hv
  have h4u : Sm ((4 : Lattice) * physU F G) := Sm_mul (Sm_const 4) hu
  have h4lxu : Sm ((4 : Lattice) * lx (physU F G)) := Sm_mul (Sm_const 4) (Sm_lx hu)
  have h4 : lx ((4 : Lattice) * physU F G) = (4 : Lattice) * lx (physU F G) :=
    lx_smul (4 : ℝ) hu
  rw [lx_sub (Sm_add (Sm_d0 h hH) (Sm_mul hun hW)) h4u,
    lx_add (Sm_d0 h hH) (Sm_mul hun hW), lx_d0 h hH, lx_mul hun hW,
    lx_add hu (Sm_const (2 * a)), lx_const (2 * a), h4]
  funext j x t
  simp only [Pi.add_apply, Pi.sub_apply, Pi.mul_apply, Pi.smul_apply, Pi.zero_apply]
  ring

private lemma lx_diff_expand (a h : ℝ) (F G : Lattice) (hF : Sm F) (hG : Sm G)
    (hFp : PositiveL F) (hGp : PositiveL G) :
    lx (normA a h F G - normC a h F G)
      = - lx (lxx (VL F G))
        + lx (lx (UL F G)) * lx (VL F G) + lx (UL F G) * lx (lx (VL F G))
        + lt (lx (VL F G)) + (2 * a) • lx (lx (VL F G)) - h • lx (lx (UL F G)) := by
  have hU' := Sm_UL F G hF hG hFp hGp
  have hV' := Sm_VL F G hF hG hFp hGp
  have hlxU : Sm (lx (UL F G)) := Sm_lx hU'
  have hlxV : Sm (lx (VL F G)) := Sm_lx hV'
  have hlxxU : Sm (lxx (UL F G)) := Sm_lxx hU'
  have hlxxV : Sm (lxx (VL F G)) := Sm_lxx hV'
  rw [norm_diff_eq a h F G hF hG hFp hGp]
  rw [lx_sub (Sm_add (Sm_add (Sm_add (Sm_neg hlxxV) (Sm_mul hlxU hlxV)) (Sm_lt hV'))
      (Sm_smul (2 * a) hlxV)) (Sm_smul h hlxU),
    lx_add (Sm_add (Sm_add (Sm_neg hlxxV) (Sm_mul hlxU hlxV)) (Sm_lt hV')) (Sm_smul (2 * a) hlxV),
    lx_add (Sm_add (Sm_neg hlxxV) (Sm_mul hlxU hlxV)) (Sm_lt hV'),
    lx_add (Sm_neg hlxxV) (Sm_mul hlxU hlxV),
    lx_neg hlxxV, lx_mul hlxU hlxV, lx_smul (2 * a) hlxV, lx_smul h hlxU, ← lt_lx hV']
  abel

theorem c14_proved : C14 := by
  intro a h F G hne hF hG hFp hGp
  have hU' : Sm (UL F G) := Sm_UL F G hF hG hFp hGp
  have hV' : Sm (VL F G) := Sm_VL F G hF hG hFp hGp
  have hZ' : Sm (ZL F G) := Sm_ZL F G hF hG hFp hGp
  have hlxU : Sm (lx (UL F G)) := Sm_lx hU'
  have hlxV : Sm (lx (VL F G)) := Sm_lx hV'
  have hv : Sm (physV h F G) := by
    rw [physV_eq]
    exact Sm_add (Sm_smul (4 / h) hlxV) (Sm_d0 h hlxU)
  have hΦ : Sm (ΦL a h F G) := Sm_ΦL a h F G hF hG hFp hGp
  have hZsm : Sm (lxx (ZL F G)) := Sm_lxx hZ'
  have h1 : normA a h F G + normC a h F G = ΦL a h F G + lxx (ZL F G) :=
    norm_sum_eq a h F G hF hG hFp hGp
  have h3 : lt (physU F G) + lx (H a h (physU F G) (physV h F G)) = lx (ΦL a h F G) := by
    rw [physU_eq, physV_eq]
    exact id3 a h hne (UL F G) (lx (VL F G)) hU' hlxV
  have h4 : lxx (mm (physV h F G) - (h ^ 2 / 4) • lap h (dm h (physU F G)))
      = dm h (lx (lxx (ZL F G))) := id4 h hne F G hF hG hFp hGp
  have h5 : lxx (d0 h (physU F G) + (h ^ 2 / 4) • lap h (W h (physU F G) (physV h F G)))
      = d0 h (lx (lxx (ZL F G))) - (4 / h) • lx (lxx (VL F G)) :=
    id5 h hne F G hF hG hFp hGp
  have h6 : lt (physV h F G) = (4 / h) • lt (lx (VL F G)) + d0 h (lt (physU F G)) :=
    lt_physV h F G hF hG hFp hGp
  have h7 : lx (d0 h (H a h (physU F G) (physV h F G))
        + (physU F G + (fun _ _ _ => 2 * a)) * W h (physU F G) (physV h F G) - 4 * physU F G)
      = d0 h (lx (H a h (physU F G) (physV h F G)))
        + lx (physU F G) * W h (physU F G) (physV h F G)
        + (physU F G + (fun _ _ _ => 2 * a)) * lx (W h (physU F G) (physV h F G))
        - 4 * lx (physU F G) := lx_HW a h F G hF hG hFp hGp
  have h8 : lx (normA a h F G - normC a h F G)
      = - lx (lxx (VL F G)) + lx (lx (UL F G)) * lx (VL F G) + lx (UL F G) * lx (lx (VL F G))
        + lt (lx (VL F G)) + (2 * a) • lx (lx (VL F G)) - h • lx (lx (UL F G)) :=
    lx_diff_expand a h F G hF hG hFp hGp
  refine ⟨?_, ?_⟩
  · show n1 a h (physU F G) (physV h F G) = dm h (lx (normA a h F G + normC a h F G))
    rw [h1, lx_add hΦ hZsm, dm_add h (lx (ΦL a h F G)) (lx (lxx (ZL F G))), ← h3, ← h4]
    rfl
  · show lt (physV h F G)
        + lx (d0 h (H a h (physU F G) (physV h F G))
            + (physU F G + (fun _ _ _ => 2 * a)) * W h (physU F G) (physV h F G)
            - 4 * physU F G)
        + lxx (d0 h (physU F G) + (h ^ 2 / 4) • lap h (W h (physU F G) (physV h F G)))
      = d0 h (lx (normA a h F G + normC a h F G))
        + (4 / h) • lx (normA a h F G - normC a h F G)
    rw [h5, h1, lx_add hΦ hZsm, d0_add h (lx (ΦL a h F G)) (lx (lxx (ZL F G))), ← h3,
      d0_add h (lt (physU F G)) (lx (H a h (physU F G) (physV h F G))), h6, h7,
      W_eq h F G, lx_smul (4 / h) hlxV, h8, physU_eq]
    funext j x t
    simp only [lxx, Pi.add_apply, Pi.sub_apply, Pi.mul_apply, Pi.smul_apply, Pi.neg_apply,
      Pi.ofNat_apply, smul_eq_mul]
    field_simp
    ring_nf

theorem c15_proved : C15 := by
  intro a h F G hne hF hG hFp hGp hsp
  have hl0 : lx (0 : Lattice) = 0 := lx_const 0
  have hA : normA a h F G = 0 := by
    funext j x t
    show (bil (a - h / 2) (F j) (G j) / (F j * G j)) x t = 0
    rw [(hsp j).1]
    simp
  have hC : normC a h F G = 0 := by
    funext j x t
    show (bil (a + h / 2) (F j) (G (j + 1)) / (F j * G (j + 1))) x t = 0
    rw [(hsp j).2]
    simp
  have hsum : normA a h F G + normC a h F G = 0 := by rw [hA, hC, add_zero]
  have hdiff : normA a h F G - normC a h F G = 0 := by rw [hA, hC, sub_zero]
  have h14 := c14_proved a h F G hne hF hG hFp hGp
  refine ⟨?_, ?_⟩
  · rw [h14.1, hsum, hl0]
    funext j x t
    simp [dm]
  · rw [h14.2, hsum, hdiff, hl0]
    funext j x t
    simp [d0]

end DLWContract

#print axioms DLWContract.c14_proved
#print axioms DLWContract.c15_proved
