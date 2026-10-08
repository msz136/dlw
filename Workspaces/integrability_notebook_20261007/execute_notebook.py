"""Execute this report in the established local Python notebook kernel."""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
source = ROOT / "Workspaces" / "notebook_reports_20261006" / "execute_report.py"
spec = spec_from_file_location("verified_notebook_execution", source)
executor = module_from_spec(spec)
spec.loader.exec_module(executor)
executor.HERE = HERE

if __name__ == "__main__":
    executor.execute(HERE / "DLW刘维尔可积性report.ipynb", "integrability", timeout=600)
