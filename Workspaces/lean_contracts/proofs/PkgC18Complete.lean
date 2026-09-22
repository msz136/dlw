import PkgC02
import PkgC11
import PkgLattice
import Mathlib.Analysis.Calculus.IteratedDeriv.Lemmas

noncomputable section
open scoped BigOperators
namespace DLWContract
namespace ConsistencyProof

theorem deriv_linear (c : ℝ) : deriv (HMul.hMul c) = fun _ => c := by
  funext x
  simpa using ((hasDerivAt_id x).const_mul c).deriv

theorem jet_add (f g : ℝ → ℝ) (hf : ContDiff ℝ ⊤ f) (hg : ContDiff ℝ ⊤ g) (n : ℕ) :
    iteratedDeriv n (fun h => f h+g h) 0 = iteratedDeriv n f 0+iteratedDeriv n g 0 :=
  iteratedDeriv_fun_add (hf.of_le le_top).contDiffAt (hg.of_le le_top).contDiffAt

theorem jet_sub (f g : ℝ → ℝ) (hf : ContDiff ℝ ⊤ f) (hg : ContDiff ℝ ⊤ g) (n : ℕ) :
    iteratedDeriv n (fun h => f h-g h) 0 = iteratedDeriv n f 0-iteratedDeriv n g 0 :=
  iteratedDeriv_fun_sub (hf.of_le le_top).contDiffAt (hg.of_le le_top).contDiffAt

theorem jet_mul (f g : ℝ → ℝ) (hf : ContDiff ℝ ⊤ f) (hg : ContDiff ℝ ⊤ g) (n : ℕ) :
    iteratedDeriv n (fun h => f h*g h) 0 =
      ∑ i ∈ Finset.range (n+1), (n.choose i : ℝ)*iteratedDeriv i f 0*iteratedDeriv (n-i) g 0 :=
  iteratedDeriv_fun_mul (hf.of_le le_top).contDiffAt (hg.of_le le_top).contDiffAt

theorem jet_shift (f : ℝ → ℝ) (hf : ContDiff ℝ ⊤ f) (y c : ℝ) (n : ℕ) :
    iteratedDeriv n (fun h => f (y+c*h)) 0 = c^n*iteratedDeriv n f y := by
  have hs : ContDiff ℝ n (fun r => f (y+r)) :=
    (hf.comp (contDiff_const.add contDiff_id)).of_le le_top
  have H := congrFun (iteratedDeriv_comp_const_mul hs c) 0
  simpa [iteratedDeriv_comp_const_add] using H

theorem divided_zero_jets (e : ℝ → ℝ) (he : ContDiff ℝ ⊤ e)
    (h0 : e 0=0) (h1 : deriv e 0=0) (h2 : iteratedDeriv 2 e 0=0) :
    PowBound 2 (fun h => e h/h) := by
  have hp : ∀ h, taylorWithinEval e 2 Set.univ 0 h=0 := by
    intro h
    rw [show h=0+h by ring, taylorWithinEval_eq_sum]
    simp [Finset.sum_range_succ,iteratedDeriv_one,h0,h1,h2]
  have H : PowBound 3 e := by
    apply c11_powBound_norm_abs
    simpa only [zero_add,hp,sub_zero] using powBound_taylor_poly 2 e 0 (he.of_le le_top)
  obtain ⟨C,hC,eps,heps,hb⟩ := H
  refine ⟨C,hC,eps,heps,?_⟩
  intro h hh hlt
  rw [abs_div]
  apply (div_le_iff₀ hh).mpr
  simpa [pow_succ,mul_assoc] using hb h hh hlt

-- The factors h*W and h*Wx have smooth extensions through h=0.
def Z (u v : ℝ → ℝ) (y h : ℝ) (j : ℝ) :=
  h*v (y+j*h)-(u (y+(j+1)*h)-u (y+(j-1)*h))/2

def correction (u ux v vx : ℝ → ℝ) (y h j : ℝ) :=
  Z u v y h j*Z ux vx y h j/16-h*Z ux vx y h j/4

