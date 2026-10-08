"""The notebook's local Lean import entry point."""
from pathlib import Path
import uuid

from lean_notebook import install_lean_magic

PROJECT = Path(__file__).resolve().parent
WORKSPACE = PROJECT.parents[1]
PROOFS = PROJECT.parent / "report_notebook_20261002" / "lean_material" / "proofs"


def load_lean():
    """Register the cell magic using installed Lean, Mathlib and cached proofs."""
    return install_lean_magic(
        PROOFS,
        workdir=PROJECT / "local_lean_runs" / uuid.uuid4().hex,
        runtime_config=WORKSPACE / "_lean_shared" / "runtime.json",
        allow_download=False,
        cache_dir=PROJECT / "proof_cache",
    )
