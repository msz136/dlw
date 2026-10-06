"""Correct only descriptive regularity metadata; never writes a proof file."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
SCOPE = "本次 Lean 验证采用实值、全局实解析且严格为正的 F、G，并假设 h≠0。"
MEANING = (
    "For each lattice index j, SmoothL requires joint real analyticity in (x,t): "
    "in this Mathlib version ContDiff ℝ ⊤ uses the ω order of WithTop ℕ∞."
)

manifest = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
for case in manifest["cases"]:
    for source in case["sources"]:
        assert hashlib.sha256(Path(source["path"]).read_bytes()).hexdigest() == source["sha256"]
    case["scopeText"] = SCOPE
    case["regularityMeaning"] = MEANING
(HERE / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

validation = json.loads((HERE / "validation.json").read_text(encoding="utf-8"))
validation["scopeText"] = SCOPE
validation["regularityMeaning"] = MEANING
(HERE / "validation.json").write_text(json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

review = json.loads((HERE / "review.json").read_text(encoding="utf-8"))
review["checked"]["formalScope"] = (
    "Real-valued F and G, globally jointly real analytic in (x,t) for each j, "
    "strictly positive; h != 0; forward implications only."
)
review["checked"]["regularityMeaning"] = MEANING
finding = {
    "severity": "material",
    "issue": "Earlier scope wording and review read bare ContDiff ℝ ⊤ as ordinary C∞; current Mathlib order is WithTop ℕ∞ and bare top is ω.",
    "resolution": "Scope wording corrected to global joint real analyticity in manifest, builder, README, validation and review metadata. No proof contents or hashes changed.",
    "sourceEvidence": [{
        "path": str(HERE.parents[2] / "_lean_shared" / "mathlib" / "Mathlib" / "Analysis" / "Calculus" / "ContDiff" / "Defs.lean"),
        "lines": [91, 1068, 1196, 1197, 1198],
    }],
}
review["resolvedFindings"] = [item for item in review["resolvedFindings"]
                              if not item["issue"].startswith("Earlier scope wording and review read bare ContDiff")]
review["resolvedFindings"].append(finding)
(HERE / "review.json").write_text(json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"scopeText": SCOPE, "proofHashesUnchanged": True, "metadataStable": True}, ensure_ascii=True, indent=2))
