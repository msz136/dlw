/-
  Direction B — spectral / pseudo-spectral semidiscretisation of the DLW system.
  Module 1: the Fourier multiplier on the retained mode band -N..N.

  Setting.  Only `y` is discretised; `x` and `t` stay continuous.  On a
  `2*pi`-periodic `y`-domain the coefficient vector `a : Fin (2*N+1) -> C`
  represents the trigonometric polynomial `sum_i a i * exp (I * (modeIdx N i) * y)`.
  Because `d/dy` of that polynomial only rescales each coefficient, the whole
  `y`-derivative is the *diagonal* multiplier `i * modeIdx N i`, encoded in
  `multLin N`.

  What is formalised here:
    * `modeIdx`, `zeroIdx`, and the exact kernel of the multiplier
      (`mult_eq_zero_iff`, `kernel_eq_zero_mode_line`): `d/dy` kills exactly the
      zero-mode line.  This is the discrete statement that a `y`-independent
      field has zero `y`-derivative, i.e. the zero-mode sector is the kernel.
    * `multLin` is diagonal in the mode basis and each mode projector is a
      spectral projector: `multLin (modeProj j a) = (i j) • modeProj j a`.
      Consequently the multiplier commutes with every mode projection, in
      particular with the mean functional; `mean (d/dy a) = 0`.
    * On the zero-mean subspace (where the zero mode is absent) the multiplier
      is *invertible*, with explicit inverse `invMultLin`:
      `mult_invMult` / `invMult_mult`, assembled into the linear equivalence
      `zeroMeanEquiv`.  This is the exact statement that the constraint
      `w = u_y` can be inverted mode by mode for every non-zero mode; the
      untouchable direction is exactly the kernel line found above.

  Nothing here is about the ill-posedness of the continuous symbol; that is
  `Spectral/Growth.lean`.
-/
import Mathlib.Basic.Complex.Basic
import Mathlib.LinearAlgebra.Pi
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Tactic

namespace DLW.Spectral

open scoped BigOperators

/-! ## Mode indexing on the retained band `-N, ..., N` -/

/-- Wavenumber (`Fourier mode index`) carried by slot `i` of the band `-N..N`. -/
def modeIdx (N : ℕ) (i : Fin (2 * N + 1)) : ℤ := ((i : ℕ) : ℤ) - (N : ℤ)

/-- The slot carrying the zero mode `l = 0`. -/
def zeroIdx (N : ℕ) : Fin (2 * N + 1) := ⟨N, by omega⟩

@[simp] theorem modeIdx_zeroIdx (N : ℕ) : modeIdx N (zeroIdx N) = 0 := by
  simp [modeIdx, zeroIdx]

theorem modeIdx_eq_zero_iff {N : ℕ} {i : Fin (2 * N + 1)} :
    modeIdx N i = 0 ↔ i = zeroIdx N := by
  constructor
  · intro h
    refine Fin.ext ?_
    have h' : ((i : ℕ) : ℤ) = (N : ℤ) := by
      have : ((i : ℕ) : ℤ) - (N : ℤ) = 0 := h
      omega
    exact_mod_cast h'
  · rintro rfl
    simp

theorem modeIdx_ne_zero_iff {N : ℕ} {i : Fin (2 * N + 1)} :
    modeIdx N i ≠ 0 ↔ i ≠ zeroIdx N := Iff.not modeIdx_eq_zero_iff

/-- Only the zero slot carries the zero mode. -/
theorem modeIdx_injective (N : ℕ) : Function.Injective (modeIdx N) := by
  intro i j h
  refine Fin.ext ?_
  have h' : ((i : ℕ) : ℤ) = ((j : ℕ) : ℤ) := by
    have : ((i : ℕ) : ℤ) - (N : ℤ) = ((j : ℕ) : ℤ) - (N : ℤ) := h
    omega
  exact_mod_cast h'

