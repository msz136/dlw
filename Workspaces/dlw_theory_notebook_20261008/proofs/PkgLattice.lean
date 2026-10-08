/-
Package: lattice-operator targets.

Targets C25 (the amplitude derivative) and C20 (periodic summing gives only a
compatibility constraint) of `Contracts.lean`.

Everything is proved from the frozen definitions; no `sorry`, no new axioms.
-/
import Contracts
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Analysis.Calculus.ContDiff.Deriv
import Mathlib.Analysis.Calculus.ContDiff.Comp
import Mathlib.Analysis.Calculus.ContDiff.Operations
import Mathlib.Analysis.Calculus.FDeriv.Prod
import Mathlib.Tactic

set_option linter.unusedSimpArgs false
set_option linter.unusedTactic false

noncomputable section
open scoped BigOperators
namespace DLWContract

/-! ## 0. scalar multiplication on `ℝ` -/

private lemma smulR (c x : ℝ) : c • x = c * x := rfl

/-! ## 1. the `C^∞` toolkit -/

/-- Regularity of a two-variable field. -/
abbrev Smo (f : XT) : Prop := SmoothXT f

/-- Lattice level regularity. -/
abbrev SmL (z : Lattice) : Prop := SmoothL z

private lemma deriv_slice_x (f : XT) (x t : ℝ)
    (hd : DifferentiableAt ℝ (fun p : ℝ × ℝ => f p.1 p.2) (x, t)) :
    deriv (fun y : ℝ => f y t) x
      = fderiv ℝ (fun p : ℝ × ℝ => f p.1 p.2) (x, t) ((1 : ℝ), (0 : ℝ)) := by
  have hι : HasFDerivAt (fun y : ℝ => (y, t)) (ContinuousLinearMap.inl ℝ ℝ ℝ) x :=
    hasFDerivAt_prodMk_left x t
  have hcomp : HasFDerivAt (fun y : ℝ => f y t)
      ((fderiv ℝ (fun p : ℝ × ℝ => f p.1 p.2) (x, t)).comp
        (ContinuousLinearMap.inl ℝ ℝ ℝ)) x :=
    (hd.hasFDerivAt).comp (f := fun y : ℝ => (y, t)) (x := x) hι
  rw [hcomp.hasDerivAt.deriv]
  rfl

private lemma deriv_slice_t (f : XT) (x t : ℝ)
    (hd : DifferentiableAt ℝ (fun p : ℝ × ℝ => f p.1 p.2) (x, t)) :
    deriv (f x) t
      = fderiv ℝ (fun p : ℝ × ℝ => f p.1 p.2) (x, t) ((0 : ℝ), (1 : ℝ)) := by
  have hι : HasFDerivAt (fun s : ℝ => (x, s)) (ContinuousLinearMap.inr ℝ ℝ ℝ) t :=
    hasFDerivAt_prodMk_right x t
  have hcomp : HasFDerivAt (fun s : ℝ => f x s)
      ((fderiv ℝ (fun p : ℝ × ℝ => f p.1 p.2) (x, t)).comp
        (ContinuousLinearMap.inr ℝ ℝ ℝ)) t :=
    (hd.hasFDerivAt).comp (f := fun s : ℝ => (x, s)) (x := t) hι
  rw [hcomp.hasDerivAt.deriv]
  rfl

lemma sm_diffAt {f : XT} (hf : Smo f) (x t : ℝ) :
    DifferentiableAt ℝ (fun p : ℝ × ℝ => f p.1 p.2) (x, t) :=
  ((hf.of_le (m := 1) le_top).differentiable_one).differentiableAt

lemma sm_diffAt_x {f : XT} (hf : Smo f) (x t : ℝ) :
    DifferentiableAt ℝ (fun y : ℝ => f y t) x := by
  have hι : HasFDerivAt (fun y : ℝ => (y, t)) (ContinuousLinearMap.inl ℝ ℝ ℝ) x :=
    hasFDerivAt_prodMk_left x t
  have hcomp : HasFDerivAt (fun y : ℝ => f y t)
      ((fderiv ℝ (fun p : ℝ × ℝ => f p.1 p.2) (x, t)).comp
        (ContinuousLinearMap.inl ℝ ℝ ℝ)) x :=
    (sm_diffAt hf x t).hasFDerivAt |>.comp (f := fun y : ℝ => (y, t)) (x := x) hι
  exact hcomp.differentiableAt

lemma sm_diffAt_t {f : XT} (hf : Smo f) (x t : ℝ) :
    DifferentiableAt ℝ (f x) t := by
  have hι : HasFDerivAt (fun s : ℝ => (x, s)) (ContinuousLinearMap.inr ℝ ℝ ℝ) t :=
    hasFDerivAt_prodMk_right x t
  have hcomp : HasFDerivAt (fun s : ℝ => f x s)
      ((fderiv ℝ (fun p : ℝ × ℝ => f p.1 p.2) (x, t)).comp
        (ContinuousLinearMap.inr ℝ ℝ ℝ)) t :=
    (sm_diffAt hf x t).hasFDerivAt |>.comp (f := fun s : ℝ => (x, s)) (x := t) hι
  exact hcomp.differentiableAt

lemma sm_dx {f : XT} (hf : Smo f) : Smo (dx f) := by
  have hbase : ContDiff ℝ ⊤ (fun p : ℝ × ℝ => f p.1 p.2) := hf
  have hderiv : ContDiff ℝ ⊤
      (fun p : ℝ × ℝ => fderiv ℝ (fun q : ℝ × ℝ => f q.1 q.2) p ((1 : ℝ), (0 : ℝ))) :=
    (hbase.fderiv_right (m := ⊤) le_top).clm_apply contDiff_const
  have hEq : (fun p : ℝ × ℝ => dx f p.1 p.2)
      = fun p : ℝ × ℝ => fderiv ℝ (fun q : ℝ × ℝ => f q.1 q.2) p ((1 : ℝ), (0 : ℝ)) := by
    funext p
    obtain ⟨x, t⟩ := p
    exact deriv_slice_x f x t (sm_diffAt hf x t)
  show ContDiff ℝ ⊤ (fun p : ℝ × ℝ => dx f p.1 p.2)
  rw [hEq]
  exact hderiv

lemma sm_dt {f : XT} (hf : Smo f) : Smo (dt f) := by
  have hbase : ContDiff ℝ ⊤ (fun p : ℝ × ℝ => f p.1 p.2) := hf
  have hderiv : ContDiff ℝ ⊤
      (fun p : ℝ × ℝ => fderiv ℝ (fun q : ℝ × ℝ => f q.1 q.2) p ((0 : ℝ), (1 : ℝ))) :=
    (hbase.fderiv_right (m := ⊤) le_top).clm_apply contDiff_const
  have hEq : (fun p : ℝ × ℝ => dt f p.1 p.2)
      = fun p : ℝ × ℝ => fderiv ℝ (fun q : ℝ × ℝ => f q.1 q.2) p ((0 : ℝ), (1 : ℝ)) := by
    funext p
    obtain ⟨x, t⟩ := p
    exact deriv_slice_t f x t (sm_diffAt hf x t)
  show ContDiff ℝ ⊤ (fun p : ℝ × ℝ => dt f p.1 p.2)
  rw [hEq]
  exact hderiv

/-! ### closure of `Smo` -/

lemma sm_add {f g : XT} (hf : Smo f) (hg : Smo g) : Smo (f + g) := ContDiff.add hf hg
lemma sm_sub {f g : XT} (hf : Smo f) (hg : Smo g) : Smo (f - g) := ContDiff.sub hf hg
lemma sm_neg {f : XT} (hf : Smo f) : Smo (-f) := ContDiff.neg hf
lemma sm_mul {f g : XT} (hf : Smo f) (hg : Smo g) : Smo (f * g) := ContDiff.mul hf hg
lemma sm_smul (c : ℝ) {f : XT} (hf : Smo f) : Smo (c • f) := ContDiff.const_smul c hf
lemma sm_div {f : XT} (hf : Smo f) (c : ℝ) : Smo (fun x t => f x t / c) :=
  ContDiff.div_const hf c
lemma sm_const (c : ℝ) : Smo (fun _ _ : ℝ => c) := contDiff_const

lemma sm_pow {f : XT} (hf : Smo f) (n : ℕ) : Smo (f ^ n) := by
  have h : (fun p : ℝ × ℝ => (f ^ n) p.1 p.2) = fun p : ℝ × ℝ => (f p.1 p.2) ^ n := rfl
  show ContDiff ℝ ⊤ (fun p : ℝ × ℝ => (f ^ n) p.1 p.2)
  rw [h]
  exact ContDiff.pow hf n

