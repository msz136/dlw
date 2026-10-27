"""Preserve superseded common-grid diagnostics after native-only export/audit."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ARCHIVE=HERE/'superseded_common_grid';ARCHIVE.mkdir(exist_ok=True)
CASES=['A','D','Gaussian','Sinusoidal']
audit=json.loads((HERE/'audit/native_output_validation.json').read_text(encoding='utf-8'))
for case in CASES:
    for name in [case+'.json',case+'.npz',case+'_history.csv']:
        src=(HERE/name).resolve();dst=(ARCHIVE/name).resolve()
        assert src.is_relative_to(HERE.resolve()) and dst.is_relative_to(HERE.resolve())
        if src.exists():
            assert not dst.exists(),dst
            src.rename(dst)
    native=HERE/'native'/(case+'.json')
    rec=json.loads(native.read_text(encoding='utf-8'))
    rec['source_experiment']=str(ARCHIVE/(case+'.json'))
    rec['superseded_source_scope']='Raw run retained for provenance; common-grid comparison and agreement-window metrics are excluded from publication.'
    native.write_text(json.dumps(rec,indent=2),encoding='utf-8')
(ARCHIVE/'README.md').write_text('''# Superseded common-grid diagnostics

The user selected each method's own native-grid perturbed-minus-unperturbed response. These raw run files retain the earlier common-grid interpolation, cross-method discrepancy and agreement-window calculations solely for reproducibility. They are not used in the accepted figures, tables or manuscript interpretation.

The same raw runs also contain the original native histories. Those histories and native physical endpoints were exported without interpolation to `../native/` and independently audited. No numerical trajectory was altered or rerun to change the presentation scope.

The original executed solver remains `../run_comparison.py`; its name reflects the initial planning stage. `../export_native.py`, `../collect_native.py`, and `../audit/validate_native_outputs.py` describe the native-only publication pipeline.
''',encoding='utf-8')
print('Preserved raw outputs in superseded_common_grid; native provenance links updated.')