/-! ## The derivative multiplier `i * l` -/

/-- The Fourier multiplier of `d/dy` on the retained band: the spectral
    representation of the `y`-derivative of the truncated
    Fourier–Galerkin semidiscretisation. -/
noncomputable def multLin (N : ℕ) :
    (Fin (2 * N + 1) → ℂ) →ₗ[ℂ] (Fin (2 * N + 1) → ℂ) where
  toFun a := fun i => ((modeIdx N i : ℂ) * Complex.I) * a i
  map_add' a b := by
    funext i
    simp only [Pi.add_apply, mul_add]
  map_smul' c a := by
    funext i
    simp only [Pi.smul_apply, smul_eq_mul, RingHom.id_apply]
    ring

@[simp] theorem multLin_apply (N : ℕ) (a : Fin (2 * N + 1) → ℂ) (i : Fin (2 * N + 1)) :
    multLin N a i = ((modeIdx N i : ℂ) * Complex.I) * a i := rfl

/-- The multiplier kills the zero mode: this is `d/dy` applied to a
    `y`-independent field. -/
theorem mult_zero_mode (N : ℕ) (a : Fin (2 * N + 1) → ℂ) :
    multLin N a (zeroIdx N) = 0 := by
  simp

/-- Exact kernel: the multiplier vanishes precisely on vectors supported on the
    zero mode.  Nothing else is annihilated. -/
theorem mult_eq_zero_iff (N : ℕ) (a : Fin (2 * N + 1) → ℂ) :
    multLin N a = 0 ↔ ∀ i, i ≠ zeroIdx N → a i = 0 := by
  constructor
  · intro h i hi
    have h1 : ((modeIdx N i : ℂ) * Complex.I) * a i = 0 := by
      have h2 := congrFun h i
      simpa using h2
    rcases mul_eq_zero.mp h1 with h2 | h3
    · rcases mul_eq_zero.mp h2 with h4 | h5
      · exact absurd (by exact_mod_cast h4 : modeIdx N i = 0) (modeIdx_ne_zero_iff.mpr hi)
      · exact absurd h5 Complex.I_ne_zero
    · exact h3
  · intro h
    funext i
    by_cases hi : i = zeroIdx N
    · subst hi
      simp
    · simp [h i hi]

/-- Kernel, stated as a one-dimensional line: the kernel is exactly the span of
    the zero-mode vector.  This is the discrete form of "`d/dy` kills
    `y`-independent fields and nothing else". -/
theorem kernel_eq_zero_mode_line (N : ℕ) (a : Fin (2 * N + 1) → ℂ) :
    multLin N a = 0 ↔ ∃ c : ℂ, a = c • Pi.single (zeroIdx N) 1 := by
  rw [mult_eq_zero_iff]
  constructor
  · intro h
    refine ⟨a (zeroIdx N), ?_⟩
    funext i
    by_cases hi : i = zeroIdx N
    · subst hi
      simp
    · have hai : a i = 0 := h i hi
      simp [hai, Pi.single_eq_of_ne hi]
  · rintro ⟨c, rfl⟩ i hi
    simp [Pi.single_eq_of_ne hi]

/-! ## The zero-mean subspace and inversion of the multiplier -/

/-- The zero-mean subspace: coefficient vectors whose zero mode vanishes.
    This is the subspace on which `d/dy` can be inverted. -/
