"""Capture exact, unchanged Lean modules and display excerpts for Report.html."""
from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parents[2]
ORIGINAL = WORKSPACE / "Workspaces" / "lean_contracts" / "proofs"
PROOFS = HERE / "proofs"
PROOFS.mkdir(parents=True, exist_ok=True)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def closure(module):
    seen = {}

    def visit(name):
        source = ORIGINAL.joinpath(*name.split(".")).with_suffix(".lean")
        if name in seen or not source.is_file():
            return
        seen[name] = source
        text = source.read_text(encoding="utf-8-sig")
        for imports in re.findall(r"^import\s+([^\n]+)", text, re.M):
            for dependency in imports.split():
                visit(dependency)

    visit(module)
    return seen


def section(text, start, end):
    return text[text.index(start):text.index(end)].strip()


def example_call(theorem_source, declaration, arguments):
    header = theorem_source[theorem_source.index("theorem "):].split(":=", 1)[0].rstrip()
    header = header.replace("theorem " + declaration, "example", 1)
    return header + " :=\n  " + declaration + " " + arguments


contracts = (ORIGINAL / "Contracts.lean").read_text(encoding="utf-8-sig")
report_source = (WORKSPACE / "Workspaces" / "gsg_project" / "dlw_report" / "_src" / "Report.md").read_text(encoding="utf-8-sig")


def display_formula(number):
    matches = [block for block in re.findall(r"\$\$[\s\S]*?\$\$", report_source)
               if "\\tag{" + str(number) + "}" in block]
    if len(matches) != 1:
        raise ValueError("Expected exactly one original Report formula " + str(number))
    return matches[0]


start_lean = "\n\n".join([
    section(contracts, "abbrev XT", "def sx"),
    section(contracts, "def SmoothXT", "def Positive3"),
    section(contracts, "def hx", "def cbil"),
    section(contracts, "def SemiPair", "def dm"),
])
operators_lean = section(contracts, "def dm", "def W")
start_latex = display_formula(1)
scope = "本次 Lean 验证采用实值、全局实解析且严格为正的 F、G，并假设 h≠0。"

uw = (ORIGINAL / "ReportNonlinearUW.lean").read_text(encoding="utf-8-sig")
qrm = (ORIGINAL / "ReportNonlinearQRM.lean").read_text(encoding="utf-8-sig")
uw_definitions = section(uw, "/-- Report (4)", "lemma smooth_logL")
uw_theorem = section(uw, "/-- Equation (1) implies BOTH", "/-- Equation (1) also gives")
uw_physical = section(uw, "/-- Equation (1) also gives", "#print axioms physical_v")
qrm_definitions = section(qrm, "def potential", "lemma smooth_potential")
qrm_theorem = section(qrm, "/-- Both heat-type", "/-- All physical reconstruction")
qrm_reconstruction = section(qrm, "/-- All physical reconstruction", "#print axioms Q_residual_identity")

specs = [
    dict(id="uw", route="uw", title="两场形式：双线性方程 → 式（7）、（8）",
         module="ReportNonlinearUW", expectedAxiomDeclarations=[
             "DLWContract.ReportUW.semiPair_implies_report7",
             "DLWContract.ReportUW.semiPair_implies_report8"],
         namespace="DLWContract.ReportUW", definitionsLean=uw_definitions,
         endLean=uw_theorem, physicalLean=uw_physical,
         endpointLean=("open DLWContract DLWContract.ReportUW\n\n" +
                       example_call(uw_theorem, "semiPair_implies_report7",
                                    "a h F G hh hF hG hFp hGp hsp") + "\n\n" +
                       example_call(uw_physical, "semiPair_implies_report8",
                                    "a h F G hh hF hG hFp hGp hsp")),
         endLatex=display_formula(7) + "\n\n" + display_formula(8),
         variableLatex=(r"u_j=(2\log F_j-\log G_j-\log G_{j+1})_x,"
                        r"\quad\omega_j=(\log G_{j+1}-\log G_j)_x,"
                        r"\quad v_j=\frac4h\omega_j+\delta_0u_j.")),
    dict(id="qrm", route="qrm", title="比值形式：双线性方程 → 式（21）、（22）",
         module="ReportNonlinearQRM", expectedAxiomDeclarations=[
             "DLWContract.ReportQRM.semiPair_implies_report21",
             "DLWContract.ReportQRM.report22"],
         namespace="DLWContract.ReportQRM", definitionsLean=qrm_definitions,
         endLean=qrm_theorem, reconstructionLean=qrm_reconstruction,
         endpointLean=("open DLWContract DLWContract.ReportQRM\n\n" +
                       example_call(qrm_theorem, "semiPair_implies_report21",
                                    "a h F G hne hF hG hFp hGp hsp") + "\n\n" +
                       example_call(qrm_reconstruction, "report22",
                                    "h F G hne hF hG hFp hGp")),
         endLatex=display_formula(21) + "\n\n" + display_formula(22),
         variableLatex=(r"Q_j=\exp\!\left(\log F_j-\frac{\log G_j+\log G_{j+1}}2\right),"
                        r"\quad M_j=(\log G_j)_x,\quad R_j=\frac{1-\omega_j/h}{Q_j}.")),
]

