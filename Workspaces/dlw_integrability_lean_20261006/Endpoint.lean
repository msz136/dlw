import SpectralVariation
import Independence
import Genericity
import ReducedPairing
import StartPoint
import DarbouxJets
import HeatIntertwiner
import LatticeResolvent
import ResidueIntegral
import PhysicalBracket

/-!
Verified algebraic endpoint. The physical link equations, formal PDO
realization and all-order physical Fourier symbols still need to be
established. This is not a completed general-field DLW theorem.
-/
namespace DLWLean
noncomputable section

variable {A : Type*} [Ring A] [Algebra ℝ A]

structure OperatorStart (par : FieldParameters) (A : Type*)
    [Ring A] [Algebra ℝ A] where
  tr : CyclicTrace A
  evolution : AlgebraEvolution A
  plus : A →ₗ[ℝ] A
  T : ℕ → A
  Q : ℕ → A
  links : ∀ j < par.M,
    evolution.toLinearMap (T j) = Q (j + 1) * T j - T j * Q j
  closed : Q par.M = Q 0
  monodromyMinusOne : Aˣ
  unit_value : (monodromyMinusOne : A) = transferProduct T par.M - 1

def OperatorStart.L {par : FieldParameters} (start : OperatorStart par A) : A :=
  normalizedL par.G par.B start.monodromyMinusOne

def OperatorStart.C {par : FieldParameters} (start : OperatorStart par A)
    (n : ℕ) : ℝ := spectralInvariant start.tr start.L n

def periodicSite (par : FieldParameters) (j : ℕ) : Fin par.M :=
  ⟨j % par.M, Nat.mod_lt _ (Nat.pos_of_ne_zero par.M_ne_zero)⟩

theorem periodicSite_succ (par : FieldParameters) (j : ℕ) :
    periodicSite par (j + 1) = nextSite par (periodicSite par j) := by
  apply Fin.ext
  change (j + 1) % par.M = (j % par.M + 1) % par.M
  exact (Nat.mod_add_mod j par.M 1).symm

/-- The finite periodic OperatorStart is now constructed from coefficient
PDE sources and actual inverse first-order factors. No transfer Lax law
occurs among the inputs. The spatial/time coefficient model and formal
PDO representation remain explicit inputs. -/
def operatorStartFromPhysicalSources
    {R : Type*} [CommRing R] [Algebra ℝ R]
    (par : FieldParameters) (model : CoefficientOperatorModel R A)
    (tr : CyclicTrace A) (plus : A →ₗ[ℝ] A)
    (source : Fin par.M → PhysicalCoefficientJet model par.h par.c)
    (hshift : ∀ j, (source j).potentialPlus = (source (nextSite par j)).potential)
    (denominator : Fin par.M → Aˣ)
    (hdenominator : ∀ j, (denominator j : A) = model.factor (source j).beta)
    (monodromyMinusOne : Aˣ)
    (hmonodromy : (monodromyMinusOne : A) =
      transferProduct (fun j => (↑(denominator (periodicSite par j))⁻¹ : A) *
        model.factor (source (periodicSite par j)).alpha) par.M - 1) :
    OperatorStart par A where
  tr := tr
  evolution := model.evolution
  plus := plus
  T j := (↑(denominator (periodicSite par j))⁻¹ : A) *
    model.factor (source (periodicSite par j)).alpha
  Q j := model.heat (source (periodicSite par j)).potential
  links j hj := by
    have h := (source (periodicSite par j)).transfer_lax_from_physical_source
      (denominator (periodicSite par j)) (hdenominator _)
    rw [hshift, ← periodicSite_succ] at h
    exact h
  closed := by
    have hsite : periodicSite par par.M = periodicSite par 0 := by
      apply Fin.ext
      simp [periodicSite]
    rw [hsite]
  monodromyMinusOne := monodromyMinusOne
  unit_value := hmonodromy