def zeroMean (N : ℕ) : Submodule ℂ (Fin (2 * N + 1) → ℂ) where
  carrier := {a | a (zeroIdx N) = 0}
  zero_mem' := by simp
  add_mem' := by
    intro a b ha hb
    have ha' : a (zeroIdx N) = 0 := ha
    have hb' : b (zeroIdx N) = 0 := hb
    simp [ha', hb']
  smul_mem' := by
    intro c a ha
    have ha' : a (zeroIdx N) = 0 := ha
    simp [ha']

@[simp] theorem mem_zeroMean_iff (N : ℕ) (a : Fin (2 * N + 1) → ℂ) :
    a ∈ zeroMean N ↔ a (zeroIdx N) = 0 := Iff.rfl

/-- Explicit inverse of the derivative multiplier on the non-zero modes. -/
noncomputable def invMultLin (N : ℕ) :
    (Fin (2 * N + 1) → ℂ) →ₗ[ℂ] (Fin (2 * N + 1) → ℂ) where
  toFun a := fun i =>
    if modeIdx N i = 0 then 0 else ((modeIdx N i : ℂ) * Complex.I)⁻¹ * a i
  map_add' a b := by
    funext i
    show (if modeIdx N i = 0 then 0
        else ((modeIdx N i : ℂ) * Complex.I)⁻¹ * (a i + b i))
      = (if modeIdx N i = 0 then 0
          else ((modeIdx N i : ℂ) * Complex.I)⁻¹ * a i)
        + (if modeIdx N i = 0 then 0
          else ((modeIdx N i : ℂ) * Complex.I)⁻¹ * b i)
    by_cases h : modeIdx N i = 0
    · simp [h]
    · rw [if_neg h, if_neg h, if_neg h, mul_add]
  map_smul' c a := by
    funext i
    by_cases h : modeIdx N i = 0
    · simp [h]
    · simp only [Pi.smul_apply, smul_eq_mul, if_neg h, RingHom.id_apply]
      ring

@[simp] theorem invMultLin_apply (N : ℕ) (a : Fin (2 * N + 1) → ℂ) (i : Fin (2 * N + 1)) :
    invMultLin N a i =
      (if modeIdx N i = 0 then 0 else ((modeIdx N i : ℂ) * Complex.I)⁻¹ * a i) := rfl

@[simp] theorem invMultLin_zeroIdx (N : ℕ) (a : Fin (2 * N + 1) → ℂ) :
    invMultLin N a (zeroIdx N) = 0 := by
  simp

/-- Left inverse on the zero-mean subspace: `d/dy` is injective there. -/
theorem invMult_mult (N : ℕ) (a : Fin (2 * N + 1) → ℂ) (ha : a (zeroIdx N) = 0) :
    invMultLin N (multLin N a) = a := by
  funext i
  by_cases h : modeIdx N i = 0
  · have hi : i = zeroIdx N := modeIdx_eq_zero_iff.mp h
    subst hi
    simp [ha]
  · have hne : ((modeIdx N i : ℂ) * Complex.I) ≠ 0 :=
      mul_ne_zero (by exact_mod_cast h) Complex.I_ne_zero
    simp only [invMultLin_apply, multLin_apply]
    rw [if_neg h, inv_mul_cancel_left₀ hne]

/-- Right inverse on the zero-mean subspace: `u` is recovered from `w = u_y`.
    This is the exact inversion identity for the non-zero modes. -/
theorem mult_invMult (N : ℕ) (a : Fin (2 * N + 1) → ℂ) (ha : a (zeroIdx N) = 0) :
    multLin N (invMultLin N a) = a := by
  funext i
  by_cases h : modeIdx N i = 0
  · have hi : i = zeroIdx N := modeIdx_eq_zero_iff.mp h
    subst hi
    simp [ha]
  · have hne : ((modeIdx N i : ℂ) * Complex.I) ≠ 0 :=
      mul_ne_zero (by exact_mod_cast h) Complex.I_ne_zero
    simp only [multLin_apply, invMultLin_apply]
    rw [if_neg h, ← mul_assoc, mul_inv_cancel₀ hne, one_mul]

theorem mult_mem_zeroMean (N : ℕ) {a : Fin (2 * N + 1) → ℂ} (ha : a ∈ zeroMean N) :
    multLin N a ∈ zeroMean N := by
  simpa using mult_zero_mode N a

theorem invMult_mem_zeroMean (N : ℕ) {a : Fin (2 * N + 1) → ℂ} (ha : a ∈ zeroMean N) :
    invMultLin N a ∈ zeroMean N := by
  simpa using invMultLin_zeroIdx N a

/-- The derivative multiplier restricted to the zero-mean subspace is a linear
    equivalence.  Its inverse is the mode-by-mode division `1/(i l)`; the
    excluded direction is exactly the kernel line `kernel_eq_zero_mode_line`. -/
noncomputable def zeroMeanEquiv (N : ℕ) : (zeroMean N) ≃ₗ[ℂ] (zeroMean N) where
  toFun a := ⟨multLin N a.1, mult_mem_zeroMean N a.2⟩
  invFun a := ⟨invMultLin N a.1, invMult_mem_zeroMean N a.2⟩
  left_inv a := by
    refine Subtype.ext ?_
    exact invMult_mult N a.1 a.2
  right_inv a := by
    refine Subtype.ext ?_
    exact mult_invMult N a.1 a.2
  map_add' a b := by
    refine Subtype.ext ?_
    exact map_add (multLin N) a.1 b.1
  map_smul' c a := by
    refine Subtype.ext ?_
    exact map_smul (multLin N) c a.1

/-! ## Diagonal structure: the multiplier commutes with every mode projection -/

/-- Spectral projector onto the slot `j`. -/
noncomputable def modeProj (N : ℕ) (j : Fin (2 * N + 1)) :
    (Fin (2 * N + 1) → ℂ) →ₗ[ℂ] (Fin (2 * N + 1) → ℂ) where
  toFun a := Pi.single j (a j)
  map_add' a b := by
    funext i
    by_cases h : i = j
    · subst h; simp
    · simp [Pi.single_eq_of_ne h]
  map_smul' c a := by
    funext i
    by_cases h : i = j
    · subst h; simp
    · simp [Pi.single_eq_of_ne h]

/-- Each mode projector is an eigenvector of the derivative multiplier with
    eigenvalue `i * l`: the multiplier maps the `j`-th mode line into itself and
    therefore commutes with every mode projection. -/
theorem mult_comp_modeProj (N : ℕ) (j : Fin (2 * N + 1)) (a : Fin (2 * N + 1) → ℂ) :
    multLin N (modeProj N j a) = ((modeIdx N j : ℂ) * Complex.I) • modeProj N j a := by
  funext i
  by_cases h : i = j
  · subst h
    simp [modeProj, Pi.smul_apply, smul_eq_mul]
  · simp [modeProj, Pi.single_eq_of_ne h]

/-- The same statement on the other side; together the two identities say that
    `multLin` is diagonal in the mode basis. -/
theorem modeProj_comp_mult (N : ℕ) (j : Fin (2 * N + 1)) (a : Fin (2 * N + 1) → ℂ) :
    modeProj N j (multLin N a) = ((modeIdx N j : ℂ) * Complex.I) • modeProj N j a := by
  funext i
  by_cases h : i = j
  · subst h
    simp [modeProj, Pi.smul_apply, smul_eq_mul]
  · simp [modeProj, Pi.single_eq_of_ne h]

/-- A pure zero mode has zero `y`-derivative. -/
theorem mult_modeProj_zero (N : ℕ) (a : Fin (2 * N + 1) → ℂ) :
    multLin N (modeProj N (zeroIdx N) a) = 0 := by
  rw [mult_comp_modeProj, modeIdx_zeroIdx]
  simp

/-- The mean functional annihilates `∂_y`: `mean (∂_y a) = 0`, i.e. `∂_y` and the
    mean commute with `∂_y mean = 0`. -/
theorem mean_mult (N : ℕ) (a : Fin (2 * N + 1) → ℂ) :
    modeProj N (zeroIdx N) (multLin N a) = 0 := by
  rw [modeProj_comp_mult, modeIdx_zeroIdx]
  simp

end DLW.Spectral
