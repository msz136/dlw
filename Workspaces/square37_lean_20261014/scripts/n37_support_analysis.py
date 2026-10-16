"""Extract fixed-branch LP and exact conditional dual certificate; no global claim."""
from pathlib import Path
from fractions import Fraction as F
import json,math,hashlib
import numpy as np
from scipy.optimize import linprog
import sympy as sp

BASE=Path(__file__).resolve().parents[1]

def main():
    cert=json.loads((BASE/'certificates/n37_rational_sat.json').read_text())
    n=cert['count']; N=2*n+1
    sq=[{k:F(s[k]) for k in ('cx','cy','ux','uy','vx','vy')} for s in cert['squares']]
    rows=[];rhs=[];labels=[]
    def add(v,b,label): rows.append(v);rhs.append(b);labels.append(label)
    for p in cert['pairs']:
        i,j=p['i'],p['j'];x,y=F(p['nx']),F(p['ny']);v=[F(0)]*N
        v[2*i]=-x;v[2*i+1]=-y;v[2*j]=x;v[2*j+1]=y
        add(v,F(p['required']),{'kind':'pair','i':i+1,'j':j+1,'owner':p['owner']+1,'axis':p['axis'],'sign':p['sign']})
    for i,s in enumerate(sq):
        hx=(abs(s['ux'])+abs(s['vx']))/2;hy=(abs(s['uy'])+abs(s['vy']))/2
        for axis,sign,h,name in [(0,1,hx,'left'),(1,1,hy,'bottom'),(0,-1,hx,'right'),(1,-1,hy,'top')]:
            v=[F(0)]*N;v[2*i+axis]=sign
            if sign<0:v[-1]=1
            add(v,h,{'kind':'wall','i':i+1,'wall':name})
    A=np.array(rows,dtype=float);b=np.array(rhs,dtype=float);obj=np.zeros(N);obj[-1]=1
    result=linprog(obj,A_ub=-A,b_ub=-b,bounds=[(None,None)]*N,method='highs')
    assert result.success,result.message
    weights=-result.ineqlin.marginals
    support=np.flatnonzero(weights>1e-9).tolist()
    M=sp.Matrix([[sp.Rational(rows[k][j].numerator,rows[k][j].denominator) for k in support] for j in range(N)])
    sol,params=M.gauss_jordan_solve(sp.Matrix([0]*(N-1)+[1]));assert not params
    assert all(x>=0 for x in sol)
    exactbound=sum(sp.Rational(rhs[k].numerator,rhs[k].denominator)*sol[t] for t,k in enumerate(support))
    report={'scope':'Conditional lower bound only: every listed directed separating inequality must hold at the supplied fixed rational square orientations. Not an unrestricted packing lower bound.','source':cert['source'],'certificate_sha256':hashlib.sha256((BASE/'certificates/n37_rational_sat.json').read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'side_numeric':float(result.fun),'lower_bound_exact':str(exactbound),'lower_bound_decimal_40':str(exactbound.evalf(40)),'positive_dual_rows':len(support),'coordinate_cancellation_exact':M*sol==sp.Matrix([0]*(N-1)+[1]),'weights_nonnegative_exact':True,'dual_support':[{'row':k,**labels[k],'weight':str(sol[t]),'weight_float':float(sol[t])} for t,k in enumerate(support)],'load_bearing_square_ids':sorted({labels[k][key] for k in support for key in ('i','j') if key in labels[k]}),'near_contact_pairs':[{'i':p['i']+1,'j':p['j']+1,'gap':p['margin']} for p in cert['pairs'] if float(F(p['margin']))<1e-8],'orientations_deg':[math.degrees(math.atan2(float(s['uy']),float(s['ux']))) for s in sq]}
    (BASE/'analysis/n37_fixed_branch_dual.json').write_text(json.dumps(report,indent=2),encoding='utf8')
    print('L',report['lower_bound_decimal_40'],'rows',len(support),'core',report['load_bearing_square_ids'])
    for z in report['dual_support']:print({k:v for k,v in z.items() if k!='weight'})

if __name__=='__main__':main()
