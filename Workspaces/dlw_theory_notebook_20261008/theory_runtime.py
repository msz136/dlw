"""DLW theory routes using the existing source-and-artifact audited Lean runner."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'Workspaces/report_colab_20261006'))
import lean_notebook as runner

def load_theory():
    for route in ('continuous','walls','interaction','gram','regular','limit','solutionlimit'):
        runner.MODULES[route]={stage:'Theory'+route.title()+stage.title() for stage in runner.STAGES}
    return runner.install_lean_magic(
        HERE/'proofs',runtime_config=ROOT/'_lean_shared/runtime.json',
        cache_dir=ROOT/'Workspaces/report_colab_20261006/proof_cache',
        seed_runs=[ROOT/'Workspaces/lean_contracts/proofs/.lean-runs',
                   ROOT/'Workspaces/report_colab_20261006/local_lean_runs'])
