"""Test a cheap defect-based solver floor on parameters omitted from calibration."""
from pathlib import Path
import sys, json, hashlib
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'lib'))
from parametric import Parameters, Exact
from parametric_open import OpenModel
from route2_budget import advance, inf

OUT=ROOT/'out/route2'
PARAMS={
 'P1':Parameters(), 'P2':Parameters(p=2,q=3,rho=5),
 'P3':Parameters(a=3), 'P4':Parameters(a=6),
 'P5':Parameters(p=.5,q=1,rho=1.5),
 'P6':Parameters(p=1,q=3,rho=4),
 'P7':Parameters(p=2,q=1,rho=3),
 'P8':Parameters(rho=.3), 'P9':Parameters(rho=30),
 'P10':Parameters(a=2,p=1.5,q=2,rho=3.5)}
TRAIN=('P2','P3','P4','P5','P7','P8','P9')
TEST=('P1','P6','P10')


def cheap_features(case):
    pars=PARAMS[case];m=OpenModel(pars,.25,256,model='structure',continuous=False)
    r=m.rhs(0,m.exact(0))-m.exact(0,True)
    phys=m.error_fields(r)
    finite=Exact(pars,.25).uv(m.js,m.X.x,.01)
    cont=Exact(pars,.25,continuous=True).uv(m.js,m.X.x,.01)
    return m, {f:{'initial_output_defect':inf(phys[i]),
                  'pilot_h_model_C':inf(finite[i]-cont[i])/.25**2}
               for i,f in enumerate(('u','v'))}


def main():
    rows=[]
    for case in TRAIN:
        m,feat=cheap_features(case)
        z,_=advance(m,T=.01,dt=.000125)
        fields=m.fields(z,.01)
        ref=Exact(PARAMS[case],.25).uv(m.js,m.X.x,.01)
        for i,f in enumerate(('u','v')):
            feat[f]['observed_solver']=inf(fields[i]-ref[i])
        rows.append({'case':case,'fields':feat})
        print('train',case,feat,flush=True)
    factors={f:float(np.median([r['fields'][f]['observed_solver'] /
                 (.01*r['fields'][f]['initial_output_defect']) for r in rows]))
             for f in ('u','v')}
    # Predictions are constructed without using any held-out trajectory.
    predictions=[]
    for case in TEST:
        _,feat=cheap_features(case)
        for f in ('u','v'):
            pred_s=factors[f]*.01*feat[f]['initial_output_defect']
            feat[f]['predicted_solver_floor']=pred_s
            feat[f]['predicted_h_balance']=float(np.sqrt(pred_s/feat[f]['pilot_h_model_C']))
            feat[f]['predicted_h_1_16_ratio']=feat[f]['pilot_h_model_C']*.0625**2/pred_s
        predictions.append({'case':case,'fields':feat})
    # Only after predictions are frozen, compare to the existing held-out runs.
    budget=json.loads((OUT/'budget.json').read_text(encoding='utf-8'))
    for row in predictions:
        actual=next(r for r in budget['runs'] if r['config']['case']==row['case'] and
                    r['config']['h']==.0625 and r['config']['nx']==256 and
                    r['config']['initial']=='finite')
        for f in ('u','v'):
            d=row['fields'][f]
            d['observed_h_1_16_ratio']=actual['errors'][f]['dominance_ratio']
            d['observed_h_1_16_solver']=actual['errors'][f]['solver_vs_finite']
            d['prediction_factor']=d['predicted_h_1_16_ratio']/d['observed_h_1_16_ratio']
        print('held-out',row['case'],row['fields'],flush=True)
    paths=[Path(__file__),ROOT/'lib/parametric.py',ROOT/'lib/parametric_open.py',
           ROOT/'experiments/route2_budget.py']
    data={'training_cases':TRAIN,'held_out_cases':TEST,'T':.01,'pilot_h':.25,
          'h_test':.0625,'nx':256,'calibration':'median of observed solver /(T * initial physical-output defect)',
          'factors':factors,'training':rows,'predictions':predictions,
          'sources_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}
    (OUT/'crossparam.json').write_text(json.dumps(data,indent=2,allow_nan=False)+'\n',encoding='utf-8')


if __name__=='__main__':main()
