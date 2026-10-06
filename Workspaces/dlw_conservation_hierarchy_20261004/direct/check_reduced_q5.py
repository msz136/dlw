"""Exact periodic reduction audit for the new direct Q5 candidate."""
import check_reduced_q4 as q
import sympy as s
import json
from pathlib import Path
eps=s.symbols('eps')

def density(U,w):
    A=q.Rp([q.D(v) for v in w]); C=q.Rp([q.D(U[i]*w[i]) for i in range(q.N)])
    out=0
    for i in range(q.N):
        u,v=U[i],w[i]; x,y=q.D(u),q.D(v);a=A[i]
        out+=u**4*v+12*u*u*v*x-4*v*x*x-16*u*x*y+8*x*q.D(y)
        out+=4*u*u*v*a+4*v*x*a-4*u*y*a+2*v*a*a-4*y*q.D(a)+2*u*v*C[i]
        out+=4*q.beta*u*u*v**3+4*q.beta*q.beta*v**5/5+8*q.beta*v**3*x/3-8*q.beta*v*y*y+8*q.beta*v**3*a/3
    return out

reduced=s.expand(s.diff(density([q.U[i]+eps*q.Ut[i] for i in range(q.N)],
                               [q.w[i]+eps*q.wt[i] for i in range(q.N)]),eps).subs(eps,0))
fullUt=[-q.D(v) for v in q.HW]; fullwt=[-q.D(v) for v in q.HU]
full=s.expand(s.diff(density([q.U[i]+eps*fullUt[i] for i in range(q.N)],
                            [q.w[i]+eps*fullwt[i] for i in range(q.N)]),eps).subs(eps,0))
def emean(U,w):
    A=q.Rp([q.D(v) for v in w])
    return sum(U[i]**2*w[i]/2+q.beta*w[i]**3/3+w[i]*q.D(U[i])+w[i]*A[i]/2 for i in range(q.N))/q.N
et=s.expand(s.diff(emean([q.U[i]+eps*q.Ut[i] for i in range(q.N)],
                        [q.w[i]+eps*q.wt[i] for i in range(q.N)])**2,eps).subs(eps,0))
out={'Q5_reduced_trace':str(reduced.coeff(q.z,0)),'Q5_full_trace':str(full.coeff(q.z,0)),
     'd_trace_emean_squared':str(et.coeff(q.z,0)),
     'ratio_Q5_to_emean_sq':str(reduced.coeff(q.z,0)/et.coeff(q.z,0)),
     'state':'same exact N3 state as reduced_q4_counterexample.json'}
print(json.dumps(out,indent=2))
Path(__file__).with_name('reduced_q5_audit.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