/-! ### closure of `SmL` -/

lemma smL_add {z w : Lattice} (hz : SmL z) (hw : SmL w) : SmL (z + w) := fun j =>
  sm_add (hz j) (hw j)
lemma smL_sub {z w : Lattice} (hz : SmL z) (hw : SmL w) : SmL (z - w) := fun j =>
  sm_sub (hz j) (hw j)
lemma smL_neg {z : Lattice} (hz : SmL z) : SmL (-z) := fun j => sm_neg (hz j)
lemma smL_mul {z w : Lattice} (hz : SmL z) (hw : SmL w) : SmL (z * w) := fun j =>
  sm_mul (hz j) (hw j)
lemma smL_smul (c : ℝ) {z : Lattice} (hz : SmL z) : SmL (c • z) := fun j =>
  sm_smul c (hz j)
lemma smL_pow {z : Lattice} (hz : SmL z) (n : ℕ) : SmL (z ^ n) := fun j => sm_pow (hz j) n
lemma smL_div {z : Lattice} (hz : SmL z) (c : ℝ) : SmL (fun j x t => z j x t / c) :=
  fun j => sm_div (hz j) c
lemma smL_const (c : ℝ) : SmL (fun _ : ℤ => fun _ _ : ℝ => c) := fun _ => sm_const c

lemma smL_dm (h : ℝ) {z : Lattice} (hz : SmL z) : SmL (dm h z) := fun j =>
  sm_smul (1 / h) (sm_sub (hz j) (hz (j - 1)))
lemma smL_d0 (h : ℝ) {z : Lattice} (hz : SmL z) : SmL (d0 h z) := fun j =>
  sm_smul (1 / (2 * h)) (sm_sub (hz (j + 1)) (hz (j - 1)))
lemma smL_mm {z : Lattice} (hz : SmL z) : SmL (mm z) := fun j =>
  sm_div (sm_add (hz j) (hz (j - 1))) 2
lemma smL_lap (h : ℝ) {z : Lattice} (hz : SmL z) : SmL (lap h z) := fun j =>
  sm_smul (1 / h ^ 2)
    (sm_add (sm_sub (hz (j + 1)) (sm_mul (sm_const 2) (hz j))) (hz (j - 1)))
lemma smL_lx {z : Lattice} (hz : SmL z) : SmL (lx z) := fun j => sm_dx (hz j)
lemma smL_lt {z : Lattice} (hz : SmL z) : SmL (lt z) := fun j => sm_dt (hz j)
lemma smL_lxx {z : Lattice} (hz : SmL z) : SmL (lxx z) := smL_lx (smL_lx hz)

/-- `4 * u` is smooth when `u` is. -/
lemma smL_four_mul {z : Lattice} (hz : SmL z) : SmL (4 * z) := fun j => by
  have h : Smo ((4 : ℝ) • (z j)) := sm_smul (4 : ℝ) (hz j)
  exact h

/-! ## 2. `dx` / `dt` are additive and homogeneous -/

lemma dx_add {f g : XT} (hf : Smo f) (hg : Smo g) : dx (f + g) = dx f + dx g := by
  funext x t
  exact deriv_fun_add (sm_diffAt_x hf x t) (sm_diffAt_x hg x t)

lemma dx_sub {f g : XT} (hf : Smo f) (hg : Smo g) : dx (f - g) = dx f - dx g := by
  funext x t
  exact deriv_fun_sub (sm_diffAt_x hf x t) (sm_diffAt_x hg x t)

lemma dx_smul (c : ℝ) {f : XT} (hf : Smo f) : dx (c • f) = c • dx f := by
  funext x t
  show deriv (fun y : ℝ => c * f y t) x = c * deriv (fun y : ℝ => f y t) x
  exact deriv_const_mul c (sm_diffAt_x hf x t)

lemma dt_add {f g : XT} (hf : Smo f) (hg : Smo g) : dt (f + g) = dt f + dt g := by
  funext x t
  exact deriv_fun_add (sm_diffAt_t hf x t) (sm_diffAt_t hg x t)

lemma dt_sub {f g : XT} (hf : Smo f) (hg : Smo g) : dt (f - g) = dt f - dt g := by
  funext x t
  exact deriv_fun_sub (sm_diffAt_t hf x t) (sm_diffAt_t hg x t)

lemma dt_smul (c : ℝ) {f : XT} (hf : Smo f) : dt (c • f) = c • dt f := by
  funext x t
  show deriv (fun s : ℝ => c * f x s) t = c * deriv (fun s : ℝ => f x s) t
  exact deriv_const_mul c (sm_diffAt_t hf x t)

/-! ## 3. linearity at the lattice level -/

lemma lx_add {z w : Lattice} (hz : SmL z) (hw : SmL w) : lx (z + w) = lx z + lx w :=
  funext fun j => dx_add (hz j) (hw j)
lemma lx_sub {z w : Lattice} (hz : SmL z) (hw : SmL w) : lx (z - w) = lx z - lx w :=
  funext fun j => dx_sub (hz j) (hw j)
lemma lx_smul (c : ℝ) {z : Lattice} (hz : SmL z) : lx (c • z) = c • lx z :=
  funext fun j => dx_smul c (hz j)

lemma lt_add {z w : Lattice} (hz : SmL z) (hw : SmL w) : lt (z + w) = lt z + lt w :=
  funext fun j => dt_add (hz j) (hw j)
lemma lt_sub {z w : Lattice} (hz : SmL z) (hw : SmL w) : lt (z - w) = lt z - lt w :=
  funext fun j => dt_sub (hz j) (hw j)
lemma lt_smul (c : ℝ) {z : Lattice} (hz : SmL z) : lt (c • z) = c • lt z :=
  funext fun j => dt_smul c (hz j)

lemma lxx_add {z w : Lattice} (hz : SmL z) (hw : SmL w) : lxx (z + w) = lxx z + lxx w := by
  show lx (lx (z + w)) = lx (lx z) + lx (lx w)
  rw [lx_add hz hw, lx_add (smL_lx hz) (smL_lx hw)]

lemma lxx_sub {z w : Lattice} (hz : SmL z) (hw : SmL w) : lxx (z - w) = lxx z - lxx w := by
  show lx (lx (z - w)) = lx (lx z) - lx (lx w)
  rw [lx_sub hz hw, lx_sub (smL_lx hz) (smL_lx hw)]

lemma lxx_smul (c : ℝ) {z : Lattice} (hz : SmL z) : lxx (c • z) = c • lxx z := by
  show lx (lx (c • z)) = c • lx (lx z)
  rw [lx_smul c hz, lx_smul c (smL_lx hz)]

/-! ## 4. pure finite-difference algebra -/

lemma dm_add (h : ℝ) (z w : Lattice) : dm h (z + w) = dm h z + dm h w := by
  funext j x t
  simp only [dm, Pi.add_apply, Pi.sub_apply, Pi.smul_apply, smulR]
  ring

lemma dm_sub (h : ℝ) (z w : Lattice) : dm h (z - w) = dm h z - dm h w := by
  funext j x t
  simp only [dm, Pi.sub_apply, Pi.smul_apply, smulR]
  ring

lemma dm_smul (h c : ℝ) (z : Lattice) : dm h (c • z) = c • dm h z := by
  funext j x t
  simp only [dm, Pi.sub_apply, Pi.smul_apply, smulR]
  ring

lemma d0_add (h : ℝ) (z w : Lattice) : d0 h (z + w) = d0 h z + d0 h w := by
  funext j x t
  simp only [d0, Pi.add_apply, Pi.sub_apply, Pi.smul_apply, smulR]
  ring

lemma d0_sub (h : ℝ) (z w : Lattice) : d0 h (z - w) = d0 h z - d0 h w := by
  funext j x t
  simp only [d0, Pi.sub_apply, Pi.smul_apply, smulR]
  ring

lemma d0_smul (h c : ℝ) (z : Lattice) : d0 h (c • z) = c • d0 h z := by
  funext j x t
  simp only [d0, Pi.sub_apply, Pi.smul_apply, smulR]
  ring

lemma mm_add (z w : Lattice) : mm (z + w) = mm z + mm w := by
  funext j x t
  simp only [mm, Pi.add_apply, Pi.div_apply, Pi.ofNat_apply, smulR]
  ring

