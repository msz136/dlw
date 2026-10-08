import NormalizationCoefficients
import Mathlib.Tactic.Linarith

/-!
General finite-period third monodromy coefficient. The trace-logarithm
coefficient calculation and its derivative corrections are explicit.
-/

namespace DLWLean
noncomputable section
open scoped BigOperators

variable {R : Type*} [CommRing R] [Algebra ℝ R]

def thirdCoefficient : R := algebraMap ℝ R ((1 : ℝ) / 3)

theorem three_mul_thirdCoefficient : 3 * (thirdCoefficient : R) = 1 := by
  change (3 : R) * algebraMap ℝ R ((1 : ℝ) / 3) = 1
  rw [← map_ofNat (algebraMap ℝ R) 3, ← map_mul]
  norm_num

/-- Coefficient of D^-3 in log(1+p1 D^-1+p2 D^-2+p3 D^-3). -/
def logThird (d : AlgebraEvolution R) (p : PDO3 R) : R :=
  p.third - p.first * p.second +
    halfCoefficient * p.first * d.toLinearMap p.first +
    thirdCoefficient * p.first ^ 3

theorem logThird_product (d : AlgebraEvolution R) (a b : PDO3 R) :
    logThird d (PDO3.mul d a b) = logThird d a + logThird d b +
      halfCoefficient * (b.first * d.toLinearMap a.first -
        a.first * d.toLinearMap b.first) := by
  calc
    _ = logThird d a + logThird d b +
      halfCoefficient * (b.first * d.toLinearMap a.first -
        a.first * d.toLinearMap b.first) +
      (2 * (halfCoefficient : R) - 1) * a.first * d.toLinearMap b.first +
      (3 * (thirdCoefficient : R) - 1) *
        (a.first ^ 2 * b.first + a.first * b.first ^ 2) := by
      simp only [logThird, PDO3.mul, map_add]
      ring
    _ = _ := by
      rw [two_mul_halfCoefficient, three_mul_thirdCoefficient]
      simp

def siteEnergyEighth (d : AlgebraEvolution R) (U g : R) : R :=
  halfCoefficient ^ 2 * U ^ 2 * g +
    (thirdCoefficient - halfCoefficient ^ 2) * g ^ 3 +
    halfCoefficient * g * d.toLinearMap U

/-- One-site logarithm density, with its exact total derivative displayed. -/
theorem transfer_logThird_exact (d : AlgebraEvolution R) (U g : R) :
    logThird d (transferCoefficients3 d U g) =
      -siteEnergyEighth d U g + d.toLinearMap (-d.toLinearMap g + U * g) := by
  calc
    _ = -siteEnergyEighth d U g + d.toLinearMap (-d.toLinearMap g + U * g) +
      (2 * (halfCoefficient : R) - 1) *
        ((U - g) * d.toLinearMap g + g * d.toLinearMap U +
          halfCoefficient * (U - g) * g ^ 2) := by
      simp only [logThird, transferCoefficients3, transferBeta, siteEnergyEighth,
        halfCoefficient, map_add, map_sub, map_neg, d.leibniz,
        evolution_algebraMap_zero, zero_mul, zero_add]
      ring
    _ = _ := by rw [two_mul_halfCoefficient, sub_self, zero_mul, add_zero]

/-- Periodic coefficient integration, with total derivatives annihilated. -/
structure PeriodicIntegral (d : AlgebraEvolution R) where
  toLinearMap : R →ₗ[ℝ] ℝ
  total_derivative_zero : ∀ r : R, toLinearMap (d.toLinearMap r) = 0

namespace PeriodicIntegral

variable {d : AlgebraEvolution R} (I : PeriodicIntegral d)

theorem scalar_mul (s : ℝ) (r : R) :
    I.toLinearMap (algebraMap ℝ R s * r) = s * I.toLinearMap r := by
  rw [← Algebra.smul_def, map_smul, smul_eq_mul]

theorem half_mul (r : R) :
    I.toLinearMap ((halfCoefficient : R) * r) = I.toLinearMap r / 2 := by
  rw [halfCoefficient, I.scalar_mul]
  ring

