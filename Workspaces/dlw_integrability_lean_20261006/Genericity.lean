import Mathlib.Algebra.Polynomial.Roots
import Mathlib.Topology.Algebra.Module.Basic
import Mathlib.Topology.Baire.Lemmas
import Mathlib.Topology.Instances.Real.Lemmas

/-!
Genericity from a nonzero polynomial witness, on a real topological vector
space. This applies to determinant minors once their continuity, line
polynomiality and physical witness have actually been established.
-/
namespace DLWLean

open Set Polynomial

theorem dense_polynomial_nonzero (p : Polynomial ℝ) (hp : p ≠ 0) :
    Dense {t : ℝ | p.eval t ≠ 0} := by
  have hroots : Set.Finite {t : ℝ | p.IsRoot t} :=
    Polynomial.finite_setOfPred_isRoot hp
  have hd := (dense_univ : Dense (Set.univ : Set ℝ)).sdiff_finite hroots
  convert hd using 1
  ext t
  simp [Polynomial.IsRoot]

/-- A nonzero coefficient of the amplitude-minor polynomial supplies
arbitrarily small positive amplitudes with a nonzero actual minor. -/
theorem polynomial_nonzero_at_small_positive_amplitude
    (p : Polynomial ℝ) (order : ℕ) (hcoefficient : p.coeff order ≠ 0)
    (radius : ℝ) (hradius : 0 < radius) :
    ∃ amplitude : ℝ, 0 < amplitude ∧ amplitude < radius ∧ p.eval amplitude ≠ 0 := by
  have hp : p ≠ 0 := by
    intro hz
    apply hcoefficient
    simp [hz]
  obtain ⟨amplitude, hinterval, heval⟩ :=
    (dense_polynomial_nonzero p hp).inter_open_nonempty
      (Set.Ioo 0 radius) isOpen_Ioo
      ⟨radius / 2, half_pos hradius, half_lt_self hradius⟩
  exact ⟨amplitude, hinterval.1, hinterval.2, heval⟩

section TopologicalVectorSpace

variable {E : Type*} [AddCommGroup E] [Module ℝ E] [TopologicalSpace E]
  [ContinuousAdd E] [ContinuousSMul ℝ E]

/-- Each affine line from an arbitrary state toward the specified witness
has an ordinary, finite real polynomial as its restriction. -/
def PolynomialAlongLinesTo (f : E → ℝ) (witness : E) : Prop :=
  ∀ z : E, ∃ p : Polynomial ℝ,
    ∀ t : ℝ, f (z + t • (witness - z)) = p.eval t

/-- Line polynomiality and one nonzero value prove density. Continuity of
the scalar functional is only needed separately for openness. -/
theorem dense_nonzero_of_polynomialAlongLinesTo (f : E → ℝ) (witness : E)
    (hpolynomial : PolynomialAlongLinesTo f witness) (hwitness : f witness ≠ 0) :
    Dense {z : E | f z ≠ 0} := by
  intro z
  obtain ⟨p, hp⟩ := hpolynomial z
  have hpnonzero : p ≠ 0 := by
    intro hz
    have hone := hp 1
    simp only [one_smul, add_sub_cancel, hz, Polynomial.eval_zero] at hone
    exact hwitness hone
  let line : ℝ → E := fun t => z + t • (witness - z)
  have hline : Continuous line :=
    continuous_const.add (continuous_id.smul continuous_const)
  have hparameter := dense_polynomial_nonzero p hpnonzero
  have hclosure : line 0 ∈ closure (line '' {t : ℝ | p.eval t ≠ 0}) :=
    mem_closure_image hline.continuousAt (hparameter 0)
  have himage : line '' {t : ℝ | p.eval t ≠ 0} ⊆ {y : E | f y ≠ 0} := by
    rintro y ⟨t, ht, rfl⟩
    change f (z + t • (witness - z)) ≠ 0
    rw [hp t]
    exact ht
  have hz := closure_mono himage hclosure
  simpa [line] using hz

theorem openDense_nonzero_of_polynomialAlongLinesTo (f : E → ℝ) (witness : E)
    (hcontinuous : Continuous f)
    (hpolynomial : PolynomialAlongLinesTo f witness) (hwitness : f witness ≠ 0) :
    IsOpen {z : E | f z ≠ 0} ∧ Dense {z : E | f z ≠ 0} :=
  ⟨isOpen_ne.preimage hcontinuous,
    dense_nonzero_of_polynomialAlongLinesTo f witness hpolynomial hwitness⟩

/-- Countably many actual witness minors have a common dense residual
nonvanishing set, once the ambient space is Baire. -/
theorem dense_residual_nonzero_family [BaireSpace E]
    (minor : ℕ → E → ℝ) (witness : ℕ → E)
    (hcontinuous : ∀ n, Continuous (minor n))
    (hpolynomial : ∀ n, PolynomialAlongLinesTo (minor n) (witness n))
    (hwitness : ∀ n, minor n (witness n) ≠ 0) :
    Dense {z : E | ∀ n, minor n z ≠ 0} ∧
      {z : E | ∀ n, minor n z ≠ 0} ∈ residual E := by
  let S : ℕ → Set E := fun n => {z : E | minor n z ≠ 0}
  have ho : ∀ n, IsOpen (S n) := fun n =>
    (openDense_nonzero_of_polynomialAlongLinesTo (minor n) (witness n)
      (hcontinuous n) (hpolynomial n) (hwitness n)).1
  have hd : ∀ n, Dense (S n) := fun n =>
    (openDense_nonzero_of_polynomialAlongLinesTo (minor n) (witness n)
      (hcontinuous n) (hpolynomial n) (hwitness n)).2
  have hset : {z : E | ∀ n, minor n z ≠ 0} = ⋂ n, S n := by
    ext z
    simp [S]
  rw [hset]
  have hcommon : Dense (⋂ n, S n) := dense_iInter_of_isOpen ho hd
  exact ⟨hcommon, residual_of_dense_Gδ (IsGδ.iInter_of_isOpen ho) hcommon⟩

end TopologicalVectorSpace

#print axioms dense_nonzero_of_polynomialAlongLinesTo
#print axioms polynomial_nonzero_at_small_positive_amplitude
#print axioms dense_residual_nonzero_family

end DLWLean
