"""Run the focused exact certificates; write an honest, reproducible validation record."""
from pathlib import Path
import hashlib,json,platform,subprocess,sys
from datetime import datetime,timezone
import sympy
ROOT=Path(__file__).resolve().parent
FILES=['verify_general_structure.py','all_rank_bilinear_certificate.py','moduli_certificate.py','physical_immersion_certificate.py','single_and_casimir_certificate.py','cross_n_certificate.py','atomic_poisson_certificate.py']
records=[]
for name in FILES:
 p=ROOT/name
 r=subprocess.run([sys.executable,str(p)],capture_output=True,text=True,cwd=ROOT,timeout=180)
 rec={'file':name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
 records.append(rec);print(name,'PASS' if r.returncode==0 else 'FAIL',flush=True)
result={'executed_at_utc':datetime.now(timezone.utc).isoformat(),'python':platform.python_version(),'sympy':sympy.__version__,'scope':'Focused exact algebra/rational certificates. General proofs remain written mathematical arguments; no Lean compilation, PDE evolution, independent review, or UI browser test is claimed.','all_passed':all(x['exit_code']==0 for x in records),'checks':records}
(ROOT/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if result['all_passed'] else 1)
