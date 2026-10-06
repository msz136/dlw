"""Run the reproducible algebra and numerical checks for the general-field report."""
from pathlib import Path
import subprocess,sys,hashlib,json,platform,datetime,time
ROOT=Path(__file__).resolve().parent
SCRIPTS=['two_site_exact.py','linearized_all_periods.py','mixed_time_certificate.py','mixed_time_probe.py','inverse_two_site_certificate.py','local_density_certificate.py','poisson_pushforward_certificate.py','lenard_generating_certificate.py','general_period_matrix_certificate.py','general_period_free_fields_certificate.py','quadratic_trace_certificate.py','q5_bch_certificate.py','periodic_monodromy_check.py']
def main():
 logs=ROOT/'logs';logs.mkdir(exist_ok=True)
 results=[]
 for name in SCRIPTS:
  start=time.monotonic();p=subprocess.run([sys.executable,str(ROOT/name)],cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=240)
  (logs/(name+'.log')).write_text(p.stdout)
  results.append({'script':name,'sha256':hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),'exit_code':p.returncode,'seconds':round(time.monotonic()-start,3),'log':'logs/'+name+'.log'})
  print(name,'PASS' if p.returncode==0 else 'FAIL',flush=True)
 import sympy,numpy
 report={'run_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':platform.python_version(),'sympy':sympy.__version__,'numpy':numpy.__version__,'checks':results,'passed':sum(x['exit_code']==0 for x in results),'total':len(results),'scope':'Exact finite symbolic certificates and one numerical mixed-boundary probe; general theorems use the accompanying written proofs.'}
 (ROOT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
 return 0 if report['passed']==report['total'] else 1
if __name__=='__main__':sys.exit(main())
