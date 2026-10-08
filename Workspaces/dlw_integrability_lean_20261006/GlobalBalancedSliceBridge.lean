import GlobalCoefficientRecurrence
import BalancedSpectralRealization
import MomentumWitness
import NormalScalarResidue

namespace DLWLean
noncomputable section
open scoped BigOperators

def balancedEta (par : FieldParameters) : ℝ := par.h * par.c / 8

theorem balancedEta_ne_zero (par : FieldParameters) : balancedEta par ≠ 0 := by
  unfold balancedEta
  exact div_ne_zero (mul_ne_zero (ne_of_gt par.h_pos) par.c_ne_zero) (by norm_num)

theorem G_eq_balancedEta (par : FieldParameters) : par.G = 2 * (par.M : ℝ) * balancedEta par := by
  unfold FieldParameters.G balancedEta
  ring

def balancedLatticeSign (par : FieldParameters) (j : Fin par.M) : ℝ :=
  (if j = firstLatticeSite par then 1 else 0) -
    (if j = secondLatticeSite par then 1 else 0)

theorem balancedCoefficientField_eq_sign_smul (par : FieldParameters)
    (f : PeriodicCoefficient par.Lx) (j : Fin par.M) :
    balancedCoefficientField par f j = balancedLatticeSign par j • f := by
  change (if j = firstLatticeSite par then f else 0) -
      (if j = secondLatticeSite par then f else 0) = _
  unfold balancedLatticeSign
  split_ifs <;> simp