theorem integration_by_parts (a b : R) :
    I.toLinearMap (a * d.toLinearMap b) =
      -I.toLinearMap (d.toLinearMap a * b) := by
  have h := I.total_derivative_zero (a * b)
  rw [d.leibniz, map_add] at h
  exact eq_neg_of_add_eq_zero_right h

theorem self_derivative_zero (a : R) :
    I.toLinearMap (a * d.toLinearMap a) = 0 := by
  have h := I.integration_by_parts a a
  rw [mul_comm (d.toLinearMap a) a] at h
  linarith

theorem logThird_product_integral (a b : PDO3 R) :
    I.toLinearMap (logThird d (PDO3.mul d a b)) =
      I.toLinearMap (logThird d a) + I.toLinearMap (logThird d b) -
        I.toLinearMap (a.first * d.toLinearMap b.first) := by
  rw [logThird_product, map_add, map_add, I.half_mul, map_sub,
    I.integration_by_parts b.first a.first,
    mul_comm (d.toLinearMap b.first) a.first]
  ring

theorem transfer_logThird_integral (U g : R) :
    I.toLinearMap (logThird d (transferCoefficients3 d U g)) =
      -I.toLinearMap (siteEnergyEighth d U g) := by
  rw [transfer_logThird_exact, map_add, map_neg, I.total_derivative_zero, add_zero]

end PeriodicIntegral

/-- Explicit all-period integrated third logarithm coefficient. The prefix
derivative term is the genuine triangular interaction of the factors. -/
theorem monodromy_logThird_integral (d : AlgebraEvolution R)
    (I : PeriodicIntegral d) (U g : ℕ → R) (n : ℕ) :
    I.toLinearMap (logThird d (monodromyCoefficients3 d U g n)) =
      -(∑ j ∈ Finset.range n, I.toLinearMap (siteEnergyEighth d (U j) (g j))) -
        (∑ j ∈ Finset.range n,
          I.toLinearMap (g j * d.toLinearMap (∑ k ∈ Finset.range j, g k))) := by
  induction n with
  | zero => simp [monodromyCoefficients3, PDO3.one, logThird]
  | succ n ih =>
    rw [monodromyCoefficients3, I.logThird_product_integral,
      I.transfer_logThird_integral, ih, monodromy_first_coefficient_sum]
    simp only [transferCoefficients3, map_neg, neg_mul, mul_neg, neg_neg,
      Finset.sum_range_succ]
    ring

/-- The exact integrated m3 decomposition follows from the constructed
PDO3 monodromy, with only fixed spatial mean as a closure condition. -/
theorem monodromy_third_integral_decomposition (d : AlgebraEvolution R)
    (I : PeriodicIntegral d) (U g : ℕ → R) (n : ℕ)
    (hmean : d.toLinearMap (∑ j ∈ Finset.range n, g j) = 0) :
    I.toLinearMap (monodromyCoefficients3 d U g n).third =
      -(∑ j ∈ Finset.range n, I.toLinearMap (siteEnergyEighth d (U j) (g j))) -
        (∑ j ∈ Finset.range n,
          I.toLinearMap (g j * d.toLinearMap (∑ k ∈ Finset.range j, g k))) +
      I.toLinearMap (halfCoefficient * (∑ j ∈ Finset.range n, g j) *
        (∑ j ∈ Finset.range n, U j * g j) -
        (halfCoefficient - thirdCoefficient) * (∑ j ∈ Finset.range n, g j) ^ 3) := by
  have hlog := monodromy_logThird_integral d I U g n
  have hid : logThird d (monodromyCoefficients3 d U g n) =
      (monodromyCoefficients3 d U g n).third -
      (halfCoefficient * (∑ j ∈ Finset.range n, g j) *
        (∑ j ∈ Finset.range n, U j * g j) -
        (halfCoefficient - thirdCoefficient) * (∑ j ∈ Finset.range n, g j) ^ 3) := by
    rw [logThird, monodromy_first_coefficient_sum,
      monodromy_second_coefficient_fixed_mean d U g n hmean]
    simp only [map_neg, hmean, neg_zero, mul_zero, add_zero]
    ring
  rw [hid, map_sub] at hlog
  linarith

