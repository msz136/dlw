# Report notebook: Lean material

`manifest.json` is the integration contract. It contains exact source excerpts, two
fixed runnable entries, complete closure hashes, scope wording, and endpoint axiom
declarations. The page can display `startLean`, `endpointLean`, and the existing
LaTeX derivation. `definitionsLean` and `fullProofLean` can be folded. There are no
editable or arbitrary-source Lean service requests in this design.

## Fixed verification entries

| Route | Entry | Complete local closure | Verified mathematical endpoints |
| --- | --- | ---: | --- |
| `uw` | `proofs/ExampleUW.lean` | 5 modules | (1) ⇒ (7), (8) |
| `qrm` | `proofs/ExampleQRM.lean` | 8 modules | (1) ⇒ (21), plus reconstruction (22) |

The generated entries contain the exact `endpointLean` text. Their `example`
declarations call the pre-existing theorems with the complete original assumptions
and goals. Every Run recompiles their full original proof closure; it also typechecks
the displayed applications. The original modules are byte-for-byte snapshots under
`proofs/`, with source and snapshot SHA-256 hashes recorded. The generated wrappers
have `generated: true` and no original path; they have their own SHA-256 hashes.

The Lean scope is real-valued lattices jointly real analytic in (x,t) on the full
domain at each lattice index, strictly positive F and G, and h ≠ 0. In this Mathlib
version, the order type is `WithTop ℕ∞`; bare `ContDiff ℝ ⊤` is the ω analytic order,
not the ∞ smooth order. This follows from `ContDiff/Defs.lean` lines 91 and 1196–1198.
`SemiPair` is the original staggered bilinear pair. `deriv` is the real
Mathlib derivative, not a collection of independent formal jets. The Q field is an
actual exponential and R an actual quotient. These are forward implications; the
verification does not assert a global converse or a complex logarithm extension.

## Standard commands

Run the shared checker with only the fixed entry selected for the route:

```powershell
python 'C:\Users\msz\aca\_lean_shared\check_lean.py' `
  --root 'C:\Users\msz\aca\Workspaces\report_notebook_20261002\lean_material\proofs' `
  --file 'C:\Users\msz\aca\Workspaces\report_notebook_20261002\lean_material\proofs\ExampleUW.lean' `
  --timeout 900
```

For `qrm`, change only the final entry filename to `ExampleQRM.lean`. The service
must bind to loopback, verify all `sources` hashes, capture the new `.lean-runs`
record, require exit code 0 and `PASSED`, and audit each required `#print axioms`
line. Accept only `propext`, `Classical.choice`, and `Quot.sound`. The shared checker
rejects `sorry`, `admit`, and explicit `axiom` placeholders in the local closure.
The service should expose this fixed case selection, never an arbitrary command.

## Real verification records

Both original complete proof modules were checked before creating the displayed
application wrappers. `validation.json` preserves these actual records:

| Original entry | Modules | Sum of compiler time | Result |
| --- | ---: | ---: | --- |
| `ReportNonlinearUW.lean` | 4 | 88.616 s | PASSED |
| `ReportNonlinearQRM.lean` | 7 | 146.447 s | PASSED |

All four required endpoint axiom declarations report exactly the three standard
axioms above. Existing linter warnings are harmless and were preserved. These old
records are evidence of the source capture, not output for a new Run. The notebook
integration will test the application wrappers through the actual UI Run buttons.
After that, `audit_validation.py` can record the fresh wrapper compilation results.
Do not claim the wrappers have passed before that check completes.

`build_material.py` rebuilds material from the unchanged existing project files;
use it deliberately, since rebuilding after upstream changes refreshes the captured
hashes and requires rebuilding the HTML content and repeating verification.
