import AmbientChartDerivative
import EulerVariationalGradient

namespace DLWLean
noncomputable section
open scoped BigOperators

/-- The Ward condition is the vanishing of the actual common-U first
variation; the gradient and its zero-sum consequence are constructed. -/
def AmbientCommonWard (par : FieldParameters)
    (p : MvPolynomial (AmbientJetIndex par) (PeriodicCoefficient par.Lx))
    (z : AmbientPeriodicPair par) : Prop :=
  ∀ a : PeriodicCoefficient par.Lx,
    ambientPolynomialIntegral par
      (ambientPolynomialVariation par ((fun _ => a), 0) p) z = 0

theorem ambientCommonWard_of_zero_derivatives (par : FieldParameters)
    (p : MvPolynomial (AmbientJetIndex par) (PeriodicCoefficient par.Lx))
    (z : AmbientPeriodicPair par)
    (hWard : ∀ a : PeriodicCoefficient par.Lx,
      HasDerivAt (fun t : ℝ => ambientPolynomialIntegral par p
        (z + t • ((fun _ => a), 0))) 0 0) : AmbientCommonWard par p z := by
  intro a
  exact (ambientPolynomialIntegral_hasDerivAt par p z ((fun _ => a), 0)).unique (hWard a)

theorem ambientEulerGradient_U_sum_zero (par : FieldParameters)
    (p : MvPolynomial (AmbientJetIndex par) (PeriodicCoefficient par.Lx))
    (z : AmbientPeriodicPair par) (hWard : AmbientCommonWard par p z) :
    (∑ j : Fin par.M, (ambientEulerGradient par p z).1 j) = 0 := by
  apply ambient_U_gradient_sum_zero_of_common_Ward par
    (ambientEulerGradient par p z).1 (ambientEulerGradient par p z).2
  intro a
  change ambientPairing par (ambientEulerGradient par p z) ((fun _ => a), 0) = 0
  rw [ambientEulerGradient_pairing]
  exact hWard a

def reducedAmbientEulerGradient (par : FieldParameters)
    (p : MvPolynomial (AmbientJetIndex par) (PeriodicCoefficient par.Lx))
    (z : AmbientPeriodicPair par) (hWard : AmbientCommonWard par p z) : ClosedPeriodicPair par :=
  reduceAmbientGradient par (ambientEulerGradient par p z).1
    (ambientEulerGradient par p z).2 (ambientEulerGradient_U_sum_zero par p z hWard)

/-- The constructed reduced Euler gradient is the actual derivative of
the original observable along every physical coordinate direction. -/
theorem reducedAmbientEulerGradient_hasDerivAt {par : FieldParameters}
    (p : MvPolynomial (AmbientJetIndex par) (PeriodicCoefficient par.Lx))
    (z : FieldCoordinates par) (hWard : AmbientCommonWard par p (coordinateAmbient z))
    (v : ClosedPeriodicPair par) :
    HasDerivAt (fun t : ℝ => ambientPolynomialIntegral par p (coordinateAmbient
      (closedPairCoordinates par ((z.closedP, z.closedS) + t • v))))
      (coefficientGradientPairing par
        (reducedAmbientEulerGradient par p (coordinateAmbient z) hWard) v) 0 := by
  have h := ambientPolynomialIntegral_hasDerivAt_coordinateLine p z v
  have hp := ambientVariationPairing_chart_reduction z v
    (ambientEulerGradient par p (coordinateAmbient z)).1
    (ambientEulerGradient par p (coordinateAmbient z)).2
    (ambientEulerGradient_U_sum_zero par p (coordinateAmbient z) hWard)
  change ambientPairing par (ambientEulerGradient par p (coordinateAmbient z))
      (coordinateAmbientTangent z v) =
    coefficientGradientPairing par
      (reducedAmbientEulerGradient par p (coordinateAmbient z) hWard) v at hp
  rw [hp] at h
  exact h

/-- The true reduced bracket of the constructed Euler gradients agrees
with the ambient constant bracket. -/
theorem reducedAmbientEulerGradient_bracket_eq (par : FieldParameters)
    (p q : MvPolynomial (AmbientJetIndex par) (PeriodicCoefficient par.Lx))
    (z : AmbientPeriodicPair par)
    (hp : AmbientCommonWard par p z) (hq : AmbientCommonWard par q z) :
    reducedBracketValue par (reducedAmbientEulerGradient par p z hp)
      (reducedAmbientEulerGradient par q z hq) =
    ambientConstantBracket par (ambientEulerGradient par p z).1
      (ambientEulerGradient par p z).2 (ambientEulerGradient par q z).1
      (ambientEulerGradient par q z).2 :=
  reducedBracketValue_eq_ambient_constant par _ _ _ _
    (ambientEulerGradient_U_sum_zero par p z hp) (ambientEulerGradient_U_sum_zero par q z hq)

#print axioms ambientEulerGradient_U_sum_zero
#print axioms reducedAmbientEulerGradient_hasDerivAt
#print axioms reducedAmbientEulerGradient_bracket_eq
end
end DLWLean
