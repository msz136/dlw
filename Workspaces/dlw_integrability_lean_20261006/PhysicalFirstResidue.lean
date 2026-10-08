import FirstResidueEnergy
import ResidueIntegral
import LatticeResolvent

/-!
The first residue-energy bridge for the actual smooth periodic fields.
The only PDO representation obligation will be the equality of the true
first residue with the explicitly computed inverse-series coefficient.
-/

namespace DLWLean
noncomputable section
open scoped BigOperators ContDiff

def actualPeriodicIntegral (Lx : ℝ) : PeriodicIntegral (periodicSpatialEvolution Lx) where
  toLinearMap := periodicCoefficientIntegral Lx
  total_derivative_zero := periodicCoefficientIntegral_space_zero Lx

theorem periodicCoefficientIntegral_one (Lx : ℝ) :
    periodicCoefficientIntegral Lx 1 = Lx := by
  change (∫ _x in (0 : ℝ)..Lx, (1 : ℝ)) = Lx
  simp

def fieldNatExtension {M : ℕ} {A : Type*} [Zero A] (f : Fin M → A) (j : ℕ) : A :=
  if hj : j < M then f ⟨j, hj⟩ else 0

theorem fieldNatExtension_apply {M : ℕ} {A : Type*} [Zero A]
    (f : Fin M → A) (j : Fin M) : fieldNatExtension f j.val = f j := by
  simp [fieldNatExtension, j.isLt]

theorem sum_fieldNatExtension {M : ℕ} {A : Type*} [AddCommMonoid A]
    (f : Fin M → A) :
    (∑ j ∈ Finset.range M, fieldNatExtension f j) = ∑ j, f j := by
  rw [← Fin.sum_univ_eq_sum_range]
  simp_rw [fieldNatExtension_apply]

def FieldCoordinates.UCoefficient {par : FieldParameters}
    (z : FieldCoordinates par) (j : Fin par.M) : PeriodicCoefficient par.Lx :=
  ⟨z.U j, z.U_smooth j, z.U_periodic j⟩

def FieldCoordinates.wCoefficient {par : FieldParameters}
    (z : FieldCoordinates par) (j : Fin par.M) : PeriodicCoefficient par.Lx :=
  ⟨z.w j, z.w_smooth j, z.w_periodic j⟩

theorem coefficientSum_eval {Lx : ℝ} {ι : Type*}
    (s : Finset ι) (f : ι → PeriodicCoefficient Lx) (x : ℝ) :
    ((∑ i ∈ s, f i : PeriodicCoefficient Lx) : ℝ → ℝ) x =
      ∑ i ∈ s, (f i : ℝ → ℝ) x := by
  change ((periodicCoefficientAlgebra Lx).val (∑ i ∈ s, f i)) x = _
  rw [map_sum]
  exact Finset.sum_apply x s (fun i => (f i : ℝ → ℝ))

theorem coefficientMean_eval {Lx : ℝ} (n : ℕ)
    (f : ℕ → PeriodicCoefficient Lx) (x : ℝ) :
    (coefficientMean (R := PeriodicCoefficient Lx) n f : ℝ → ℝ) x =
      (∑ j ∈ Finset.range n, (f j : ℝ → ℝ) x) / (n : ℝ) := by
  simp [coefficientMean, div_eq_mul_inv, mul_comm]

theorem coefficientPrefix_eval {Lx : ℝ}
    (f : ℕ → PeriodicCoefficient Lx) (j : ℕ) (x : ℝ) :
    (coefficientPrefix (R := PeriodicCoefficient Lx) f j : ℝ → ℝ) x =
      ∑ k ∈ Finset.range j, (f k : ℝ → ℝ) x := by
  simp [coefficientPrefix, coefficientSum_eval]

