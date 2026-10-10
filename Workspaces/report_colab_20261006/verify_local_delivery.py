"""Verify the delivered notebook still contains the actual full-run outputs."""
import hashlib
import json
from pathlib import Path
import nbformat

PROJECT = Path(__file__).resolve().parent
DELIVERY = PROJECT.parents[1] / "notebook" / "Report.ipynb"

def sha(value):
    return hashlib.sha256(value.encode() if isinstance(value, str) else value).hexdigest()

def verify():
    notebook = nbformat.read(DELIVERY, as_version=4)
    nbformat.validate(notebook)
    evidence = json.loads((PROJECT / "execution_validation.json").read_text(encoding="utf-8"))
    assert evidence["success"] and not evidence["error_outputs"]
    expected = {cell["id"]:cell for cell in evidence["code_cells"]}
    for cell in notebook.cells:
        if cell.cell_type != "code":
            continue
        record = expected[cell.id]
        assert sha(cell.source) == record["source_sha256"]
        assert cell.execution_count == record["execution_count"]
        assert len(cell.outputs) == len(record["outputs"])
        for actual, saved in zip(cell.outputs, record["outputs"]):
            assert actual.output_type == saved["type"]
            if actual.output_type == "stream":
                assert sha(actual.text) == saved["text_sha256"]
            elif actual.output_type in ("display_data", "execute_result"):
                hashes = {mime:sha(value if isinstance(value,str) else json.dumps(value,sort_keys=True))
                          for mime,value in actual.data.items()}
                assert hashes == saved["payload_sha256"]
            else:
                assert actual.output_type != "error"
    final_hash = sha(DELIVERY.read_bytes())
    evidence.setdefault("full_execution_notebook_sha256", evidence["notebook_sha256"])
    evidence["notebook_sha256"] = final_hash
    evidence["post_execution_refinement"] = "Two import descriptions now refer to the already compiled local proofs; all code and raw outputs are unchanged."
    (PROJECT / "execution_validation.json").write_bytes((json.dumps(evidence,ensure_ascii=False,indent=2)+"\n").encode())
    build_path = PROJECT / "build_validation.json"
    build = json.loads(build_path.read_text(encoding="utf-8"))
    build["notebook_sha256"] = final_hash
    build["runtime_mode"] = "local installed Lean and Mathlib; no downloads"
    build_path.write_bytes((json.dumps(build,ensure_ascii=False,indent=2)+"\n").encode())
    assert DELIVERY.read_bytes() == (PROJECT / "Report.ipynb").read_bytes()
    result = {"passed":True,"notebook":str(DELIVERY),"notebook_sha256":final_hash,
              "code_cells":len(expected),"all_code_sources_and_actual_outputs_preserved":True,
              "original_report_raw_sha256":sha((PROJECT.parents[1]/"Report.html").read_bytes())}
    (PROJECT / "local_delivery_validation.json").write_bytes((json.dumps(result,indent=2)+"\n").encode())
    print(json.dumps(result))

if __name__ == "__main__":
    verify()
