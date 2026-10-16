"""Compare the native printed 2HS norms with the original numerical results."""
import hashlib
import json
from pathlib import Path
import nbformat

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
PATH = ROOT / "notebook" / "2HS数值分析report.ipynb"
TARGETS = {
    "hs-error": {"Integrable": (0.010012749796509766, 0.0011496748742060303),
                 "FD": (9.399310918062342e-7, 3.046420677166317e-6)},
    "hs-two-error": {"Integrable": (0.03450850312633234, 0.003993212856966077),
                     "FD": (9.634527271124016e-7, 3.1699951051900044e-6)},
}


def verify():
    notebook = nbformat.read(PATH, 4)
    rows = []
    for cell in notebook.cells:
        if cell.id not in TARGETS:
            continue
        raw = "\n".join(output.text for output in cell.outputs if output.output_type == "stream")
        seen = set()
        for line in raw.splitlines():
            parts = line.split()
            if not parts or parts[0] not in TARGETS[cell.id]:
                continue
            seen.add(parts[0])
            values = [float(value) for value in parts[1:]]
            target = TARGETS[cell.id][parts[0]]
            differences = [abs(values[i]-target[i]) for i in range(2)]
            assert max(differences) < 2e-11
            if cell.id == "hs-error":
                assert values[2] > 0 and values[3] > 0
            rows.append({"cell": cell.id, "scheme": parts[0], "observed_printed_norms": values[:2],
                         "original_norms": target, "absolute_differences": differences})
        assert seen == set(TARGETS[cell.id])
    assert len(rows) == 4
    evidence = json.loads((HERE / "hs_two_reference_validation.json").read_text("utf-8"))
    assert evidence.get("success", evidence.get("passed", False)) or evidence.get("status") == "passed"
    validation = {"success": True, "notebook": str(PATH),
                  "notebook_sha256": hashlib.sha256(PATH.read_bytes()).hexdigest(),
                  "original_table_norms_checked": 8,
                  "maximum_absolute_difference": max(max(row["absolute_differences"]) for row in rows),
                  "norms": rows, "two_reference_validation": "hs_two_reference_validation.json",
                  "native_kernel_execution": "hs_execution_validation.json"}
    (HERE / "hs_numerical_validation.json").write_text(json.dumps(validation, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(validation, ensure_ascii=False, indent=2))
    return validation


if __name__ == "__main__":
    verify()
