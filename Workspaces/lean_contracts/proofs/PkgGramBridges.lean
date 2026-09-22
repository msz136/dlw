import Contracts
import PkgGramEntry
import PkgNonlinear
import Mathlib.Tactic

noncomputable section
namespace DLWContract

/-- The zero layer does not depend on the auxiliary parameter. -/
theorem gram_tau_zero_parameter {N : ℕ} (D : Data N) (h s r : ℝ) (j : ℤ) :
    tau D h s 0 j = tau D h r 0 j := by
  funext x t
  simp [tau, entry]

/-- Integration bridge only: C07 remains an explicit, unproved premise here. -/
theorem c08_of_c07 (h07 : C07) : C08 := by
  intro N D h hD j
  have hm : LayerOK D (D.a-h/2) := by
    constructor
    · intro i
      convert (hD.2.2.1 i).2 using 1 <;> ring
    · intro k
      convert (hD.2.2.2 k).1 using 1 <;> ring
  have hp : LayerOK D (D.a+h/2) := by
    constructor
    · intro i
      convert (hD.2.2.1 i).1 using 1 <;> ring
    · intro k
      convert (hD.2.2.2 k).2 using 1 <;> ring
  constructor
  · have H := h07 N D h (D.a-h/2) hD hm 0 j
    norm_num only [zero_add] at H
    rw [gram_tau_zero_parameter D h (D.a-h/2) D.a j] at H
    exact H
  · have H := h07 N D h (D.a+h/2) hD hp 0 (j+1)
    norm_num only [zero_add] at H
    rw [gram_tau_zero_parameter D h (D.a+h/2) D.a (j+1)] at H
    change bil (D.a+h/2) (tau D h (D.a-h/2) 1 j) (tau D h D.a 0 (j+1)) = 0
    rw [c05_proved N D h hD 1 j]
    exact H

/-- No assumption is hidden: full Gram nonlinear exactness needs C08 and C09. -/
theorem c16_of_c08_c09 (h08 : C08) (h09 : C09) : C16 := by
  intro N D h hD
  obtain ⟨hA,hF,hG,hsF,hsG⟩ := h09 N D h hD
  exact c15_proved D.a h (F D h) (G D h) hA.1 hsF hsG hF hG (h08 N D h hA)

end DLWContract
#print axioms DLWContract.c08_of_c07
#print axioms DLWContract.c16_of_c08_c09
