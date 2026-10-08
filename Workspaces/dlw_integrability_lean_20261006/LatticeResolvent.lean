import StartPoint

/-!
Concrete finite cyclic lattice resolvent, for every admissible M.
The prefix primitive is projected on both sides, so no lattice inverse
or potential-shift conclusion is assumed.
-/

namespace DLWLean
noncomputable section
open scoped BigOperators

def latticePrefix {M : ℕ} (f : Fin M → ℝ) (j : Fin M) : ℝ :=
  ∑ i, if i.val < j.val then f i else 0

theorem latticePrefix_add {M : ℕ} (f g : Fin M → ℝ) (j : Fin M) :
    latticePrefix (fun i => f i + g i) j = latticePrefix f j + latticePrefix g j := by
  unfold latticePrefix
  rw [← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro i _
  split_ifs <;> ring

theorem latticePrefix_smul {M : ℕ} (a : ℝ) (f : Fin M → ℝ) (j : Fin M) :
    latticePrefix (fun i => a * f i) j = a * latticePrefix f j := by
  unfold latticePrefix
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro i _
  split_ifs <;> ring

theorem latticePrefix_zero {M : ℕ} (f : Fin M → ℝ) (j : Fin M) (hj : j.val = 0) :
    latticePrefix f j = 0 := by
  simp [latticePrefix, hj]

theorem latticePrefix_successor {M : ℕ} (f : Fin M → ℝ) (j k : Fin M)
    (hjk : j.val = k.val + 1) : latticePrefix f j - latticePrefix f k = f k := by
  unfold latticePrefix
  rw [← Finset.sum_sub_distrib]
  have hpoint : ∀ i : Fin M,
      (if i.val < j.val then f i else 0) - (if i.val < k.val then f i else 0) =
        if i = k then f i else 0 := by
    intro i
    by_cases hik : i = k
    · subst i
      have hkj : k.val < j.val := by omega
      simp [hkj]
    · have hval : i.val ≠ k.val := fun h => hik (Fin.ext h)
      by_cases hiklt : i.val < k.val
      · have hijlt : i.val < j.val := by omega
        simp [hiklt, hijlt, hik]
      · have hijlt : ¬ i.val < j.val := by omega
        simp [hiklt, hijlt, hik]
  simp_rw [hpoint]
  simp

theorem latticePrefix_last {M : ℕ} (f : Fin M → ℝ) (j : Fin M)
    (hj : j.val + 1 = M) : latticePrefix f j + f j = ∑ i, f i := by
  have hpoint : ∀ i : Fin M,
      (if i.val < j.val then f i else 0) + (if i = j then f i else 0) = f i := by
    intro i
    by_cases hij : i = j
    · subst i
      simp
    · have hval : i.val ≠ j.val := fun h => hij (Fin.ext h)
      have hijlt : i.val < j.val := by have := i.isLt; omega
      simp [hij, hijlt]
  have hsum := congrArg (fun a : Fin M → ℝ => ∑ i, a i) (funext hpoint)
  simpa only [Finset.sum_add_distrib, Finset.sum_ite_eq', Finset.mem_univ,
    ite_true, latticePrefix] using hsum

theorem previousSite_val_zero (par : FieldParameters) (j : Fin par.M)
    (hj : j.val = 0) : (previousSite par j).val + 1 = par.M := by
  change (j.val + par.M - 1) % par.M + 1 = par.M
  rw [hj]
  simp only [zero_add]
  rw [Nat.mod_eq_of_lt (by have := par.M_ge_two; omega)]
  omega

theorem previousSite_val_pos (par : FieldParameters) (j : Fin par.M)
    (hj : 0 < j.val) : (previousSite par j).val + 1 = j.val := by
  change (j.val + par.M - 1) % par.M + 1 = j.val
  have heq : j.val + par.M - 1 = (j.val - 1) + par.M := by omega
  rw [heq, Nat.add_mod]
  simp only [Nat.mod_self, Nat.add_zero, Nat.mod_mod]
  rw [Nat.mod_eq_of_lt (by have := j.isLt; omega)]
  omega

theorem latticePrefix_cyclic_difference (par : FieldParameters)
    (f : Fin par.M → ℝ) (hf : latticeMean f = 0) (j : Fin par.M) :
    latticePrefix f j - latticePrefix f (previousSite par j) =
      f (previousSite par j) := by
  by_cases hj : j.val = 0
  · have hp0 := latticePrefix_zero f j hj
    have hlast := latticePrefix_last f (previousSite par j) (previousSite_val_zero par j hj)
    have hsum : (∑ i, f i) = 0 := by
      rw [sum_eq_card_mul_latticeMean par.M_ne_zero f, hf, mul_zero]
    linarith
  · apply latticePrefix_successor
    have hp := previousSite_val_pos par j (by omega)
    omega

/-- Prefix primitive of the centered cyclic difference equation. -/
def latticePrimitive (par : FieldParameters) (f : Fin par.M → ℝ) (j : Fin par.M) : ℝ :=
  par.h * (latticePrefix f j + f j / 2)

def latticeProjectionLinear (par : FieldParameters) :
    (Fin par.M → ℝ) →ₗ[ℝ] (Fin par.M → ℝ) where
  toFun := latticeP0
  map_add' f g := by
    funext j
    change (f j + g j) - latticeMean (fun i => f i + g i) =
      (f j - latticeMean f) + (g j - latticeMean g)
    rw [latticeMean_add]
    ring
  map_smul' a f := by
    funext j
    change a * f j - latticeMean (fun i => a * f i) = a * (f j - latticeMean f)
    rw [latticeMean_mul_left]
    ring

def latticePrimitiveLinear (par : FieldParameters) :
    (Fin par.M → ℝ) →ₗ[ℝ] (Fin par.M → ℝ) where
  toFun := latticePrimitive par
  map_add' f g := by
    funext j
    change par.h * (latticePrefix (fun i => f i + g i) j + (f j + g j) / 2) =
      par.h * (latticePrefix f j + f j / 2) + par.h * (latticePrefix g j + g j / 2)
    rw [latticePrefix_add]
    ring
  map_smul' a f := by
    funext j
    change par.h * (latticePrefix (fun i => a * f i) j + a * f j / 2) =
      a * (par.h * (latticePrefix f j + f j / 2))
    rw [latticePrefix_smul]
    ring

/-- R = P0 Q P0, where Q is the explicitly defined finite prefix primitive. -/
def latticeResolvent (par : FieldParameters) :
    (Fin par.M → ℝ) →ₗ[ℝ] (Fin par.M → ℝ) :=
  (latticeProjectionLinear par).comp
    ((latticePrimitiveLinear par).comp (latticeProjectionLinear par))

theorem latticeResolvent_apply (par : FieldParameters) (f : Fin par.M → ℝ)
    (j : Fin par.M) :
    latticeResolvent par f j = latticeP0 (latticePrimitive par (latticeP0 f)) j := rfl

theorem latticeP0_idempotent {M : ℕ} (hM : M ≠ 0) (f : Fin M → ℝ) :
    latticeP0 (latticeP0 f) = latticeP0 f := by
  funext j
  rw [latticeP0, latticeMean_P0 hM]
  simp

theorem latticeResolvent_projection (par : FieldParameters) (f : Fin par.M → ℝ) :
    latticeResolvent par (latticeP0 f) = latticeResolvent par f := by
  funext j
  rw [latticeResolvent_apply, latticeResolvent_apply, latticeP0_idempotent par.M_ne_zero]

theorem latticeResolvent_zero_mean (par : FieldParameters) (f : Fin par.M → ℝ) :
    latticeMean (latticeResolvent par f) = 0 :=
  latticeMean_P0 par.M_ne_zero (latticePrimitive par (latticeP0 f))

theorem latticePrimitive_cyclic_difference (par : FieldParameters)
    (f : Fin par.M → ℝ) (hf : latticeMean f = 0) (j : Fin par.M) :
    latticePrimitive par f j - latticePrimitive par f (previousSite par j) =
      par.h * (f j + f (previousSite par j)) / 2 := by
  have hp := latticePrefix_cyclic_difference par f hf j
  unfold latticePrimitive
  calc
    par.h * (latticePrefix f j + f j / 2) -
        par.h * (latticePrefix f (previousSite par j) + f (previousSite par j) / 2) =
      par.h * ((latticePrefix f j - latticePrefix f (previousSite par j)) +
        (f j - f (previousSite par j)) / 2) := by ring
    _ = par.h * (f (previousSite par j) + (f j - f (previousSite par j)) / 2) := by rw [hp]
    _ = par.h * (f j + f (previousSite par j)) / 2 := by ring

theorem latticeResolvent_cyclic_difference (par : FieldParameters)
    (f : Fin par.M → ℝ) (j : Fin par.M) :
    latticeResolvent par f j - latticeResolvent par f (previousSite par j) =
      par.h * (latticeP0 f j + latticeP0 f (previousSite par j)) / 2 := by
  rw [latticeResolvent_apply, latticeResolvent_apply]
  change (latticePrimitive par (latticeP0 f) j -
      latticeMean (latticePrimitive par (latticeP0 f))) -
    (latticePrimitive par (latticeP0 f) (previousSite par j) -
      latticeMean (latticePrimitive par (latticeP0 f))) = _
  calc
    _ = latticePrimitive par (latticeP0 f) j -
      latticePrimitive par (latticeP0 f) (previousSite par j) := by ring
    _ = _ := latticePrimitive_cyclic_difference par (latticeP0 f)
      (latticeMean_P0 par.M_ne_zero f) j

theorem deltaMinus_latticeResolvent (par : FieldParameters)
    (f : Fin par.M → ℝ) (j : Fin par.M) :
    deltaMinus par (latticeResolvent par f) j = averageMinus par (latticeP0 f) j := by
  unfold deltaMinus averageMinus
  rw [latticeResolvent_cyclic_difference]
  field_simp [ne_of_gt par.h_pos]

def nextSite (par : FieldParameters) (j : Fin par.M) : Fin par.M :=
  ⟨(j.val + 1) % par.M, Nat.mod_lt _ (lt_of_lt_of_le (by decide : 0 < 2) par.M_ge_two)⟩

theorem previousSite_nextSite (par : FieldParameters) (j : Fin par.M) :
    previousSite par (nextSite par j) = j := by
  apply Fin.ext
  by_cases hj : j.val + 1 < par.M
  · have hn : (nextSite par j).val = j.val + 1 := Nat.mod_eq_of_lt hj
    have hp := previousSite_val_pos par (nextSite par j) (by rw [hn]; omega)
    omega
  · have hjlast : j.val + 1 = par.M := by have := j.isLt; omega
    have hn : (nextSite par j).val = 0 := by simp [nextSite, hjlast]
    have hp := previousSite_val_zero par (nextSite par j) hn
    omega

/-- Actual lattice heat potential, with an arbitrary lattice-common term. -/
def latticeHeatPotential (par : FieldParameters) (f : Fin par.M → ℝ)
    (common : ℝ) (j : Fin par.M) : ℝ :=
  latticeResolvent par f j / 2 - par.h * f j / 4 + common

theorem latticeHeatPotential_shift (par : FieldParameters)
    (f : Fin par.M → ℝ) (hf : latticeMean f = 0) (common : ℝ) (j : Fin par.M) :
    latticeHeatPotential par f common (nextSite par j) -
        latticeHeatPotential par f common j = par.h * f j / 2 := by
  have hdiff := latticeResolvent_cyclic_difference par f (nextSite par j)
  rw [previousSite_nextSite] at hdiff
  simp only [latticeP0, hf, sub_zero] at hdiff
  unfold latticeHeatPotential
  linarith

theorem latticePrefix_pairing_symmetric {M : ℕ} (f g : Fin M → ℝ) :
    (∑ i, f i * latticePrefix g i) + (∑ i, latticePrefix f i * g i) +
        (∑ i, f i * g i) = (∑ i, f i) * (∑ i, g i) := by
  have hleft : (∑ i, f i * latticePrefix g i) =
      ∑ i, ∑ k, if k.val < i.val then f i * g k else 0 := by
    simp only [latticePrefix, Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro i _
    apply Finset.sum_congr rfl
    intro k _
    split_ifs <;> ring
  have hright : (∑ i, latticePrefix f i * g i) =
      ∑ i, ∑ k, if i.val < k.val then f i * g k else 0 := by
    simp only [latticePrefix, Finset.sum_mul]
    rw [Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro i _
    apply Finset.sum_congr rfl
    intro k _
    split_ifs <;> ring
  have hdiag : (∑ i, f i * g i) =
      ∑ i, ∑ k, if i = k then f i * g k else 0 := by
    symm
    apply Finset.sum_congr rfl
    intro i _
    simp
  rw [hleft, hright, hdiag]
  simp_rw [← Finset.sum_add_distrib]
  rw [Finset.sum_mul]
  simp_rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro i _
  apply Finset.sum_congr rfl
  intro k _
  rcases lt_trichotomy i.val k.val with hik | hik | hki
  · have hnot : ¬ k.val < i.val := by omega
    have hne : i ≠ k := by intro heq; subst k; omega
    simp [hik, hnot, hne]
  · have heq : i = k := Fin.ext hik
    subst k
    simp
  · have hnot : ¬ i.val < k.val := by omega
    have hne : i ≠ k := by intro heq; subst k; omega
    simp [hki, hnot, hne]

theorem latticePrimitive_pairing_symmetric (par : FieldParameters)
    (f g : Fin par.M → ℝ) :
    (∑ i, f i * latticePrimitive par g i) +
        (∑ i, latticePrimitive par f i * g i) =
      par.h * (∑ i, f i) * (∑ i, g i) := by
  have hleft : (∑ i, f i * latticePrimitive par g i) =
      par.h * (∑ i, f i * latticePrefix g i) + par.h / 2 * (∑ i, f i * g i) := by
    calc
      _ = ∑ i, (par.h * (f i * latticePrefix g i) + par.h / 2 * (f i * g i)) := by
        apply Finset.sum_congr rfl
        intro i _
        unfold latticePrimitive
        ring
      _ = _ := by rw [Finset.sum_add_distrib, ← Finset.mul_sum, ← Finset.mul_sum]
  have hright : (∑ i, latticePrimitive par f i * g i) =
      par.h * (∑ i, latticePrefix f i * g i) + par.h / 2 * (∑ i, f i * g i) := by
    calc
      _ = ∑ i, (par.h * (latticePrefix f i * g i) + par.h / 2 * (f i * g i)) := by
        apply Finset.sum_congr rfl
        intro i _
        unfold latticePrimitive
        ring
      _ = _ := by rw [Finset.sum_add_distrib, ← Finset.mul_sum, ← Finset.mul_sum]
  rw [hleft, hright]
  calc
    _ = par.h * ((∑ i, f i * latticePrefix g i) +
      (∑ i, latticePrefix f i * g i) + (∑ i, f i * g i)) := by ring
    _ = par.h * ((∑ i, f i) * (∑ i, g i)) := by rw [latticePrefix_pairing_symmetric]
    _ = _ := by ring

theorem latticeP0_pairing_selfadjoint {M : ℕ} (f g : Fin M → ℝ) :
    (∑ i, f i * latticeP0 g i) = ∑ i, latticeP0 f i * g i := by
  simp only [latticeP0, mul_sub, sub_mul, Finset.sum_sub_distrib,
    ← Finset.sum_mul, ← Finset.mul_sum]
  unfold latticeMean
  ring

theorem latticeResolvent_skew (par : FieldParameters) (f g : Fin par.M → ℝ) :
    (∑ i, f i * latticeResolvent par g i) =
      -(∑ i, latticeResolvent par f i * g i) := by
  have hleft : (∑ i, f i * latticeResolvent par g i) =
      ∑ i, latticeP0 f i * latticePrimitive par (latticeP0 g) i := by
    simp_rw [latticeResolvent_apply]
    exact latticeP0_pairing_selfadjoint f (latticePrimitive par (latticeP0 g))
  have hright : (∑ i, latticeResolvent par f i * g i) =
      ∑ i, latticePrimitive par (latticeP0 f) i * latticeP0 g i := by
    simp_rw [latticeResolvent_apply]
    exact (latticeP0_pairing_selfadjoint (latticePrimitive par (latticeP0 f)) g).symm
  have hsf : (∑ i, latticeP0 f i) = 0 := by
    rw [sum_eq_card_mul_latticeMean par.M_ne_zero, latticeMean_P0 par.M_ne_zero, mul_zero]
  have hsg : (∑ i, latticeP0 g i) = 0 := by
    rw [sum_eq_card_mul_latticeMean par.M_ne_zero, latticeMean_P0 par.M_ne_zero, mul_zero]
  have hsym := latticePrimitive_pairing_symmetric par (latticeP0 f) (latticeP0 g)
  rw [hsf, hsg, mul_zero] at hsym
  rw [hleft, hright]
  linarith

theorem kernel_cyclic_difference (par : FieldParameters) (f : Fin par.M → ℝ)
    (hf : ∀ j, f j - f (previousSite par j) = 0) (j : Fin par.M) :
    f j = latticeMean f := by
  let first : Fin par.M := ⟨0, lt_of_lt_of_le (by decide : 0 < 2) par.M_ge_two⟩
  have hconst : ∀ n : ℕ, ∀ k : Fin par.M, k.val = n → f k = f first := by
    intro n
    induction n with
    | zero =>
      intro k hk
      have hfirst : k = first := Fin.ext (by simpa only [first] using hk)
      rw [hfirst]
    | succ n ih =>
      intro k hk
      have hp : (previousSite par k).val = n := by
        have := previousSite_val_pos par k (by omega)
        omega
      exact (sub_eq_zero.mp (hf k)).trans (ih (previousSite par k) hp)
  have hfun : f = fun _ => f first := funext fun k => hconst k.val k rfl
  have hmean : latticeMean f = f first := by
    rw [hfun, latticeMean_const par.M_ne_zero]
  exact (hconst j.val j rfl).trans hmean.symm

theorem kernel_deltaMinus (par : FieldParameters) (f : Fin par.M → ℝ)
    (hf : ∀ j, deltaMinus par f j = 0) (j : Fin par.M) :
    f j = latticeMean f := by
  apply kernel_cyclic_difference par f _ j
  intro k
  have hscale := congrArg (fun a : ℝ => a * par.h) (hf k)
  simpa only [deltaMinus, div_mul_cancel₀ _ (ne_of_gt par.h_pos), zero_mul] using hscale

theorem zeroMean_deltaMinus_unique (par : FieldParameters)
    (f g : Fin par.M → ℝ) (hf : latticeMean f = 0) (hg : latticeMean g = 0)
    (hdelta : ∀ j, deltaMinus par f j = deltaMinus par g j) : f = g := by
  have hkernel : ∀ j, (f j - g j) - (f (previousSite par j) - g (previousSite par j)) = 0 := by
    intro j
    have hscale := congrArg (fun a : ℝ => a * par.h) (hdelta j)
    simp only [deltaMinus, div_mul_cancel₀ _ (ne_of_gt par.h_pos)] at hscale
    linarith
  funext j
  have hk := kernel_cyclic_difference par (fun i => f i - g i) hkernel j
  rw [latticeMean_sub, hf, hg] at hk
  linarith

/-- The concrete R is the unique zero-mean solution of the defining
inverse-difference equation δ_- r = M_- P0 f. -/
theorem latticeResolvent_unique (par : FieldParameters) (f r : Fin par.M → ℝ)
    (hr : latticeMean r = 0)
    (heq : ∀ j, deltaMinus par r j = averageMinus par (latticeP0 f) j) :
    r = latticeResolvent par f := by
  apply zeroMean_deltaMinus_unique par r (latticeResolvent par f)
    hr (latticeResolvent_zero_mean par f)
  intro j
  rw [heq j, deltaMinus_latticeResolvent]

end
end DLWLean
