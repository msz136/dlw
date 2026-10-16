import StaticFactorVariation

namespace DLWLean
noncomputable section
open scoped BigOperators

variable {par : FieldParameters} {z : AmbientPeriodicPair par}
  {A : Type*} [Ring A] [Algebra ℝ A]

theorem staticTrace_scalar_left (base : AmbientSpectrumBase par z A)
    (a : PeriodicCoefficient par.Lx) (X : A) :
    base.tr.toLinearMap (base.model.coefficient a * X) =
      periodicCoefficientIntegral par.Lx (a * base.model.coefficients X (-1)) := by
  rw [base.trace_eq, base.model.scalar_left_coefficient]

def staticSiteTraceCotangent (base : AmbientSpectrumBase par z A)
    (Y : A) (j : Fin par.M) : FactorPeriodicPair par :=
  (fun i => if i = j then -base.model.coefficients
      (Y * (↑(base.factors.denominator j)⁻¹ : A)) (-1) else 0,
    fun i => if i = j then base.model.coefficients
      ((1 + base.factors.site j) * Y * (↑(base.factors.denominator j)⁻¹ : A)) (-1) else 0)

theorem staticSiteTraceCotangent_pairing (base : AmbientSpectrumBase par z A)
    (Y : A) (v : FactorPeriodicPair par) (j : Fin par.M) :
    factorPairing par (staticSiteTraceCotangent base Y j) v =
      base.tr.toLinearMap (Y * staticFactorVariation base v j) := by
  classical
  unfold factorPairing staticSiteTraceCotangent
  rw [Finset.sum_eq_single j]
  · simp only [Prod.fst, Prod.snd, ↓reduceIte]
    let Q : A := (↑(base.factors.denominator j)⁻¹ : A)
    let T : A := 1 + base.factors.site j
    let a := v.1 j
    let b := v.2 j
    change periodicCoefficientIntegral par.Lx
      (-base.model.coefficients (Y * Q) (-1) * a +
        base.model.coefficients (T * Y * Q) (-1) * b) =
      base.tr.toLinearMap (Y * (Q * base.model.coefficient b * T - Q * base.model.coefficient a))
    have ha : base.tr.toLinearMap (Y * (Q * base.model.coefficient a)) =
        periodicCoefficientIntegral par.Lx (a * base.model.coefficients (Y * Q) (-1)) := by
      rw [← mul_assoc, base.tr.cyclic, staticTrace_scalar_left]
    have hb : base.tr.toLinearMap (Y * (Q * base.model.coefficient b * T)) =
        periodicCoefficientIntegral par.Lx (b * base.model.coefficients (T * Y * Q) (-1)) := by
      calc
        _ = base.tr.toLinearMap (T * (Y * Q * base.model.coefficient b)) := by
          rw [← mul_assoc Y, ← mul_assoc Y, base.tr.cyclic]
        _ = base.tr.toLinearMap (base.model.coefficient b * (T * Y * Q)) := by
          rw [← mul_assoc, ← mul_assoc, base.tr.cyclic]
        _ = _ := staticTrace_scalar_left base _ _
    rw [mul_sub, map_sub, hb, ha]
    rw [← map_sub]
    congr 1
    ring
  · intro i _ hi
    simp [hi]
  · simp

theorem staticFactorPairing_add_left (f g v : FactorPeriodicPair par) :
    factorPairing par (f + g) v = factorPairing par f v + factorPairing par g v := by
  unfold factorPairing
  simp only [Prod.fst_add, Prod.snd_add, Pi.add_apply, add_mul]
  rw [← map_add, ← Finset.sum_add_distrib]
  congr 1
  apply Finset.sum_congr rfl
  intro j _
  ring

theorem staticFactorPairing_zero_left (v : FactorPeriodicPair par) :
    factorPairing par 0 v = 0 := by
  simp [factorPairing]

/-- Cotangents are computed by the literal finite product rule. -/
def staticFactorTraceCotangentPartial (base : AmbientSpectrumBase par z A) :
    ℕ → A → FactorPeriodicPair par
  | 0, _ => 0
  | n + 1, X =>
      (if hn : n < par.M then
        staticSiteTraceCotangent base (base.factors.monodromy n * X) ⟨n, hn⟩
      else 0) +
      staticFactorTraceCotangentPartial base n (X * (1 + base.factors.siteNat n))

theorem staticFactorTraceCotangentPartial_pairing (base : AmbientSpectrumBase par z A)
    (n : ℕ) (X : A) (v : FactorPeriodicPair par) :
    factorPairing par (staticFactorTraceCotangentPartial base n X) v =
      base.tr.toLinearMap (X * staticMonodromyVariation base v n) := by
  induction n generalizing X with
  | zero => simp [staticFactorTraceCotangentPartial, staticMonodromyVariation,
      staticFactorPairing_zero_left]
  | succ n ih =>
    rw [staticFactorTraceCotangentPartial, staticFactorPairing_add_left, ih,
      staticMonodromyVariation]
    rw [mul_add X (staticFactorVariationNat base v n * base.factors.monodromy n)
      ((1 + base.factors.siteNat n) * staticMonodromyVariation base v n), map_add]
    congr 1
    · unfold staticFactorVariationNat
      split_ifs with hn
      · rw [staticSiteTraceCotangent_pairing]
        rw [mul_assoc, base.tr.cyclic, mul_assoc]
      · simp [staticFactorPairing_zero_left]
    · rw [mul_assoc]

def staticFactorTraceCotangent (base : AmbientSpectrumBase par z A) (X : A) :
    FactorPeriodicPair par := staticFactorTraceCotangentPartial base par.M X

theorem staticFactorTraceCotangent_pairing (base : AmbientSpectrumBase par z A)
    (X : A) (v : FactorPeriodicPair par) :
    factorPairing par (staticFactorTraceCotangent base X) v =
      base.tr.toLinearMap (X * staticMonodromyVariation base v par.M) :=
  staticFactorTraceCotangentPartial_pairing base par.M X v

#print axioms staticSiteTraceCotangent_pairing
#print axioms staticFactorTraceCotangent_pairing
end
end DLWLean