theorem sum_fieldNatExtension_eval {M : ℕ} {Lx : ℝ}
    (f : Fin M → PeriodicCoefficient Lx) (x : ℝ) :
    (∑ j ∈ Finset.range M,
      (fieldNatExtension (A := PeriodicCoefficient Lx) f j : ℝ → ℝ) x) =
      ∑ j, (f j : ℝ → ℝ) x := by
  rw [← Fin.sum_univ_eq_sum_range]
  simp_rw [fieldNatExtension_apply]

theorem prefix_fieldNatExtension {M : ℕ} {A : Type*} [CommRing A] [Algebra ℝ A]
    (f : Fin M → A) (j : Fin M) :
    coefficientPrefix (fieldNatExtension f) j.val =
      ∑ i, if i.val < j.val then f i else 0 := by
  unfold coefficientPrefix
  calc
    _ = ∑ i ∈ Finset.range j.val,
        if i < j.val then fieldNatExtension f i else 0 := by
      apply Finset.sum_congr rfl
      intro i hi
      simp [Finset.mem_range.mp hi]
    _ = ∑ i ∈ Finset.range M,
        if i < j.val then fieldNatExtension f i else 0 := by
      apply Finset.sum_subset (Finset.range_mono (Nat.le_of_lt j.isLt))
      intro i _ hij
      simp [Finset.mem_range] at hij
      simp [hij]
    _ = _ := by
      rw [← Fin.sum_univ_eq_sum_range]
      simp_rw [fieldNatExtension_apply]

theorem coefficientResolvent_field_eval (par : FieldParameters)
    (f : Fin par.M → PeriodicCoefficient par.Lx) (j : Fin par.M) (x : ℝ) :
    (coefficientResolvent (R := PeriodicCoefficient par.Lx)
      par.h par.M (fieldNatExtension f) j.val : ℝ → ℝ) x =
      latticeResolvent par (fun i => (f i : ℝ → ℝ) x) j := by
  have hmean := coefficientMean_eval par.M (fieldNatExtension f) x
  rw [sum_fieldNatExtension_eval] at hmean
  have hp0 : ∀ i : Fin par.M,
      (coefficientP0 (R := PeriodicCoefficient par.Lx)
        par.M (fieldNatExtension f) i.val : ℝ → ℝ) x =
        latticeP0 (fun k => (f k : ℝ → ℝ) x) i := by
    intro i
    simp only [coefficientP0, Subalgebra.coe_sub, Pi.sub_apply,
      fieldNatExtension_apply, hmean, latticeP0, latticeMean]
  have hprim : ∀ i : Fin par.M,
      (coefficientPrimitive (R := PeriodicCoefficient par.Lx)
        (coefficientP0 par.M (fieldNatExtension f)) i.val : ℝ → ℝ) x =
        latticePrefix (latticeP0 (fun k => (f k : ℝ → ℝ) x)) i +
          latticeP0 (fun k => (f k : ℝ → ℝ) x) i / 2 := by
    intro i
    unfold coefficientPrimitive
    simp only [Subalgebra.coe_add, Pi.add_apply, Subalgebra.coe_mul, Pi.mul_apply,
      coefficientPrefix_eval, halfCoefficient, Subalgebra.coe_algebraMap, Pi.algebraMap_apply]
    -- Restrict the prefix to Fin M without changing its values.
    have hprefix : (∑ k ∈ Finset.range i.val,
        (coefficientP0 (R := PeriodicCoefficient par.Lx)
          par.M (fieldNatExtension f) k : ℝ → ℝ) x) =
        latticePrefix (latticeP0 (fun k => (f k : ℝ → ℝ) x)) i := by
      have hsum := prefix_fieldNatExtension
        (fun k : Fin par.M => (coefficientP0 (R := PeriodicCoefficient par.Lx)
          par.M (fieldNatExtension f) k.val : ℝ → ℝ) x) i
      simp only [coefficientPrefix] at hsum
      have heq : (∑ k ∈ Finset.range i.val,
          fieldNatExtension
            (fun k : Fin par.M => (coefficientP0 (R := PeriodicCoefficient par.Lx)
              par.M (fieldNatExtension f) k.val : ℝ → ℝ) x) k) =
          ∑ k ∈ Finset.range i.val, (coefficientP0 (R := PeriodicCoefficient par.Lx)
            par.M (fieldNatExtension f) k : ℝ → ℝ) x := by
        apply Finset.sum_congr rfl
        intro k hk
        simp [fieldNatExtension, lt_trans (Finset.mem_range.mp hk) i.isLt]
      rw [heq] at hsum
      simpa only [hp0, latticePrefix] using hsum
    rw [hprefix, hp0]
    change latticePrefix (latticeP0 (fun k => (f k : ℝ → ℝ) x)) i +
        (1 / 2 : ℝ) * latticeP0 (fun k => (f k : ℝ → ℝ) x) i = _
    ring
  unfold coefficientResolvent coefficientResolventNormalized
  rw [coefficientP0]
  simp only [Subalgebra.coe_mul, Pi.mul_apply, Subalgebra.coe_algebraMap,
    Pi.algebraMap_apply, Subalgebra.coe_sub, Pi.sub_apply, coefficientMean_eval]
  rw [← Fin.sum_univ_eq_sum_range]
  simp_rw [hprim]
  rw [latticeResolvent_apply]
  unfold latticeP0 latticePrimitive latticeMean
  change par.h * _ = _
  rw [← Finset.mul_sum]
  ring

