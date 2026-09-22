import Mathlib.Basic.Complex.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.LinearCombination

/-!
# B-direction: exact dispersion of the y-spectral (Fourier) modal system

Setting: constant background `(u0, v0)`; perturbations `u = U e^{ikx+iℓy}`,
`w = W e^{ikx+iℓy}`, `v = V e^{ikx+iℓy}`; `c := u0 + 2a`, `β := v0 + 2λ`
(first-round convention λ = −2, so β = v0 − 4).

The y-spectral (Fourier) semidiscretization keeps modes |ℓ| ≤ N and replaces
∂_y by the **exact** multiplier iℓ. The linearized modal system at each
retained mode is (x-derivatives continuous, hence exact):

  W1 modal:  (s + i c k) W = k² V
  W2 modal:  (s + i c k) V + i k (β − k ℓ) U = 0
  constraint: W = iℓ U          (w = u_y, exact in y-spectral)

From these three exact algebraic facts we derive, **without dividing by k
or by ℓ**, the multiplied dispersion identity

  ℓ · (s + i c k)² = ℓ · k⁴ − β · k³ ,

which for ℓ ≠ 0 is exactly the continuous dispersion of the spec (M3):

  (s + i c k)² = k⁴ − β k³ / ℓ .

Consequence (the "spectral match"): for the y-only Fourier truncation the
discrete dispersion of every retained mode coincides with the continuous
one with **no N-dependent error**: y-truncation is spectrally exact.
The M4 obstruction (|s| ~ k² for |k| → ∞ at fixed ℓ ≠ 0) is therefore
present *exactly* in the truncated system as well — y-truncation alone
does not remove the continuous ill-posedness.

Everything is pure algebra in ℂ; no smoothness/convergence assumptions.
-/

namespace DLWBSpec

/-- Modal equation 1 (from W1) at spectral mode (k, ℓ), constant background:
    (s + i(u0+2a)k) W = k² V. -/
def ModalEq1 (s k c W V : ℂ) : Prop := (s + Complex.I * (c*k)) * W = k^2 * V

/-- Modal equation 2 (from W2) at spectral mode (k, ℓ), constant background:
    (s + i c k) V + i k (β − kℓ) U = 0, β = v0 + 2λ. -/
def ModalEq2 (s k c β : ℂ) (ℓ : ℤ) (V U : ℂ) : Prop :=
  (s + Complex.I * (c*k)) * V + Complex.I * k * (β - k*(ℓ : ℂ)) * U = 0

/-- **Dispersion identity (multiplied form, no division at all).** -/
theorem dispersion_mult {s k c β U V W : ℂ} {ℓ : ℤ}
    (h1 : ModalEq1 s k c W V)
    (h2 : ModalEq2 s k c β ℓ V U)
    (h3 : W = Complex.I * (ℓ : ℂ) * U)
    (hU : U ≠ 0) :
    (ℓ : ℂ) * (s + Complex.I * (c*k))^2 = k^4 * (ℓ : ℂ) - β * k^3 := by
  have h1' : (s + Complex.I * (c*k)) * (Complex.I * (ℓ : ℂ) * U) = k^2 * V := by
    rw [← h1, h3]
  have hA : (s + Complex.I * (c*k))^2 * (Complex.I * (ℓ : ℂ) * U)
      + Complex.I * k^3 * (β - k*(ℓ : ℂ)) * U = 0 := by
    have h5 : k^2 * ((s + Complex.I * (c*k)) * V
        + Complex.I * k * (β - k*(ℓ : ℂ)) * U) = 0 := by
      rw [h2, mul_zero]
    rw [mul_add] at h5
    have e2 : k^2 * ((s + Complex.I * (c*k)) * V)
        = (s + Complex.I * (c*k)) * (k^2 * V) := by ring
    rw [e2, ← h1, h3] at h5
    linear_combination h5
  have hfac : Complex.I * U * ((ℓ : ℂ) * (s + Complex.I * (c*k))^2
      + k^3 * (β - k*(ℓ : ℂ))) = 0 := by
    linear_combination hA
  rw [mul_assoc, mul_eq_zero, or_iff_right Complex.I_ne_zero,
    mul_eq_zero, or_iff_right hU] at hfac
  linear_combination hfac

/-- Nontriviality: for `k ≠ 0`, `U = 0` forces `V = 0` (so a nontrivial
mode always has `U ≠ 0`, as used above). -/
theorem V_eq_zero_of_U_eq_zero {s k c β U V W : ℂ} {ℓ : ℤ}
    (h1 : ModalEq1 s k c W V) (h3 : W = Complex.I * (ℓ : ℂ) * U)
    (hU : U = 0) (hk : k ≠ 0) : V = 0 := by
  have h2 : k^2 * V = 0 := by
    rw [← h1, h3, hU, mul_zero, mul_zero]
  rw [mul_eq_zero, or_iff_right (pow_ne_zero 2 hk)] at h2
  exact h2

/-- **Standard (divided) dispersion form**, exactly the continuous M3
dispersion — the precise "spectral in y" match statement. -/
theorem dispersion_div {s k c β U V W : ℂ} {ℓ : ℤ}
    (hℓ : (ℓ : ℂ) ≠ 0)
    (h1 : ModalEq1 s k c W V)
    (h2 : ModalEq2 s k c β ℓ V U)
    (h3 : W = Complex.I * (ℓ : ℂ) * U)
    (hU : U ≠ 0) :
    (s + Complex.I * (c*k))^2 = k^4 - β * k^3 / (ℓ : ℂ) := by
  have h := dispersion_mult h1 h2 h3 hU
  have key : (k^4 - β * k^3 / (ℓ:ℂ)) * (ℓ:ℂ) = k^4 * (ℓ:ℂ) - β * k^3 := by
    field_simp [hℓ]
  exact mul_right_cancel₀ hℓ (by
    rw [key, mul_comm ((s + Complex.I * (c*k))^2) (ℓ:ℂ)]
    exact h)

end DLWBSpec
