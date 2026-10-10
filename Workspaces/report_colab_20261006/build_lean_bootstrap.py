"""Write the small import cell for the existing local Lean installation."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROOFS = HERE.parent / "report_notebook_20261002" / "lean_material" / "proofs"

bootstrap = '''# @title 载入本地 Lean 证明库
import sys
sys.path.insert(0, "C:/Users/msz/aca/Workspaces/report_colab_20261006")

from report_runtime import load_lean
lean_notebook_session = load_lean()
'''
(HERE / "bootstrap_source.txt").write_bytes(bootstrap.encode("utf-8"))
hashes = {str(source): hashlib.sha256(source.read_bytes()).hexdigest()
          for source in sorted(PROOFS.glob("*.lean"))}
manifest = {"mode": "existing-local-runtime", "automatic_download": False,
            "runtime_config": str(HERE.parents[1] / "_lean_shared" / "runtime.json"),
            "proof_sources": hashes,
            "helper_sha256": hashlib.sha256((HERE / "lean_notebook.py").read_bytes()).hexdigest(),
            "stage_sources_embedded": False, "proof_sources_embedded": False}
(HERE / "local_import_manifest.json").write_bytes(
    (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
print(f"Local import cell ready: {len(bootstrap.splitlines())} lines")
