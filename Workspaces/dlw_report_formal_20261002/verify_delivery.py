"""Validate the final Lean run against current source and record endpoint evidence."""
from pathlib import Path
import argparse
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
PROOFS = ROOT / 'Workspaces/lean_contracts/proofs'
ENDPOINTS = [
    'DLWContract.ReportEndpoints.Q_is_centered_ratio',
    'DLWContract.ReportEndpoints.bilinear_to_report7',
    'DLWContract.ReportEndpoints.bilinear_to_report21_22',
    'DLWContract.ReportEndpoints.bilinear_to_both',
]
STANDARD = {'propext', 'Classical.choice', 'Quot.sound'}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

parser = argparse.ArgumentParser()
parser.add_argument('--run', required=True)
args = parser.parse_args()
run = PROOFS / '.lean-runs' / args.run
result_path = run / 'result.json'
result = json.loads(result_path.read_text(encoding='utf-8-sig'))
assert result['status'] == 'PASSED'
assert Path(result['target']).resolve() == (PROOFS / 'ReportEndpoints.lean').resolve()
log = (run / 'build.log').read_text(encoding='utf-8-sig')
hash_checks = []
for entry in result['files']:
    path = Path(entry['file'])
    actual = sha(path)
    assert entry['passed'] and entry['exit_code'] == 0
    assert actual == entry['sha256'], str(path)
    hash_checks.append({'file': str(path.relative_to(ROOT)), 'sha256': actual})
audits = []
for name in ENDPOINTS:
    match = re.search(re.escape("'" + name + "' depends on axioms: ") + r'\[([^\]]*)\]', log)
    assert match, name
    axioms = [v.strip() for v in match.group(1).split(',') if v.strip()]
    assert set(axioms) <= STANDARD, (name, axioms)
    audits.append({'theorem': name, 'axioms': axioms})

# Compare frozen sources with the previously verified complete historical entry.
historical = json.loads((PROOFS / '.lean-runs/20260922_221626_2fd722e0/result.json')
                        .read_text(encoding='utf-8-sig'))
frozen = []
for filename in ['Contracts.lean', 'Main.lean']:
    entry = next(v for v in historical['files'] if Path(v['file']).name == filename)
    actual = sha(PROOFS / filename)
    assert actual == entry['sha256'], filename
    frozen.append({'file': filename, 'unchanged_sha256': actual})

new_sources = ['ReportEndpoints.lean', 'ReportNonlinearUW.lean',
               'ReportNonlinearQRM.lean', 'ReportQRMCalculus.lean', 'ReportQRatio.lean']
source_checks = []
for filename in new_sources:
    source = (PROOFS / filename).read_text(encoding='utf-8')
    # This scan supports, and does not replace, the kernel axiom audits above.
    assert not re.search(r'\b(sorry|admit|axiom)\b', source), filename
    declarations = [{'name': m[1], 'line': source[:m.start()].count('\n') + 1}
                    for m in re.finditer(r'^(?:theorem|lemma|def)\s+(\w+)', source, re.M)]
    source_checks.append({'file': filename, 'declarations': declarations})

scope = {
    'parameters': 'a,h real; h != 0; j integer',
    'tau': 'F_j,G_j are positive real functions on the whole (x,t) plane',
    'regularity': 'SmoothL = per-j ContDiff real top of the joint (x,t) function; '
                  'in this Mathlib top is omega (analytic), not the inner infinity (C-infinity)',
    'starting_equations': 'SemiPair a h F G, the two actual Hirota bilinear equations',
    'direction': 'forward implications and physical reconstruction identities',
    'extra_R_nonzero_or_positive_assumption': False,
    'extra_zero_integration_constant_assumption': False,
}
report = {
    'status': 'passed', 'run_id': args.run, 'local_module_count': len(result['files']),
    'toolchain': result['toolchain'], 'mathlib_commit': result['mathlib_commit'],
    'result_path': str(result_path.relative_to(ROOT)),
    'build_log_path': str((run / 'build.log').relative_to(ROOT)),
    'result_sha256': sha(result_path), 'build_log_sha256': sha(run / 'build.log'),
    'current_source_hashes_match': True, 'source_hashes': hash_checks,
    'frozen_sources': frozen, 'endpoint_axiom_audits': audits,
    'scope': scope, 'new_source_declarations': source_checks,
    'formula_review': {'authoritative': 'Workspaces/gsg_project/dlw_report/_src/Report.md',
                       'sha256': sha(ROOT / 'Workspaces/gsg_project/dlw_report/_src/Report.md'),
                       'endpoints': [7, 21, 22],
                       'independent_reviews': 2,
                       'coefficients_signs_shifts_and_unscaled_omega_match': True},
    'regularity_reference': {'file': '_lean_shared/mathlib/Mathlib/Analysis/Calculus/ContDiff/Defs.lean',
                            'notation_line': 91, 'analytic_equivalence_line': 1196},
}
(HERE / 'lean_validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n',
                                           encoding='utf-8')
print(json.dumps({'status': report['status'], 'run_id': args.run,
                  'local_modules': report['local_module_count'],
                  'endpoint_audits': len(audits), 'source_hashes_match': True,
                  'frozen_sources_unchanged': True}, ensure_ascii=False))