def numerator1 (A u ux v vx B C : ℝ → ℝ) (y h : ℝ) :=
  A y-A (y+(-1)*h)+correction u ux v vx y h 0-correction u ux v vx y h (-1)+
  h*(B y+B (y+(-1)*h))/2-(C (y+1*h)-3*C y+3*C (y+(-1)*h)-C (y+(-2)*h))/4

theorem numerator1_consistency (A u ux v vx B C : ℝ → ℝ)
    (hA : ContDiff ℝ ⊤ A) (hu : ContDiff ℝ ⊤ u) (hux : ContDiff ℝ ⊤ ux)
    (hv : ContDiff ℝ ⊤ v) (hvx : ContDiff ℝ ⊤ vx)
    (hB : ContDiff ℝ ⊤ B) (hC : ContDiff ℝ ⊤ C) (y : ℝ) :
    PowBound 2 (fun h => numerator1 A u ux v vx B C y h/h-
      (deriv A (y+(-1/2)*h)+B (y+(-1/2)*h))) := by
  let e : ℝ → ℝ := fun h => numerator1 A u ux v vx B C y h-
    h*(deriv A (y+(-1/2)*h)+B (y+(-1/2)*h))
  have hDA : ContDiff ℝ ⊤ (deriv A) := hA.deriv'
  have he : ContDiff ℝ ⊤ e := by unfold e numerator1 correction Z; fun_prop
  have hj : ∀ n ≤ 2, iteratedDeriv n e 0=0 := by
    intro n hn
    unfold e numerator1 correction Z
    interval_cases n <;>
      simp (disch := fun_prop) only [jet_add,jet_sub,jet_mul,jet_shift,
        iteratedDeriv_div_const,iteratedDeriv_const_mul_field,Finset.sum_range_succ,Finset.sum_range_zero,
        Nat.reduceAdd,Nat.reduceSub] <;>
      norm_num [iteratedDeriv_const,iteratedDeriv_fun_id,iteratedDeriv_zero,
        ← iteratedDeriv_one, ← iteratedDeriv_succ'] <;>
      simp only [iteratedDeriv_succ',iteratedDeriv_zero,deriv_linear,deriv_const] <;> ring
  have H := divided_zero_jets e he (by simpa using hj 0 (by omega))
    (by simpa only [iteratedDeriv_one] using hj 1 (by omega)) (hj 2 (by omega))
  apply c11_powBound_congr_ne _ H
  intro h hh
  dsimp [e]
  field_simp

def numerator2 (a : ℝ) (A u ux v vx B C T : ℝ → ℝ) (y h : ℝ) :=
  h*T y+(A (y+1*h)-A (y+(-1)*h)+
    correction u ux v vx y h 1-correction u ux v vx y h (-1))/2+
  ux y*Z u v y h 0+(u y+2*a)*Z ux vx y h 0-4*h*ux y+
  (C (y+1*h)-C (y+(-1)*h))/2+
  (Z C B y h 1-2*Z C B y h 0+Z C B y h (-1))/4

def limit2 (a : ℝ) (A u ux v vx C T : ℝ → ℝ) (y : ℝ) :=
  T y+deriv A y+ux y*(v y-deriv u y)+(u y+2*a)*(vx y-deriv ux y)-
  4*ux y+deriv C y

theorem numerator2_consistency (a : ℝ) (A u ux v vx B C T : ℝ → ℝ)
    (hA : ContDiff ℝ ⊤ A) (hu : ContDiff ℝ ⊤ u) (hux : ContDiff ℝ ⊤ ux)
    (hv : ContDiff ℝ ⊤ v) (hvx : ContDiff ℝ ⊤ vx)
    (hB : ContDiff ℝ ⊤ B) (hC : ContDiff ℝ ⊤ C) (hT : ContDiff ℝ ⊤ T) (y : ℝ) :
    PowBound 2 (fun h => numerator2 a A u ux v vx B C T y h/h-
      limit2 a A u ux v vx C T y) := by
  let e : ℝ → ℝ := fun h => numerator2 a A u ux v vx B C T y h-
    h*limit2 a A u ux v vx C T y
  have he : ContDiff ℝ ⊤ e := by unfold e numerator2 correction Z; fun_prop
  have hj : ∀ n ≤ 2, iteratedDeriv n e 0=0 := by
    intro n hn
    unfold e numerator2 correction Z limit2
    interval_cases n <;>
      simp (disch := fun_prop) only [jet_add,jet_sub,jet_mul,jet_shift,
        iteratedDeriv_div_const,iteratedDeriv_const_mul_field,Finset.sum_range_succ,Finset.sum_range_zero,
        Nat.reduceAdd,Nat.reduceSub] <;>
      norm_num [iteratedDeriv_const,iteratedDeriv_fun_id,iteratedDeriv_zero,
        ← iteratedDeriv_one, ← iteratedDeriv_succ'] <;>
      simp only [iteratedDeriv_succ',iteratedDeriv_zero,deriv_linear,deriv_const] <;> ring
  have H := divided_zero_jets e he (by simpa using hj 0 (by omega))
    (by simpa only [iteratedDeriv_one] using hj 1 (by omega)) (hj 2 (by omega))
  apply c11_powBound_congr_ne _ H
  intro h hh
  dsimp [e]
  field_simp

theorem smooth_x_slice (f : XYT) (hf : Smooth3 f) (y t : ℝ) :
    ContDiff ℝ ⊤ (fun x => f x y t) :=
  hf.comp (contDiff_id.prodMk (contDiff_const.prodMk contDiff_const))

theorem smooth_y_slice (f : XYT) (hf : Smooth3 f) (x t : ℝ) :
    ContDiff ℝ ⊤ (fun y => f x y t) :=
  hf.comp (contDiff_const.prodMk (contDiff_id.prodMk contDiff_const))

def flux (a : ℝ) (u : XYT) : XYT := u*sx u+(2*a) • sx u

theorem residual1_numerator (a h : ℝ) (u v : XYT) (hu : Smooth3 u) (hv : Smooth3 v)
    (hh : h ≠ 0) (x y t : ℝ) :
    h*n1 a h (localSamples y h u) (localSamples y h v) 0 x t =
      numerator1 (fun Y => st u x Y t+flux a u x Y t)
        (fun Y => u x Y t) (fun Y => sx u x Y t)
        (fun Y => v x Y t) (fun Y => sx v x Y t)
        (fun Y => sx (sx v) x Y t) (fun Y => sx (sx u) x Y t) y h := by
  have hux := c02_smooth_sx hu
  have hvx := c02_smooth_sx hv
  have DU (X Y : ℝ) : deriv (fun r => u r Y t) X = sx u X Y t := rfl
  have DV (X Y : ℝ) : deriv (fun r => v r Y t) X = sx v X Y t := rfl
  have DUX (X Y : ℝ) : deriv (fun r => sx u r Y t) X = sx (sx u) X Y t := rfl
  have DVX (X Y : ℝ) : deriv (fun r => sx v r Y t) X = sx (sx v) X Y t := rfl
  have DTU (X Y : ℝ) : deriv (slice u Y X) t = st u X Y t := rfl
  have dU (X Y : ℝ) := c02_diff_x u hu X Y t
  have dV (X Y : ℝ) := c02_diff_x v hv X Y t
  have dUX (X Y : ℝ) := c02_diff_x (sx u) hux X Y t
  have dVX (X Y : ℝ) := c02_diff_x (sx v) hvx X Y t
  simp only [n1,dm,lt,lxx,lx,dx,dt,H,W,d0,mm,lap,localSamples,slice,
    Pi.add_apply,Pi.sub_apply,Pi.mul_apply,Pi.div_apply,Pi.pow_apply,Pi.smul_apply,
    Pi.ofNat_apply,smul_eq_mul]
  simp (disch := fun_prop) only [deriv_fun_add,deriv_fun_sub,deriv_fun_mul,
    deriv_fun_pow,deriv_div_const,deriv_const_mul_field,deriv_mul_const_field,
    deriv_const,DU,DV,DUX,DVX,DTU]
  simp only [numerator1,correction,Z,flux,Pi.add_apply,Pi.mul_apply,Pi.smul_apply,smul_eq_mul]
  norm_num
  field_simp
  <;> ring

theorem residual2_numerator (a h : ℝ) (u v : XYT) (hu : Smooth3 u) (hv : Smooth3 v)
    (hh : h ≠ 0) (x y t : ℝ) :
    h*n2 a h (localSamples y h u) (localSamples y h v) 0 x t =
      numerator2 a (fun Y => flux a u x Y t)
        (fun Y => u x Y t) (fun Y => sx u x Y t)
        (fun Y => v x Y t) (fun Y => sx v x Y t)
        (fun Y => sx (sx v) x Y t) (fun Y => sx (sx u) x Y t)
        (fun Y => st v x Y t) y h := by
  have hux := c02_smooth_sx hu
  have hvx := c02_smooth_sx hv
  have DU (X Y : ℝ) : deriv (fun r => u r Y t) X = sx u X Y t := rfl
  have DV (X Y : ℝ) : deriv (fun r => v r Y t) X = sx v X Y t := rfl
  have DUX (X Y : ℝ) : deriv (fun r => sx u r Y t) X = sx (sx u) X Y t := rfl
  have DVX (X Y : ℝ) : deriv (fun r => sx v r Y t) X = sx (sx v) X Y t := rfl
  have DTV (X Y : ℝ) : deriv (slice v Y X) t = st v X Y t := rfl
  have dU (X Y : ℝ) := c02_diff_x u hu X Y t
  have dV (X Y : ℝ) := c02_diff_x v hv X Y t
  have dUX (X Y : ℝ) := c02_diff_x (sx u) hux X Y t
  have dVX (X Y : ℝ) := c02_diff_x (sx v) hvx X Y t
  simp only [n2,dm,lt,lxx,lx,dx,dt,H,W,d0,mm,lap,localSamples,slice,
    Pi.add_apply,Pi.sub_apply,Pi.mul_apply,Pi.div_apply,Pi.pow_apply,Pi.smul_apply,
    Pi.ofNat_apply,smul_eq_mul]
  simp (disch := fun_prop) only [deriv_fun_add,deriv_fun_sub,deriv_fun_mul,
    deriv_fun_pow,deriv_div_const,deriv_const_mul_field,deriv_mul_const_field,
    deriv_const,DU,DV,DUX,DVX,DTV]
  simp only [numerator2,correction,Z,flux,Pi.add_apply,Pi.mul_apply,Pi.smul_apply,smul_eq_mul]
  norm_num
  field_simp
  <;> ring

theorem flux_smooth (a : ℝ) (u : XYT) (hu : Smooth3 u) : Smooth3 (flux a u) :=
  c02_smooth_add (c02_smooth_mul hu (c02_smooth_sx hu))
    (c02_smooth_smul (2*a) (c02_smooth_sx hu))

theorem limit1_eq (a : ℝ) (u v : XYT) (hu : Smooth3 u) (hv : Smooth3 v) (x y t : ℝ) :
    deriv (fun Y => st u x Y t+flux a u x Y t) y+sx (sx v) x y t = c1 a u v x y t := by
  change sy (st u+flux a u) x y t+sx (sx v) x y t = _
  rw [c02_sy_add (st u) (flux a u) (c02_smooth_st hu) (flux_smooth a u hu)]
  simp only [flux,c1,c02_sy_add _ _ (c02_smooth_mul hu (c02_smooth_sx hu))
      (c02_smooth_smul (2*a) (c02_smooth_sx hu)),
    c02_sy_mul u (sx u) hu (c02_smooth_sx hu),c02_sy_smul,
    c02_sy_sx u hu,c02_sx_mul u (sy u) hu (c02_smooth_sy hu),
    Pi.add_apply,Pi.mul_apply,Pi.smul_apply,smul_eq_mul]
  ring

theorem limit2_eq (a : ℝ) (u v : XYT) (hu : Smooth3 u) (hv : Smooth3 v) (x y t : ℝ) :
    limit2 a (fun Y => flux a u x Y t) (fun Y => u x Y t) (fun Y => sx u x Y t)
      (fun Y => v x Y t) (fun Y => sx v x Y t) (fun Y => sx (sx u) x Y t)
      (fun Y => st v x Y t) y = c2 a u v x y t := by
  change st v x y t+sy (flux a u) x y t+
    sx u x y t*(v x y t-sy u x y t)+(u x y t+2*a)*(sx v x y t-sy (sx u) x y t)-
      4*sx u x y t+sy (sx (sx u)) x y t = _
  simp only [flux,c2,c02_sy_add _ _ (c02_smooth_mul hu (c02_smooth_sx hu))
      (c02_smooth_smul (2*a) (c02_smooth_sx hu)),
    c02_sy_mul u (sx u) hu (c02_smooth_sx hu),c02_sy_smul,
    c02_sy_sx (sx u) (c02_smooth_sx hu),c02_sy_sx u hu,
    c02_sx_mul u v hu hv,Pi.add_apply,Pi.sub_apply,Pi.mul_apply,Pi.smul_apply,
    Pi.ofNat_apply,smul_eq_mul]
  ring

end ConsistencyProof

theorem c18_proved : C18 := by
  intro a u v hu hv x y t
  have hux := c02_smooth_sx hu
  have hvx := c02_smooth_sx hv
  have hf := ConsistencyProof.flux_smooth a u hu
  have h1 := ConsistencyProof.numerator1_consistency
    (fun Y => st u x Y t+ConsistencyProof.flux a u x Y t)
    (fun Y => u x Y t) (fun Y => sx u x Y t)
    (fun Y => v x Y t) (fun Y => sx v x Y t)
    (fun Y => sx (sx v) x Y t) (fun Y => sx (sx u) x Y t)
    (ConsistencyProof.smooth_y_slice (st u+ConsistencyProof.flux a u)
      (c02_smooth_add (c02_smooth_st hu) hf) x t)
    (ConsistencyProof.smooth_y_slice u hu x t)
    (ConsistencyProof.smooth_y_slice (sx u) hux x t)
    (ConsistencyProof.smooth_y_slice v hv x t)
    (ConsistencyProof.smooth_y_slice (sx v) hvx x t)
    (ConsistencyProof.smooth_y_slice (sx (sx v)) (c02_smooth_sx hvx) x t)
    (ConsistencyProof.smooth_y_slice (sx (sx u)) (c02_smooth_sx hux) x t) y
  have h2 := ConsistencyProof.numerator2_consistency a
    (fun Y => ConsistencyProof.flux a u x Y t)
    (fun Y => u x Y t) (fun Y => sx u x Y t)
    (fun Y => v x Y t) (fun Y => sx v x Y t)
    (fun Y => sx (sx v) x Y t) (fun Y => sx (sx u) x Y t) (fun Y => st v x Y t)
    (ConsistencyProof.smooth_y_slice (ConsistencyProof.flux a u) hf x t)
    (ConsistencyProof.smooth_y_slice u hu x t)
    (ConsistencyProof.smooth_y_slice (sx u) hux x t)
    (ConsistencyProof.smooth_y_slice v hv x t)
    (ConsistencyProof.smooth_y_slice (sx v) hvx x t)
    (ConsistencyProof.smooth_y_slice (sx (sx v)) (c02_smooth_sx hvx) x t)
    (ConsistencyProof.smooth_y_slice (sx (sx u)) (c02_smooth_sx hux) x t)
    (ConsistencyProof.smooth_y_slice (st v) (c02_smooth_st hv) x t) y
  constructor
  · apply c11_powBound_congr_ne _ h1
    intro h hh
    rw [← ConsistencyProof.residual1_numerator a h u v hu hv hh x y t,
      ConsistencyProof.limit1_eq a u v hu hv]
    rw [show y+(-1/2)*h=y-h/2 by ring]
    field_simp
  · apply c11_powBound_congr_ne _ h2
    intro h hh
    rw [← ConsistencyProof.residual2_numerator a h u v hu hv hh x y t,
      ConsistencyProof.limit2_eq a u v hu hv]
    field_simp

#print axioms c18_proved
end DLWContract