theorem derivative_fieldNatExtension {M : ℕ} {Lx : ℝ}
    (f : Fin M → PeriodicCoefficient Lx) :
    (fun j => (periodicSpatialEvolution Lx).toLinearMap (fieldNatExtension f j)) =
      fieldNatExtension (fun j => (periodicSpatialEvolution Lx).toLinearMap (f j)) := by
  funext j
  unfold fieldNatExtension
  split_ifs <;> simp

theorem physical_hamiltonianDensityW_eval (par : FieldParameters)
    (z : FieldCoordinates par) (x : ℝ) :
    (hamiltonianDensityW (R := PeriodicCoefficient par.Lx) (periodicSpatialEvolution par.Lx)
        (fieldNatExtension z.UCoefficient) (fieldNatExtension z.wCoefficient)
        par.h par.M : ℝ → ℝ) x =
      par.h * ∑ j,
        ((z.U j x) ^ 2 * z.w j x / 2 + beta par * (z.w j x) ^ 3 / 3 +
          z.w j x * deriv (z.U j) x +
            z.w j x * latticeResolvent par (fun i => deriv (z.w i) x) j / 2) := by
  unfold hamiltonianDensityW
  simp only [Subalgebra.coe_mul, Pi.mul_apply, Subalgebra.coe_algebraMap,
    Pi.algebraMap_apply, coefficientSum_eval]
  rw [← Fin.sum_univ_eq_sum_range]
  congr 1
  apply Finset.sum_congr rfl
  intro j _
  rw [derivative_fieldNatExtension]
  simp only [fieldNatExtension_apply, Subalgebra.coe_add, Pi.add_apply,
    Subalgebra.coe_mul, Pi.mul_apply, Subalgebra.coe_pow, Pi.pow_apply,
    halfCoefficient, Subalgebra.coe_algebraMap, Pi.algebraMap_apply]
  rw [coefficientResolvent_field_eval]
  change (1 / 2 : ℝ) * (z.U j x) ^ 2 * z.w j x +
      (par.h ^ 2 / 96) * (z.w j x) ^ 3 + z.w j x * deriv (z.U j) x +
      (1 / 2 : ℝ) * z.w j x * latticeResolvent par (fun i => deriv (z.w i) x) j = _
  unfold beta
  ring

