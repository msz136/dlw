"""Compare the preserved SD2/FD solvers with their production models."""
from pathlib import Path
import importlib.util
import hashlib
import json
import sys
from dlw_numeric_cells import CELLS

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ns = {}
for name in ('imports', 'config', 'reference', 'spatial', 'sd_fd', 'sd', 'fd', 'sd2_lift', 'sd2_evolution', 'mesh', 'time'):
    exec(CELLS[name], ns)
np = ns['np']
sys.path.insert(0, str(ROOT/'Workspaces/dlw_single_aligned_20260929'))
import experiment as original
import models
import reference
records = []
for case, case_old in (('A', 'fig1a'), ('B', 'fig1b'), ('C', 'fig3')):
    models.TwoExact = original.SingleExact if case in ('A', 'B') else reference.TwoExact
    for model in ('SD2', 'FD'):
        for mesh in ('fixed', 'moving'):
            s = dict(ns['CONFIG'], case=case_old, model=model, mesh=mesh)
            old = original.Problem(s)
            new = ns['Problem'](case, model, mesh)
            old_state, new_state = old.initial(), new.initial()
            initial_difference = float(abs(old_state-new_state).max())
            node_difference = float(abs(old.X.x-new.X.x).max())
            samples = []
            for perturb in (False, True):
                # Same deterministic perturbation tests the nonlinear formulas beyond the exact initial orbit.
                delta = 1e-8*np.sin(np.arange(len(old_state))) if perturb else np.zeros_like(old_state)
                delta[-old.X.n:] = 0
                a, b = old_state+delta, new_state+delta
                t = .0003 if perturb else 0.
                ou, nu = old.fields(a, t), new.fields(b, t)
                fields = max(float(abs(x-y).max()) for x, y in zip(ou, nu))
                of, nf = old.rhs(t, a), new.stage(t, b)
                rhs = float(abs(of-nf).max())
                scale = max(1., float(abs(of).max()))
                samples.append(dict(perturbation=perturb, field_difference=fields,
                                    rhs_difference=rhs, rhs_scaled_difference=rhs/scale))
            record = dict(case=case, model=model, mesh=mesh, initial_state_difference=initial_difference,
                          initial_node_difference=node_difference, samples=samples)
            records.append(record)
            print(case, model, mesh, max(r['rhs_difference'] for r in samples), flush=True)
            assert initial_difference < 1e-8 and node_difference < 1e-10
            assert all(r['field_difference'] < 1e-8 and r['rhs_scaled_difference'] < 1e-8 for r in samples)
source = HERE/'dlw_numeric_cells.py'
result = dict(success=True, configurations=12, nonlinear_samples=24,
              implementation_sha256=hashlib.sha256(source.read_bytes()).hexdigest(), records=records)
(HERE/'dlw_model_validation.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
