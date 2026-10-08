import PkgRK4

noncomputable section
open scoped BigOperators
namespace DLWContract
namespace RK4Proof
variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]

theorem multi_diag_scale {n : ℕ} (B : ContinuousMultilinearMap ℝ (fun _ : Fin n => E) E)
    (c : ℝ) (v : E) : B (fun _ => c • v) = c^n • B (fun _ => v) := by
  simpa using B.map_smul_univ (fun _ => c) (fun _ => v)

theorem multi_two_scale (B : ContinuousMultilinearMap ℝ (fun _ : Fin 2 => E) E)
    (c d : ℝ) (v w : E) : B ![c • v, d • w] = (c*d) • B ![v,w] := by
  have hv : (fun i : Fin 2 => ![c,d] i • ![v,w] i) = ![c • v,d • w] := by
    funext i; fin_cases i <;> rfl
  simpa [hv, Fin.prod_univ_two] using B.map_smul_univ ![c,d] ![v,w]

def stage (F : E → E) (z : E) (c : ℝ) (g : ℝ → E) : ℝ → E :=
  fun h => F (z+(c*h) • g h)

theorem stage_smooth (F : E → E) (z : E) (c : ℝ) (g : ℝ → E)
    (hF : ContDiff ℝ ⊤ F) (hg : ContDiff ℝ ⊤ g) :
    ContDiff ℝ ⊤ (stage F z c g) := by
  unfold stage
  exact hF.comp (contDiff_const.add ((contDiff_const.mul contDiff_id).smul hg))

theorem stage_jets (F : E → E) (z : E) (c : ℝ) (g : ℝ → E)
    (hF : ContDiff ℝ ⊤ F) (hg : ContDiff ℝ ⊤ g) :
    let A := fderiv ℝ F z
    let B := iteratedFDeriv ℝ 2 F z
    let C := iteratedFDeriv ℝ 3 F z
    stage F z c g 0 = F z ∧
    deriv (stage F z c g) 0 = c • A (g 0) ∧
    iteratedDeriv 2 (stage F z c g) 0 =
      c^2 • B (fun _ => g 0) + (2*c) • A (deriv g 0) ∧
    iteratedDeriv 3 (stage F z c g) 0 =
      c^3 • C (fun _ => g 0) +
      (2*c^2) • B ![deriv g 0,g 0] +
      (4*c^2) • B ![g 0,deriv g 0] +
      (3*c) • A (iteratedDeriv 2 g 0) := by
  dsimp only
  let q : ℝ → E := fun h => z+(c*h) • g h
  have hq : ContDiff ℝ ⊤ q :=
    contDiff_const.add ((contDiff_const.mul contDiff_id).smul hg)
  have q0 : q 0 = z := by simp [q]
  have q1 : deriv q 0 = c • g 0 := by
    simpa [q, iteratedDeriv_one] using jet_path g hg z c 0 (by omega)
  have q2 : iteratedDeriv 2 q 0 = (2*c) • deriv g 0 := by
    simpa [iteratedDeriv_one] using jet_path g hg z c 1 (by omega)
  have q3 : iteratedDeriv 3 q 0 = (3*c) • iteratedDeriv 2 g 0 := by
    simpa using jet_path g hg z c 2 (by omega)
  refine ⟨by simp [stage], ?_, ?_, ?_⟩
  · change deriv (fun h => F (q h)) 0 = _
    rw [comp_one F q hF hq, q0, q1, map_smul]
  · change iteratedDeriv 2 (fun h => F (q h)) 0 = _
    rw [comp_two F q hF hq, q0, q1, q2, multi_diag_scale, map_smul]
  · change iteratedDeriv 3 (fun h => F (q h)) 0 = _
    rw [comp_three F q hF hq, q0, q1, q2, q3,
      multi_diag_scale, multi_two_scale, multi_two_scale, map_smul]
    module

theorem multi_two_left (B : ContinuousMultilinearMap ℝ (fun _ : Fin 2 => E) E)
    (c : ℝ) (v w : E) : B ![c • v,w] = c • B ![v,w] := by
  simpa using multi_two_scale B c 1 v w

theorem multi_two_right (B : ContinuousMultilinearMap ℝ (fun _ : Fin 2 => E) E)
    (c : ℝ) (v w : E) : B ![v,c • w] = c • B ![v,w] := by
  simpa using multi_two_scale B 1 c v w

