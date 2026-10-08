"""Reproduce the old initialized-then-reset state in a real notebook kernel."""
from pathlib import Path
import sys

import nbformat

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
sys.path.insert(0, str(PROJECT))
from execute_notebook import executor
executor.HERE = HERE


def main():
    report = nbformat.read(PROJECT / "DLW刘维尔可积性report.ipynb", 4)
    conditions = next(c.source for c in report.cells if c.id == "lean-conditions")
    project_path = repr(str(PROJECT))
    cells = [
        nbformat.v4.new_code_cell(f"""from pathlib import Path
import sys, types, importlib
project = Path({project_path})
sys.path.insert(0, str(project))
legacy = types.ModuleType('integrability_runtime')
legacy.__file__ = str(project / 'integrability_runtime.py')
sys.modules['integrability_runtime'] = legacy
exec((project / 'session_fix' / 'before' / 'integrability_runtime.py').read_text('utf-8'), legacy.__dict__)
legacy.load_lean()
first_session = _integrability_lean
""", id="legacy-prepare"),
        nbformat.v4.new_code_cell("%%lean library\nimport FinalEndpoint\n#check DLWLean.StartPoint\n", id="legacy-library"),
        nbformat.v4.new_code_cell("""legacy.load_lean()
assert _integrability_lean is not first_session
assert not _integrability_lean.library_ready
old_error = None
try:
    _integrability_lean.run_cell('conditions', 'import FinalEndpoint\n')
except Exception as exc:
    old_error = str(exc)
assert old_error == 'Run the Lean library import cell first.'
assert not _integrability_lean.history
patched = importlib.reload(legacy)
patched.load_lean()
fixed_session = _integrability_lean
patched.load_lean()
assert _integrability_lean is fixed_session
""".replace("'import FinalEndpoint\n'", "'import FinalEndpoint\\n'"), id="reproduce-reset-and-reload"),
        nbformat.v4.new_code_cell(conditions, id="conditions-without-library"),
        nbformat.v4.new_code_cell("""assert [h['cell'] for h in _integrability_lean.history] == ['conditions']
patched.load_lean()
assert _integrability_lean is fixed_session
get_ipython().register_magic_function(lambda line, cell: None, magic_kind='cell', magic_name='lean')
patched.load_lean()
assert get_ipython().find_cell_magic('lean').__self__ is fixed_session
""", id="repeat-prepare-and-magic-switch"),
        nbformat.v4.new_code_cell(conditions, id="conditions-after-repeat-prepare"),
        nbformat.v4.new_code_cell("""import json
assert [h['cell'] for h in _integrability_lean.history] == ['conditions', 'conditions']
assert all(h['passed'] and h['exit_code'] == 0 for h in _integrability_lean.history)
evidence = {'success': True, 'old_error_reproduced': old_error,
            'repeated_prepare_preserves_instance': True, 'other_magic_restored': True,
            'current_conditions_source_compiled_twice': True,
            'no_hidden_library_cell_or_previous_cell_execution': True,
            'history': str(_integrability_lean.workdir / 'history.json')}
(project / 'session_fix' / 'session_behavior_validation.json').write_text(
    json.dumps(evidence, ensure_ascii=False, indent=2) + '\\n', encoding='utf-8')
""", id="record-session-evidence"),
    ]
    nb = nbformat.v4.new_notebook(cells=cells, metadata=report.metadata)
    path = HERE / "session_regression.ipynb"
    nbformat.write(nb, path)
    executor.execute(path, "session_regression", timeout=600)


if __name__ == "__main__":
    main()
