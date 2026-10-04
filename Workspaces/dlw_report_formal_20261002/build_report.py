"""Build the self-contained mathematical report only from a passed unified Lean run."""
from pathlib import Path
import argparse
import base64
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
PROOFS = ROOT / 'Workspaces/lean_contracts/proofs'
ASSETS = ROOT / 'Workspaces/gsg_project/dlw_report/_assets/package/dist'
SOURCE = HERE / 'report.source.html'
OUTPUT = ROOT / 'report/dlw_bilinear_nonlinear_lean.html'
ENDPOINTS = ['bilinear_to_report7', 'bilinear_to_report21_22', 'bilinear_to_both']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', required=True, help='Passed ReportEndpoints run identifier.')
    args = parser.parse_args()
    if not re.fullmatch(r'\d{8}_\d{6}_[0-9a-f]{8}', args.run):
        raise ValueError('Supply an actual unified Lean run identifier.')
    run_dir = PROOFS / '.lean-runs' / args.run
    result_path = run_dir / 'result.json'
    result = json.loads(result_path.read_text(encoding='utf-8'))
    if result.get('status') != 'PASSED':
        raise ValueError('The unified Lean run has not passed.')
    if Path(result['target']).resolve() != (PROOFS / 'ReportEndpoints.lean').resolve():
        raise ValueError('The certificate must target the unified ReportEndpoints module.')
    checked_sources = {}
    for item in result['files']:
        file = Path(item['file'])
        digest = hashlib.sha256(file.read_bytes()).hexdigest()
        if not item['passed'] or item['exit_code'] != 0 or digest != item['sha256']:
            raise ValueError('The run does not certify the current source: ' + str(file))
        checked_sources[str(file.relative_to(ROOT))] = digest
    log = (run_dir / 'build.log').read_text(encoding='utf-8')
    for name in ENDPOINTS:
        line = next((line for line in log.splitlines()
                     if "'DLWContract.ReportEndpoints." + name + "' depends on axioms:" in line), None)
        if line is None or 'sorryAx' in line:
            raise ValueError('Missing valid axiom audit for ' + name)
        found = set(re.findall(r'(?:propext|Classical\.choice|Quot\.sound)', line))
        if found != {'propext', 'Classical.choice', 'Quot.sound'}:
            raise ValueError('Unexpected axiom audit for ' + name)
        tail = line.split('depends on axioms:', 1)[1].strip()
        if set(x.strip() for x in tail.strip('[]').split(',')) != found:
            raise ValueError('The endpoint uses additional axioms: ' + name)

    page = SOURCE.read_text(encoding='utf-8').replace('__COMBINED_RUN__', args.run)
    css = (ASSETS / 'katex.min.css').read_text(encoding='utf-8')
    embedded_fonts = []

    def embed(match):
        file = ASSETS / 'fonts' / match[1]
        mime = {'.woff2': 'font/woff2', '.woff': 'font/woff', '.ttf': 'font/ttf'}[file.suffix]
        embedded_fonts.append(file.name)
        return 'url(data:' + mime + ';base64,' + base64.b64encode(file.read_bytes()).decode() + ')'

    css = re.sub(r'url\((?:"|\x27)?fonts/([^\)"\x27]+)(?:"|\x27)?\)', embed, css)
    js = (ASSETS / 'katex.min.js').read_text(encoding='utf-8') + '\n' + (
        ASSETS / 'contrib/auto-render.min.js').read_text(encoding='utf-8')
    page = page.replace('@@KATEX_CSS@@', css).replace('@@KATEX_JS@@', js)
    if '@@' in page or '__COMBINED_RUN__' in page:
        raise ValueError('An unresolved report placeholder remains.')
    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(page, encoding='utf-8')
    manifest = {
        'output': str(OUTPUT),
        'sha256': hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
        'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        'combined_run': args.run,
        'lean_result': str(result_path),
        'local_modules': len(result['files']),
        'endpoint_axioms': ['propext', 'Classical.choice', 'Quot.sound'],
        'fonts_embedded': len(embedded_fonts),
        'checked_source_hashes': checked_sources,
    }
    (HERE / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: value for key, value in manifest.items() if key != 'checked_source_hashes'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