lemma mm_sub (z w : Lattice) : mm (z - w) = mm z - mm w := by
  funext j x t
  simp only [mm, Pi.add_apply, Pi.sub_apply, Pi.div_apply, Pi.ofNat_apply, smulR]
  ring

lemma mm_smul (c : ℝ) (z : Lattice) : mm (c • z) = c • mm z := by
  funext j x t
  simp only [mm, Pi.add_apply, Pi.div_apply, Pi.smul_apply, Pi.ofNat_apply, smulR]
  ring

lemma lap_add (h : ℝ) (z w : Lattice) : lap h (z + w) = lap h z + lap h w := by
  funext j x t
  simp only [lap, Pi.add_apply, Pi.sub_apply, Pi.mul_apply, Pi.smul_apply, Pi.ofNat_apply, smulR]
  ring

lemma lap_sub (h : ℝ) (z w : Lattice) : lap h (z - w) = lap h z - lap h w := by
  funext j x t
  simp only [lap, Pi.add_apply, Pi.sub_apply, Pi.mul_apply, Pi.smul_apply, Pi.ofNat_apply, smulR]
  ring

lemma lap_smul (h c : ℝ) (z : Lattice) : lap h (c • z) = c • lap h z := by
  funext j x t
  simp only [lap, Pi.add_apply, Pi.sub_apply, Pi.mul_apply, Pi.smul_apply, Pi.ofNat_apply, smulR]
  ring

lemma mm_neg (z : Lattice) : mm (-z) = -mm z := by
  funext j x t
  simp only [mm, Pi.add_apply, Pi.neg_apply, Pi.div_apply, Pi.ofNat_apply, smulR]
  ring

lemma mm_eq (z : Lattice) : mm z = (1 / 2 : ℝ) • (z + fun j => z (j - 1)) := by
  funext j x t
  simp only [mm, Pi.add_apply, Pi.div_apply, Pi.smul_apply, Pi.ofNat_apply, smulR]
  ring

lemma lxx_shm (z : Lattice) : lxx (fun j => z (j - 1)) = fun j => lxx z (j - 1) := rfl
lemma lxx_sh1 (z : Lattice) : lxx (fun j => z (j + 1)) = fun j => lxx z (j + 1) := rfl

/-! ## 5. `mm` versus `lxx`, and `lt` versus `d0` -/

lemma mm_lxx {z : Lattice} (hz : SmL z) : mm (lxx z) = lxx (mm z) := by
  have hzs : SmL (z + fun j => z (j - 1)) := smL_add hz (fun j => hz (j - 1))
  calc mm (lxx z) = (1 / 2 : ℝ) • (lxx z + fun j => lxx z (j - 1)) := mm_eq (lxx z)
    _ = (1 / 2 : ℝ) • (lxx z + lxx (fun j => z (j - 1))) := by rw [lxx_shm]
    _ = (1 / 2 : ℝ) • lxx (z + fun j => z (j - 1)) := by
          rw [lxx_add hz (fun j => hz (j - 1))]
    _ = lxx ((1 / 2 : ℝ) • (z + fun j => z (j - 1))) := by rw [lxx_smul (1 / 2) hzs]
    _ = lxx (mm z) := by rw [mm_eq z]

lemma lt_d0 (h : ℝ) {z : Lattice} (hz : SmL z) : lt (d0 h z) = d0 h (lt z) := by
  funext j x t
  have hsub : DifferentiableAt ℝ (fun s : ℝ => z (j + 1) x s - z (j - 1) x s) t :=
    (sm_diffAt_t (hz (j + 1)) x t).sub (sm_diffAt_t (hz (j - 1)) x t)
  show deriv (fun s : ℝ => (1 / (2 * h)) * (z (j + 1) x s - z (j - 1) x s)) t
      = (1 / (2 * h)) • (deriv (fun s : ℝ => z (j + 1) x s) t
          - deriv (fun s : ℝ => z (j - 1) x s) t)
  rw [deriv_const_mul (1 / (2 * h)) hsub,
    deriv_fun_sub (sm_diffAt_t (hz (j + 1)) x t) (sm_diffAt_t (hz (j - 1)) x t), smulR]

/-! ## 6. the `ε`-scaling of `n1` and `n2` -/

/-- quadratic part of `H`. -/
def quadH (h : ℝ) (u v : Lattice) : Lattice :=
  u ^ 2 / 2 + h ^ 2 • ((W h u v) ^ 2 / 32)

lemma W_smul (h ε : ℝ) (u v : Lattice) : W h (ε • u) (ε • v) = ε • W h u v := by
  funext j x t
  simp only [W, d0, Pi.sub_apply, Pi.smul_apply, smulR]
  ring

lemma H_smul (a h ε : ℝ) (u v : Lattice) :
    H a h (ε • u) (ε • v) = ε ^ 2 • quadH h u v + ε • linearH a h u v := by
  funext j x t
  simp only [H, quadH, linearH, W, d0, Pi.add_apply, Pi.sub_apply, Pi.mul_apply,
    Pi.div_apply, Pi.pow_apply, Pi.smul_apply, Pi.ofNat_apply, smulR]
  ring

lemma deriv_eps (A B : ℝ) : deriv (fun ε : ℝ => ε * A + ε ^ 2 * B) 0 = A := by
  have h1 : HasDerivAt (fun ε : ℝ => ε * A) A 0 := by
    simpa using (hasDerivAt_id (0 : ℝ)).mul_const A
  have h2 : HasDerivAt (fun ε : ℝ => ε ^ 2 * B) 0 0 := by
    simpa using (((hasDerivAt_id (0 : ℝ)).pow 2).mul_const B)
  have h3 : HasDerivAt (fun ε : ℝ => ε * A + ε ^ 2 * B) (A + 0) 0 := h1.add h2
  rw [h3.deriv, add_zero]

/-- The lattice operators `dm`, `lx` are additive, so the `ε`-expansion of `n1`. -/
lemma n1_smul_decomp (a h ε : ℝ) (u v : Lattice) (hu : SmL u) (hv : SmL v) :
    n1 a h (ε • u) (ε • v)
      = ε • linearN1 a h u v + ε ^ 2 • dm h (lx (quadH h u v)) := by
  have hW : SmL (W h u v) := smL_sub hv (smL_d0 h hu)
  have hQ : SmL (quadH h u v) :=
    smL_add (smL_div (smL_pow hu 2) 2) (smL_smul (h ^ 2) (smL_div (smL_pow hW 2) 32))
  have hL : SmL (linearH a h u v) :=
    smL_sub (smL_smul (2 * a) hu) (smL_smul (h ^ 2 / 4) hW)
  have hε2Q : SmL (ε ^ 2 • quadH h u v) := smL_smul (ε ^ 2) hQ
  have hεL : SmL (ε • linearH a h u v) := smL_smul ε hL
  have hX : SmL (mm v - (h ^ 2 / 4) • lap h (dm h u)) :=
    smL_sub (smL_mm hv) (smL_smul (h ^ 2 / 4) (smL_lap h (smL_dm h hu)))
  have h1 : lt (ε • u) + lx (H a h (ε • u) (ε • v))
      = ε • (lt u + lx (linearH a h u v)) + ε ^ 2 • lx (quadH h u v) := by
    rw [H_smul, lt_smul (z := u) ε hu, lx_add (z := ε ^ 2 • quadH h u v)
        (w := ε • linearH a h u v) hε2Q hεL,
      lx_smul (z := quadH h u v) (ε ^ 2) hQ, lx_smul (z := linearH a h u v) ε hL,
      smul_add]
    abel
  have h2 : mm (ε • v) - (h ^ 2 / 4) • lap h (dm h (ε • u))
      = ε • (mm v - (h ^ 2 / 4) • lap h (dm h u)) := by
    funext j x t
    simp only [mm, dm, lap, Pi.sub_apply, Pi.add_apply, Pi.div_apply, Pi.mul_apply,
      Pi.smul_apply, Pi.ofNat_apply, smulR]
    ring
  calc n1 a h (ε • u) (ε • v)
      = dm h (ε • (lt u + lx (linearH a h u v)) + ε ^ 2 • lx (quadH h u v))
          + lxx (ε • (mm v - (h ^ 2 / 4) • lap h (dm h u))) := by
        simp only [n1]
        rw [h1, h2]
    _ = ε • linearN1 a h u v + ε ^ 2 • dm h (lx (quadH h u v)) := by
        rw [dm_add, dm_smul, dm_smul,
          lxx_smul (z := mm v - (h ^ 2 / 4) • lap h (dm h u)) ε hX]
        simp only [linearN1, smul_add]
        abel

