import Independence
import Mathlib.LinearAlgebra.Dual.Lemmas

namespace DLWLean
noncomputable section
open scoped BigOperators

variable {V : Type*} [AddCommGroup V] [Module ℝ V]

def finiteCovectorCombination {N : ℕ} (f : Fin N → V →ₗ[ℝ] ℝ) :
    (Fin N → ℝ) →ₗ[ℝ] V →ₗ[ℝ] ℝ where
  toFun a := ∑ i, a i • f i
  map_add' a b := by simp only [Pi.add_apply, add_smul, Finset.sum_add_distrib]
  map_smul' r a := by
    simp only [Pi.smul_apply, smul_eq_mul, mul_smul, Finset.smul_sum, RingHom.id_apply]

/-- A finite independent list of actual covectors always admits an
evaluation minor equal to the identity. This uses only vector-space
duality, with finite-dimensional coefficient space; V may be infinite.
-/
theorem covectors_independent_exists_identity_minor {N : ℕ}
    (f : Fin N → V →ₗ[ℝ] ℝ) (hf : LinearIndependent ℝ f) :
    ∃ directions : Fin N → V, covectorMinor f directions = 1 := by
  classical
  let B := finiteCovectorCombination f
  have hinj : Function.Injective B := by
    intro a b hab
    have hzero : B (a - b) = 0 := by rw [map_sub, hab, sub_self]
    have hcoeff := Fintype.linearIndependent_iff.mp hf (a - b) hzero
    funext i
    exact sub_eq_zero.mp (hcoeff i)
  have hsurj : Function.Surjective B.flip :=
    (LinearMap.flip_injective_iff₂ (B := B.flip)).mp hinj
  let eval (j : Fin N) : (Fin N → ℝ) →ₗ[ℝ] ℝ :=
    { toFun := fun a => a j
      map_add' := fun _ _ => rfl
      map_smul' := fun _ _ => rfl }
  choose directions hdirections using fun j => hsurj (eval j)
  refine ⟨directions, ?_⟩
  ext i j
  have h := congrArg (fun g : (Fin N → ℝ) →ₗ[ℝ] ℝ => g (Pi.single i 1))
    (hdirections j)
  simp only [B, finiteCovectorCombination, LinearMap.flip_apply,
    LinearMap.coe_mk, AddHom.coe_mk, LinearMap.sum_apply, LinearMap.smul_apply,
    smul_eq_mul, eval] at h
  have hsum : (∑ k : Fin N, (Pi.single i (1 : ℝ) : Fin N → ℝ) k * f k (directions j)) =
      f i (directions j) := by
    rw [Finset.sum_eq_single i]
    · simp only [Pi.single_eq_same, one_mul]
    · intro k _ hki
      rw [Pi.single_eq_of_ne hki, zero_mul]
    · simp
  rw [hsum] at h
  change f i (directions j) = (1 : Matrix (Fin N) (Fin N) ℝ) i j
  simpa [Matrix.one_apply, Pi.single_apply, eq_comm] using h

theorem covectors_independent_exists_nonzero_minor {N : ℕ}
    (f : Fin N → V →ₗ[ℝ] ℝ) (hf : LinearIndependent ℝ f) :
    ∃ directions : Fin N → V, (covectorMinor f directions).det ≠ 0 := by
  obtain ⟨directions, hdirections⟩ := covectors_independent_exists_identity_minor f hf
  exact ⟨directions, by rw [hdirections, Matrix.det_one]; exact one_ne_zero⟩

#print axioms covectors_independent_exists_identity_minor
end
end DLWLean
