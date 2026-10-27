"""Rerun the exact base bounds used by the Gaussian obstruction.

This invokes the existing interval bound and transform checks without
rewriting the older base certificate or regenerating point samples.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import sys

HERE=Path(__file__).resolve().parent
PROJECT=HERE.parents[2]
BASE=PROJECT/'reference_certificate_20261024/nondegenerate_benchmarks'
sys.path.insert(0,str(BASE))
spec=importlib.util.spec_from_file_location('dlw_current_base_check',BASE/'check.py')
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
old_certificate=(BASE/'certificate.json').read_bytes()
bounds=mod.uniform_bounds()
symbolic=mod.symbolic_laplace()
assert symbolic and (BASE/'certificate.json').read_bytes()==old_certificate
out=dict(date='2026-10-26',meaning='Independent rerun of the existing global denominator/truncation bounds and exact Laplace identities used by the new theorem',
         base_check_sha256=hashlib.sha256((BASE/'check.py').read_bytes()).hexdigest(),
         base_reference_sha256=hashlib.sha256((BASE/'reference.py').read_bytes()).hexdigest(),
         full_global_bound_function_rerun=True,exact_laplace_transform_identity_rerun=True,
         older_base_certificate_preserved=True,pointwise_evaluator_samples_rerun=False,
         bounds=bounds,actual_perturbed_reference_certified=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in out.items() if k!='bounds'},indent=2))