theorem multi_two_zero_left (B : ContinuousMultilinearMap ℝ (fun _ : Fin 2 => E) E)
    (w : E) : B ![0,w] = 0 := B.map_coord_zero 0 rfl

theorem multi_two_zero_right (B : ContinuousMultilinearMap ℝ (fun _ : Fin 2 => E) E)
    (v : E) : B ![v,0] = 0 := B.map_coord_zero 1 rfl

theorem jet_weighted (v : E) (g₂ g₃ g₄ : ℝ → E)
    (h₂ : ContDiff ℝ ⊤ g₂) (h₃ : ContDiff ℝ ⊤ g₃) (h₄ : ContDiff ℝ ⊤ g₄)
    (n : ℕ) :
    iteratedDeriv n (fun h => v+(2:ℝ) • g₂ h+(2:ℝ) • g₃ h+g₄ h) 0 =
      (if n=0 then v else 0) + (2:ℝ) • iteratedDeriv n g₂ 0 +
        (2:ℝ) • iteratedDeriv n g₃ 0 + iteratedDeriv n g₄ 0 := by
  have h2 : ContDiff ℝ n g₂ := h₂.of_le le_top
  have h3 : ContDiff ℝ n g₃ := h₃.of_le le_top
  have h4 : ContDiff ℝ n g₄ := h₄.of_le le_top
  rw [iteratedDeriv_fun_add (by fun_prop) h4.contDiffAt,
    iteratedDeriv_fun_add (by fun_prop) (by fun_prop),
    iteratedDeriv_fun_add (by fun_prop) (by fun_prop)]
  simp [iteratedDeriv_const_smul_field, iteratedDeriv_const]