/-- The coefficient-algebra versions of mean, prefix primitive and P0.
The normalized resolvent below is exactly P0(prefix+1/2)P0 = R/h. -/
def coefficientMean (n : ℕ) (f : ℕ → R) : R :=
  algebraMap ℝ R (n : ℝ)⁻¹ * ∑ j ∈ Finset.range n, f j

def coefficientPrefix (f : ℕ → R) (j : ℕ) : R := ∑ k ∈ Finset.range j, f k

def coefficientP0 (n : ℕ) (f : ℕ → R) (j : ℕ) : R := f j - coefficientMean n f

def coefficientPrimitive (f : ℕ → R) (j : ℕ) : R :=
  coefficientPrefix f j + halfCoefficient * f j

def coefficientResolventNormalized (n : ℕ) (f : ℕ → R) (j : ℕ) : R :=
  coefficientP0 n (coefficientPrimitive (coefficientP0 n f)) j

theorem coefficientMean_derivative (d : AlgebraEvolution R) (n : ℕ) (f : ℕ → R) :
    d.toLinearMap (coefficientMean n f) =
      coefficientMean n (fun j => d.toLinearMap (f j)) := by
  simp only [coefficientMean, d.leibniz, evolution_algebraMap_zero,
    zero_mul, zero_add, map_sum]

theorem coefficientPrefix_derivative (d : AlgebraEvolution R)
    (f : ℕ → R) (j : ℕ) : d.toLinearMap (coefficientPrefix f j) =
      coefficientPrefix (fun k => d.toLinearMap (f k)) j := by
  simp only [coefficientPrefix, map_sum]

theorem coefficientPrimitive_derivative (d : AlgebraEvolution R)
    (f : ℕ → R) (j : ℕ) : d.toLinearMap (coefficientPrimitive f j) =
      coefficientPrimitive (fun k => d.toLinearMap (f k)) j := by
  simp only [coefficientPrimitive, map_add, coefficientPrefix_derivative,
    d.leibniz, halfCoefficient, evolution_algebraMap_zero, zero_mul, zero_add]

/-- With fixed total mean, the triangular interaction and the projected
cyclic resolvent pairing differ only by integrated total derivatives. -/
theorem triangular_resolvent_integral (d : AlgebraEvolution R)
    (I : PeriodicIntegral d) (g : ℕ → R) (n : ℕ)
    (hmean : d.toLinearMap (∑ j ∈ Finset.range n, g j) = 0) :
    (∑ j ∈ Finset.range n, I.toLinearMap (g j *
      coefficientResolventNormalized n (fun k => d.toLinearMap (g k)) j)) =
    (∑ j ∈ Finset.range n,
      I.toLinearMap (g j * d.toLinearMap (coefficientPrefix g j))) := by
  have hsum : (∑ j ∈ Finset.range n, d.toLinearMap (g j)) = 0 := by
    simpa only [map_sum] using hmean
  have hmeanD : coefficientMean n (fun j => d.toLinearMap (g j)) = 0 := by
    simp only [coefficientMean, hsum, mul_zero]
  have hp : d.toLinearMap (coefficientMean n (coefficientPrimitive g)) =
      coefficientMean n (coefficientPrimitive (fun k => d.toLinearMap (g k))) := by
    rw [coefficientMean_derivative]
    simp_rw [coefficientPrimitive_derivative]
  have hQ : ∀ j, coefficientResolventNormalized n
      (fun k => d.toLinearMap (g k)) j =
      d.toLinearMap (coefficientPrefix g j) + halfCoefficient * d.toLinearMap (g j) -
        d.toLinearMap (coefficientMean n (coefficientPrimitive g)) := by
    intro j
    unfold coefficientResolventNormalized coefficientP0
    simp only [hmeanD, sub_zero]
    rw [← hp]
    simp only [coefficientPrimitive, coefficientPrefix_derivative]
  have hpoint : ∀ j,
      I.toLinearMap (g j * coefficientResolventNormalized n
        (fun k => d.toLinearMap (g k)) j) =
      I.toLinearMap (g j * d.toLinearMap (coefficientPrefix g j)) -
        I.toLinearMap (g j *
          d.toLinearMap (coefficientMean n (coefficientPrimitive g))) := by
    intro j
    rw [hQ, mul_sub, mul_add, map_sub, map_add]
    have hself : I.toLinearMap (g j * (halfCoefficient * d.toLinearMap (g j))) = 0 := by
      calc
        _ = I.toLinearMap (halfCoefficient * (g j * d.toLinearMap (g j))) := by
          congr 1
          ring
        _ = 0 := by rw [I.half_mul, I.self_derivative_zero, zero_div]
    rw [hself, add_zero]
  simp_rw [hpoint]
  rw [Finset.sum_sub_distrib]
  have hconstant : (∑ j ∈ Finset.range n,
      I.toLinearMap (g j *
        d.toLinearMap (coefficientMean n (coefficientPrimitive g)))) = 0 := by
    rw [← map_sum, ← Finset.sum_mul, I.integration_by_parts, hmean,
      zero_mul, map_zero, neg_zero]
  rw [hconstant, sub_zero]

