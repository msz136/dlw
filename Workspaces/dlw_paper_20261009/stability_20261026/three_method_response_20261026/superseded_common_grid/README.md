# Superseded common-grid diagnostics

The user selected each method's own native-grid perturbed-minus-unperturbed response. These raw run files retain the earlier common-grid interpolation, cross-method discrepancy and agreement-window calculations solely for reproducibility. They are not used in the accepted figures, tables or manuscript interpretation.

The same raw runs also contain the original native histories. Those histories and native physical endpoints were exported without interpolation to `../native/` and independently audited. No numerical trajectory was altered or rerun to change the presentation scope.

The original executed solver remains `../run_comparison.py`; its name reflects the initial planning stage. `../export_native.py`, `../collect_native.py`, and `../audit/validate_native_outputs.py` describe the native-only publication pipeline.