theorem periodicSpatialIterate_eq_coefficientSpatialJet (par : FieldParameters)
    (k : ℕ) (f : PeriodicCoefficient par.Lx) :
    periodicSpatialIterate k f = coefficientSpatialJet par k f := by
  induction k with
  | zero => rfl
  | succ k ih =>
    unfold periodicSpatialIterate at *
    rw [Function.iterate_succ_apply', ih]
    rfl

theorem balancedCoefficientField_spatial_jet (par : FieldParameters)
    (f : PeriodicCoefficient par.Lx) (j : Fin par.M) (k : ℕ) (x : ℝ) :
    (periodicSpatialIterate k (balancedCoefficientField par f j) : ℝ → ℝ) x =
      balancedLatticeSign par j * iteratedDeriv k (f : ℝ → ℝ) x := by
  rw [balancedCoefficientField_eq_sign_smul,
    periodicSpatialIterate_eq_coefficientSpatialJet, map_smul]
  change balancedLatticeSign par j * (coefficientSpatialJet par k f : ℝ → ℝ) x = _
  rw [coefficientSpatialJet_value]

def balancedPeriodicJet (par : FieldParameters) (f : PeriodicCoefficient par.Lx) :
    BalancedPDO.JetVariable par.M → PeriodicCoefficient par.Lx
  | .b => algebraMap ℝ (PeriodicCoefficient par.Lx) par.B
  | .eta => algebraMap ℝ (PeriodicCoefficient par.Lx) (balancedEta par)
  | .field j k => periodicSpatialIterate k (balancedCoefficientField par f j)

def balancedPeriodicEvaluation (par : FieldParameters) (f : PeriodicCoefficient par.Lx) :
    BalancedPDO.Poly par.M →ₐ[ℝ] PeriodicCoefficient par.Lx :=
  MvPolynomial.aeval (balancedPeriodicJet par f)

theorem balancedPeriodicEvaluation_C (par : FieldParameters) (f : PeriodicCoefficient par.Lx) (r : ℝ) :
    balancedPeriodicEvaluation par f (MvPolynomial.C r) = algebraMap ℝ (PeriodicCoefficient par.Lx) r :=
  (balancedPeriodicEvaluation par f).commutes r

theorem balancedPeriodicEvaluation_X (par : FieldParameters) (f : PeriodicCoefficient par.Lx)
    (i : BalancedPDO.JetVariable par.M) :
    balancedPeriodicEvaluation par f (MvPolynomial.X i) = balancedPeriodicJet par f i := by
  simp [balancedPeriodicEvaluation]

theorem balancedPeriodicEvaluation_generatorDerivative (par : FieldParameters)
    (f : PeriodicCoefficient par.Lx) (i : BalancedPDO.JetVariable par.M) :
    balancedPeriodicEvaluation par f (BalancedPDO.generatorDerivative par.M i) =
      (periodicSpatialEvolution par.Lx).toLinearMap (balancedPeriodicJet par f i) := by
  cases i with
  | b => simp only [BalancedPDO.generatorDerivative, map_zero, balancedPeriodicJet,
      evolution_algebraMap_zero]
  | eta => simp only [BalancedPDO.generatorDerivative, map_zero, balancedPeriodicJet,
      evolution_algebraMap_zero]
  | field j k =>
    rw [BalancedPDO.generatorDerivative, balancedPeriodicEvaluation_X]
    exact Function.iterate_succ_apply' _ k _

theorem balancedPeriodicEvaluation_spatial (par : FieldParameters) (f : PeriodicCoefficient par.Lx)
    (p : BalancedPDO.Poly par.M) :
    balancedPeriodicEvaluation par f (BalancedPDO.spatialDerivative par.M p) =
      (periodicSpatialEvolution par.Lx).toLinearMap (balancedPeriodicEvaluation par f p) := by
  induction p using MvPolynomial.induction_on with
  | C r =>
    rw [MvPolynomial.derivation_C, map_zero, balancedPeriodicEvaluation_C]
    symm
    exact evolution_algebraMap_zero _ r
  | add p q hp hq => simp only [map_add, hp, hq]
  | mul_X p i hp =>
    rw [Derivation.leibniz]
    have hXi : BalancedPDO.spatialDerivative par.M (MvPolynomial.X i) =
        BalancedPDO.generatorDerivative par.M i := MvPolynomial.mkDerivation_X _ _ _
    simp only [Algebra.smul_def, Algebra.algebraMap_self, RingHom.id_apply,
      map_add, map_mul, balancedPeriodicEvaluation_X, hXi,
      balancedPeriodicEvaluation_generatorDerivative, hp,
      (periodicSpatialEvolution par.Lx).leibniz]
    ring

def balancedPeriodicDifferentialEvaluation (par : FieldParameters) (f : PeriodicCoefficient par.Lx) :
    BalancedPDO.DifferentialEvaluation par.M (PeriodicCoefficient par.Lx) (periodicSpatialEvolution par.Lx) where
  evaluation := balancedPeriodicEvaluation par f
  derivative_compatible := balancedPeriodicEvaluation_spatial par f

theorem evolutionIterate_smul {R : Type*} [Ring R] [Algebra ℝ R]
    (d : AlgebraEvolution R) (k : ℕ) (r : ℝ) (x : R) :
    (d.toLinearMap)^[k] (r • x) = r • (d.toLinearMap)^[k] x := by
  induction k with
  | zero => rfl
  | succ k ih => rw [Function.iterate_succ_apply', ih, map_smul, Function.iterate_succ_apply']

theorem evolutionIterate_algebraMap {R : Type*} [CommRing R] [Algebra ℝ R]
    (d : AlgebraEvolution R) (k : ℕ) (r : ℝ) :
    (d.toLinearMap)^[k] (algebraMap ℝ R r) = if k = 0 then algebraMap ℝ R r else 0 := by
  cases k with
  | zero => rfl
  | succ k =>
    rw [Function.iterate_succ_apply, evolution_algebraMap_zero, evolutionIterate_zero]
    simp

theorem normalProductCoefficient_smul_both {R : Type*} [CommRing R] [Algebra ℝ R]
    (d : AlgebraEvolution R) (order : ℤ) (a b : ℕ → R) (r s : ℝ) (k : ℕ) :
    normalProductCoefficient d order (fun i => r • a i) (fun i => s • b i) k =
      (r * s) • normalProductCoefficient d order a b k := by
  classical
  unfold normalProductCoefficient
  rw [Finset.smul_sum]
  apply Finset.sum_congr rfl
  intro i _
  rw [Finset.smul_sum]
  apply Finset.sum_congr rfl
  intro j _
  split_ifs
  · rw [evolutionIterate_smul]
    simp only [Algebra.smul_def, map_mul]
    ring
  · exact (smul_zero _).symm

theorem normalProductCoefficient_constant_right {R : Type*} [CommRing R] [Algebra ℝ R]
    (d : AlgebraEvolution R) (order : ℤ) (a : ℕ → R) (r : ℝ) (k : ℕ) :
    normalProductCoefficient d order a (fun s => if s = 0 then algebraMap ℝ R r else 0) k =
      a k * algebraMap ℝ R r := by
  classical
  rw [normalProductCoefficient_scalar_right, Finset.sum_eq_single (Fin.last k)]
  · simp
  · intro i _ hi
    have hne : k - i.val ≠ 0 := by
      have hv : i.val ≠ k := by intro h; apply hi; exact Fin.ext h
      have hlt := i.isLt
      omega
    rw [evolutionIterate_algebraMap, if_neg hne, mul_zero]
  · simp

theorem GlobalPDO.balanced_g_eval (par : FieldParameters) (f : PeriodicCoefficient par.Lx)
    (j : Fin par.M) :
    GlobalPDO.evaluation par (balancedMomentumState par f) (GlobalPDO.g par j) =
      algebraMap ℝ (PeriodicCoefficient par.Lx) (2 * balancedEta par) := by
  rw [GlobalPDO.g, GlobalPDO.w, map_mul, map_add, GlobalPDO.evaluation_C,
    GlobalPDO.evaluation_C, GlobalPDO.s_eval]
  change algebraMap ℝ (PeriodicCoefficient par.Lx) (par.h / 4) *
    (algebraMap ℝ (PeriodicCoefficient par.Lx) par.c + 0) = _
  rw [add_zero, ← map_mul]
  congr 1
  unfold balancedEta
  ring

theorem GlobalPDO.balanced_beta_eval (par : FieldParameters) (f : PeriodicCoefficient par.Lx)
    (j : Fin par.M) :
    GlobalPDO.evaluation par (balancedMomentumState par f) (GlobalPDO.beta par j) =
      balancedPeriodicEvaluation par f (BalancedPDO.balancedBeta par.M j) := by
  rw [GlobalPDO.beta, map_mul, map_sub, GlobalPDO.evaluation_C, GlobalPDO.U,
    map_add, GlobalPDO.p_eval, GlobalPDO.commonU, map_mul, map_sub,
    GlobalPDO.evaluation_C, GlobalPDO.evaluation_C, GlobalPDO.meanPS,
    map_mul, map_sum, GlobalPDO.evaluation_C]
  simp only [map_mul, GlobalPDO.p_eval, GlobalPDO.s_eval]
  change algebraMap ℝ (PeriodicCoefficient par.Lx) (1 / 2) *
    ((2 : ℝ) • balancedCoefficientField par f j +
      algebraMap ℝ (PeriodicCoefficient par.Lx) par.c⁻¹ *
        (algebraMap ℝ (PeriodicCoefficient par.Lx) par.gamma -
          algebraMap ℝ (PeriodicCoefficient par.Lx) (par.M : ℝ)⁻¹ *
            ∑ i : Fin par.M, ((2 : ℝ) • balancedCoefficientField par f i) * 0) -
      GlobalPDO.evaluation par (balancedMomentumState par f) (GlobalPDO.g par j)) = _
  rw [GlobalPDO.balanced_g_eval]
  simp only [mul_zero, Finset.sum_const_zero, sub_zero]
  rw [BalancedPDO.balancedBeta, map_sub, map_add,
    balancedPeriodicEvaluation_X, balancedPeriodicEvaluation_X, balancedPeriodicEvaluation_X]
  apply Subtype.ext
  funext x
  change (1 / 2 : ℝ) * (2 * (balancedCoefficientField par f j : ℝ → ℝ) x +
    par.c⁻¹ * par.gamma - 2 * balancedEta par) =
      par.B + (balancedCoefficientField par f j : ℝ → ℝ) x - balancedEta par
  unfold FieldParameters.B
  ring

namespace GlobalBalancedSlice
variable (par : FieldParameters) (f : PeriodicCoefficient par.Lx)
local notation "EG" => GlobalPDO.evaluation par (balancedMomentumState par f)
local notation "EB" => balancedPeriodicEvaluation par f

theorem resolvent_eval (j : Fin par.M) (k : ℕ) :
    EG (GlobalPDO.resolventCoefficient par j k) = EB (BalancedPDO.resolventCoefficient par.M j k) := by
  induction k with
  | zero => simp [GlobalPDO.resolventCoefficient, BalancedPDO.resolventCoefficient]
  | succ k ih =>
    rw [GlobalPDO.resolventCoefficient, map_sub, map_mul,
      GlobalPDO.balanced_beta_eval, GlobalPDO.evaluation_derivative,
      BalancedPDO.resolventCoefficient, map_sub, map_mul,
      balancedPeriodicEvaluation_spatial, ih]

theorem site_eval (j : Fin par.M) (k : ℕ) :
    EG (GlobalPDO.siteCoefficient par j k) =
      balancedEta par • EB (BalancedPDO.siteQuotientCoefficient par.M j k) := by
  rw [GlobalPDO.siteCoefficient, map_neg, GlobalPDO.normalProduct_eval]
  have hright : (fun r : ℕ => EG (if r = 0 then GlobalPDO.g par j else 0)) =
      (fun r => if r = 0 then algebraMap ℝ (PeriodicCoefficient par.Lx) (2 * balancedEta par) else 0) := by
    funext r
    split_ifs
    · exact GlobalPDO.balanced_g_eval par f j
    · exact map_zero _
  simp only [resolvent_eval]
  rw [hright, normalProductCoefficient_constant_right,
    BalancedPDO.siteQuotientCoefficient, map_mul (balancedPeriodicEvaluation par f), balancedPeriodicEvaluation_C]
  simp only [Algebra.smul_def, map_mul, map_neg, map_ofNat]
  ring

theorem sites_eval (j k : ℕ) :
    EG (GlobalPDO.sites par j k) = balancedEta par • EB (BalancedPDO.balancedSites par.M j k) := by
  unfold GlobalPDO.sites BalancedPDO.balancedSites
  split_ifs
  · exact site_eval par f _ k
  · simp

theorem monodromyDifference_eval (n k : ℕ) :
    EG (GlobalPDO.monodromyDifferenceCoefficient par n k) =
      balancedEta par • EB (BalancedPDO.regularQuotientCoefficient par.M (BalancedPDO.balancedSites par.M) n k) := by
  induction n generalizing k with
  | zero => simp [GlobalPDO.monodromyDifferenceCoefficient, BalancedPDO.regularQuotientCoefficient]
  | succ n ih =>
    cases k with
    | zero =>
      rw [GlobalPDO.monodromyDifferenceCoefficient, map_add, sites_eval, ih,
        BalancedPDO.regularQuotientCoefficient, map_add, smul_add]
    | succ k =>
      rw [GlobalPDO.monodromyDifferenceCoefficient, map_add, map_add,
        GlobalPDO.normalProduct_eval]
      simp only [sites_eval, ih]
      rw [normalProductCoefficient_smul_both, BalancedPDO.regularQuotientCoefficient,
        map_add, map_add, map_mul, balancedPeriodicEvaluation_X]
      have hproduct := (balancedPeriodicDifferentialEvaluation par f).normalProduct_eval (-1)
        (BalancedPDO.balancedSites par.M n)
        (BalancedPDO.regularQuotientCoefficient par.M (BalancedPDO.balancedSites par.M) n) k
      change EB (BalancedPDO.normalProduct par.M (-1)
        (BalancedPDO.balancedSites par.M n)
        (BalancedPDO.regularQuotientCoefficient par.M (BalancedPDO.balancedSites par.M) n) k) =
        normalProductCoefficient (periodicSpatialEvolution par.Lx) (-1)
          (fun r => EB (BalancedPDO.balancedSites par.M n r))
          (fun r => EB (BalancedPDO.regularQuotientCoefficient par.M (BalancedPDO.balancedSites par.M) n r)) k at hproduct
      rw [hproduct]
      simp only [balancedPeriodicJet, Algebra.smul_def, map_mul]
      ring

theorem monodromy_eval (k : ℕ) :
    EG (GlobalPDO.monodromyCoefficient par k) =
      balancedEta par • EB (BalancedPDO.balancedQuotientCoefficient par.M k) :=
  monodromyDifference_eval par f par.M k

theorem inverse_scalar : (-par.G)⁻¹ = (balancedEta par)⁻¹ * (-2 * (par.M : ℝ))⁻¹ := by
  rw [G_eq_balancedEta]
  have he : -(2 * (par.M : ℝ) * balancedEta par) = (-2 * (par.M : ℝ)) * balancedEta par := by ring
  rw [he, mul_inv_rev]

theorem normalized_scalar : (-par.G) * (balancedEta par)⁻¹ = -2 * (par.M : ℝ) := by
  rw [G_eq_balancedEta]
  calc
    _ = (-2 * (par.M : ℝ)) * (balancedEta par * (balancedEta par)⁻¹) := by ring
    _ = _ := by rw [mul_inv_cancel₀ (balancedEta_ne_zero par), mul_one]

theorem inverse_eval (k : ℕ) :
    EG (GlobalPDO.inverseCoefficient par k) = (balancedEta par)⁻¹ •
      EB (BalancedPDO.inverseCoefficient par.M (BalancedPDO.balancedQuotientCoefficient par.M)
        (-2 * (par.M : ℝ))⁻¹ k) := by
  classical
  induction k using Nat.strong_induction_on with
  | h k ih =>
    cases k with
    | zero =>
      rw [GlobalPDO.inverseCoefficient, GlobalPDO.evaluation_C, BalancedPDO.inverseCoefficient,
        balancedPeriodicEvaluation_C, inverse_scalar, map_mul, Algebra.smul_def]
    | succ n =>
      rw [GlobalPDO.inverseCoefficient, map_mul, GlobalPDO.evaluation_C,
        BalancedPDO.inverseCoefficient, map_mul, balancedPeriodicEvaluation_C]
      have hsum : EG (∑ t : Fin (n + 1), ∑ r : Fin (n + 2),
          if r.val + t.val ≤ n + 1 then
            MvPolynomial.C ((Ring.choose (-1 - (r.val : ℤ))
              (n + 1 - (r.val + t.val)) : ℤ) : ℝ) * GlobalPDO.monodromyCoefficient par r.val *
                (GlobalPDO.spatialDerivative par)^[n + 1 - (r.val + t.val)]
                  (GlobalPDO.inverseCoefficient par t.val)
          else 0) =
        EB (∑ t : Fin (n + 1), ∑ r : Fin (n + 2),
          if r.val + t.val ≤ n + 1 then
            MvPolynomial.C ((Ring.choose (-1 - (r.val : ℤ))
              (n + 1 - (r.val + t.val)) : ℤ) : ℝ) * BalancedPDO.balancedQuotientCoefficient par.M r.val *
                BalancedPDO.spatialIterate par.M (n + 1 - (r.val + t.val))
                  (BalancedPDO.inverseCoefficient par.M (BalancedPDO.balancedQuotientCoefficient par.M)
                    (-2 * (par.M : ℝ))⁻¹ t.val)
          else 0) := by
        rw [map_sum, map_sum]
        apply Finset.sum_congr rfl
        intro t _
        rw [map_sum, map_sum]
        apply Finset.sum_congr rfl
        intro r _
        split_ifs
        · rw [map_mul, map_mul, GlobalPDO.evaluation_C, monodromy_eval,
            GlobalPDO.evaluation_iterate, ih t.val t.isLt, evolutionIterate_smul,
            map_mul, map_mul, balancedPeriodicEvaluation_C]
          have hiterate := (balancedPeriodicDifferentialEvaluation par f).spatialIterate_eval
            (n + 1 - (r.val + t.val))
            (BalancedPDO.inverseCoefficient par.M (BalancedPDO.balancedQuotientCoefficient par.M)
              (-2 * (par.M : ℝ))⁻¹ t.val)
          change EB (BalancedPDO.spatialIterate par.M _ _) =
            ((periodicSpatialEvolution par.Lx).toLinearMap)^[n + 1 - (r.val + t.val)]
              (EB (BalancedPDO.inverseCoefficient par.M (BalancedPDO.balancedQuotientCoefficient par.M)
                (-2 * (par.M : ℝ))⁻¹ t.val)) at hiterate
          rw [hiterate]
          have hcancel : algebraMap ℝ (PeriodicCoefficient par.Lx) (balancedEta par) *
              algebraMap ℝ (PeriodicCoefficient par.Lx) (balancedEta par)⁻¹ = 1 := by
            rw [← map_mul, mul_inv_cancel₀ (balancedEta_ne_zero par), map_one]
          simp only [Algebra.smul_def]
          calc
            _ = (algebraMap ℝ (PeriodicCoefficient par.Lx) (balancedEta par) *
                algebraMap ℝ (PeriodicCoefficient par.Lx) (balancedEta par)⁻¹) *
              (algebraMap ℝ (PeriodicCoefficient par.Lx) _ *
                EB (BalancedPDO.balancedQuotientCoefficient par.M r.val) *
                ((periodicSpatialEvolution par.Lx).toLinearMap)^[n + 1 - (r.val + t.val)]
                  (EB (BalancedPDO.inverseCoefficient par.M (BalancedPDO.balancedQuotientCoefficient par.M)
                    (-2 * (par.M : ℝ))⁻¹ t.val))) := by ring
            _ = _ := by rw [hcancel, one_mul]
        · rw [map_zero, map_zero]
      rw [hsum, inverse_scalar]
      simp only [Algebra.smul_def, map_neg, map_mul]
      ring

theorem normalized_eval (k : ℕ) :
    EG (GlobalPDO.normalizedCoefficient par k) = EB (BalancedPDO.balancedNormalizedCoefficient par.M k) := by
  rw [GlobalPDO.normalizedCoefficient, map_add, map_mul, GlobalPDO.evaluation_C,
    inverse_eval, BalancedPDO.balancedNormalizedCoefficient, BalancedPDO.normalizedCoefficient,
    map_add, map_mul, balancedPeriodicEvaluation_C]
  have hinv : algebraMap ℝ (PeriodicCoefficient par.Lx) (-par.G) *
      ((balancedEta par)⁻¹ • EB (BalancedPDO.inverseCoefficient par.M
        (BalancedPDO.balancedQuotientCoefficient par.M) (-2 * (par.M : ℝ))⁻¹ k)) =
      algebraMap ℝ (PeriodicCoefficient par.Lx) (-2 * (par.M : ℝ)) *
        EB (BalancedPDO.inverseCoefficient par.M (BalancedPDO.balancedQuotientCoefficient par.M)
          (-2 * (par.M : ℝ))⁻¹ k) := by
    rw [Algebra.smul_def, ← mul_assoc, ← map_mul, normalized_scalar]
  rw [hinv]
  congr 1
  split_ifs with hk
  · rw [GlobalPDO.evaluation_C, map_sub (balancedPeriodicEvaluation par f),
      map_mul (balancedPeriodicEvaluation par f), balancedPeriodicEvaluation_C,
      balancedPeriodicEvaluation_X, balancedPeriodicEvaluation_X]
    change algebraMap ℝ (PeriodicCoefficient par.Lx) (par.B - par.G / 2) =
      algebraMap ℝ (PeriodicCoefficient par.Lx) par.B -
        algebraMap ℝ (PeriodicCoefficient par.Lx) (par.M : ℝ) *
          algebraMap ℝ (PeriodicCoefficient par.Lx) (balancedEta par)
    rw [← map_mul, ← map_sub]
    congr 1
    rw [G_eq_balancedEta]
    ring
  · rw [map_zero, map_zero]

theorem power_eval (n k : ℕ) :
    EG (GlobalPDO.powerCoefficient par n k) =
      EB (BalancedPDO.powerCoefficient par.M (BalancedPDO.balancedNormalizedCoefficient par.M) n k) := by
  induction n generalizing k with
  | zero =>
    rw [GlobalPDO.powerCoefficient, BalancedPDO.powerCoefficient]
    split_ifs <;> simp
  | succ n ih =>
    rw [GlobalPDO.powerCoefficient, GlobalPDO.normalProduct_eval,
      BalancedPDO.powerCoefficient]
    simp only [ih, normalized_eval]
    exact ((balancedPeriodicDifferentialEvaluation par f).normalProduct_eval _ _ _ k).symm

theorem residue_eval (n : ℕ) :
    EG (GlobalPDO.residuePolynomial par n) = EB (BalancedPDO.balancedResiduePolynomial par.M n) :=
  power_eval par f n (n + 1)

/-- The complete charge restricted to the genuine f,-f physical slice
is the balanced polynomial integral, proved only by finite recurrences. -/
theorem constructedCharge_balanced_slice (n : ℕ) :
    GlobalPDO.constructedCharge par n (balancedMomentumState par f) =
      (n : ℝ)⁻¹ * periodicCoefficientIntegral par.Lx
        (EB (BalancedPDO.balancedResiduePolynomial par.M n)) := by
  unfold GlobalPDO.constructedCharge fieldPolynomialIntegral
  rw [GlobalPDO.periodicDensityPolynomial_eval, GlobalPDO.spectralDensityPolynomial,
    map_mul, GlobalPDO.evaluation_C, residue_eval]
  change periodicCoefficientIntegral par.Lx
    ((n : ℝ)⁻¹ • EB (BalancedPDO.balancedResiduePolynomial par.M n)) = _
  exact map_smul (periodicCoefficientIntegral par.Lx) _ _

end GlobalBalancedSlice
#print axioms GlobalBalancedSlice.residue_eval
#print axioms GlobalBalancedSlice.constructedCharge_balanced_slice
end
end DLWLean