/-- One eighth of the actual Hamiltonian density after substituting
g=h*w/4, with the explicit cyclic resolvent R/h. -/
def energyEighthG (d : AlgebraEvolution R) (U g : ℕ → R) (n : ℕ) : R :=
  (∑ j ∈ Finset.range n, siteEnergyEighth d (U j) (g j)) +
    (∑ j ∈ Finset.range n, g j *
      coefficientResolventNormalized n (fun k => d.toLinearMap (g k)) j)

/-- General-period m3 energy identity, established from the exact transfer
product and the explicit projected prefix resolvent. -/
theorem monodromy_third_integral_energy (d : AlgebraEvolution R)
    (I : PeriodicIntegral d) (U g : ℕ → R) (n : ℕ)
    (hmean : d.toLinearMap (∑ j ∈ Finset.range n, g j) = 0) :
    I.toLinearMap (monodromyCoefficients3 d U g n).third =
      -I.toLinearMap (energyEighthG d U g n) +
      I.toLinearMap (halfCoefficient * (∑ j ∈ Finset.range n, g j) *
        (∑ j ∈ Finset.range n, U j * g j) -
        (halfCoefficient - thirdCoefficient) * (∑ j ∈ Finset.range n, g j) ^ 3) := by
  rw [monodromy_third_integral_decomposition d I U g n hmean]
  simp only [energyEighthG, map_add, map_sum]
  rw [triangular_resolvent_integral d I g n hmean]
  simp only [coefficientPrefix, map_sum]
  ring

theorem halfCoefficient_sq : (halfCoefficient : R) ^ 2 =
    algebraMap ℝ R ((1 : ℝ) / 4) := by
  rw [halfCoefficient, ← map_pow]
  norm_num

theorem third_sub_halfCoefficient_sq :
    (thirdCoefficient : R) - halfCoefficient ^ 2 =
      algebraMap ℝ R ((1 : ℝ) / 12) := by
  rw [halfCoefficient_sq, thirdCoefficient, ← map_sub]
  norm_num

theorem half_sub_thirdCoefficient : (halfCoefficient : R) - thirdCoefficient =
    algebraMap ℝ R ((1 : ℝ) / 6) := by
  rw [halfCoefficient, thirdCoefficient, ← map_sub]
  norm_num

/-- Physical Hamiltonian density written in g=h*w/4 coordinates. -/
def hamiltonianDensityG (d : AlgebraEvolution R) (U g : ℕ → R) (n : ℕ) : R :=
  ∑ j ∈ Finset.range n,
    (2 * U j ^ 2 * g j + algebraMap ℝ R ((2 : ℝ) / 3) * g j ^ 3 +
      4 * g j * d.toLinearMap (U j) +
      8 * g j * coefficientResolventNormalized n (fun k => d.toLinearMap (g k)) j)

