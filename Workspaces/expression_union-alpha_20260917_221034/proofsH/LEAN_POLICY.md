# Lean proof policy (project-wide)

- Verification entry: `C:\Users\msz\学术内容\_lean_shared\Check-Lean.ps1` with `-Root <this dir>` and `-File <target>`.
- Mathlib v4.34.0 is available; import only needed modules (e.g. `Mathlib.Tactic.Ring`).
- `sorry`, `admit`, and new `axiom` are rejected by the entry.
- Add `#print axioms <theorem>` for key theorems; record the output in the report.
- PASSED means compile success only; evidence grading per `common/SPEC.md` still applies.