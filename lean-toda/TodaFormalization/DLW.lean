/-
Copyright: formal companion to the GSG/DLW semi-discretization project.

# One entry point for the whole DLW formalization

`dsh`-sanctioned check:

```
& 'C:\Users\msz\学术内容\_lean_shared\Check-Lean.ps1' `
  -Root 'C:\Users\msz\学术内容\lean-toda' `
  -File 'C:\Users\msz\学术内容\lean-toda\TodaFormalization\DLW.lean'
```

This module pulls in every DLW file, so a single run covers the whole development, and
ends with a `#print axioms` audit of the main results.

## Layout

* `TodaFormalization/DLWDiscretePair.lean` — the **discrete** layer (pure algebra):
  the staggered bilinear pair `(6)_h`, `(7)_h`, the forced offsets `a ∓ h/2`, the
  elementwise spectral/lattice identity, the all-`N` determinant lift (T2), the
  rate-blindness and rate-sensitivity lemmas, and the exact jet expansions.
* `TodaFormalization/DLWContinuum.lean` — the **analytic** (T1) layer: the Taylor bridges
  (third and fourth order) and the three template reductions
  `½[(6)_h+(7)_h] = M₀ + (h²/8)(P''+4Q') + O(h⁴)`,
  `[(6)_h-(7)_h]/h = M₁ + O(h²)` (class `C⁴`), and its sharp form
  `[(6)_h-(7)_h]/h = M₁ + (h²/24)(P'''+6Q'') + O(h⁴)` (class `C⁵` for `P`).
* `TodaFormalization/DLWContinuumRate.lean` — the `y`-rate: `(1/h)·log χ → 1/P`, plus the
  exact centred-rate identity.
* `TodaFormalization/DLWSemidiscrete.lean`, `DLWOneSoliton.lean`, `DLWStaggered.lean` —
  the earlier exploratory checkpoints (route-A / one-soliton / staggered), kept for the
  record; they are superseded by the three files above.
-/
import TodaFormalization.DLWDiscretePair
import TodaFormalization.DLWContinuum
import TodaFormalization.DLWContinuumRate
import TodaFormalization.DLWSemidiscrete
import TodaFormalization.DLWOneSoliton
import TodaFormalization.DLWStaggered

/-! ## Axiom audit

Every `#print axioms` below must report only Lean's three standard axioms
(`propext`, `Classical.choice`, `Quot.sound`) — in particular **no** `sorryAx`, which is
how a `sorry`/`admit` would show up. -/

-- discrete layer: the pair, the forced offsets, and the shared `τ`
#print axioms DLW.discretePair_iff_centred
#print axioms DLW.offsets_are_a_cell
#print axioms DLW.staggered_entry_identity
#print axioms DLW.tau1_det_staggered
#print axioms DLW.tau1_det_staggered_two
#print axioms DLW.T2_discrete_pair_exact

-- discrete layer: rate-blindness / rate-sensitivity and the exact jet expansions
#print axioms DLW.lemmaA_vanishes
#print axioms DLW.propC_continuum_rate
#print axioms DLW.symmetric_expansion_general
#print axioms DLW.antisymmetric_expansion_general
#print axioms DLW.six_iff_M1
#print axioms DLW.latticeMult_factorizes

-- analytic (T1) layer
#print axioms DLW.taylor_jet3_isBigO
#print axioms DLW.taylor_jet4_isBigO
#print axioms DLW.symmetric_remainder_isBigO
#print axioms DLW.antisymmetric_remainder_isBigO
#print axioms DLW.antisymmetric_remainder_isBigO4
#print axioms DLW.div_id_of_isBigO_pow

-- the `y`-rate
#print axioms DLW.lattice_rate_tendsto
#print axioms DLW.lattice_rate_centred_exact
#print axioms DLW.lattice_rate_centred_exact_h
