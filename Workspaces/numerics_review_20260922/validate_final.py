"""Validate regenerated artifacts and capture the exact final source hashes."""
from pathlib import Path
import json,math,hashlib
N=Path(__file__).resolve().parents[2]/'Workspaces/dlw_semidiscrete/numerics'
def load(name):return json.loads((N/'out'/name).read_text(encoding='utf-8'))
checks=[]
def check(label,condition):
    assert condition,label
    checks.append(label)
e1=load('e1_continuum.json')
check('E1 weighted fixed-window second order',all(abs(r['slope_E2_u']-2)<.05 for r in e1['cases']['A']['observed_slopes']))
e5=load('e5_conservation.json')
rows=e5['solver_conservation']
check('E5 nonempty actual trajectories',len(rows)==3)
check('E5 correct site, t0 and final time',all(r['site']==0 and r['initial_t']==0 and abs(r['final_t']-.005)<1e-12 and r['stopped'] is None and r['finite'] for r in rows))
check('E5 bounded finite drift',all(math.isfinite(r['max_dI_v']) and r['max_dI_v']<1e-10 and r['max_dI_W']<1e-10 for r in rows))
e6=load('e6_growth.json')
check('E6 four live perturbation runs',len(e6['solver_growth'])==4)
check('E6 mode and RHS agreement',all(r['relative_error']<1e-5 and r['mode_shape_error']<1e-7 and r['jacobian_error']<1e-8 for r in e6['solver_growth']))
check('E6 six complete open-chain spectra',len(e6['grid_gmax'])==6 and all(r['linear_log_norm']>=r['g_max_discrete'] for r in e6['grid_gmax']))
e7=load('e7_fd_baseline.json')
check('E7 regenerated order',len(e7['dt_refinement'])==4 and all(r['slope_v']>3.5 for r in e7['dt_refinement'][1:]))
e23=load('e2_e3_solver.json')
check('E2/E3 all expected time studies',len(e23['time_refinement'])==18)
check('E2/E3 all runs complete and finite',all(r['steps']==math.ceil(.05/r['dt']-1e-12) and math.isfinite(r['Einf_u']) and math.isfinite(r['Einf_v']) for r in e23['time_refinement']))
check('E2/E3 trapezoid residuals small',all(r.get('trap_max_resid',0)<1e-12 for r in e23['time_refinement']))
log=(N/'out/final_regressions_log.txt').read_text(encoding='utf-8')
check('40 behavioral and artifact checks passed','RESULT: all regression checks PASSED' in log and '[FAIL]' not in log and log.count('[PASS]')==40)
runlog=(N/'out/final_four_fixes_log.txt').read_text(encoding='utf-8')
check('all five rerun stages completed','all experiments completed' in runlog and 'FAILED' not in runlog)
st=load('e2_e3_self_convergence.json')
check('six fixed-grid time self-convergence studies passed',st['passed'] and len(st['studies'])==6 and all(s['accepted'] for s in st['studies']))
check('all 30 new trajectories reached their target',all(len(s['runs'])==5 and all(r['stopped'] is None and abs(r['final_t']-s['t_end'])<1e-14 and r['steps']==r['n'] for r in s['runs']) for s in st['studies']))
check('self-convergence measured all state and physical components',all(set(s['successive_differences'][-1]['orders'])=={'P','W','u','v'} and all(abs(p-s['expected_order'])<.35 for p in s['successive_differences'][-1]['orders'].values()) for s in st['studies']))
check('self-convergence source hashes match current source',all(hashlib.sha256((N/p).read_bytes()).hexdigest()==v for p,v in st['source_sha256'].items()))
manifest={'checks':checks,'regression_pass_count':40,'scope':'Four review fixes plus six same-grid time self-convergence studies; no Lean or general nonlinear stability certification',
          'files':{str(p.relative_to(N)):hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in N.rglob('*') if p.is_file() and '__pycache__' not in str(p)
                   and p.name!='final_validation_manifest.json'}}
(N/'out/final_validation_manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps({'passed':checks,'regression_pass_count':40},ensure_ascii=False,indent=2))