theorem trajectory_jets (F : E → E) (q : ℝ → E)
    (hF : ContDiff ℝ ⊤ F) (hq : ContDiff ℝ ⊤ q)
    (hode : ∀ t, HasDerivAt q (F (q t)) t) :
    let v := F (q 0)
    let A := fderiv ℝ F (q 0)
    let B := iteratedFDeriv ℝ 2 F (q 0)
    let C := iteratedFDeriv ℝ 3 F (q 0)
    deriv q 0 = v ∧ iteratedDeriv 2 q 0 = A v ∧
    iteratedDeriv 3 q 0 = B (fun _ => v)+A (A v) ∧
    iteratedDeriv 4 q 0 = C (fun _ => v)+B ![A v,v]+
      (2:ℝ) • B ![v,A v]+A (B (fun _ => v)+A (A v)) := by
  dsimp only
  have heq : deriv q = fun t => F (q t) := funext fun t => (hode t).deriv
  have d1 : deriv q 0 = F (q 0) := (hode 0).deriv
  have d2 : iteratedDeriv 2 q 0 = fderiv ℝ F (q 0) (F (q 0)) := by
    rw [iteratedDeriv_succ', heq, iteratedDeriv_one, comp_one F q hF hq, d1]
  have d3 : iteratedDeriv 3 q 0 =
      iteratedFDeriv ℝ 2 F (q 0) (fun _ => F (q 0)) +
        fderiv ℝ F (q 0) (fderiv ℝ F (q 0) (F (q 0))) := by
    rw [iteratedDeriv_succ', heq, comp_two F q hF hq, d1, d2]
  refine ⟨d1,d2,d3,?_⟩
  rw [iteratedDeriv_succ', heq, comp_three F q hF hq, d1, d2, d3]
  norm_cast

theorem autoStep_jets (F : E → E) (z : E) (hF : ContDiff ℝ ⊤ F) :
    let v := F z
    let A := fderiv ℝ F z
    let B := iteratedFDeriv ℝ 2 F z
    let C := iteratedFDeriv ℝ 3 F z
    deriv (fun h => autoStep F h z) 0 = v ∧
    iteratedDeriv 2 (fun h => autoStep F h z) 0 = A v ∧
    iteratedDeriv 3 (fun h => autoStep F h z) 0 = B (fun _ => v)+A (A v) ∧
    iteratedDeriv 4 (fun h => autoStep F h z) 0 =
      C (fun _ => v)+B ![A v,v]+(2:ℝ) • B ![v,A v]+A (B (fun _ => v)+A (A v)) := by
  dsimp only
  let v := F z
  let A := fderiv ℝ F z
  let B := iteratedFDeriv ℝ 2 F z
  let C := iteratedFDeriv ℝ 3 F z
  let K₂ := stage F z (1/2) (fun _ => v)
  let K₃ := stage F z (1/2) K₂
  let K₄ := stage F z 1 K₃
  have h₂ : ContDiff ℝ ⊤ K₂ := stage_smooth F z _ _ hF contDiff_const
  have h₃ : ContDiff ℝ ⊤ K₃ := stage_smooth F z _ _ hF h₂
  have h₄ : ContDiff ℝ ⊤ K₄ := stage_smooth F z _ _ hF h₃
  obtain ⟨k20,k21,k22,k23⟩ := stage_jets F z (1/2) (fun _ => v) hF contDiff_const
  change K₂ 0 = v at k20
  change deriv K₂ 0 = _ at k21
  change iteratedDeriv 2 K₂ 0 = _ at k22
  change iteratedDeriv 3 K₂ 0 = _ at k23
  norm_num [deriv_const, iteratedDeriv_const, multi_two_zero_left,
    multi_two_zero_right] at k21 k22 k23
  obtain ⟨k30,k31,k32,k33⟩ := stage_jets F z (1/2) K₂ hF h₂
  change K₃ 0 = v at k30
  change deriv K₃ 0 = _ at k31
  change iteratedDeriv 2 K₃ 0 = _ at k32
  change iteratedDeriv 3 K₃ 0 = _ at k33
  rw [k20] at k31
  rw [k20,k21] at k32
  rw [k20,k21,k22] at k33
  simp only [map_smul, multi_two_left, multi_two_right] at k32 k33
  obtain ⟨k40,k41,k42,k43⟩ := stage_jets F z 1 K₃ hF h₃
  change K₄ 0 = v at k40
  change deriv K₄ 0 = _ at k41
  change iteratedDeriv 2 K₄ 0 = _ at k42
  change iteratedDeriv 3 K₄ 0 = _ at k43
  rw [k30] at k41
  rw [k30,k31] at k42
  rw [k30,k31,k32] at k43
  simp only [map_add, map_smul, multi_two_left, multi_two_right] at k42 k43
  let w : ℝ → E := fun h => v+(2:ℝ) • K₂ h+(2:ℝ) • K₃ h+K₄ h
  have hw : ContDiff ℝ ⊤ w :=
    ((contDiff_const.add (contDiff_const.smul h₂)).add (contDiff_const.smul h₃)).add h₄
  have hstep : (fun h => autoStep F h z) = (fun h => z+((1/6:ℝ)*h) • w h) := by
    funext h
    simp [autoStep, w, K₂, K₃, K₄, stage, v, div_eq_mul_inv, mul_comm,
      ← Nat.cast_smul_eq_nsmul ℝ]
  have sj (n : ℕ) (hn : n ≤ 3) :
      iteratedDeriv (n+1) (fun h => autoStep F h z) 0 =
      (((n+1:ℕ):ℝ)*(1/6:ℝ)) •
        ((if n=0 then v else 0)+(2:ℝ) • iteratedDeriv n K₂ 0+
          (2:ℝ) • iteratedDeriv n K₃ 0+iteratedDeriv n K₄ 0) := by
    rw [hstep, jet_path w hw z (1/6) n hn, jet_weighted v K₂ K₃ K₄ h₂ h₃ h₄ n]
  refine ⟨?_,?_,?_,?_⟩
  · have H := sj 0 (by omega)
    simp only [Nat.zero_add, iteratedDeriv_one, iteratedDeriv_zero, k20,k30,k40] at H
    rw [H]
    dsimp only [v]
    norm_num
    module
  · have H := sj 1 (by omega)
    simp only [iteratedDeriv_one, k21,k31,k41] at H
    rw [H]
    norm_num
    module
  · have H := sj 2 (by omega)
    rw [k22,k32,k42] at H
    rw [H]
    norm_num
    module
  · have H := sj 3 (by omega)
    rw [k23,k33,k43] at H
    rw [H]
    simp only [map_add]
    norm_num
    module

theorem autoStep_smooth (F : E → E) (z : E) (hF : ContDiff ℝ ⊤ F) :
    ContDiff ℝ ⊤ (fun h => autoStep F h z) := by
  unfold autoStep
  fun_prop

theorem autoStep_local (F : E → E) (q : ℝ → E)
    (hF : ContDiff ℝ ⊤ F) (hq : ContDiff ℝ ⊤ q)
    (hode : ∀ t, HasDerivAt q (F (q t)) t) :
    PowBound 5 (fun h => ‖q h-autoStep F h (q 0)‖) := by
  let S : ℝ → E := fun h => autoStep F h (q 0)
  have hS : ContDiff ℝ ⊤ S := autoStep_smooth F (q 0) hF
  obtain ⟨q1,q2,q3,q4⟩ := trajectory_jets F q hF hq hode
  obtain ⟨s1,s2,s3,s4⟩ := autoStep_jets F (q 0) hF
  have hj : ∀ n ≤ 4, iteratedDeriv n q 0 = iteratedDeriv n S 0 := by
    intro n hn
    interval_cases n
    · simp [S,autoStep]
    · simpa only [iteratedDeriv_one] using q1.trans s1.symm
    · exact q2.trans s2.symm
    · exact q3.trans s3.symm
    · exact q4.trans s4.symm
  have hp : ∀ h, taylorWithinEval q 4 Set.univ 0 h = taylorWithinEval S 4 Set.univ 0 h := by
    intro h
    rw [show h=0+h by ring, taylorWithinEval_eq_sum, taylorWithinEval_eq_sum]
    apply Finset.sum_congr rfl
    intro n hn
    rw [hj n (by simpa using Nat.le_of_lt_succ (Finset.mem_range.mp hn))]
  have hqR : PowBound 5 (fun h => ‖q h-taylorWithinEval q 4 Set.univ 0 h‖) := by
    simpa using powBound_taylor_poly 4 q 0 (hq.of_le le_top)
  have hsR : PowBound 5 (fun h => ‖taylorWithinEval S 4 Set.univ 0 h-S h‖) := by
    simpa only [zero_add, norm_sub_rev] using powBound_taylor_poly 4 S 0 (hS.of_le le_top)
  apply powBound_add_of_eq hqR hsR
  intro h
  rw [hp h]
  dsimp only [S]
  abel

theorem autoStep_time {m : ℕ} (f : ℝ → (Fin m → ℝ) → (Fin m → ℝ))
    (t h : ℝ) (z : Fin m → ℝ) :
    autoStep (fun q : ℝ × (Fin m → ℝ) => (1, f q.1 q.2)) h (t,z) =
      (t+h, rk4 f t h z) := by
  ext i
  · simp [autoStep]
    ring
  · simp [autoStep, rk4]

end RK4Proof

theorem n01_rk4_part :
    ∀ (m : ℕ) (f : ℝ → (Fin m → ℝ) → (Fin m → ℝ)) (z : ℝ → (Fin m → ℝ)),
      ContDiff ℝ ⊤ (fun q : ℝ × (Fin m → ℝ) => f q.1 q.2) → ContDiff ℝ ⊤ z →
      (∀ t, HasDerivAt z (f t (z t)) t) → ∀ t,
      PowBound 5 (fun h => ‖z (t+h)-rk4 f t h (z t)‖) := by
  intro m f z hf hz hode t
  let F : (ℝ × (Fin m → ℝ)) → (ℝ × (Fin m → ℝ)) := fun p => (1,f p.1 p.2)
  let q : ℝ → (ℝ × (Fin m → ℝ)) := fun s => (t+s,z (t+s))
  have hF : ContDiff ℝ ⊤ F := contDiff_const.prodMk hf
  have hq : ContDiff ℝ ⊤ q :=
    (contDiff_const.add contDiff_id).prodMk (hz.comp (contDiff_const.add contDiff_id))
  have hq' : ∀ s, HasDerivAt q (F (q s)) s := by
    intro s
    have hs : HasDerivAt (fun s : ℝ => t+s) 1 s := (hasDerivAt_id s).const_add t
    have hzshift : HasDerivAt (fun r => z (t+r)) (f (t+s) (z (t+s))) s :=
      (hode (t+s)).comp_const_add t
    exact hs.prodMk hzshift
  have H := RK4Proof.autoStep_local F q hF hq hq'
  apply powBound_congr (e₁ := fun h => ‖q h-RK4Proof.autoStep F h (q 0)‖) _ H
  intro h
  simp [F,q,RK4Proof.autoStep_time,Prod.norm_def]

theorem n01_proved : N01 := by
  intro m f z hf hz hode t
  exact ⟨n01_euler_part m f z hf hz hode t,
    n01_rk4_part m f z hf hz hode t,n01_trapezoid_part m f z hf hz hode t⟩

#print axioms n01_proved
end DLWContract