/-- This theorem proves conservation rates and Adler pairings of the
constructed normalized operator, for every positive integer order.
The link equations and physical realization have different logical roles. -/
theorem operator_endpoint (par : FieldParameters) (start : OperatorStart par A) :
    (∀ n : ℕ, 0 < n →
      spectralInvariantRate start.tr start.evolution start.L n = 0) ∧
    (∀ m n : ℕ, 0 < m → 0 < n →
      start.tr.toLinearMap
        (rationalGradient par.G par.B start.monodromyMinusOne m *
          adler start.plus (transferProduct start.T par.M)
            (rationalGradient par.G par.B start.monodromyMinusOne n)) = 0) := by
  constructor
  · intro n hn
    exact normalized_periodic_spectral_rates_zero start.tr start.evolution
      start.T start.Q par.M start.links start.closed par.G par.B
      start.monodromyMinusOne start.unit_value n
  · intro m n hm hn
    exact rationalGradients_adler_involution start.tr start.plus
      (transferProduct start.T par.M) par.G par.B start.monodromyMinusOne
      start.unit_value m n

/-- The source uses a nonzero leading coefficient in ε, not an exact
Vandermonde formula for the full nonlinear Jacobian. The polynomial
minor and its leading symbol are explicit, still required physical
premises in this general witness-transfer theorem. -/
theorem independent_physical_block_of_leading_frequency_minor
    {V : Type*} [AddCommGroup V] [Module ℝ V] (par : FieldParameters)
    (N : ℕ) (dC₁ dP : ℝ → V →ₗ[ℝ] ℝ) (tail : ℝ → Fin N → V →ₗ[ℝ] ℝ)
    (directions : ℝ → Fin (N + 1) → V) (extra : ℝ → V)
    (frequency : Fin (N + 1) → ℝ)
    (polynomials : Fin (N + 1) → Polynomial ℝ)
    (hpositive : ∀ i, 0 < frequency i)
    (hdistinct : Function.Injective frequency)
    (hdegree : ∀ i, (polynomials i).natDegree ≤ (i : ℕ))
    (hlead : ∀ i, (polynomials i).coeff (i : ℕ) ≠ 0)
    (minorPolynomial : Polynomial ℝ) (order : ℕ) (scale : ℝ) (hscale : scale ≠ 0)
    (hminor : ∀ ε, (covectorMinor (Fin.cons (dC₁ ε) (tail ε)) (directions ε)).det =
      minorPolynomial.eval ε)
    (hleading : minorPolynomial.coeff order =
      scale * (polynomialFrequencyMatrix (fun i => (frequency i) ^ 2) polynomials).det)
    (hannihilate : ∀ ε i, dP ε (directions ε i) = 0)
    (hextra : ∀ ε, ε ≠ 0 → dP ε (extra ε) ≠ 0)
    (radius : ℝ) (hradius : 0 < radius) :
    ∃ ε : ℝ, 0 < ε ∧ ε < radius ∧ LinearIndependent ℝ
      (Fin.cons ((-8 * par.G) • dC₁ ε + (par.gamma / par.c) • dP ε)
        (Fin.cons (dP ε) (tail ε))) := by
  have hcoeff : minorPolynomial.coeff order ≠ 0 := by
    rw [hleading]
    exact mul_ne_zero hscale (squaredFrequencyPolynomial_det_ne_zero frequency
      polynomials hpositive hdistinct hdegree hlead)
  obtain ⟨ε, hε, hsmall, hvalue⟩ := polynomial_nonzero_at_small_positive_amplitude
    minorPolynomial order hcoeff radius hradius
  refine ⟨ε, hε, hsmall, ?_⟩
  apply physical_covectors_independent_from_odd_minor (dC₁ ε) (dP ε) (tail ε)
    (directions ε) (extra ε) par.G (par.gamma / par.c) par.G_ne_zero _
      (hannihilate ε) (hextra ε (ne_of_gt hε))
  rwa [hminor]

#print axioms operator_endpoint
#print axioms independent_physical_block_of_leading_frequency_minor

end
end DLWLean
