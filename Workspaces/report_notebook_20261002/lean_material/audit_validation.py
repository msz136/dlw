"""Record real checker results, proof assumptions, and endpoint axiom audits."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
manifest = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
records = []
for case in manifest["cases"]:
    results = []
    for path in Path(case["root"]).glob(".lean-runs/*/result.json"):
        result = json.loads(path.read_text(encoding="utf-8"))
        if result.get("target") == case["target"] and result.get("status") == "PASSED":
            results.append((path.stat().st_mtime, path, result))
    if not results:
        raise RuntimeError("No successful checker result for " + case["id"])
    _, result_path, result = max(results)
    log_path = result_path.parent / "build.log"
    log = log_path.read_text(encoding="utf-8")
    found = dict(re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", log))
    axioms = {}
    for declaration in case["expectedAxiomDeclarations"]:
        if declaration not in found:
            raise RuntimeError("Missing endpoint axiom audit: " + declaration)
        used = [name.strip() for name in found[declaration].split(",") if name.strip()]
        if set(used) - set(manifest["allowedAxioms"]):
            raise RuntimeError("Unexpected endpoint axioms: " + declaration)
        axioms[declaration] = used
    compiled = {str(Path(item["file"]).resolve()): item for item in result["files"]}
    for source in case["sources"]:
        path = Path(source["path"])
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != source["sha256"]:
            raise RuntimeError("Displayed proof source changed: " + str(path))
        checked = compiled.get(str(path.resolve()))
        if not checked or checked["sha256"] != digest or not checked["passed"]:
            raise RuntimeError("Proof closure was not completely checked: " + str(path))
    seconds = sum(item["seconds"] for item in result["files"])
    records.append(dict(id=case["id"], status="PASSED", checkedModules=len(result["files"]),
                        seconds=seconds, axioms=axioms, resultPath=str(result_path),
                        logPath=str(log_path), target=case["target"], root=case["root"],
                        command=[manifest["pythonExe"], manifest["checker"], "--root",
                                 case["root"], "--file", case["target"], "--timeout", "900"],
                        verifiedSourceHashes={source["module"]: source["sha256"]
                                              for source in case["sources"]}))

validation = dict(recordedAtUtc=datetime.now(timezone.utc).isoformat(),
                  toolchain="leanprover/lean4:v4.34.0", cases=records,
                  scopeText=manifest["cases"][0]["scopeText"],
                  noProofPlaceholders=True,
                  note="These are genuine compilation records. They are evidence of this capture, not substitutes for a fresh Run.")
(HERE / "validation.json").write_text(json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"validation": str(HERE / "validation.json"),
                  "cases": [{"id": record["id"], "seconds": record["seconds"],
                             "checkedModules": record["checkedModules"]} for record in records]},
                 ensure_ascii=False, indent=2))
