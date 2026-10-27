"""Read-only audit of actual A/D data used in the finite-Laplace-chain theorem."""
from pathlib import Path
import ast
import json
import numpy as np
import sympy as sp
from scipy.special import logsumexp

HERE=Path(__file__).resolve().parent
PROJECT=HERE.parents[1]
SOURCE=PROJECT/'paper_comparison_20261022/solver_snapshot.py'
assignment=next(n for n in ast.parse(SOURCE.read_text(encoding='utf8')).body
                if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CASES' for t in n.targets))
cases=ast.literal_eval(assignment.value)
records=[]
for case in ['A','D']:
    ps,qs=[[sp.Rational(str(x)) for x in row] for row in cases[case]]
    ell=[1/(p-2)+1/(q+2) for p,q in zip(ps,qs)]
    sums=[p+q for p,q in zip(ps,qs)]
    shifts=[-(p-2)/(q+2) for p,q in zip(ps,qs)]
    subsets=np.array([[0],[1]]) if case=='A' else np.array([[0,0],[1,0],[0,1],[1,1]])
    coeff=[sp.Integer(1),1/sums[0]]
    if case=='D':
        coeff += [1/sums[1],(ps[0]-ps[1])*(qs[0]-qs[1])/((ps[0]+qs[0])*(ps[0]+qs[1])*(ps[1]+qs[0])*(ps[1]+qs[1]))]
    fcoeff=[c*sp.prod(shifts[j]**int(ss[j]) for j in range(len(ps))) for c,ss in zip(coeff,subsets)]
    assert all(c>0 for c in coeff+fcoeff)
    assert all(sp.simplify(sp.exp(8*sp.pi*sp.I*g)-1)==0 for g in ell)
    data=np.load(PROJECT/'stability_20261026/perturbation_pilot/four_case_kappa_pi_over_2'/(case+'.npz'))
    x,y,yv=data['x'],data['y'],data['yv']
    rates_x=subsets@np.array(sums,dtype=float)
    rates_y=subsets@np.array(ell,dtype=float)
    def profiles(yy):
        def stats(cs):
            logs=np.log(np.array(cs,dtype=float))[:,None,None]+rates_x[:,None,None]*x[None,None,:]+rates_y[:,None,None]*yy[None,:,None]
            w=np.exp(logs-logsumexp(logs,axis=0)[None])
            mx=np.sum(rates_x[:,None,None]*w,axis=0)
            my=np.sum(rates_y[:,None,None]*w,axis=0)
            cov=np.sum((rates_x*rates_y)[:,None,None]*w,axis=0)-mx*my
            return mx,cov
        fx,fxy=stats(fcoeff);gx,gxy=stats(coeff)
        return 2*(fx-gx),2*(fxy+gxy)
    u,w=data['z0'][0];h=.1
    v=np.diff(u,axis=0)/h+(w[1:]+w[:-1])/2
    eu=float(np.max(abs(u-profiles(y)[0])))
    ev=float(np.max(abs(v-profiles(yv)[1])))
    assert eu<1e-12 and ev<1e-12
    records.append(dict(case=case,p=[str(q) for q in ps],q=[str(q) for q in qs],
        transverse_exponents=[str(q) for q in ell],g_coefficients=[str(q) for q in coeff],
        f_coefficients=[str(q) for q in fcoeff],all_coefficients_positive=True,
        imaginary_y_period='8*pi',y_interval=[float(y[0]),float(y[-1])],
        envelope_length=float(y[-1]-y[0]),envelope_transverse_frequency=float(np.pi/(y[-1]-y[0])),
        stored_initial_u_vs_continuous_Gram_maxdiff=eu,
        stored_initial_v_vs_continuous_Gram_maxdiff=ev))
out=dict(records=records,scope='Exact parameter/period checks and ordinary-floating comparison to stored initial fields; no continuum evolution certificate')
(HERE/'audit_soliton_laplace_checks.json').write_text(json.dumps(out,indent=2),encoding='utf8')
print(json.dumps(out,indent=2))
