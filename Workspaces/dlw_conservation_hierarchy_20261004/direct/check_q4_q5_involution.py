"""Exact nonzero-field periodic sample for {Q5corrected,Q4}_red."""
import check_reduced_q5 as q5
import check_reduced_q4 as q
import sympy as s
import json
from pathlib import Path
eps=q5.eps
q4p=q.P([q.QU[i]-q.r[i]*q.Pi(q.QU)/q.c for i in range(q.N)])
q4r=q.P([q.QW[i]-q.p[i]*q.Pi(q.QU)/q.c for i in range(q.N)])
pt=[-q.D(v) for v in q4r];rt=[-q.D(v) for v in q4p]
Bt=-q.Pi([pt[i]*q.r[i]+q.p[i]*rt[i] for i in range(q.N)])/q.c
Ut=[s.expand(v+Bt) for v in pt];wt=rt
Ueps=[q.U[i]+eps*Ut[i] for i in range(q.N)]
weps=[q.w[i]+eps*wt[i] for i in range(q.N)]
corrected=q5.density(Ueps,weps)-8*q.N/q.c*q5.emean(Ueps,weps)**2
bracket=s.expand(s.diff(corrected,eps).subs(eps,0)).coeff(q.z,0)
out={'N':q.N,'h':str(q.h),'Q4_Q5corrected_reduced_bracket_trace':str(bracket),
     'scope':'exact sample only; zero is supporting evidence rather than general involution proof'}
print(json.dumps(out,indent=2))
Path(__file__).with_name('q4_q5_involution_sample.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