lemma n2_smul_decomp (a h ε : ℝ) (u v : Lattice) (hu : SmL u) (hv : SmL v) :
    n2 a h (ε • u) (ε • v)
      = ε • linearN2 a h u v
        + ε ^ 2 • lx (d0 h (quadH h u v) + u * W h u v) := by
  have hW : SmL (W h u v) := smL_sub hv (smL_d0 h hu)
  have hQ : SmL (quadH h u v) :=
    smL_add (smL_div (smL_pow hu 2) 2) (smL_smul (h ^ 2) (smL_div (smL_pow hW 2) 32))
  have hL : SmL (linearH a h u v) :=
    smL_sub (smL_smul (2 * a) hu) (smL_smul (h ^ 2 / 4) hW)
  have h4u : SmL (4 * u) := smL_four_mul hu
  have hP : SmL (d0 h (quadH h u v) + u * W h u v) :=
    smL_add (smL_d0 h hQ) (smL_mul hu hW)
  have hR : SmL (d0 h (linearH a h u v) + (2 * a) • (W h u v) - 4 * u) :=
    smL_sub (smL_add (smL_d0 h hL) (smL_smul (2 * a) hW)) h4u
  have hS : SmL (d0 h u + (h ^ 2 / 4) • lap h (W h u v)) :=
    smL_add (smL_d0 h hu) (smL_smul (h ^ 2 / 4) (smL_lap h hW))
  have hε2P : SmL (ε ^ 2 • (d0 h (quadH h u v) + u * W h u v)) := smL_smul (ε ^ 2) hP
  have hεR : SmL (ε • (d0 h (linearH a h u v) + (2 * a) • (W h u v) - 4 * u)) :=
    smL_smul ε hR
  have hE : d0 h (H a h (ε • u) (ε • v))
        + (ε • u + (fun _ _ _ => 2 * a)) * W h (ε • u) (ε • v) - 4 * (ε • u)
      = ε ^ 2 • (d0 h (quadH h u v) + u * W h u v)
        + ε • (d0 h (linearH a h u v) + (2 * a) • (W h u v) - 4 * u) := by
    funext j x t
    simp only [H, quadH, linearH, W, d0, Pi.add_apply, Pi.sub_apply, Pi.mul_apply,
      Pi.div_apply, Pi.pow_apply, Pi.smul_apply, Pi.ofNat_apply, smulR]
    ring
  have hF : d0 h (ε • u) + (h ^ 2 / 4) • lap h (W h (ε • u) (ε • v))
      = ε • (d0 h u + (h ^ 2 / 4) • lap h (W h u v)) := by
    funext j x t
    simp only [W, d0, lap, Pi.add_apply, Pi.sub_apply, Pi.mul_apply, Pi.smul_apply,
      Pi.ofNat_apply, smulR]
    ring
  calc n2 a h (ε • u) (ε • v)
      = lt (ε • v)
          + lx (ε ^ 2 • (d0 h (quadH h u v) + u * W h u v)
                + ε • (d0 h (linearH a h u v) + (2 * a) • (W h u v) - 4 * u))
          + lxx (ε • (d0 h u + (h ^ 2 / 4) • lap h (W h u v))) := by
        simp only [n2]
        rw [hE, hF]
    _ = ε • linearN2 a h u v + ε ^ 2 • lx (d0 h (quadH h u v) + u * W h u v) := by
        rw [lt_smul (z := v) ε hv,
          lx_add (z := ε ^ 2 • (d0 h (quadH h u v) + u * W h u v))
            (w := ε • (d0 h (linearH a h u v) + (2 * a) • (W h u v) - 4 * u)) hε2P hεR,
          lx_smul (z := d0 h (quadH h u v) + u * W h u v) (ε ^ 2) hP,
          lx_smul (z := d0 h (linearH a h u v) + (2 * a) • (W h u v) - 4 * u) ε hR,
          lxx_smul (z := d0 h u + (h ^ 2 / 4) • lap h (W h u v)) ε hS]
        simp only [linearN2, smul_add]
        abel

theorem c25_proved : C25 := by
  intro a h u v hh hu hv j x t
  constructor
  · have hkey : (fun ε : ℝ => n1 a h (ε • u) (ε • v) j x t)
        = fun ε : ℝ =>
            ε * linearN1 a h u v j x t + ε ^ 2 * (dm h (lx (quadH h u v)) j x t) := by
      funext ε
      have h := congrArg (fun w : Lattice => w j x t) (n1_smul_decomp a h ε u v hu hv)
      simpa only [Pi.add_apply, Pi.smul_apply, smulR] using h
    rw [hkey]
    exact deriv_eps _ _
  · have hkey : (fun ε : ℝ => n2 a h (ε • u) (ε • v) j x t)
        = fun ε : ℝ =>
            ε * linearN2 a h u v j x t
              + ε ^ 2 * (lx (d0 h (quadH h u v) + u * W h u v) j x t) := by
      funext ε
      have h := congrArg (fun w : Lattice => w j x t) (n2_smul_decomp a h ε u v hu hv)
      simpa only [Pi.add_apply, Pi.smul_apply, smulR] using h
    rw [hkey]
    exact deriv_eps _ _

/-! ## 7. periodic closure and telescoping sums -/

lemma per_add {m : ℕ} {z w : Lattice} (hz : PeriodicL m z) (hw : PeriodicL m w) :
    PeriodicL m (z + w) := fun j => by
  change z (j + (m : ℤ)) + w (j + (m : ℤ)) = z j + w j
  rw [hz j, hw j]

lemma per_sub {m : ℕ} {z w : Lattice} (hz : PeriodicL m z) (hw : PeriodicL m w) :
    PeriodicL m (z - w) := fun j => by
  change z (j + (m : ℤ)) - w (j + (m : ℤ)) = z j - w j
  rw [hz j, hw j]

lemma per_smul {m : ℕ} (c : ℝ) {z : Lattice} (hz : PeriodicL m z) :
    PeriodicL m (c • z) := fun j => by
  change c • z (j + (m : ℤ)) = c • z j
  rw [hz j]

lemma per_pow {m : ℕ} {z : Lattice} (hz : PeriodicL m z) (n : ℕ) :
    PeriodicL m (z ^ n) := fun j => by
  change (z (j + (m : ℤ))) ^ n = (z j) ^ n
  rw [hz j]

lemma per_dm {m : ℕ} (h : ℝ) {z : Lattice} (hz : PeriodicL m z) :
    PeriodicL m (dm h z) := fun j => by
  have h2 : z (j + (m : ℤ) - 1) = z (j - 1) := by
    have h1 : j + (m : ℤ) - 1 = (j - 1) + (m : ℤ) := by ring
    rw [h1, hz (j - 1)]
  have h3 : z (j + (m : ℤ)) = z j := hz j
  change dm h z (j + (m : ℤ)) = dm h z j
  simp only [dm]
  rw [h3, h2]

lemma per_d0 {m : ℕ} (h : ℝ) {z : Lattice} (hz : PeriodicL m z) :
    PeriodicL m (d0 h z) := fun j => by
  have h1 : z (j + (m : ℤ) + 1) = z (j + 1) := by
    have hh : j + (m : ℤ) + 1 = (j + 1) + (m : ℤ) := by ring
    rw [hh, hz (j + 1)]
  have h2 : z (j + (m : ℤ) - 1) = z (j - 1) := by
    have hh : j + (m : ℤ) - 1 = (j - 1) + (m : ℤ) := by ring
    rw [hh, hz (j - 1)]
  change d0 h z (j + (m : ℤ)) = d0 h z j
  simp only [d0]
  rw [h1, h2]

lemma per_mm {m : ℕ} {z : Lattice} (hz : PeriodicL m z) : PeriodicL m (mm z) := fun j => by
  have h2 : z (j + (m : ℤ) - 1) = z (j - 1) := by
    have hh : j + (m : ℤ) - 1 = (j - 1) + (m : ℤ) := by ring
    rw [hh, hz (j - 1)]
  change mm z (j + (m : ℤ)) = mm z j
  simp only [mm]
  rw [hz j, h2]