theorem physical_hamiltonianDensityW_integral (par : FieldParameters)
    (z : FieldCoordinates par) :
    periodicCoefficientIntegral par.Lx
      (hamiltonianDensityW (R := PeriodicCoefficient par.Lx) (periodicSpatialEvolution par.Lx)
        (fieldNatExtension z.UCoefficient) (fieldNatExtension z.wCoefficient)
        par.h par.M) = physicalEnergy par (latticeResolvent par) z := by
  change (∫ x in (0 : ℝ)..par.Lx,
      (hamiltonianDensityW (R := PeriodicCoefficient par.Lx) (periodicSpatialEvolution par.Lx)
        (fieldNatExtension z.UCoefficient) (fieldNatExtension z.wCoefficient)
        par.h par.M : ℝ → ℝ) x) = _
  simp_rw [physical_hamiltonianDensityW_eval]
  rw [intervalIntegral.integral_const_mul]
  unfold physicalEnergy
  congr 1
  apply intervalIntegral.integral_finsetSum
  intro j _
  -- Each summand is a member of the smooth periodic coefficient algebra.
  let d := periodicSpatialEvolution par.Lx
  let density : PeriodicCoefficient par.Lx :=
    halfCoefficient * z.UCoefficient j ^ 2 * z.wCoefficient j +
      algebraMap ℝ (PeriodicCoefficient par.Lx) (par.h ^ 2 / 96) * z.wCoefficient j ^ 3 +
      z.wCoefficient j * d.toLinearMap (z.UCoefficient j) +
      halfCoefficient * z.wCoefficient j *
        coefficientResolvent par.h par.M
          (fieldNatExtension (fun i => d.toLinearMap (z.wCoefficient i))) j.val
  have hden : (density : ℝ → ℝ) = fun x =>
      (z.U j x) ^ 2 * z.w j x / 2 + beta par * (z.w j x) ^ 3 / 3 +
        z.w j x * deriv (z.U j) x +
          z.w j x * latticeResolvent par (fun i => deriv (z.w i) x) j / 2 := by
    funext x
    simp only [density, Subalgebra.coe_add, Pi.add_apply, Subalgebra.coe_mul,
      Pi.mul_apply, Subalgebra.coe_pow, Pi.pow_apply, halfCoefficient,
      Subalgebra.coe_algebraMap, Pi.algebraMap_apply, coefficientResolvent_field_eval]
    change (1 / 2 : ℝ) * (z.U j x) ^ 2 * z.w j x +
      (par.h ^ 2 / 96) * (z.w j x) ^ 3 + z.w j x * deriv (z.U j) x +
      (1 / 2 : ℝ) * z.w j x * latticeResolvent par (fun i => deriv (z.w i) x) j = _
    unfold beta
    ring
  rw [← hden]
  exact density.property.1.continuous.intervalIntegrable 0 par.Lx

def FieldParameters.T (par : FieldParameters) : ℝ :=
  par.h * (par.M : ℝ) * par.gamma / 4

theorem physical_meanG_coefficient (par : FieldParameters) (z : FieldCoordinates par) :
    (∑ j ∈ Finset.range par.M, latticeQuarter par.h *
      fieldNatExtension z.wCoefficient j) =
        algebraMap ℝ (PeriodicCoefficient par.Lx) par.G := by
  rw [← Finset.mul_sum, sum_fieldNatExtension]
  apply Subtype.ext
  funext x
  simp only [Subalgebra.coe_mul, Pi.mul_apply, latticeQuarter,
    Subalgebra.coe_algebraMap, Pi.algebraMap_apply, coefficientSum_eval]
  change (par.h / 4) * (∑ j, z.w j x) = par.G
  rw [sum_eq_card_mul_latticeMean par.M_ne_zero, z.mean_w]
  unfold FieldParameters.G
  ring

