import AmbientEulerVariational
import BalancedRealization

/-!
Finite differential-polynomial normal coefficients on the entire closed
physical field space. Both coordinates are projected algebraically before
forming U and w. In particular g=hw/4 is a variable coefficient on the
right of the resolvent; all of its spatial derivatives enter the literal
normal product. Evaluation uses the actual smooth periodic field jets.
-/
namespace DLWLean.AmbientPDO
noncomputable section
open scoped BigOperators ContDiff

abbrev Poly (par : FieldParameters) := MvPolynomial (AmbientJetIndex par) ℝ

def generatorDerivative (par : FieldParameters) (i : AmbientJetIndex par) : Poly par :=
  MvPolynomial.X (i.1, i.2.1, i.2.2 + 1)

def spatialDerivative (par : FieldParameters) : Derivation ℝ (Poly par) (Poly par) :=
  MvPolynomial.mkDerivation ℝ (generatorDerivative par)

def spatialEvolution (par : FieldParameters) : AlgebraEvolution (Poly par) where
  toLinearMap :=
    { toFun := fun p => spatialDerivative par p
      map_add' := (spatialDerivative par).map_add
      map_smul' := (spatialDerivative par).map_smul }
  leibniz p q := by
    change spatialDerivative par (p * q) =
      spatialDerivative par p * q + p * spatialDerivative par q
    simpa only [Algebra.smul_def, Algebra.algebraMap_self, RingHom.id_apply,
      smul_eq_mul, add_comm, mul_comm] using (spatialDerivative par).leibniz p q

def evaluation (par : FieldParameters) (z : AmbientPeriodicPair par) :
    Poly par →ₐ[ℝ] PeriodicCoefficient par.Lx :=
  MvPolynomial.aeval (fun i => ambientJet par i z)

theorem evaluation_C (par : FieldParameters) (z : AmbientPeriodicPair par) (r : ℝ) :
    evaluation par z (MvPolynomial.C r) = algebraMap ℝ (PeriodicCoefficient par.Lx) r :=
  (evaluation par z).commutes r

theorem evaluation_X (par : FieldParameters) (z : AmbientPeriodicPair par)
    (i : AmbientJetIndex par) : evaluation par z (MvPolynomial.X i) = ambientJet par i z := by
  simp [evaluation]

theorem evaluation_derivative (par : FieldParameters) (z : AmbientPeriodicPair par)
    (p : Poly par) : evaluation par z (spatialDerivative par p) =
      (periodicSpatialEvolution par.Lx).toLinearMap (evaluation par z p) := by
  induction p using MvPolynomial.induction_on with
  | C r =>
    rw [MvPolynomial.derivation_C, map_zero, evaluation_C]
    apply Subtype.ext
    funext x
    change 0 = deriv (fun _ : ℝ => r) x
    simp
  | add p q hp hq =>
    simp only [map_add, hp, hq]
  | mul_X p i hp =>
    rw [Derivation.leibniz]
    simp only [Algebra.smul_def, Algebra.algebraMap_self, RingHom.id_apply,
      map_add, map_mul, evaluation_X, hp,
      (periodicSpatialEvolution par.Lx).leibniz]
    have hXi : spatialDerivative par (MvPolynomial.X i) = generatorDerivative par i :=
      MvPolynomial.mkDerivation_X ℝ (generatorDerivative par) i
    rw [hXi]
    simp only [generatorDerivative, evaluation_X]
    have hi : ambientJet par (i.1, i.2.1, i.2.2 + 1) z =
        (periodicSpatialEvolution par.Lx).toLinearMap (ambientJet par i z) := rfl
    rw [hi]
    ring

theorem evaluation_iterate (par : FieldParameters) (z : AmbientPeriodicPair par)
    (k : ℕ) (p : Poly par) :
    evaluation par z ((spatialDerivative par)^[k] p) =
      ((periodicSpatialEvolution par.Lx).toLinearMap)^[k] (evaluation par z p) := by
  induction k with
  | zero => rfl
  | succ k ih =>
    rw [Function.iterate_succ_apply', evaluation_derivative,
      Function.iterate_succ_apply', ih]

def projectedJet (par : FieldParameters) (component : Bool) (j : Fin par.M) (k : ℕ) :
    Poly par :=
  MvPolynomial.X (component, j, k) -
    MvPolynomial.C (par.M : ℝ)⁻¹ * ∑ i : Fin par.M, MvPolynomial.X (component, i, k)

theorem projectedJet_sum (par : FieldParameters) (component : Bool) (k : ℕ) :
    (∑ j, projectedJet par component j k) = 0 := by
  have hM : (par.M : ℝ) ≠ 0 := by exact_mod_cast par.M_ne_zero
  have hcast : (par.M : Poly par) = MvPolynomial.C (par.M : ℝ) :=
    (map_natCast MvPolynomial.C par.M).symm
  simp only [projectedJet, Finset.sum_sub_distrib, Finset.sum_const, Finset.card_univ,
    Fintype.card_fin, nsmul_eq_mul, hcast]
  rw [← mul_assoc, ← map_mul, mul_inv_cancel₀ hM, map_one, one_mul, sub_self]

def s (par : FieldParameters) (j : Fin par.M) : Poly par := projectedJet par false j 0
def U (par : FieldParameters) (j : Fin par.M) : Poly par := MvPolynomial.X (true, j, 0)
def w (par : FieldParameters) (j : Fin par.M) : Poly par := MvPolynomial.C par.c + s par j
def g (par : FieldParameters) (j : Fin par.M) : Poly par :=
  MvPolynomial.C (par.h / 4) * w par j
def beta (par : FieldParameters) (j : Fin par.M) : Poly par :=
  MvPolynomial.C (1 / 2 : ℝ) * (U par j - g par j)

theorem g_sum (par : FieldParameters) : (∑ j, g par j) = MvPolynomial.C par.G := by
  have hs : (∑ j, s par j) = 0 := projectedJet_sum par false 0
  have hcast : (par.M : Poly par) = MvPolynomial.C (par.M : ℝ) :=
    (map_natCast MvPolynomial.C par.M).symm
  simp only [g, w, ← Finset.mul_sum, Finset.sum_add_distrib, hs, add_zero,
    Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul,
    hcast, ← map_mul]
  congr 1
  unfold FieldParameters.G
  ring

/-- Literal finite normal product, including derivative corrections on
the right factor. -/
def normalProduct (par : FieldParameters) (leftOrder : ℤ)
    (a b : ℕ → Poly par) (k : ℕ) : Poly par :=
  normalProductCoefficient (spatialEvolution par) leftOrder a b k

theorem normalProduct_eval (par : FieldParameters) (z : AmbientPeriodicPair par)
    (leftOrder : ℤ) (a b : ℕ → Poly par) (k : ℕ) :
    evaluation par z (normalProduct par leftOrder a b k) =
      normalProductCoefficient (periodicSpatialEvolution par.Lx) leftOrder
        (fun r => evaluation par z (a r)) (fun r => evaluation par z (b r)) k := by
  classical
  unfold normalProduct normalProductCoefficient
  rw [map_sum]
  apply Finset.sum_congr rfl
  intro r _
  rw [map_sum]
  apply Finset.sum_congr rfl
  intro t _
  split_ifs
  · rw [map_mul, map_mul]
    simp only [AlgHom.commutes, spatialEvolution, LinearMap.coe_mk, AddHom.coe_mk]
    rw [evaluation_iterate]
  · rw [map_zero]

def resolventCoefficient (par : FieldParameters) (j : Fin par.M) : ℕ → Poly par
  | 0 => 1
  | k + 1 => beta par j * resolventCoefficient par j k -
      spatialDerivative par (resolventCoefficient par j k)

/-- Coefficients of -Q_j g_j, where Q_j=(D-beta_j)^-1. The variable g_j
is on the right; this finite product retains derivatives of g_j. -/
def siteCoefficient (par : FieldParameters) (j : Fin par.M) (k : ℕ) : Poly par :=
  -normalProduct par (-1) (resolventCoefficient par j)
    (fun r => if r = 0 then g par j else 0) k

def sites (par : FieldParameters) (j k : ℕ) : Poly par :=
  if hj : j < par.M then siteCoefficient par ⟨j, hj⟩ k else 0

/-- Coefficients of M_n-1 (order minus one). M_{n+1}=T_n M_n. -/
def monodromyDifferenceCoefficient (par : FieldParameters) : ℕ → ℕ → Poly par
  | 0, _ => 0
  | n + 1, 0 => sites par n 0 + monodromyDifferenceCoefficient par n 0
  | n + 1, k + 1 => sites par n (k + 1) + monodromyDifferenceCoefficient par n (k + 1) +
      normalProduct par (-1) (sites par n) (monodromyDifferenceCoefficient par n) k

def monodromyCoefficient (par : FieldParameters) (k : ℕ) : Poly par :=
  monodromyDifferenceCoefficient par par.M k

theorem siteCoefficient_leading (par : FieldParameters) (j : Fin par.M) :
    siteCoefficient par j 0 = -g par j := by
  simp [siteCoefficient, normalProduct, normalProductCoefficient, resolventCoefficient]

theorem monodromyDifference_leading (par : FieldParameters) (n : ℕ) :
    monodromyDifferenceCoefficient par n 0 = ∑ j ∈ Finset.range n, sites par j 0 := by
  induction n with
  | zero => simp [monodromyDifferenceCoefficient]
  | succ n ih => rw [monodromyDifferenceCoefficient, ih, Finset.sum_range_succ, add_comm]

theorem monodromyCoefficient_leading (par : FieldParameters) :
    monodromyCoefficient par 0 = MvPolynomial.C (-par.G) := by
  rw [monodromyCoefficient, monodromyDifference_leading, ← Fin.sum_univ_eq_sum_range]
  have hsite : ∀ j : Fin par.M, sites par j.val 0 = -g par j := by
    intro j
    simp only [sites, dite_true, j.isLt, siteCoefficient_leading]
  simp only [hsite, Finset.sum_neg_distrib, g_sum, map_neg]

/-- Inverting the order-minus-one monodromy difference divides only by
the fixed nonzero scalar -G. Every coefficient is a finite polynomial. -/
def inverseCoefficient (par : FieldParameters) : ℕ → Poly par
  | 0 => MvPolynomial.C (-par.G)⁻¹
  | n + 1 => MvPolynomial.C (-(-par.G)⁻¹) *
      ∑ t : Fin (n + 1), ∑ r : Fin (n + 2),
        if r.val + t.val ≤ n + 1 then
          MvPolynomial.C ((Ring.choose (-1 - (r.val : ℤ))
            (n + 1 - (r.val + t.val)) : ℤ) : ℝ) * monodromyCoefficient par r.val *
              (spatialDerivative par)^[n + 1 - (r.val + t.val)]
                (inverseCoefficient par t.val)
        else 0
termination_by k => k
decreasing_by exact t.isLt

def normalizedCoefficient (par : FieldParameters) (k : ℕ) : Poly par :=
  MvPolynomial.C (-par.G) * inverseCoefficient par k +
    if k = 1 then MvPolynomial.C (par.B - par.G / 2) else 0

theorem normalizedCoefficient_leading (par : FieldParameters) :
    normalizedCoefficient par 0 = 1 := by
  simp [normalizedCoefficient, inverseCoefficient, ← map_mul, par.G_ne_zero]

def powerCoefficient (par : FieldParameters) : ℕ → ℕ → Poly par
  | 0, k => if k = 0 then 1 else 0
  | n + 1, k => normalProduct par (n : ℤ) (powerCoefficient par n)
      (normalizedCoefficient par) k

def residuePolynomial (par : FieldParameters) (n : ℕ) : Poly par :=
  powerCoefficient par n (n + 1)

def spectralDensityPolynomial (par : FieldParameters) (n : ℕ) : Poly par :=
  MvPolynomial.C (n : ℝ)⁻¹ * residuePolynomial par n

def periodicDensityPolynomial (par : FieldParameters) (n : ℕ) :
    MvPolynomial (AmbientJetIndex par) (PeriodicCoefficient par.Lx) :=
  MvPolynomial.map (algebraMap ℝ (PeriodicCoefficient par.Lx))
    (spectralDensityPolynomial par n)

def constructedCharge (par : FieldParameters) (n : ℕ) (z : AmbientPeriodicPair par) : ℝ :=
  ambientPolynomialIntegral par (periodicDensityPolynomial par n) z

#print axioms evaluation_derivative
#print axioms monodromyCoefficient_leading
end
end DLWLean.AmbientPDO