lemma per_lap {m : ℕ} (h : ℝ) {z : Lattice} (hz : PeriodicL m z) :
    PeriodicL m (lap h z) := fun j => by
  have h1 : z (j + (m : ℤ) + 1) = z (j + 1) := by
    have hh : j + (m : ℤ) + 1 = (j + 1) + (m : ℤ) := by ring
    rw [hh, hz (j + 1)]
  have h2 : z (j + (m : ℤ) - 1) = z (j - 1) := by
    have hh : j + (m : ℤ) - 1 = (j - 1) + (m : ℤ) := by ring
    rw [hh, hz (j - 1)]
  change lap h z (j + (m : ℤ)) = lap h z j
  simp only [lap]
  rw [h1, hz j, h2]

lemma per_lt {m : ℕ} {z : Lattice} (hz : PeriodicL m z) : PeriodicL m (lt z) := fun j => by
  show dt (z (j + (m : ℤ))) = dt (z j)
  exact congrArg dt (hz j)

lemma per_lx {m : ℕ} {z : Lattice} (hz : PeriodicL m z) : PeriodicL m (lx z) := fun j => by
  show dx (z (j + (m : ℤ))) = dx (z j)
  exact congrArg dx (hz j)

lemma per_H {m : ℕ} (a h : ℝ) {u v : Lattice} (hu : PeriodicL m u) (hv : PeriodicL m v) :
    PeriodicL m (H a h u v) := by
  have hW : PeriodicL m (W h u v) := per_sub hv (per_d0 h hu)
  intro j
  have e0 : u (j + (m : ℤ)) = u j := hu j
  have e2 : W h u v (j + (m : ℤ)) = W h u v j := hW j
  change H a h u v (j + (m : ℤ)) = H a h u v j
  funext x t
  simp only [H, Pi.add_apply, Pi.sub_apply, Pi.mul_apply, Pi.div_apply, Pi.pow_apply,
    Pi.smul_apply, Pi.ofNat_apply, smulR]
  rw [e0, e2]

/-- telescoping sum of a finite difference. -/
lemma sum_range_telescope {M : Type*} [AddCommGroup M] (f : ℕ → M) (n : ℕ) :
    ∑ i ∈ Finset.range n, (f (i + 1) - f i) = f n - f 0 := by
  induction n with
  | zero => simp
  | succ n ih => rw [Finset.sum_range_succ, ih]; abel

lemma sum_shift_pos (m : ℕ) (G : Lattice) (hG : PeriodicL m G) :
    ∑ j ∈ Finset.range m, G ((j : ℤ) + 1) = ∑ j ∈ Finset.range m, G (j : ℤ) := by
  have h := sum_range_telescope (fun j : ℕ => G (j : ℤ)) m
  have hGm : G ((m : ℤ)) = G (((0 : ℕ) : ℤ)) := by simpa using hG 0
  have hnat : ∑ j ∈ Finset.range m, (G (((j + 1 : ℕ) : ℤ)) - G ((j : ℤ))) = 0 := by
    rw [h, hGm, sub_self]
  have key : ∑ j ∈ Finset.range m, (G ((j : ℤ) + 1) - G (j : ℤ)) = 0 := by
    rw [show (∑ j ∈ Finset.range m, (G ((j : ℤ) + 1) - G (j : ℤ)))
        = ∑ j ∈ Finset.range m, (G (((j + 1 : ℕ) : ℤ)) - G ((j : ℤ))) from
      Finset.sum_congr rfl (fun j _ => by
        show G ((j : ℤ) + 1) - G (j : ℤ) = G (((j + 1 : ℕ) : ℤ)) - G ((j : ℤ))
        rw [show (((j + 1 : ℕ) : ℤ)) = (j : ℤ) + 1 from by omega])]
    exact hnat
  rw [Finset.sum_sub_distrib] at key
  exact sub_eq_zero.mp key

lemma sum_shift_neg (m : ℕ) (G : Lattice) (hG : PeriodicL m G) :
    ∑ j ∈ Finset.range m, G ((j : ℤ) - 1) = ∑ j ∈ Finset.range m, G (j : ℤ) := by
  have h := sum_range_telescope (fun j : ℕ => G ((j : ℤ) - 1)) m
  have hm : G ((m : ℤ) - 1) = G (-1) := by
    have h1 := hG (-1)
    rwa [show (-1 : ℤ) + (m : ℤ) = (m : ℤ) - 1 from by ring] at h1
  have h0 : G (((0 : ℕ) : ℤ) - 1) = G (-1) := by
    rw [show (((0 : ℕ) : ℤ) - 1) = (-1 : ℤ) from by norm_num]
  have hnat : ∑ j ∈ Finset.range m, (G (((j + 1 : ℕ) : ℤ) - 1) - G ((j : ℤ) - 1)) = 0 := by
    rw [h, hm, h0, sub_self]
  have key : ∑ j ∈ Finset.range m, (G (j : ℤ) - G ((j : ℤ) - 1)) = 0 := by
    rw [show (∑ j ∈ Finset.range m, (G (j : ℤ) - G ((j : ℤ) - 1)))
        = ∑ j ∈ Finset.range m, (G (((j + 1 : ℕ) : ℤ) - 1) - G ((j : ℤ) - 1)) from
      Finset.sum_congr rfl (fun j _ => by
        show G (j : ℤ) - G ((j : ℤ) - 1) = G (((j + 1 : ℕ) : ℤ) - 1) - G ((j : ℤ) - 1)
        rw [show (((j + 1 : ℕ) : ℤ) - 1) = (j : ℤ) from by omega])]
    exact hnat
  rw [Finset.sum_sub_distrib] at key
  exact (sub_eq_zero.mp key).symm

lemma sum_dm_periodic (m : ℕ) (h : ℝ) (Z : Lattice) (hZ : PeriodicL m Z) :
    ∑ j ∈ Finset.range m, dm h Z (j : ℤ) = 0 := by
  have hshift : ∑ j ∈ Finset.range m, Z ((j : ℤ) - 1) = ∑ j ∈ Finset.range m, Z (j : ℤ) :=
    sum_shift_neg m Z hZ
  have h3 : ∑ j ∈ Finset.range m, dm h Z (j : ℤ)
      = (1 / h) • ∑ j ∈ Finset.range m, (Z (j : ℤ) - Z ((j : ℤ) - 1)) := by
    rw [Finset.smul_sum]
    rfl
  rw [h3, Finset.sum_sub_distrib, hshift, sub_self, smul_zero]

lemma sum_lap_periodic (m : ℕ) (h : ℝ) (G : Lattice) (hG : PeriodicL m G) :
    ∑ j ∈ Finset.range m, lap h G (j : ℤ) = 0 := by
  have hp : ∑ j ∈ Finset.range m, G ((j : ℤ) + 1) = ∑ j ∈ Finset.range m, G (j : ℤ) :=
    sum_shift_pos m G hG
  have hn : ∑ j ∈ Finset.range m, G ((j : ℤ) - 1) = ∑ j ∈ Finset.range m, G (j : ℤ) :=
    sum_shift_neg m G hG
  have h3 : ∑ j ∈ Finset.range m, lap h G (j : ℤ)
      = (1 / h ^ 2) •
          ∑ j ∈ Finset.range m, (G ((j : ℤ) + 1) - 2 * G (j : ℤ) + G ((j : ℤ) - 1)) := by
    rw [Finset.smul_sum]
    rfl
  rw [h3]
  have h4 : ∑ j ∈ Finset.range m, (G ((j : ℤ) + 1) - 2 * G (j : ℤ) + G ((j : ℤ) - 1)) = 0 := by
    rw [Finset.sum_add_distrib, Finset.sum_sub_distrib, hp, hn, ← Finset.mul_sum]
    funext x t
    simp only [Pi.add_apply, Pi.sub_apply, Pi.mul_apply, Pi.ofNat_apply, smulR]
    ring
  rw [h4, smul_zero]

/-! ## 8. `x`-differentiation commutes with finite sums -/

lemma dx_sum {ι : Type*} (s : Finset ι) (F : ι → XT) (hF : ∀ i ∈ s, Smo (F i)) :
    dx (∑ i ∈ s, F i) = ∑ i ∈ s, dx (F i) := by
  funext x t
  simp only [dx, Finset.sum_apply]
  exact deriv_fun_sum (u := s) (A := fun i y => F i y t)
    (fun i hi => sm_diffAt_x (hF i hi) x t)

lemma xx_sum {ι : Type*} (s : Finset ι) (F : ι → XT) (hF : ∀ i ∈ s, Smo (F i)) :
    xx (∑ i ∈ s, F i) = ∑ i ∈ s, xx (F i) := by
  show dx (dx (∑ i ∈ s, F i)) = ∑ i ∈ s, dx (dx (F i))
  rw [dx_sum s F hF, dx_sum s (fun i => dx (F i)) (fun i hi => sm_dx (hF i hi))]