theorem physical_meanT_coefficient (par : FieldParameters) (z : FieldCoordinates par) :
    (∑ j ∈ Finset.range par.M, fieldNatExtension z.UCoefficient j *
      (latticeQuarter par.h * fieldNatExtension z.wCoefficient j)) =
        algebraMap ℝ (PeriodicCoefficient par.Lx) par.T := by
  rw [← Fin.sum_univ_eq_sum_range]
  simp_rw [fieldNatExtension_apply]
  apply Subtype.ext
  funext x
  simp only [Subalgebra.coe_mul, Pi.mul_apply, latticeQuarter,
    Subalgebra.coe_algebraMap, Pi.algebraMap_apply, coefficientSum_eval]
  change (∑ j, z.U j x * ((par.h / 4) * z.w j x)) = par.T
  calc
    _ = (par.h / 4) * (∑ j, z.U j x * z.w j x) := by
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro j _
      ring
    _ = _ := by
      rw [sum_eq_card_mul_latticeMean par.M_ne_zero, z.mean_Uw]
      unfold FieldParameters.T
      ring

theorem physical_monodromy_first_second (par : FieldParameters)
    (z : FieldCoordinates par) :
    (monodromyCoefficients3 (periodicSpatialEvolution par.Lx)
      (fieldNatExtension z.UCoefficient)
      (fun j => latticeQuarter par.h * fieldNatExtension z.wCoefficient j) par.M).first =
        algebraMap ℝ (PeriodicCoefficient par.Lx) (-par.G) ∧
    (monodromyCoefficients3 (periodicSpatialEvolution par.Lx)
      (fieldNatExtension z.UCoefficient)
      (fun j => latticeQuarter par.h * fieldNatExtension z.wCoefficient j) par.M).second =
        algebraMap ℝ (PeriodicCoefficient par.Lx) ((par.G ^ 2 - par.T) / 2) := by
  have hg := physical_meanG_coefficient par z
  have ht := physical_meanT_coefficient par z
  have hd : (periodicSpatialEvolution par.Lx).toLinearMap
      (∑ j ∈ Finset.range par.M, latticeQuarter par.h * fieldNatExtension z.wCoefficient j) = 0 := by
    rw [hg, evolution_algebraMap_zero]
  constructor
  · rw [monodromy_first_coefficient_sum, hg, map_neg]
  · rw [monodromy_second_coefficient_fixed_mean _ _ _ _ hd, hg, ht,
      halfCoefficient, ← map_pow, ← map_sub, ← map_mul]
    congr 1
    ring

theorem physical_normalizing_constant (par : FieldParameters) :
    ((par.G ^ 2 - par.T) / 2) / (-par.G) = par.B - par.G / 2 := by
  have ht : par.T = 2 * par.G * par.B := by
    unfold FieldParameters.T FieldParameters.G FieldParameters.B
    field_simp [par.c_ne_zero]
  rw [ht]
  field_simp [par.G_ne_zero]
  ring

def physicalFirstResidueCoefficient (par : FieldParameters) (z : FieldCoordinates par) :
    PeriodicCoefficient par.Lx :=
  firstResidueFromCoefficients par.G par.T
    (monodromyCoefficients3 (periodicSpatialEvolution par.Lx)
      (fieldNatExtension z.UCoefficient)
      (fun j => latticeQuarter par.h * fieldNatExtension z.wCoefficient j) par.M).third

def physicalComputedC1 (par : FieldParameters) (z : FieldCoordinates par) : ℝ :=
  periodicCoefficientIntegral par.Lx (physicalFirstResidueCoefficient par z)