theorem energyEighthG_is_density_eighth (d : AlgebraEvolution R)
    (U g : ℕ → R) (n : ℕ) :
    energyEighthG d U g n =
      algebraMap ℝ R ((1 : ℝ) / 8) * hamiltonianDensityG d U g n := by
  have h8quarter : 8 * (halfCoefficient : R) ^ 2 = 2 := by
    rw [halfCoefficient_sq, ← map_ofNat (algebraMap ℝ R) 8, ← map_mul]
    norm_num
    exact map_ofNat (algebraMap ℝ R) 2
  have h8twelfth : 8 * ((thirdCoefficient : R) - halfCoefficient ^ 2) =
      algebraMap ℝ R ((2 : ℝ) / 3) := by
    rw [third_sub_halfCoefficient_sq, ← map_ofNat (algebraMap ℝ R) 8, ← map_mul]
    norm_num
  have h8half : 8 * (halfCoefficient : R) = 4 := by
    rw [halfCoefficient, ← map_ofNat (algebraMap ℝ R) 8, ← map_mul]
    norm_num
    exact map_ofNat (algebraMap ℝ R) 4
  have h8 : 8 * energyEighthG d U g n = hamiltonianDensityG d U g n := by
    unfold energyEighthG hamiltonianDensityG
    rw [mul_add, Finset.mul_sum, Finset.mul_sum, ← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro j _
    simp only [siteEnergyEighth, mul_add, ← mul_assoc, h8quarter, h8twelfth, h8half]
  have hinv8 : algebraMap ℝ R ((1 : ℝ) / 8) * 8 = 1 := by
    rw [← map_ofNat (algebraMap ℝ R) 8, ← map_mul]
    norm_num
  have hh := congrArg (fun r : R => algebraMap ℝ R ((1 : ℝ) / 8) * r) h8
  simpa only [← mul_assoc, hinv8, one_mul] using hh

/-- The desired p3 Hamiltonian identity is a theorem of the constructed
finite PDO product, not an input residue formula. -/
theorem monodromy_third_integral_H0 (d : AlgebraEvolution R)
    (I : PeriodicIntegral d) (U g : ℕ → R) (n : ℕ)
    (hmean : d.toLinearMap (∑ j ∈ Finset.range n, g j) = 0) :
    I.toLinearMap (monodromyCoefficients3 d U g n).third =
      -I.toLinearMap (hamiltonianDensityG d U g n) / 8 +
      I.toLinearMap (halfCoefficient * (∑ j ∈ Finset.range n, g j) *
        (∑ j ∈ Finset.range n, U j * g j) -
        algebraMap ℝ R ((1 : ℝ) / 6) * (∑ j ∈ Finset.range n, g j) ^ 3) := by
  rw [monodromy_third_integral_energy d I U g n hmean,
    energyEighthG_is_density_eighth, I.scalar_mul, half_sub_thirdCoefficient]
  ring

theorem coefficientMean_mul (r : R) (n : ℕ) (f : ℕ → R) :
    coefficientMean n (fun j => r * f j) = r * coefficientMean n f := by
  simp only [coefficientMean, ← Finset.mul_sum]
  ring

theorem coefficientPrefix_mul (r : R) (f : ℕ → R) (j : ℕ) :
    coefficientPrefix (fun k => r * f k) j = r * coefficientPrefix f j := by
  simp only [coefficientPrefix, ← Finset.mul_sum]

theorem coefficientP0_mul (r : R) (n : ℕ) (f : ℕ → R) (j : ℕ) :
    coefficientP0 n (fun k => r * f k) j = r * coefficientP0 n f j := by
  rw [coefficientP0, coefficientMean_mul, coefficientP0]
  ring

theorem coefficientPrimitive_mul (r : R) (f : ℕ → R) (j : ℕ) :
    coefficientPrimitive (fun k => r * f k) j = r * coefficientPrimitive f j := by
  rw [coefficientPrimitive, coefficientPrefix_mul, coefficientPrimitive]
  ring

theorem coefficientResolventNormalized_mul (r : R) (n : ℕ) (f : ℕ → R) (j : ℕ) :
    coefficientResolventNormalized n (fun k => r * f k) j =
      r * coefficientResolventNormalized n f j := by
  unfold coefficientResolventNormalized
  have hp : coefficientP0 n (fun k => r * f k) =
      fun k => r * coefficientP0 n f k :=
    funext (coefficientP0_mul r n f)
  rw [hp]
  have hq : coefficientPrimitive (fun k => r * coefficientP0 n f k) =
      fun k => r * coefficientPrimitive (coefficientP0 n f) k :=
    funext (coefficientPrimitive_mul r (coefficientP0 n f))
  rw [hq, coefficientP0_mul]

def coefficientResolvent (h : ℝ) (n : ℕ) (f : ℕ → R) (j : ℕ) : R :=
  algebraMap ℝ R h * coefficientResolventNormalized n f j

/-- The source Hamiltonian density h Σ[U²w/2+h²w³/96+w U_x+w Rw_x/2],
with R=h P0(prefix+1/2)P0 constructed explicitly. -/
def hamiltonianDensityW (d : AlgebraEvolution R) (U w : ℕ → R)
    (h : ℝ) (n : ℕ) : R :=
  algebraMap ℝ R h * ∑ j ∈ Finset.range n,
    (halfCoefficient * U j ^ 2 * w j + algebraMap ℝ R (h ^ 2 / 96) * w j ^ 3 +
      w j * d.toLinearMap (U j) + halfCoefficient * w j *
        coefficientResolvent h n (fun k => d.toLinearMap (w k)) j)

theorem hamiltonianDensityG_eq_physicalW (d : AlgebraEvolution R)
    (U w : ℕ → R) (h : ℝ) (n : ℕ) :
    hamiltonianDensityG d U (fun j => latticeQuarter h * w j) n =
      hamiltonianDensityW d U w h n := by
  have hd : ∀ j, d.toLinearMap (latticeQuarter h * w j) =
      latticeQuarter h * d.toLinearMap (w j) := by
    intro j
    simp only [latticeQuarter, d.leibniz, evolution_algebraMap_zero, zero_mul, zero_add]
  have hc1 : 2 * (latticeQuarter h : R) = algebraMap ℝ R h * halfCoefficient := by
    unfold latticeQuarter halfCoefficient
    rw [← map_ofNat (algebraMap ℝ R) 2, ← map_mul, ← map_mul]
    congr 1
    ring
  have hc2 : algebraMap ℝ R ((2 : ℝ) / 3) * (latticeQuarter h : R) ^ 3 =
      algebraMap ℝ R h * algebraMap ℝ R (h ^ 2 / 96) := by
    unfold latticeQuarter
    rw [← map_pow, ← map_mul, ← map_mul]
    congr 1
    ring
  have hc3 : 4 * (latticeQuarter h : R) = algebraMap ℝ R h := by
    unfold latticeQuarter
    rw [← map_ofNat (algebraMap ℝ R) 4, ← map_mul]
    congr 1
    ring
  have hc4 : 8 * (latticeQuarter h : R) ^ 2 =
      algebraMap ℝ R h * halfCoefficient * algebraMap ℝ R h := by
    unfold latticeQuarter halfCoefficient
    rw [← map_ofNat (algebraMap ℝ R) 8, ← map_pow, ← map_mul, ← map_mul, ← map_mul]
    congr 1
    ring
  unfold hamiltonianDensityG hamiltonianDensityW
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro j _
  simp_rw [hd, coefficientResolventNormalized_mul]
  calc
    _ = (2 * latticeQuarter h) * U j ^ 2 * w j +
      (algebraMap ℝ R ((2 : ℝ) / 3) * (latticeQuarter h) ^ 3) * w j ^ 3 +
      (4 * latticeQuarter h) * w j * d.toLinearMap (U j) +
      (8 * (latticeQuarter h) ^ 2) * w j *
        coefficientResolventNormalized n (fun k => d.toLinearMap (w k)) j := by ring
    _ = _ := by rw [hc1, hc2, hc3, hc4]; unfold coefficientResolvent; ring

theorem monodromy_third_integral_physical_energy (d : AlgebraEvolution R)
    (I : PeriodicIntegral d) (U w : ℕ → R) (h : ℝ) (n : ℕ)
    (hmean : d.toLinearMap (∑ j ∈ Finset.range n, latticeQuarter h * w j) = 0) :
    I.toLinearMap (monodromyCoefficients3 d U (fun j => latticeQuarter h * w j) n).third =
      -I.toLinearMap (hamiltonianDensityW d U w h n) / 8 +
      I.toLinearMap (halfCoefficient * (∑ j ∈ Finset.range n, latticeQuarter h * w j) *
        (∑ j ∈ Finset.range n, U j * (latticeQuarter h * w j)) -
        algebraMap ℝ R ((1 : ℝ) / 6) *
          (∑ j ∈ Finset.range n, latticeQuarter h * w j) ^ 3) := by
  rw [monodromy_third_integral_H0 d I U (fun j => latticeQuarter h * w j) n hmean,
    hamiltonianDensityG_eq_physicalW]

theorem PeriodicIntegral.scalar_coefficient {d : AlgebraEvolution R}
    (I : PeriodicIntegral d) (s : ℝ) :
    I.toLinearMap (algebraMap ℝ R s) = s * I.toLinearMap 1 := by
  have h := I.scalar_mul s (1 : R)
  simpa only [mul_one] using h

/-- The extracted first-residue coefficient for a=-G and
b=(G²-T)/2. Its inverse-series derivation is in NormalizationCoefficients. -/
def firstResidueFromCoefficients (G T : ℝ) (m3 : R) : R :=
  algebraMap ℝ R (((G ^ 2 - T) / 2) ^ 2 / G ^ 2) + algebraMap ℝ R G⁻¹ * m3

/-- With the two constant mean closures, the first normalized residue trace
is computed from the actual finite transfer coefficients and physical H0.
The desired first-residue energy formula is the conclusion, not a premise. -/
theorem firstResidue_integral_physical_energy (d : AlgebraEvolution R)
    (I : PeriodicIntegral d) (U w : ℕ → R) (h G T : ℝ) (n : ℕ)
    (hG : G ≠ 0)
    (hmeanG : (∑ j ∈ Finset.range n, latticeQuarter h * w j) = algebraMap ℝ R G)
    (hmeanT : (∑ j ∈ Finset.range n, U j * (latticeQuarter h * w j)) =
      algebraMap ℝ R T) :
    I.toLinearMap (firstResidueFromCoefficients G T
      (monodromyCoefficients3 d U (fun j => latticeQuarter h * w j) n).third) =
      -I.toLinearMap (hamiltonianDensityW d U w h n) / (8 * G) +
        (G ^ 2 / 12 + T ^ 2 / (4 * G ^ 2)) * I.toLinearMap 1 := by
  have hmean : d.toLinearMap (∑ j ∈ Finset.range n, latticeQuarter h * w j) = 0 := by
    rw [hmeanG, evolution_algebraMap_zero]
  have hm3 := monodromy_third_integral_physical_energy d I U w h n hmean
  rw [hmeanG, hmeanT, halfCoefficient, ← map_mul, ← map_mul,
    ← map_pow, ← map_mul, ← map_sub, I.scalar_coefficient] at hm3
  unfold firstResidueFromCoefficients
  rw [map_add, I.scalar_coefficient, I.scalar_mul, hm3]
  field_simp [hG]
  ring

#print axioms transfer_logThird_exact
#print axioms monodromy_logThird_integral
#print axioms monodromy_third_integral_decomposition
#print axioms triangular_resolvent_integral
#print axioms monodromy_third_integral_energy
#print axioms monodromy_third_integral_H0
#print axioms hamiltonianDensityG_eq_physicalW
#print axioms monodromy_third_integral_physical_energy
#print axioms firstResidue_integral_physical_energy

end
end DLWLean
