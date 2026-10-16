"""Deterministically emit kernel-checked rational SAT proofs from the 37 certificate.

The Python output is untrusted proof text: Lean norm_num proves every condition.
No native_decide, external oracle, proof placeholder, or floating-point arithmetic.
"""
import hashlib
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "certificates" / "n37_rational_sat.json"
OUT = ROOT / "lean"


def rat(value):
    f = Fraction(value)
    if f.denominator == 1:
        return str(f.numerator) if f.numerator >= 0 else f"({f.numerator})"
    return f"({f.numerator} / {f.denominator})"


def write(name, lines):
    (OUT / name).write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    assert data["count"] == 37 and len(data["pairs"]) == 666
    normals = list(dict.fromkeys((p["nx"], p["ny"]) for p in data["pairs"]))
    ni = {n: k for k, n in enumerate(normals)}
    pairs = {(p["i"], p["j"]): p for p in data["pairs"]}
    assert set(pairs) == {(i, j) for i in range(37) for j in range(i + 1, 37)}
    header = ["import PackingGeometry", "import Mathlib.Tactic.FinCases", "import Mathlib.Data.Fin.VecNotation", "import Mathlib.Data.Fintype.Basic",
              "", "set_option maxRecDepth 10000", "set_option maxHeartbeats 0", "",
              "namespace Packing37", "open PackingGeometry", ""]
    lines = header[:]
    lines += [f"-- Certificate SHA256: {hashlib.sha256(SOURCE.read_bytes()).hexdigest()}",
              f"def side : ℚ := {rat(data['L'])}", ""]
    for s in data["squares"]:
        i = s["i"]
        lines += [f"def sq_{i} : QSquare := ⟨{', '.join(rat(s[k]) for k in ['cx','cy','ux','uy'])}⟩"]
    lines += ["", "def squares : Fin 37 → QSquare :=", "  ![" + ", ".join(f"sq_{i}" for i in range(37)) + "]", ""]
    for k, (nx, ny) in enumerate(normals):
        lines += [f"def normal_{k} : ℚ × ℚ := ({rat(nx)}, {rat(ny)})"]
    lines += ["", f"def normals : Fin {len(normals)} → ℚ × ℚ :=", "  ![" + ", ".join(f"normal_{k}" for k in range(len(normals))) + "]", ""]
    lines += [f"def normalIndices : Fin 37 → Fin 37 → Fin {len(normals)} :=", "  !["]
    for i in range(37):
        row = [str(ni[(pairs[i, j]['nx'], pairs[i, j]['ny'])]) if i < j else "0" for j in range(37)]
        lines += ["    ![" + ", ".join(row) + "]" + ("," if i < 36 else "")]
    lines += ["  ]", "", "def normal (i j : Fin 37) : ℚ × ℚ := normals (normalIndices i j)", "", "end Packing37"]
    write("CertificateData.lean", lines)
    header[0] = "import CertificateData"
    lines = header[:]
    for s in data["squares"]:
        i = s["i"]
        lines += [f"theorem unit_{i} : sq_{i}.unit := by", f"  norm_num [QSquare.unit, sq_{i}]", "",
                  f"theorem bounds_{i} : sq_{i}.bounds side := by", f"  norm_num [QSquare.bounds, sq_{i}, side]", ""]
    for label, predicate in [("all_unit", "(squares i).unit"), ("all_bounds", "(squares i).bounds side")]:
        lines += [f"theorem {label} : ∀ i, {predicate} := by", "  intro i", "  fin_cases i"]
        lines += [f"  · exact {'unit' if label == 'all_unit' else 'bounds'}_{i}" for i in range(37)]
        lines += [""]
    lines += ["end Packing37"]
    write("CertificateWalls.lean", lines)
    chunks = []
    for start in range(0, 37, 6):
        chunk = f"CertificatePairs{start // 6}"
        chunks.append(chunk)
        lines = header[:]
        for i in range(start, min(start + 6, 37)):
            for j in range(i + 1, 37):
                p = pairs[i, j]
                k = ni[p["nx"], p["ny"]]
                lines += [f"theorem sep_{i}_{j} : QStrictSeparated sq_{i} sq_{j} normal_{k}.1 normal_{k}.2 := by",
                          f"  norm_num [QStrictSeparated, qsupport, sq_{i}, sq_{j}, normal_{k}]", ""]
            lines += [f"theorem row_{i} : ∀ j : Fin 37, ({i} : Fin 37) < j →",
                      f"    QStrictSeparated (squares {i}) (squares j) (normal {i} j).1 (normal {i} j).2 := by",
                      "  intro j h", "  fin_cases j"]
            for j in range(37):
                lines += ["  · norm_num at h" if j <= i else f"  · exact sep_{i}_{j}"]
            lines += [""]
        lines += ["end Packing37"]
        write(chunk + ".lean", lines)
    lines = ["import CertificateWalls"] + [f"import {c}" for c in chunks]
    lines += ["", "namespace Packing37", "open PackingGeometry", "",
              "theorem all_strict_separated : ∀ i j : Fin 37, i < j →",
              "    QStrictSeparated (squares i) (squares j) (normal i j).1 (normal i j).2 := by",
              "  intro i j h", "  fin_cases i"]
    lines += [f"  · exact row_{i} j h" for i in range(37)]
    lines += ["", "theorem all_separated : ∀ i j : Fin 37, i < j →",
              "    QSeparated (squares i) (squares j) (normal i j).1 (normal i j).2 :=",
              "  fun i j h => (all_strict_separated i j h).weak", "",
              "theorem closed_disjoint : ∀ i j : Fin 37, i ≠ j → ∀ p : Point,",
              "    ¬ ((squares i).real.closed p ∧ (squares j).real.closed p) := by",
              "  intro i j hij p hp",
              "  rcases lt_or_gt_of_ne hij with h | h",
              "  · exact real_closed_separated (squares i) (squares j) _ _ (all_strict_separated i j h) p hp",
              "  · exact real_closed_separated (squares j) (squares i) _ _ (all_strict_separated j i h) p ⟨hp.2, hp.1⟩", "",
              "theorem certified_packing : IsPacking (side : ℝ) (fun i => (squares i).real) :=",
              "  packing_of_rational_certificate side squares normal all_unit all_bounds all_separated", "",
              "theorem exists_packing_37 : ∃ s : Fin 37 → Square,",
              f"    IsPacking ({rat(data['L'])} : ℝ) s := by",
              "  refine ⟨fun i => (squares i).real, ?_⟩",
              "  simpa [side] using certified_packing", "",
              "#print axioms all_unit", "#print axioms all_bounds", "#print axioms all_separated",
              "#print axioms closed_disjoint", "#print axioms certified_packing", "#print axioms exists_packing_37", "", "end Packing37"]
    write("Packing37.lean", lines)
    print(json.dumps({"source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(), "pair_count": len(pairs),
                      "normal_count": len(normals), "target": str(OUT / "Packing37.lean")}, indent=2))


if __name__ == "__main__":
    main()