/-! ## 9. C20 - periodic summing gives only a compatibility constraint -/

theorem c20_proved : C20 := by
  intro m a h u v hm hh hu hv hpu hpv hnp
  have hW : SmL (W h u v) := smL_sub hv (smL_d0 h hu)
  have hZper : PeriodicL m (lt u + lx (H a h u v)) :=
    per_add (per_lt hpu) (per_lx (per_H a h hpu hpv))
  have hW' : SmL (mm v - (h ^ 2 / 4) • lap h (dm h u)) :=
    smL_sub (smL_mm hv) (smL_smul (h ^ 2 / 4) (smL_lap h (smL_dm h hu)))
  have hn1 : n1 a h u v = 0 := hnp.1
  have hsum0 : ∑ j ∈ Finset.range m, n1 a h u v (j : ℤ) = 0 := by
    rw [hn1]
    simp
  have hsplit : ∑ j ∈ Finset.range m, n1 a h u v (j : ℤ)
      = (∑ j ∈ Finset.range m, dm h (lt u + lx (H a h u v)) (j : ℤ))
        + ∑ j ∈ Finset.range m, lxx (mm v - (h ^ 2 / 4) • lap h (dm h u)) (j : ℤ) := by
    have h1 : ∀ j : ℕ, n1 a h u v (j : ℤ)
        = dm h (lt u + lx (H a h u v)) (j : ℤ)
          + lxx (mm v - (h ^ 2 / 4) • lap h (dm h u)) (j : ℤ) := by
      intro j
      simp only [n1, Pi.add_apply]
    calc ∑ j ∈ Finset.range m, n1 a h u v (j : ℤ)
        = ∑ j ∈ Finset.range m, (dm h (lt u + lx (H a h u v)) (j : ℤ)
            + lxx (mm v - (h ^ 2 / 4) • lap h (dm h u)) (j : ℤ)) :=
          Finset.sum_congr rfl (fun j _ => h1 j)
      _ = (∑ j ∈ Finset.range m, dm h (lt u + lx (H a h u v)) (j : ℤ))
          + ∑ j ∈ Finset.range m, lxx (mm v - (h ^ 2 / 4) • lap h (dm h u)) (j : ℤ) :=
          Finset.sum_add_distrib
  have hdm0 : ∑ j ∈ Finset.range m, dm h (lt u + lx (H a h u v)) (j : ℤ) = 0 :=
    sum_dm_periodic m h _ hZper
  have hlxx0 : ∑ j ∈ Finset.range m, lxx (mm v - (h ^ 2 / 4) • lap h (dm h u)) (j : ℤ) = 0 := by
    have h1 : (∑ j ∈ Finset.range m, dm h (lt u + lx (H a h u v)) (j : ℤ))
        + (∑ j ∈ Finset.range m,
            lxx (mm v - (h ^ 2 / 4) • lap h (dm h u)) (j : ℤ)) = 0 := by
      rw [← hsplit, hsum0]
    rw [hdm0, zero_add] at h1
    exact h1
  have hxx0 : xx (∑ j ∈ Finset.range m, (mm v - (h ^ 2 / 4) • lap h (dm h u)) (j : ℤ)) = 0 := by
    rw [xx_sum (Finset.range m)
      (fun j : ℕ => (mm v - (h ^ 2 / 4) • lap h (dm h u)) (j : ℤ))
      (fun j _ => hW' j)]
    simpa only [xx, lxx, lx] using hlxx0
  have hmm : ∑ j ∈ Finset.range m, mm v (j : ℤ) = ∑ j ∈ Finset.range m, v (j : ℤ) := by
    have hshift : ∑ j ∈ Finset.range m, v ((j : ℤ) - 1) = ∑ j ∈ Finset.range m, v (j : ℤ) :=
      sum_shift_neg m v hpv
    have h1 : ∀ j : ℕ, mm v (j : ℤ) = (1 / 2 : ℝ) • (v (j : ℤ) + v ((j : ℤ) - 1)) := by
      intro j
      have hc := congrFun (mm_eq v) (j : ℤ)
      simpa only [Pi.smul_apply, Pi.add_apply] using hc
    calc ∑ j ∈ Finset.range m, mm v (j : ℤ)
        = ∑ j ∈ Finset.range m, (1 / 2 : ℝ) • (v (j : ℤ) + v ((j : ℤ) - 1)) :=
          Finset.sum_congr rfl (fun j _ => h1 j)
      _ = (1 / 2 : ℝ) • ∑ j ∈ Finset.range m, (v (j : ℤ) + v ((j : ℤ) - 1)) := by
          rw [Finset.smul_sum]
      _ = (1 / 2 : ℝ) •
            ((∑ j ∈ Finset.range m, v (j : ℤ))
              + ∑ j ∈ Finset.range m, v ((j : ℤ) - 1)) := by
          rw [Finset.sum_add_distrib]
      _ = (1 / 2 : ℝ) •
            ((∑ j ∈ Finset.range m, v (j : ℤ)) + ∑ j ∈ Finset.range m, v (j : ℤ)) := by
          rw [hshift]
      _ = ∑ j ∈ Finset.range m, v (j : ℤ) := by
          rw [smul_add, ← add_smul, show (1 / 2 : ℝ) + 1 / 2 = 1 by norm_num, one_smul]
  have hlap : ∑ j ∈ Finset.range m, lap h (dm h u) (j : ℤ) = 0 :=
    sum_lap_periodic m h (dm h u) (per_dm h hpu)
  have hW'sum : ∑ j ∈ Finset.range m, (mm v - (h ^ 2 / 4) • lap h (dm h u)) (j : ℤ)
      = ∑ j ∈ Finset.range m, v (j : ℤ) := by
    have hsub : ∑ j ∈ Finset.range m, (mm v - (h ^ 2 / 4) • lap h (dm h u)) (j : ℤ)
        = (∑ j ∈ Finset.range m, mm v (j : ℤ))
          - (h ^ 2 / 4) • (∑ j ∈ Finset.range m, lap h (dm h u) (j : ℤ)) := by
      have h1 : ∀ j : ℕ, (mm v - (h ^ 2 / 4) • lap h (dm h u)) (j : ℤ)
          = mm v (j : ℤ) - (h ^ 2 / 4) • lap h (dm h u) (j : ℤ) := by
        intro j
        simp only [Pi.sub_apply, Pi.smul_apply]
      calc ∑ j ∈ Finset.range m, (mm v - (h ^ 2 / 4) • lap h (dm h u)) (j : ℤ)
          = ∑ j ∈ Finset.range m,
              (mm v (j : ℤ) - (h ^ 2 / 4) • lap h (dm h u) (j : ℤ)) :=
            Finset.sum_congr rfl (fun j _ => h1 j)
        _ = (∑ j ∈ Finset.range m, mm v (j : ℤ))
            - ∑ j ∈ Finset.range m, (h ^ 2 / 4) • lap h (dm h u) (j : ℤ) := by
            rw [Finset.sum_sub_distrib]
        _ = (∑ j ∈ Finset.range m, mm v (j : ℤ))
            - (h ^ 2 / 4) • (∑ j ∈ Finset.range m, lap h (dm h u) (j : ℤ)) := by
            rw [Finset.smul_sum]
    rw [hsub, hmm, hlap, smul_zero, sub_zero]
  rw [hW'sum] at hxx0
  exact hxx0

/-! ## 10. shifts, the C19 operator identities, and C19 -/

/-- the constant lattice `2a`. -/
def CC (a : ℝ) : Lattice := fun _ _ _ => 2 * a

/-- forward shift. -/
def Sh (z : Lattice) : Lattice := fun j => z (j + 1)

/-- backward shift. -/
def Shb (z : Lattice) : Lattice := fun j => z (j - 1)

lemma iz_add_sub (a b : ℤ) : a + b - b = a := by ring
lemma iz_sub_add (a b : ℤ) : a - b + b = a := by ring

lemma smL_Sh {z : Lattice} (hz : SmL z) : SmL (Sh z) := fun j => hz (j + 1)
lemma smL_Shb {z : Lattice} (hz : SmL z) : SmL (Shb z) := fun j => hz (j - 1)

lemma Sh_add (z w : Lattice) : Sh (z + w) = Sh z + Sh w := by funext j; rfl
lemma Sh_sub (z w : Lattice) : Sh (z - w) = Sh z - Sh w := by funext j; rfl
lemma Sh_neg (z : Lattice) : Sh (-z) = -Sh z := by funext j; rfl
lemma Sh_smul (c : ℝ) (z : Lattice) : Sh (c • z) = c • Sh z := by funext j; rfl
lemma Shb_add (z w : Lattice) : Shb (z + w) = Shb z + Shb w := by funext j; rfl
lemma Shb_sub (z w : Lattice) : Shb (z - w) = Shb z - Shb w := by funext j; rfl
lemma Shb_neg (z : Lattice) : Shb (-z) = -Shb z := by funext j; rfl
lemma Shb_smul (c : ℝ) (z : Lattice) : Shb (c • z) = c • Shb z := by funext j; rfl

lemma Sh_Shb (z : Lattice) : Sh (Shb z) = z := by
  funext j
  have h : (j : ℤ) + 1 - 1 = j := by ring
  simp only [Sh, Shb, h]

lemma Shb_Sh (z : Lattice) : Shb (Sh z) = z := by
  funext j
  have h : (j : ℤ) - 1 + 1 = j := by ring
  simp only [Sh, Shb, h]

lemma Sh_lx (z : Lattice) : Sh (lx z) = lx (Sh z) := by funext j; rfl
lemma Shb_lx (z : Lattice) : Shb (lx z) = lx (Shb z) := by funext j; rfl
lemma lxx_Sh (z : Lattice) : lxx (Sh z) = Sh (lxx z) := by funext j; rfl

lemma d0_eq (h : ℝ) (z : Lattice) : d0 h z = (1 / (2 * h)) • (Sh z - Shb z) := by
  funext j x t
  simp only [d0, Sh, Shb, Pi.sub_apply, Pi.smul_apply, smulR]

lemma Sh_mm (z : Lattice) : Sh (mm z) = mm (Sh z) := by
  funext j x t
  simp only [Sh, mm, Pi.add_apply, Pi.div_apply, Pi.ofNat_apply, smulR,
    iz_add_sub, iz_sub_add]

lemma Shb_mm (z : Lattice) : Shb (mm z) = mm (Shb z) := by
  funext j x t
  simp only [Shb, mm, Pi.add_apply, Pi.div_apply, Pi.ofNat_apply, smulR,
    iz_add_sub, iz_sub_add]

lemma Sh_mm_lxx {X : Lattice} (hX : SmL X) : Sh (mm (lxx X)) = lxx (Sh (mm X)) := by
  rw [Sh_mm, ← lxx_Sh, mm_lxx (smL_Sh hX), ← Sh_mm]

lemma d0_lx (h : ℝ) {z : Lattice} (hz : SmL z) : d0 h (lx z) = lx (d0 h z) := by
  have h1 : SmL (Sh z) := smL_Sh hz
  have h2 : SmL (Shb z) := smL_Shb hz
  have h3 : SmL (Sh z - Shb z) := smL_sub h1 h2
  calc d0 h (lx z) = (1 / (2 * h)) • (Sh (lx z) - Shb (lx z)) := d0_eq h (lx z)
    _ = (1 / (2 * h)) • (lx (Sh z) - lx (Shb z)) := by rw [Sh_lx, Shb_lx]
    _ = (1 / (2 * h)) • lx (Sh z - Shb z) := by rw [lx_sub h1 h2]
    _ = lx ((1 / (2 * h)) • (Sh z - Shb z)) := by
          rw [lx_smul (z := Sh z - Shb z) (1 / (2 * h)) h3]
    _ = lx (d0 h z) := by rw [d0_eq h z]

lemma smL_H (a h : ℝ) {u v : Lattice} (hu : SmL u) (hv : SmL v) : SmL (H a h u v) := by
  have hW : SmL (W h u v) := smL_sub hv (smL_d0 h hu)
  exact smL_add (smL_add (smL_div (smL_pow hu 2) 2) (smL_smul (2 * a) hu))
    (smL_smul (h ^ 2) (smL_sub (smL_div (smL_pow hW 2) 32) (smL_div hW 4)))

lemma four_mul_eq_smul (z : Lattice) : (4 : Lattice) * z = (4 : ℝ) • z := by
  funext j x t
  simp only [Pi.mul_apply, Pi.smul_apply, Pi.ofNat_apply, smulR]

lemma lx_four_smul {z : Lattice} (hz : SmL z) : lx (4 * z) = (4 : ℝ) • lx z := by
  have h : lx ((4 : ℝ) • z) = (4 : ℝ) • lx z := lx_smul (z := z) (4 : ℝ) hz
  rw [four_mul_eq_smul z]
  exact h

/-- shift-average-average: `Sh(mm(mm v)) = (h²/4)·Δ_h v + v`. -/
lemma Sh_mmmm (h : ℝ) (hh : h ≠ 0) (v : Lattice) :
    Sh (mm (mm v)) = (h ^ 2 / 4) • lap h v + v := by
  have hh2 : h ^ 2 ≠ 0 := pow_ne_zero 2 hh
  funext j x t
  simp only [Sh, mm, lap, Pi.add_apply, Pi.sub_apply, Pi.mul_apply, Pi.div_apply,
    Pi.smul_apply, Pi.ofNat_apply, smulR, iz_add_sub, iz_sub_add]
  field_simp
  ring

/-- `Sh(mm(Δ_h ∘ D⁻)) = Δ_h ∘ D⁰`. -/
lemma Sh_mm_lap_dm (h : ℝ) (hh : h ≠ 0) (u : Lattice) :
    Sh (mm (lap h (dm h u))) = lap h (d0 h u) := by
  have hh2 : h ^ 2 ≠ 0 := pow_ne_zero 2 hh
  have h2h : 2 * h ≠ 0 := mul_ne_zero two_ne_zero hh
  funext j x t
  simp only [Sh, mm, lap, d0, dm, Pi.add_apply, Pi.sub_apply, Pi.mul_apply, Pi.div_apply,
    Pi.smul_apply, Pi.ofNat_apply, smulR, iz_add_sub, iz_sub_add]
  field_simp
  ring

/-! ### abbreviations matching the frozen definitions -/

def c19ZZ (a h : ℝ) (u v : Lattice) : Lattice := lt u + lx (H a h u v)
def c19WW (h : ℝ) (u v : Lattice) : Lattice := mm v - (h ^ 2 / 4) • lap h (dm h u)
def c19AA (a h : ℝ) (u v : Lattice) : Lattice :=
  d0 h (H a h u v) + (u + CC a) * W h u v - 4 * u
def c19BB (_a h : ℝ) (u v : Lattice) : Lattice :=
  d0 h u + (h ^ 2 / 4) • lap h (W h u v)

/-- `Sh(mm W') = B + W`. -/
lemma Sh_mm_WW (a h : ℝ) (hh : h ≠ 0) (u v : Lattice) :
    Sh (mm (c19WW h u v)) = c19BB a h u v + W h u v := by
  have h1 : mm (c19WW h u v) = mm (mm v) - (h ^ 2 / 4) • mm (lap h (dm h u)) := by
    rw [show c19WW h u v = mm v - (h ^ 2 / 4) • lap h (dm h u) from rfl, mm_sub, mm_smul]
  rw [h1, Sh_sub, Sh_smul, Sh_mm_lap_dm h hh u]
  have h2 : Sh (mm (mm v)) = (h ^ 2 / 4) • lap h v + v := Sh_mmmm h hh v
  have h3 : lap h (d0 h u) + lap h (W h u v) = lap h v := by
    rw [← lap_add h (d0 h u) (W h u v)]
    rw [show d0 h u + W h u v = v from by
      show d0 h u + (v - d0 h u) = v
      abel]
  rw [h2, ← h3, smul_add,
    show c19BB a h u v = d0 h u + (h ^ 2 / 4) • lap h (W h u v) from rfl,
    show W h u v = v - d0 h u from rfl]
  abel

/-- from `n1 = 0`: `-D⁰ Z = lxx (Sh (mm W'))`. -/
lemma neg_d0_of_dm (h : ℝ) (hh : h ≠ 0) {Z X : Lattice} (hdm : dm h Z = - lxx X) :
    - d0 h Z = Sh (mm (lxx X)) := by
  funext j x t
  have hrel : ∀ k : ℤ, Z k x t - Z (k - 1) x t = - (h * (lxx X k x t)) := by
    intro k
    have h1 : (1 / h) * (Z k x t - Z (k - 1) x t) = - (lxx X k x t) := by
      have hk := congrFun (congrFun (congrFun hdm k) x) t
      simpa only [dm, Pi.sub_apply, Pi.smul_apply, Pi.neg_apply, smulR] using hk
    have hmul := congrArg (fun r : ℝ => h * r) h1
    rw [← mul_assoc, show h * (1 / h) = (1 : ℝ) from by rw [one_div, mul_inv_cancel₀ hh],
      one_mul, mul_neg] at hmul
    exact hmul
  have e1 := hrel (j + 1)
  have e2 := hrel j
  have hJ : (j : ℤ) + 1 - 1 = j := by ring
  have e3 : Z (j + 1) x t - Z (j - 1) x t
      = - (h * (lxx X (j + 1) x t)) + - (h * (lxx X j x t)) := by
    rw [show (j : ℤ) + 1 - 1 = j from by ring] at e1
    linarith [e1, e2]
  simp only [d0, Sh, mm, Pi.sub_apply, Pi.add_apply, Pi.div_apply, Pi.smul_apply,
    Pi.neg_apply, Pi.ofNat_apply, smulR, hJ]
  rw [e3]
  have h2h : 2 * h ≠ 0 := mul_ne_zero two_ne_zero hh
  field_simp
  ring

/-! ### the linear expansions used in the C19 chain -/

lemma lx_add_lx {z w : Lattice} (hz : SmL z) (hw : SmL w) :
    lx (z + lx w) = lx z + lxx w := by
  rw [lx_add hz (smL_lx hw)]
  simp only [lxx]

lemma lt_W (h : ℝ) {u v : Lattice} (hu : SmL u) (hv : SmL v) :
    lt (W h u v) = lt v - d0 h (lt u) := by
  rw [show W h u v = v - d0 h u from rfl, lt_sub hv (smL_d0 h hu), lt_d0 h hu]

lemma lx_JW (a h : ℝ) {u v : Lattice} (hu : SmL u) (hv : SmL v) :
    lx (JW a h u v) = lx ((u + CC a) * W h u v) - (4 : ℝ) • lx u - lxx (W h u v) := by
  have hW : SmL (W h u v) := smL_sub hv (smL_d0 h hu)
  have hP : SmL ((u + CC a) * W h u v) :=
    smL_mul (smL_add hu (smL_const (2 * a))) hW
  have h4u : SmL (4 * u) := smL_four_mul hu
  rw [show JW a h u v = (u + CC a) * W h u v - 4 * u - lx (W h u v) from rfl]
  rw [lx_sub (smL_sub hP h4u) (smL_lx hW), lx_sub hP h4u, lx_four_smul hu]
  simp only [lxx]

lemma lx_AA (a h : ℝ) {u v : Lattice} (hu : SmL u) (hv : SmL v) :
    lx (c19AA a h u v)
      = lx (d0 h (H a h u v)) + lx ((u + CC a) * W h u v) - (4 : ℝ) • lx u := by
  have hH : SmL (H a h u v) := smL_H a h hu hv
  have hW : SmL (W h u v) := smL_sub hv (smL_d0 h hu)
  have hP : SmL ((u + CC a) * W h u v) :=
    smL_mul (smL_add hu (smL_const (2 * a))) hW
  have h4u : SmL (4 * u) := smL_four_mul hu
  rw [show c19AA a h u v = d0 h (H a h u v) + (u + CC a) * W h u v - 4 * u from rfl]
  rw [lx_sub (smL_add (smL_d0 h hH) hP) h4u, lx_add (smL_d0 h hH) hP, lx_four_smul hu]

lemma lxx_BB (h : ℝ) {u v : Lattice} (hu : SmL u) (hv : SmL v) :
    lxx (c19BB a h u v)
      = lxx (d0 h u) + (h ^ 2 / 4) • lxx (lap h (W h u v)) := by
  have hW : SmL (W h u v) := smL_sub hv (smL_d0 h hu)
  have hl : SmL (lap h (W h u v)) := smL_lap h hW
  rw [show c19BB a h u v = d0 h u + (h ^ 2 / 4) • lap h (W h u v) from rfl]
  rw [lxx_add (smL_d0 h hu) (smL_smul (h ^ 2 / 4) hl),
    lxx_smul (z := lap h (W h u v)) (h ^ 2 / 4) hl]

lemma d0_ZZ (a h : ℝ) {u v : Lattice} (hu : SmL u) (hv : SmL v) :
    d0 h (c19ZZ a h u v) = d0 h (lt u) + lx (d0 h (H a h u v)) := by
  have hH : SmL (H a h u v) := smL_H a h hu hv
  rw [show c19ZZ a h u v = lt u + lx (H a h u v) from rfl]
  rw [d0_add h (lt u) (lx (H a h u v)), d0_lx h hH]

theorem c19_proved : C19 := by
  intro a h u v hh hu hv hnp
  have hn1 : n1 a h u v = 0 := hnp.1
  have hn2 : n2 a h u v = 0 := hnp.2
  have hW : SmL (W h u v) := smL_sub hv (smL_d0 h hu)
  have hH : SmL (H a h u v) := smL_H a h hu hv
  have hZZ : SmL (c19ZZ a h u v) := smL_add (smL_lt hu) (smL_lx hH)
  have hWW : SmL (c19WW h u v) :=
    smL_sub (smL_mm hv) (smL_smul (h ^ 2 / 4) (smL_lap h (smL_dm h hu)))
  have hBB : SmL (c19BB a h u v) :=
    smL_add (smL_d0 h hu) (smL_smul (h ^ 2 / 4) (smL_lap h hW))
  have hAA : SmL (c19AA a h u v) :=
    smL_sub (smL_add (smL_d0 h hH) (smL_mul (smL_add hu (smL_const (2 * a))) hW))
      (smL_four_mul hu)
  constructor
  · have hdm : dm h (c19ZZ a h u v) = - lxx (c19WW h u v) := by
      have hzero : dm h (c19ZZ a h u v) + lxx (c19WW h u v) = 0 := by
        have h0 := hn1
        rw [n1] at h0
        exact h0
      calc dm h (c19ZZ a h u v)
          = (dm h (c19ZZ a h u v) + lxx (c19WW h u v)) - lxx (c19WW h u v) := by abel
        _ = 0 - lxx (c19WW h u v) := by rw [hzero]
        _ = - lxx (c19WW h u v) := by abel
    have hd0Z : d0 h (c19ZZ a h u v) = - lxx (Sh (mm (c19WW h u v))) := by
      have h1 : - d0 h (c19ZZ a h u v) = lxx (Sh (mm (c19WW h u v))) := by
        rw [neg_d0_of_dm h hh hdm, Sh_mm_lxx hWW]
      rw [← h1, neg_neg]
    have hpure : Sh (mm (c19WW h u v)) = c19BB a h u v + W h u v := Sh_mm_WW a h hh u v
    have hltv : lt v = - lxx (c19BB a h u v) - lx (c19AA a h u v) := by
      have h2eq : lt v + lx (c19AA a h u v) + lxx (c19BB a h u v) = 0 := by
        have h0 := hn2
        rw [n2] at h0
        exact h0
      have hsub : lt v + lx (c19AA a h u v) = - lxx (c19BB a h u v) := by
        calc lt v + lx (c19AA a h u v)
            = (lt v + lx (c19AA a h u v) + lxx (c19BB a h u v)) - lxx (c19BB a h u v) := by
              abel
          _ = 0 - lxx (c19BB a h u v) := by rw [h2eq]
          _ = - lxx (c19BB a h u v) := by abel
      calc lt v = (lt v + lx (c19AA a h u v)) - lx (c19AA a h u v) := by abel
        _ = - lxx (c19BB a h u v) - lx (c19AA a h u v) := by rw [hsub]
    have hE1 : lt (W h u v) + lx (JW a h u v)
        = - lxx (c19BB a h u v) - d0 h (c19ZZ a h u v) - lxx (W h u v) := by
      rw [lt_W h hu hv, lx_JW a h hu hv, hltv, lx_AA a h hu hv, lxx_BB h hu hv,
        d0_ZZ a h hu hv]
      abel
    rw [hE1]
    rw [hd0Z, hpure, lxx_add hBB hW]
    abel
  · have h2c : lt v + lx (JV a h u v) = n2 a h u v := by
      have hA : SmL (c19AA a h u v) := hAA
      have hB : SmL (c19BB a h u v) := hBB
      show lt v + lx (c19AA a h u v + lx (c19BB a h u v))
          = lt v + lx (c19AA a h u v) + lxx (c19BB a h u v)
      rw [lx_add_lx hA hB]
      abel
    rw [h2c, hn2]

end DLWContract