theorem physicalComputedC1_eq_energy (par : FieldParameters) (z : FieldCoordinates par) :
    physicalComputedC1 par z = -physicalEnergy par (latticeResolvent par) z / (8 * par.G) +
      (par.G ^ 2 / 12 + par.B ^ 2) * par.Lx := by
  have h := firstResidue_integral_physical_energy (periodicSpatialEvolution par.Lx)
    (actualPeriodicIntegral par.Lx) (fieldNatExtension z.UCoefficient)
    (fieldNatExtension z.wCoefficient) par.h par.G par.T par.M par.G_ne_zero
    (physical_meanG_coefficient par z) (physical_meanT_coefficient par z)
  change physicalComputedC1 par z =
    -periodicCoefficientIntegral par.Lx
      (hamiltonianDensityW (periodicSpatialEvolution par.Lx)
        (fieldNatExtension z.UCoefficient) (fieldNatExtension z.wCoefficient) par.h par.M) /
      (8 * par.G) +
      (par.G ^ 2 / 12 + par.T ^ 2 / (4 * par.G ^ 2)) *
        periodicCoefficientIntegral par.Lx 1 at h
  rw [physical_hamiltonianDensityW_integral, periodicCoefficientIntegral_one] at h
  have hTG : par.T = 2 * par.G * par.B := by
    unfold FieldParameters.T FieldParameters.G FieldParameters.B
    field_simp [par.c_ne_zero]
  have hquot : par.T ^ 2 / (4 * par.G ^ 2) = par.B ^ 2 := by
    rw [hTG]
    field_simp [par.G_ne_zero]
    ring
  rwa [hquot] at h

theorem physicalK_eq_computed_first_residue (par : FieldParameters)
    (z : FieldCoordinates par) :
    physicalK par (latticeResolvent par) z =
      -8 * par.G * physicalComputedC1 par z +
        (par.gamma / par.c) * z.physicalMomentum + energyConstant par :=
  physicalK_eq_of_first_residue par (latticeResolvent par) z
    (physicalComputedC1 par z) (physicalComputedC1_eq_energy par z)

/-- The first residue coefficient follows from the three literal
coefficient equations of (M-1) (M-1)^-1 = 1. This interface asks for the
PDO product representation rather than the computed residue formula. -/
theorem firstResidue_of_inverse_coefficient_equations {Lx : ℝ}
    (G T : ℝ) (m3 qLead qConst qResidue : PeriodicCoefficient Lx)
    (hG : G ≠ 0)
    (hLead : algebraMap ℝ (PeriodicCoefficient Lx) (-G) * qLead = 1)
    (hConst : algebraMap ℝ (PeriodicCoefficient Lx) (-G) * qConst +
      algebraMap ℝ (PeriodicCoefficient Lx) ((G ^ 2 - T) / 2) * qLead = 0)
    (hResidue : algebraMap ℝ (PeriodicCoefficient Lx) (-G) * qResidue +
      algebraMap ℝ (PeriodicCoefficient Lx) ((G ^ 2 - T) / 2) * qConst + m3 * qLead = 0) :
    algebraMap ℝ (PeriodicCoefficient Lx) (-G) * qResidue =
      firstResidueFromCoefficients G T m3 := by
  apply Subtype.ext
  funext x
  have h1 := congrArg (fun r : PeriodicCoefficient Lx => (r : ℝ → ℝ) x) hLead
  have h0 := congrArg (fun r : PeriodicCoefficient Lx => (r : ℝ → ℝ) x) hConst
  have hm := congrArg (fun r : PeriodicCoefficient Lx => (r : ℝ → ℝ) x) hResidue
  simp only [Subalgebra.coe_mul, Pi.mul_apply, Subalgebra.coe_algebraMap,
    Pi.algebraMap_apply, Subalgebra.coe_add, Pi.add_apply,
    Subalgebra.coe_one, Pi.one_apply, Subalgebra.coe_zero, Pi.zero_apply] at h1 h0 hm
  change -G * (qLead : ℝ → ℝ) x = 1 at h1
  change -G * (qConst : ℝ → ℝ) x + ((G ^ 2 - T) / 2) * (qLead : ℝ → ℝ) x = 0 at h0
  change -G * (qResidue : ℝ → ℝ) x + ((G ^ 2 - T) / 2) * (qConst : ℝ → ℝ) x +
    (m3 : ℝ → ℝ) x * (qLead : ℝ → ℝ) x = 0 at hm
  have hq1 : (qLead : ℝ → ℝ) x = -G⁻¹ := by
    apply (mul_left_cancel₀ hG)
    have hinv : G * G⁻¹ = 1 := mul_inv_cancel₀ hG
    nlinarith
  have hq0 : (qConst : ℝ → ℝ) x = -((G ^ 2 - T) / 2) / G ^ 2 := by
    rw [hq1] at h0
    apply (mul_left_cancel₀ hG)
    field_simp [hG] at h0 ⊢
    nlinarith
  simp only [firstResidueFromCoefficients, Subalgebra.coe_add, Pi.add_apply,
    Subalgebra.coe_mul, Pi.mul_apply, Subalgebra.coe_algebraMap, Pi.algebraMap_apply]
  change -G * (qResidue : ℝ → ℝ) x =
    ((G ^ 2 - T) / 2) ^ 2 / G ^ 2 + G⁻¹ * (m3 : ℝ → ℝ) x
  calc
    _ = -((G ^ 2 - T) / 2) * (qConst : ℝ → ℝ) x -
        (m3 : ℝ → ℝ) x * (qLead : ℝ → ℝ) x := by linarith
    _ = _ := by rw [hq0, hq1]; field_simp [hG]; ring