cases = []
for spec in specs:
    module = spec["module"]
    copied_sources = []
    for name, source in closure(module).items():
        target = PROOFS.joinpath(*name.split(".")).with_suffix(".lean")
        target.parent.mkdir(parents=True, exist_ok=True)
        # Exact bytes, including line endings: compilation and display refer to this snapshot.
        target.write_bytes(source.read_bytes())
        copied_sources.append(dict(module=name, path=str(target), originalPath=str(source),
                                   sha256=sha(target), originalSha256=sha(source)))
    proof_target = PROOFS / (module + ".lean")
    example_module = "ExampleUW" if spec["id"] == "uw" else "ExampleQRM"
    target = PROOFS / (example_module + ".lean")
    example_code = ("import " + module + "\n\nnoncomputable section\n\n" +
                    spec["endpointLean"] + "\n\n" +
                    "\n".join("#print axioms " + name
                              for name in spec["expectedAxiomDeclarations"]) + "\n")
    target.write_text(example_code, encoding="utf-8")
    copied_sources.append(dict(module=example_module, path=str(target), originalPath=None,
                               sha256=sha(target), originalSha256=None,
                               generated=True, origin="displayed-example"))
    case = dict(spec, target=str(target), targetModule=example_module,
                proofValidationTarget=str(proof_target), root=str(PROOFS), sources=copied_sources,
                startLean=start_lean, operatorsLean=operators_lean, startLatex=start_latex,
                scopeText=scope, fullProofLean=proof_target.read_text(encoding="utf-8-sig"),
                regularityMeaning="For each lattice index j, SmoothL requires joint real analyticity in (x,t): in this Mathlib version ContDiff ℝ ⊤ uses the ω order of WithTop ℕ∞.",
                runnableEntryLean=example_code,
                endpointSourcePath=str(target),
                displayMode="readonly-exact-source",
                verificationDirectives="\n".join("#print axioms " + name
                    for name in spec["expectedAxiomDeclarations"]),
                proofDirection="forward",
                theoremAssumptions=["h ≠ 0", "SmoothL F", "SmoothL G", "PositiveL F",
                                    "PositiveL G", "SemiPair a h F G"],
                timeoutSeconds=900)
    cases.append(case)
    (HERE / (module + ".start.txt")).write_text(start_lean + "\n", encoding="utf-8")
    (HERE / (module + ".definitions.txt")).write_text(spec["definitionsLean"] + "\n", encoding="utf-8")
    (HERE / (module + ".endpoint.txt")).write_text(spec["endLean"] + "\n", encoding="utf-8")
    (HERE / (module + ".example.txt")).write_text(spec["endpointLean"] + "\n", encoding="utf-8")

manifest = dict(version=1, proofRoot=str(PROOFS), checker=str(WORKSPACE / "_lean_shared" / "check_lean.py"),
                pythonExe="C:\\Users\\msz\\AppData\\Local\\Programs\\Python\\Python313\\python.exe",
                allowedAxioms=["propext", "Classical.choice", "Quot.sound"], cases=cases,
                runtimeNote="Each Run compiles the complete local import closure and audits printed endpoint axioms.")
(HERE / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"manifest": str(HERE / "manifest.json"),
                  "cases": [{"id": case["id"], "moduleCount": len(case["sources"]),
                             "target": case["target"]} for case in cases]}, ensure_ascii=False, indent=2))
