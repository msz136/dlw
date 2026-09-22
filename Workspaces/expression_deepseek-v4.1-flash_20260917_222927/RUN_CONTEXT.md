# RUN CONTEXT

## Identity

| Field | Value |
| --- | --- |
| Run directory | `C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927` |
| `model_slug` | `deepseek-v4.1-flash` |
| Model-name source | Declared in the main agent's own system context ("powered by the `deepseek-v4.1-flash` model"). **Not** inferred from a filename or guessed. |
| Date of run | 2026-09-17, started 22:29:27 local (UTC+8) |
| Main agent role | task dispatch, mathematical review, Lean verification, integration, final recommendations |

`model_slug` was sanitised for the filesystem: no characters were replaced, as
`.` and `-` are legal in Windows path components.

## Environment (deployed, shared, do not rebuild)

| Field | Value |
| --- | --- |
| Lean | 4.34.0 (`leanprover/lean4:v4.34.0`) |
| Mathlib | v4.34.0, commit `5ed2965256430c3649e86755f9576b54eca72435` |
| Verification entry | `C:\Users\msz\学术内容\_lean_shared\Check-Lean.ps1` |
| Entry contract | return code `0` **and** `PASSED`; `sorry`/`admit`/new `axiom` rejected |
| Run artefacts | `<root>\.lean-runs\<run-id>\result.json` and `build.log` |
| Python | 3.13.3, SymPy 1.13.3 (`C:\Users\msz\AppData\Local\Programs\Python\Python313\python.exe`) |
| Node | v24.14.0 |
| `pdftotext` | MiKTeX `C:\Program Files\MiKTeX\miktex\bin\x64\pdftotext.exe` |
| No `AGENTS.md` | searched the whole workspace: none present |

Reference checkout `lean-toda` was inspected **read-only** and was **not**
modified. `_lean_shared` was inspected read-only and was not modified.

## Primary source

H.-H. Sheng, G.-F. Yu, *Physica D* **432** (2022) 133140,
DOI `10.1016/j.physd.2021.133140`.
Local: `PhysD-published.pdf`; independent extraction `pdftext/PhysD.txt`.
Secondary local source: `2 Huner Saxton.pdf` = A. Hori, Y. Tanaka, K. Maruno,
Y. Ohta, *An integrable semi-discretization of the two-component Hunter–Saxton
equation*, arXiv:2606.18701v2 (relevant prior art for directions G/H).
`hirota-book-new.pdf` = Hirota bilinear-method reference.

## Research hypotheses under test

1. Discretising **only** `y` can produce a locally closed nonlinear system whose
   continuum limit is (1)–(2).
2. Integrable / geometric structure (determinant tau family, conservation law,
   Hamiltonian or multisymplectic form) can survive `y`-discretisation.
3. A discrete variable transformation (VT) exists making the semi-discrete
   nonlinear form **local and closed**.
4. The continuous ill-posedness found in the constant-background linearisation
   (`|Re sigma| ~ k^2`, see `common/SHARED_MATH_SPEC.md` §2) can be evaded by a
   suitable discretisation.

Hypothesis 4 is expected to **fail**; it is recorded so the failure is documented
rather than assumed away.

## Main-agent verified results (before subagent dispatch)

All produced by `python -u common/MAIN_verify_core.py` and recorded in
`reports/MAIN_VERIFICATION.md`:

| ID | Result |
| --- | --- |
| V2 | `D_y(P f.g) = d_y(P f.g) - 2 P(f.g_y)` for constant-coefficient `P` |
| V3 | `(D_yB - 4D_x) f.g = -2[B f.g_y + 2 D_x f.g]` on `{B f.g = 0}`; hence the staggered continuum limit **is** the paper's system at `lam = -2` |
| V4 | Sheng–Yu `tau_n` solves (6),(7) and induces a solution of (1),(2), `N = 1,2,3` |
| V5 | exact `w = u_y` rewrite of both nonlinear equations |
| V6 | linearisation `[sigma + i(u0+2a)k]^2 = k^4 - (v0+2 lam) k^3/ell`; `|Re sigma| ~ k^2` |
| V7 | `v ≡ -2 lam`, `u = U(x,t)` arbitrary is an exact solution (zero mode) |
| V8 | staggered two-tau: all general-parameter two-soliton coefficients vanish |
| V9 | staggered tau family exact-rational `N = 1..5`, all coefficients vanish |
| V10 | `A_h`, `C_h` have no `h^1` term; formal second-order consistency |

Independent correction to the pre-existing workspace note: the naive step
`D_y B f.g = d_y(B f.g)` is **false**; the correct identity carries the extra
`-2 B(f.g_y)`. See `SHARED_MATH_SPEC.md` §3.2.

## Directory map

```
RUN_CONTEXT.md
common/           main-agent shared specification + main verification script
A_finite_difference/ .. H_toda_hierarchy/    one subagent directory each
proofs/           main-agent Lean root (Common/Operators.lean + probes)
lean/             main-agent Lean scratch (ApiProbe etc.)
experiments/      main-agent numerical / symbolic experiments
reports/          main-agent integration reports
pdftext/          independent PDF extractions
```

Isolation rule: each subagent writes **only** inside its own direction directory
(and its own `$proofRoot` there). The main agent owns `common/`, `proofs/`,
`reports/`, `experiments/`. No subagent may edit `common/SHARED_MATH_SPEC.md`.

## Reproduce (top level)

```powershell
cd 'C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927'
python -u common\MAIN_verify_core.py
& 'C:\Users\msz\学术内容\_lean_shared\Check-Lean.ps1' `
  -Root "$PWD\proofs" -File "$PWD\proofs\Common\Operators.lean" -TimeoutSeconds 300
```

See `reports/REPRODUCE.md` for the full per-direction procedure.