theorem physicalK_eq_of_residue_coefficient_realization {A : Type*} [Ring A] [Algebra ℝ A]
    (par : FieldParameters) (z : FieldCoordinates par)
    (residue : A →ₗ[ℝ] PeriodicCoefficient par.Lx) (L : A)
    (hrealization : residue L = physicalFirstResidueCoefficient par z) :
    physicalK par (latticeResolvent par) z =
      -8 * par.G * periodicCoefficientIntegral par.Lx (residue L) +
        (par.gamma / par.c) * z.physicalMomentum + energyConstant par := by
  rw [hrealization]
  exact physicalK_eq_computed_first_residue par z

theorem physicalK_eq_of_PDO_inverse_coefficients {A : Type*} [Ring A] [Algebra ℝ A]
    (par : FieldParameters) (z : FieldCoordinates par)
    (residue : A →ₗ[ℝ] PeriodicCoefficient par.Lx) (L : A)
    (qLead qConst qResidue : PeriodicCoefficient par.Lx)
    (hLead : algebraMap ℝ (PeriodicCoefficient par.Lx) (-par.G) * qLead = 1)
    (hConst : algebraMap ℝ (PeriodicCoefficient par.Lx) (-par.G) * qConst +
      algebraMap ℝ (PeriodicCoefficient par.Lx) ((par.G ^ 2 - par.T) / 2) * qLead = 0)
    (hResidue : algebraMap ℝ (PeriodicCoefficient par.Lx) (-par.G) * qResidue +
      algebraMap ℝ (PeriodicCoefficient par.Lx) ((par.G ^ 2 - par.T) / 2) * qConst +
      (monodromyCoefficients3 (periodicSpatialEvolution par.Lx)
        (fieldNatExtension z.UCoefficient)
        (fun j => latticeQuarter par.h * fieldNatExtension z.wCoefficient j) par.M).third *
          qLead = 0)
    (hNormalization : residue L =
      algebraMap ℝ (PeriodicCoefficient par.Lx) (-par.G) * qResidue) :
    physicalK par (latticeResolvent par) z =
      -8 * par.G * periodicCoefficientIntegral par.Lx (residue L) +
        (par.gamma / par.c) * z.physicalMomentum + energyConstant par := by
  apply physicalK_eq_of_residue_coefficient_realization par z residue L
  rw [hNormalization]
  exact firstResidue_of_inverse_coefficient_equations par.G par.T _ _ _ _
    par.G_ne_zero hLead hConst hResidue

#print axioms actualPeriodicIntegral
#print axioms sum_fieldNatExtension
#print axioms coefficientResolvent_field_eval
#print axioms physical_monodromy_first_second
#print axioms physicalComputedC1_eq_energy
#print axioms physicalK_eq_computed_first_residue
#print axioms physicalK_eq_of_PDO_inverse_coefficients

end
end DLWLean
