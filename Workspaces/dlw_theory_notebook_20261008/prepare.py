from pathlib import Path
import shutil, hashlib, json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
before=HERE/'before'
before.mkdir(exist_ok=True)
original=ROOT/'notebook/非线性化report.ipynb'
if not (before/original.name).exists():
    shutil.copy2(original,before/original.name)
proofs=HERE/'proofs'
proofs.mkdir(exist_ok=True)
manifest={}
for src in (ROOT/'Workspaces/lean_contracts/proofs').glob('*.lean'):
    shutil.copy2(src,proofs/src.name)
    manifest[src.name]={'source':str(src.relative_to(ROOT)),'sha256':hashlib.sha256(src.read_bytes()).hexdigest()}
for src in (ROOT/'Workspaces/report_notebook_20261002/lean_material/proofs').glob('*.lean'):
    if src.name in manifest:
        assert src.read_bytes()==(proofs/src.name).read_bytes(),src.name
        continue
    shutil.copy2(src,proofs/src.name)
    manifest[src.name]={'source':str(src.relative_to(ROOT)),'sha256':hashlib.sha256(src.read_bytes()).hexdigest()}
(HERE/'proof_sources.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('Preserved original notebook; collected',len(manifest),'unchanged Lean sources')
