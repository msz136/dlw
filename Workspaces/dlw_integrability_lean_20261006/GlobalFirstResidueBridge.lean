import GlobalSpectralRealization
import PhysicalFirstResidue

namespace DLWLean
noncomputable section
open scoped BigOperators ContDiff

theorem normalProductCoefficient_zero {R : Type*} [CommRing R] [Algebra ℝ R]
    (d : AlgebraEvolution R) (p : ℤ) (a b : ℕ → R) :
    normalProductCoefficient d p a b 0 = a 0 * b 0 := by
  simp [normalProductCoefficient]

theorem normalProductCoefficient_minus_one_one {R : Type*} [CommRing R] [Algebra ℝ R]
    (d : AlgebraEvolution R) (a b : ℕ → R) :
    normalProductCoefficient d (-1) a b 1 =
      a 0 * b 1 + a 1 * b 0 - a 0 * d.toLinearMap (b 0) := by
  simp [normalProductCoefficient, Fin.sum_univ_succ, Ring.choose_one_right,
    Function.iterate_succ_apply']
  ring

theorem normalProductCoefficient_minus_one_two {R : Type*} [CommRing R] [Algebra ℝ R]
    (d : AlgebraEvolution R) (a b : ℕ → R) :
    normalProductCoefficient d (-1) a b 2 =
      a 0 * b 2 + a 1 * b 1 + a 2 * b 0 -
        a 0 * d.toLinearMap (b 1) - 2 * a 1 * d.toLinearMap (b 0) +
          a 0 * d.toLinearMap (d.toLinearMap (b 0)) := by
  have hm : Ring.choose (-1 : ℤ) 2 = 1 := by
    rw [Ring.choose_neg', Ring.multichoose_one]
    change (2 : ℤ).negOnePow • (1 : ℤ) = 1
    rw [Int.negOnePow_even 2 ⟨1, by norm_num⟩, one_smul]
  norm_num [normalProductCoefficient, Fin.sum_univ_succ, hm, Ring.choose_one_right,
    Function.iterate_succ_apply']
  ring

theorem normalInverseRemainder_zero {R : Type*} [CommRing R] [Algebra ℝ R]
    (d : AlgebraEvolution R) (H V : ℕ → R) :
    normalInverseRemainder d H V 0 = H 1 * V 0 - H 0 * d.toLinearMap (V 0) := by
  simp [normalInverseRemainder, Fin.sum_univ_succ]
  ring

theorem normalInverseRemainder_one {R : Type*} [CommRing R] [Algebra ℝ R]
    (d : AlgebraEvolution R) (H V : ℕ → R) :
    normalInverseRemainder d H V 1 =
      H 1 * V 1 + H 2 * V 0 - H 0 * d.toLinearMap (V 1) -
        2 * H 1 * d.toLinearMap (V 0) + H 0 * d.toLinearMap (d.toLinearMap (V 0)) := by
  have h := normalProductCoefficient_isolate_inverse d H V 1
  rw [normalProductCoefficient_minus_one_two] at h
  linear_combination -h

namespace GlobalPDO

theorem beta_eq_transferBeta (par : FieldParameters) (j : Fin par.M) :
    beta par j = transferBeta (U par j) (g par j) := rfl

theorem siteCoefficient_first3 (par : FieldParameters) (j : Fin par.M) :
    siteCoefficient par j 0 = (transferCoefficients3 (spatialEvolution par) (U par j) (g par j)).first ∧
    siteCoefficient par j 1 = (transferCoefficients3 (spatialEvolution par) (U par j) (g par j)).second ∧
    siteCoefficient par j 2 = (transferCoefficients3 (spatialEvolution par) (U par j) (g par j)).third := by
  constructor
  · exact siteCoefficient_leading par j
  constructor
  · rw [siteCoefficient, normalProduct, normalProductCoefficient_minus_one_one]
    simp only [resolventCoefficient, Nat.one_ne_zero, ite_false, ite_true,
      spatialEvolution, LinearMap.coe_mk, AddHom.coe_mk, Derivation.map_one_eq_zero, map_zero,
      mul_one, one_mul, sub_zero, transferCoefficients3, ← beta_eq_transferBeta]
    ring
  · rw [siteCoefficient, normalProduct, normalProductCoefficient_minus_one_two]
    simp only [resolventCoefficient, Nat.one_ne_zero, (by decide : (2 : ℕ) ≠ 0), ite_false, ite_true,
      spatialEvolution, LinearMap.coe_mk, AddHom.coe_mk, Derivation.map_one_eq_zero, map_zero, map_sub,
      mul_one, one_mul, sub_zero, transferCoefficients3, ← beta_eq_transferBeta]
    ring

def transfer3 (par : FieldParameters) (n : ℕ) : PDO3 (Poly par) :=
  transferCoefficients3 (spatialEvolution par)
    (fieldNatExtension (U par) n) (fieldNatExtension (g par) n)

theorem sites_first3 (par : FieldParameters) (n : ℕ) :
    sites par n 0 = (transfer3 par n).first ∧
    sites par n 1 = (transfer3 par n).second ∧
    sites par n 2 = (transfer3 par n).third := by
  unfold sites transfer3 fieldNatExtension
  split_ifs with hn
  · exact siteCoefficient_first3 par ⟨n, hn⟩
  · simp [transferCoefficients3, transferBeta]

theorem monodromyDifference_first3 (par : FieldParameters) (n : ℕ) :
    monodromyDifferenceCoefficient par n 0 =
      (monodromyCoefficients3 (spatialEvolution par) (fieldNatExtension (U par))
        (fieldNatExtension (g par)) n).first ∧
    monodromyDifferenceCoefficient par n 1 =
      (monodromyCoefficients3 (spatialEvolution par) (fieldNatExtension (U par))
        (fieldNatExtension (g par)) n).second ∧
    monodromyDifferenceCoefficient par n 2 =
      (monodromyCoefficients3 (spatialEvolution par) (fieldNatExtension (U par))
        (fieldNatExtension (g par)) n).third := by
  induction n with
  | zero => simp [monodromyDifferenceCoefficient, monodromyCoefficients3, PDO3.one]
  | succ n ih =>
    obtain ⟨hs0, hs1, hs2⟩ := sites_first3 par n
    constructor
    · simp only [monodromyDifferenceCoefficient, monodromyCoefficients3, PDO3.mul,
        hs0, ih.1, transfer3]
    constructor
    · simp only [monodromyDifferenceCoefficient, normalProduct, normalProductCoefficient_zero,
        monodromyCoefficients3, PDO3.mul, hs0, hs1, ih.1, ih.2.1, transfer3]
    · simp only [monodromyDifferenceCoefficient, normalProduct,
        normalProductCoefficient_minus_one_one,
        monodromyCoefficients3, PDO3.mul, hs0, hs1, hs2, ih.1, ih.2.1, ih.2.2, transfer3]
      ring

end GlobalPDO

namespace GlobalPDO

def evaluatePDO3 (par : FieldParameters) (z : ClosedPeriodicPair par) (q : PDO3 (Poly par)) :
    PDO3 (PeriodicCoefficient par.Lx) :=
  ⟨evaluation par z q.first, evaluation par z q.second, evaluation par z q.third⟩

theorem evaluation_spatialEvolution (par : FieldParameters) (z : ClosedPeriodicPair par)
    (p : Poly par) : evaluation par z ((spatialEvolution par).toLinearMap p) =
      (periodicSpatialEvolution par.Lx).toLinearMap (evaluation par z p) :=
  evaluation_derivative par z p

theorem evaluatePDO3_mul (par : FieldParameters) (z : ClosedPeriodicPair par)
    (a b : PDO3 (Poly par)) :
    evaluatePDO3 par z (PDO3.mul (spatialEvolution par) a b) =
      PDO3.mul (periodicSpatialEvolution par.Lx) (evaluatePDO3 par z a) (evaluatePDO3 par z b) := by
  ext <;> simp only [evaluatePDO3, PDO3.mul, map_add, map_sub, map_mul,
    evaluation_spatialEvolution]

theorem evaluate_transfer3 (par : FieldParameters) (z : ClosedPeriodicPair par)
    (a b : Poly par) :
    evaluatePDO3 par z (transferCoefficients3 (spatialEvolution par) a b) =
      transferCoefficients3 (periodicSpatialEvolution par.Lx) (evaluation par z a) (evaluation par z b) := by
  have hbeta : evaluation par z (transferBeta a b) =
      transferBeta (evaluation par z a) (evaluation par z b) := by
    simp only [transferBeta, halfCoefficient, map_mul, map_sub]
    exact congrArg (fun q => q * (evaluation par z a - evaluation par z b))
      ((evaluation par z).commutes (1 / 2 : ℝ))
  ext <;> simp only [evaluatePDO3, transferCoefficients3, map_add, map_sub, map_neg,
    map_mul, map_pow, map_ofNat, evaluation_spatialEvolution, hbeta]

theorem evaluate_monodromy3 (par : FieldParameters) (z : ClosedPeriodicPair par)
    (a b : ℕ → Poly par) (n : ℕ) :
    evaluatePDO3 par z (monodromyCoefficients3 (spatialEvolution par) a b n) =
      monodromyCoefficients3 (periodicSpatialEvolution par.Lx)
        (fun j => evaluation par z (a j)) (fun j => evaluation par z (b j)) n := by
  induction n with
  | zero => ext <;> simp [evaluatePDO3, monodromyCoefficients3, PDO3.one]
  | succ n ih =>
    rw [monodromyCoefficients3, evaluatePDO3_mul, evaluate_transfer3, ih]
    rfl

theorem U_eval_coefficient (par : FieldParameters) (z : ClosedPeriodicPair par)
    (j : Fin par.M) :
    evaluation par z (U par j) = (closedPairCoordinates par z).UCoefficient j := by
  apply Subtype.ext
  funext x
  exact U_eval_value par z j x

theorem w_eval_coefficient (par : FieldParameters) (z : ClosedPeriodicPair par)
    (j : Fin par.M) :
    evaluation par z (w par j) = (closedPairCoordinates par z).wCoefficient j := by
  apply Subtype.ext
  funext x
  exact w_eval_value par z j x

theorem g_eval_coefficient (par : FieldParameters) (z : ClosedPeriodicPair par)
    (j : Fin par.M) :
    evaluation par z (g par j) =
      latticeQuarter par.h * (closedPairCoordinates par z).wCoefficient j := by
  rw [g, map_mul, evaluation_C, w_eval_coefficient]
  rfl

theorem evaluate_physical_monodromy3 (par : FieldParameters) (z : ClosedPeriodicPair par) (n : ℕ) :
    evaluatePDO3 par z
      (monodromyCoefficients3 (spatialEvolution par) (fieldNatExtension (U par))
        (fieldNatExtension (g par)) n) =
      monodromyCoefficients3 (periodicSpatialEvolution par.Lx)
        (fieldNatExtension (closedPairCoordinates par z).UCoefficient)
        (fun j => latticeQuarter par.h * fieldNatExtension (closedPairCoordinates par z).wCoefficient j) n := by
  rw [evaluate_monodromy3]
  have hU : (fun j => evaluation par z (fieldNatExtension (U par) j)) =
      fieldNatExtension (closedPairCoordinates par z).UCoefficient := by
    funext j
    unfold fieldNatExtension
    split_ifs
    · exact U_eval_coefficient par z _
    · exact map_zero _
  have hg : (fun j => evaluation par z (fieldNatExtension (g par) j)) =
      (fun j => latticeQuarter par.h * fieldNatExtension (closedPairCoordinates par z).wCoefficient j) := by
    funext j
    unfold fieldNatExtension
    split_ifs
    · exact g_eval_coefficient par z _
    · simp
  rw [hU, hg]

theorem evaluated_monodromy_first3 (par : FieldParameters) (z : ClosedPeriodicPair par) :
    evaluation par z (monodromyCoefficient par 0) =
      (monodromyCoefficients3 (periodicSpatialEvolution par.Lx)
        (fieldNatExtension (closedPairCoordinates par z).UCoefficient)
        (fun j => latticeQuarter par.h * fieldNatExtension (closedPairCoordinates par z).wCoefficient j)
        par.M).first ∧
    evaluation par z (monodromyCoefficient par 1) =
      (monodromyCoefficients3 (periodicSpatialEvolution par.Lx)
        (fieldNatExtension (closedPairCoordinates par z).UCoefficient)
        (fun j => latticeQuarter par.h * fieldNatExtension (closedPairCoordinates par z).wCoefficient j)
        par.M).second ∧
    evaluation par z (monodromyCoefficient par 2) =
      (monodromyCoefficients3 (periodicSpatialEvolution par.Lx)
        (fieldNatExtension (closedPairCoordinates par z).UCoefficient)
        (fun j => latticeQuarter par.h * fieldNatExtension (closedPairCoordinates par z).wCoefficient j)
        par.M).third := by
  have hm := evaluate_physical_monodromy3 par z par.M
  have hp := monodromyDifference_first3 par par.M
  constructor
  · rw [monodromyCoefficient, hp.1]
    exact congrArg PDO3.first hm
  constructor
  · rw [monodromyCoefficient, hp.2.1]
    exact congrArg PDO3.second hm
  · rw [monodromyCoefficient, hp.2.2]
    exact congrArg PDO3.third hm

theorem inverseCoefficient_eval_succ (par : FieldParameters) (z : ClosedPeriodicPair par) (n : ℕ) :
    evaluation par z (inverseCoefficient par (n + 1)) =
      algebraMap ℝ (PeriodicCoefficient par.Lx) (-(-par.G)⁻¹) *
        normalInverseRemainder (periodicSpatialEvolution par.Lx)
          (fun k => evaluation par z (monodromyCoefficient par k))
          (fun k => evaluation par z (inverseCoefficient par k)) n := by
  classical
  rw [inverseCoefficient, map_mul, evaluation_C]
  congr 1
  unfold normalInverseRemainder
  rw [map_sum]
  apply Finset.sum_congr rfl
  intro t _
  rw [map_sum]
  apply Finset.sum_congr rfl
  intro r _
  split_ifs
  · rw [map_mul, map_mul, evaluation_C, evaluation_iterate]
  · rw [map_zero]

theorem evaluated_first_residue_eq_physical (par : FieldParameters) (z : ClosedPeriodicPair par) :
    evaluation par z (normalizedCoefficient par 2) =
      physicalFirstResidueCoefficient par (closedPairCoordinates par z) := by
  let d := periodicSpatialEvolution par.Lx
  let q : ℕ → PeriodicCoefficient par.Lx := fun k => evaluation par z (inverseCoefficient par k)
  let H : ℕ → PeriodicCoefficient par.Lx := fun k => evaluation par z (monodromyCoefficient par k)
  have hH0 : H 0 = algebraMap ℝ (PeriodicCoefficient par.Lx) (-par.G) := by
    simp only [H, monodromyCoefficient_leading, evaluation_C]
  have hH1 : H 1 = algebraMap ℝ (PeriodicCoefficient par.Lx) ((par.G ^ 2 - par.T) / 2) := by
    change evaluation par z (monodromyCoefficient par 1) = _
    rw [(evaluated_monodromy_first3 par z).2.1]
    exact (physical_monodromy_first_second par (closedPairCoordinates par z)).2
  have hq0 : q 0 = algebraMap ℝ (PeriodicCoefficient par.Lx) (-par.G)⁻¹ := by
    simp only [q, inverseCoefficient, evaluation_C]
  have hd0 : d.toLinearMap (q 0) = 0 := by rw [hq0, evolution_algebraMap_zero]
  have hq1 : q 1 = algebraMap ℝ (PeriodicCoefficient par.Lx) (-(-par.G)⁻¹) * (H 1 * q 0) := by
    have h := inverseCoefficient_eval_succ par z 0
    change q 1 = algebraMap ℝ _ _ * normalInverseRemainder d H q 0 at h
    simpa only [normalInverseRemainder_zero, hd0, mul_zero, sub_zero] using h
  have hd1 : d.toLinearMap (q 1) = 0 := by
    rw [hq1, hH1, hq0, d.leibniz, d.leibniz]
    simp only [evolution_algebraMap_zero, zero_mul, mul_zero, add_zero]
  have hq2 : q 2 = algebraMap ℝ (PeriodicCoefficient par.Lx) (-(-par.G)⁻¹) *
      (H 1 * q 1 + H 2 * q 0) := by
    have h := inverseCoefficient_eval_succ par z 1
    change q 2 = algebraMap ℝ _ _ * normalInverseRemainder d H q 1 at h
    simpa only [normalInverseRemainder_one, hd0, hd1, map_zero, mul_zero, sub_zero, add_zero] using h
  have hcancel : algebraMap ℝ (PeriodicCoefficient par.Lx) (-par.G) *
      algebraMap ℝ (PeriodicCoefficient par.Lx) (-(-par.G)⁻¹) = -1 := by
    rw [← map_mul]
    have hr : (-par.G) * (-(-par.G)⁻¹) = -1 := by
      rw [mul_neg, mul_inv_cancel₀ (neg_ne_zero.mpr par.G_ne_zero)]
    rw [hr, map_neg, map_one]
  have hlead : algebraMap ℝ (PeriodicCoefficient par.Lx) (-par.G) * q 0 = 1 := by
    rw [hq0, ← map_mul, mul_inv_cancel₀ (neg_ne_zero.mpr par.G_ne_zero), map_one]
  have hconst : algebraMap ℝ (PeriodicCoefficient par.Lx) (-par.G) * q 1 +
      algebraMap ℝ (PeriodicCoefficient par.Lx) ((par.G ^ 2 - par.T) / 2) * q 0 = 0 := by
    rw [hq1, ← mul_assoc, hcancel, hH1]
    ring
  have hresidue : algebraMap ℝ (PeriodicCoefficient par.Lx) (-par.G) * q 2 +
      algebraMap ℝ (PeriodicCoefficient par.Lx) ((par.G ^ 2 - par.T) / 2) * q 1 + H 2 * q 0 = 0 := by
    rw [hq2, ← mul_assoc, hcancel, hH1]
    ring
  have hc := firstResidue_of_inverse_coefficient_equations par.G par.T (H 2)
    (q 0) (q 1) (q 2) par.G_ne_zero hlead hconst hresidue
  have hlow := (evaluated_monodromy_first3 par z).2.2
  change H 2 = _ at hlow
  rw [hlow] at hc
  change algebraMap ℝ (PeriodicCoefficient par.Lx) (-par.G) * q 2 =
    physicalFirstResidueCoefficient par (closedPairCoordinates par z) at hc
  simpa only [normalizedCoefficient, (by decide : (2 : ℕ) ≠ 1), ite_false,
    add_zero, map_mul, evaluation_C] using hc

theorem residuePolynomial_one (par : FieldParameters) :
    residuePolynomial par 1 = normalizedCoefficient par 2 := by
  unfold residuePolynomial powerCoefficient normalProduct
  change normalProductCoefficient (spatialEvolution par) 0
    (fun r => if r = 0 then 1 else 0) (normalizedCoefficient par) 2 = _
  rw [normalProductCoefficient_scalar_left]
  exact one_mul _

/-- A pure identity of actual physical field functionals. It requires no
field-dependent formal PDO instance or unit construction. -/
theorem constructedCharge_one_eq_physicalComputedC1 (par : FieldParameters) (z : ClosedPeriodicPair par) :
    constructedCharge par 1 z = physicalComputedC1 par (closedPairCoordinates par z) := by
  unfold constructedCharge fieldPolynomialIntegral
  rw [periodicDensityPolynomial_eval]
  simp only [spectralDensityPolynomial, Nat.cast_one, inv_one, map_one, one_mul]
  rw [residuePolynomial_one, evaluated_first_residue_eq_physical]
  rfl

theorem physicalK_eq_constructed_C1 (par : FieldParameters) (z : ClosedPeriodicPair par) :
    physicalK par (latticeResolvent par) (closedPairCoordinates par z) =
      -8 * par.G * constructedCharge par 1 z +
        (par.gamma / par.c) * coefficientMomentum par z + energyConstant par := by
  rw [constructedCharge_one_eq_physicalComputedC1, physicalK_eq_computed_first_residue]
  rw [← coefficientMomentum_eq_physical]
  rfl

namespace NormalizedRealization
variable {par : FieldParameters} {A : Type*} [Ring A] [Algebra ℝ A]
    {z : ClosedPeriodicPair par}
    {model : NormalPDOModel (PeriodicCoefficient par.Lx) A}
    {factors : FactorRealization par z model}
    (realization : NormalizedRealization factors)

theorem physical_monodromy_first3 :
    model.coefficientBelow (realization.difference : A) (-1) 0 =
      (monodromyCoefficients3 (periodicSpatialEvolution par.Lx)
        (fieldNatExtension (closedPairCoordinates par z).UCoefficient)
        (fun j => latticeQuarter par.h * fieldNatExtension (closedPairCoordinates par z).wCoefficient j)
        par.M).first ∧
    model.coefficientBelow (realization.difference : A) (-1) 1 =
      (monodromyCoefficients3 (periodicSpatialEvolution par.Lx)
        (fieldNatExtension (closedPairCoordinates par z).UCoefficient)
        (fun j => latticeQuarter par.h * fieldNatExtension (closedPairCoordinates par z).wCoefficient j)
        par.M).second ∧
    model.coefficientBelow (realization.difference : A) (-1) 2 =
      (monodromyCoefficients3 (periodicSpatialEvolution par.Lx)
        (fieldNatExtension (closedPairCoordinates par z).UCoefficient)
        (fun j => latticeQuarter par.h * fieldNatExtension (closedPairCoordinates par z).wCoefficient j)
        par.M).third := by
  have hm := evaluate_physical_monodromy3 par z par.M
  have hp := monodromyDifference_first3 par par.M
  constructor
  · rw [realization.difference_coefficient, monodromyCoefficient, hp.1]
    exact congrArg PDO3.first hm
  constructor
  · rw [realization.difference_coefficient, monodromyCoefficient, hp.2.1]
    exact congrArg PDO3.second hm
  · rw [realization.difference_coefficient, monodromyCoefficient, hp.2.2]
    exact congrArg PDO3.third hm

theorem difference_second_constant :
    model.coefficientBelow (realization.difference : A) (-1) 1 =
      algebraMap ℝ (PeriodicCoefficient par.Lx) ((par.G ^ 2 - par.T) / 2) := by
  rw [realization.physical_monodromy_first3.2.1]
  exact (physical_monodromy_first_second par (closedPairCoordinates par z)).2

theorem inverse_low_spatial_zero :
    model.d.toLinearMap (model.coefficientBelow (↑realization.difference⁻¹ : A) 1 0) = 0 ∧
    model.d.toLinearMap (model.coefficientBelow (↑realization.difference⁻¹ : A) 1 1) = 0 := by
  have hq0 := model.constantLeading_inverse_zero realization.difference (-par.G)
    (neg_ne_zero.mpr par.G_ne_zero) realization.difference_bound realization.difference_leading
  have hd0 : model.d.toLinearMap
      (model.coefficientBelow (↑realization.difference⁻¹ : A) 1 0) = 0 := by
    rw [hq0, evolution_algebraMap_zero]
  refine ⟨hd0, ?_⟩
  have hq1 := model.constantLeading_inverse_succ realization.difference (-par.G)
    (neg_ne_zero.mpr par.G_ne_zero) realization.difference_bound realization.difference_leading 0
  rw [normalInverseRemainder_zero, hd0, mul_zero, sub_zero,
    realization.difference_second_constant, hq0] at hq1
  rw [hq1, model.d.leibniz, model.d.leibniz]
  simp only [evolution_algebraMap_zero, zero_mul, mul_zero, add_zero]

/-- The true D^-1 coefficient of L is now connected to the physical
first-residue energy computation, using only the actual inverse product
equations and the proved first-three monodromy coefficient realization. -/
theorem first_residue_eq_physical :
    model.coefficients realization.L (-1) =
      physicalFirstResidueCoefficient par (closedPairCoordinates par z) := by
  let q : ℕ → PeriodicCoefficient par.Lx :=
    model.coefficientBelow (↑realization.difference⁻¹ : A) 1
  let H : ℕ → PeriodicCoefficient par.Lx :=
    model.coefficientBelow (realization.difference : A) (-1)
  have hH0 : H 0 = algebraMap ℝ (PeriodicCoefficient par.Lx) (-par.G) := by
    exact realization.difference_leading
  have hH1 : H 1 = algebraMap ℝ (PeriodicCoefficient par.Lx) ((par.G ^ 2 - par.T) / 2) :=
    realization.difference_second_constant
  have hd0 : model.d.toLinearMap (q 0) = 0 := realization.inverse_low_spatial_zero.1
  have hd1 : model.d.toLinearMap (q 1) = 0 := realization.inverse_low_spatial_zero.2
  have hprod (k : ℕ) := model.product_coefficient (realization.difference : A)
    (↑realization.difference⁻¹ : A) (-1) 1 realization.difference_bound realization.inverse_bound k
  have hlead := hprod 0
  rw [Units.mul_inv, model.coeff_one, normalProductCoefficient_zero] at hlead
  have hconst := hprod 1
  rw [Units.mul_inv, model.coeff_one, normalProductCoefficient_minus_one_one] at hconst
  have hresidue := hprod 2
  rw [Units.mul_inv, model.coeff_one, normalProductCoefficient_minus_one_two] at hresidue
  change 1 = H 0 * q 0 at hlead
  change 0 = H 0 * q 1 + H 1 * q 0 - H 0 * model.d.toLinearMap (q 0) at hconst
  change 0 = H 0 * q 2 + H 1 * q 1 + H 2 * q 0 - H 0 * model.d.toLinearMap (q 1) -
    2 * H 1 * model.d.toLinearMap (q 0) + H 0 * model.d.toLinearMap (model.d.toLinearMap (q 0)) at hresidue
  rw [hd0, mul_zero, sub_zero, hH0, hH1] at hconst
  simp only [hd0, hd1, map_zero, mul_zero, sub_zero, add_zero,
    hH0, hH1] at hresidue
  rw [hH0] at hlead
  have hc := firstResidue_of_inverse_coefficient_equations par.G par.T (H 2)
    (q 0) (q 1) (q 2) par.G_ne_zero hlead.symm hconst.symm hresidue.symm
  have hlow := realization.physical_monodromy_first3.2.2
  change H 2 = _ at hlow
  rw [hlow] at hc
  change algebraMap ℝ (PeriodicCoefficient par.Lx) (-par.G) * q 2 =
    physicalFirstResidueCoefficient par (closedPairCoordinates par z) at hc
  convert hc using 1
  simp only [L, map_add, map_smul, Pi.add_apply, Pi.smul_apply, model.coeff_one]
  simp only [(by decide : (-1 : ℤ) ≠ 0), ite_false, smul_zero, add_zero, Algebra.smul_def,
    mul_zero]
  rfl

theorem spectral_C1_eq_physicalComputedC1 (tr : CyclicTrace A)
    (trace_eq : ∀ X, tr.toLinearMap X =
      periodicCoefficientIntegral par.Lx (model.coefficients X (-1))) :
    spectralInvariant tr realization.L 1 = physicalComputedC1 par (closedPairCoordinates par z) := by
  simp only [spectralInvariant, Nat.cast_one, inv_one, one_mul]
  rw [trace_eq, pow_one, realization.first_residue_eq_physical]
  rfl

theorem physicalK_eq_actual_C1 (tr : CyclicTrace A)
    (trace_eq : ∀ X, tr.toLinearMap X =
      periodicCoefficientIntegral par.Lx (model.coefficients X (-1))) :
    physicalK par (latticeResolvent par) (closedPairCoordinates par z) =
      -8 * par.G * spectralInvariant tr realization.L 1 +
        (par.gamma / par.c) * coefficientMomentum par z + energyConstant par := by
  rw [realization.spectral_C1_eq_physicalComputedC1 tr trace_eq,
    physicalK_eq_computed_first_residue]
  rw [← coefficientMomentum_eq_physical]
  rfl

end NormalizedRealization
end GlobalPDO

#print axioms GlobalPDO.NormalizedRealization.physical_monodromy_first3
#print axioms GlobalPDO.NormalizedRealization.first_residue_eq_physical
#print axioms GlobalPDO.NormalizedRealization.physicalK_eq_actual_C1
#print axioms GlobalPDO.constructedCharge_one_eq_physicalComputedC1
#print axioms GlobalPDO.physicalK_eq_constructed_C1

end
end DLWLean
