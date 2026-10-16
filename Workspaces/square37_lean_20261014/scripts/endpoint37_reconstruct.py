"""Exact number-field reconstruction of the Cantrell 37 endpoint.

Floating-point LP is used only to choose a linear-system basis. All returned
centers, supports and margins are solved/checked over QQ(q), with exact zero
tests and rational interval sign checks on the isolated positive root q.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,itertools,time
import numpy as np
from scipy.optimize import linprog
from scipy.linalg import qr
import sympy as S

BASE=Path(__file__).resolve().parents[1]
SOURCE=BASE/'certificates/n37_rational_sat.json'
SYMBOLIC=BASE/'analysis/n37_symbolic_support.json'

class Interval:
    def __init__(self,a,b=None):self.a=F(a);self.b=F(a if b is None else b)
    def __add__(self,o):
        o=o if isinstance(o,Interval) else Interval(o);return Interval(self.a+o.a,self.b+o.b)
    __radd__=__add__
    def __mul__(self,o):
        o=o if isinstance(o,Interval) else Interval(o);v=[x*y for x in(self.a,self.b) for y in(o.a,o.b)];return Interval(min(v),max(v))
    __rmul__=__mul__
    def serial(self):return {'lo':str(self.a),'hi':str(self.b)}

def field_coeffs(value):return [F(int(z.numerator),int(z.denominator)) for z in value.to_list()]

def evaluate(value,qbox):
    ans=Interval(0)
    for z in field_coeffs(value):ans=ans*qbox+z
    return ans

def serial(value):return [str(z) for z in field_coeffs(value)]

def exact_solve(rows,rhs,K):
    """Sparse Gauss-Jordan elimination in the exact algebraic field."""
    rows=[{j:v for j,v in enumerate(row) if v} for row in rows]
    rhs=list(rhs);n=len(rows)
    for col in range(n):
        choices=[i for i in range(col,n) if rows[i].get(col,K.zero)]
        if not choices:raise ValueError(f'exact singular basis at {col}')
        p=min(choices,key=lambda i:len(rows[i]))
        rows[col],rows[p]=rows[p],rows[col];rhs[col],rhs[p]=rhs[p],rhs[col]
        pivot=rows[col][col]
        rows[col]={j:v/pivot for j,v in rows[col].items()};rhs[col]/=pivot
        for i in range(n):
            if i==col:continue
            fac=rows[i].get(col,K.zero)
            if not fac:continue
            for j,v in rows[col].items():
                nv=rows[i].get(j,K.zero)-fac*v
                if nv:rows[i][j]=nv
                else:rows[i].pop(j,None)
            rhs[i]-=fac*rhs[col]
    assert all(row=={i:K.one} for i,row in enumerate(rows))
    return rhs

def main():
    start=time.time();source=json.loads(SOURCE.read_text());root=json.loads(SYMBOLIC.read_text())
    qlo,qhi=F(root['q_interval']['lo']),F(root['q_interval']['hi']);qbox=Interval(qlo,qhi)
    q=S.symbols('q');M=S.Poly(7*q**8+44*q**6+66*q**4-4*q**2-1,q)
    assert M.is_irreducible
    K=S.QQ.alg_field_from_poly(M,root_index=1,alias='q');Q=K.unit
    one,zero=K.one,K.zero
    C=(one-Q*Q)/(one+Q*Q);Sn=2*Q/(one+Q*Q)
    R=(4*Q**4+12*Q*Q)/(one+Q*Q)**2
    L=(7+10*Q-Q*Q)/(one+2*Q-Q*Q)
    assert C*C+Sn*Sn==one and R*R==2*one
    assert (4-R)*Q**4+(12-2*R)*Q*Q-R==zero
    assert evaluate(R,qbox).a>0
    units=[]
    for i in range(37):
        if 9<=i<=14:u=(C,-Sn)
        elif 18<=i<=23:u=(C,Sn)
        elif i>=34:u=(R/2,R/2)
        else:u=(one,zero)
        units.append((u,(-u[1],u[0])))
    def dot(a,b):return a[0]*b[0]+a[1]*b[1]
    abs_checks=[]
    def exact_abs(v):
        if not v:return zero
        box=evaluate(v,qbox)
        assert box.a>0 or box.b<0,('ambiguous sign',serial(v),box.serial())
        return v if box.a>0 else -v
    rows=[];rhs=[];labels=[]
    for pair in source['pairs']:
        i,j=pair['i'],pair['j'];owner=pair['owner'];axis=0 if pair['axis']=='u' else 1
        normal=tuple(pair['sign']*z for z in units[owner][axis]);row=[zero]*74
        row[2*i]=-normal[0];row[2*i+1]=-normal[1];row[2*j]=normal[0];row[2*j+1]=normal[1]
        required=sum((exact_abs(dot(normal,v)) for k in(i,j) for v in units[k]),zero)/2
        rows.append(row);rhs.append(required);labels.append({'kind':'pair','i':i+1,'j':j+1,'owner':owner+1,'axis':pair['axis'],'sign':pair['sign'],'nx':serial(normal[0]),'ny':serial(normal[1]),'required':serial(required)})
    for i,(u,v) in enumerate(units):
        h=[(exact_abs(u[k])+exact_abs(v[k]))/2 for k in(0,1)]
        for axis,sgn,name in [(0,1,'left'),(1,1,'bottom'),(0,-1,'right'),(1,-1,'top')]:
            row=[zero]*74;row[2*i+axis]=sgn*one
            rows.append(row);rhs.append(h[axis]-(L if sgn<0 else zero));labels.append({'kind':'wall','i':i+1,'wall':name})
    midpoint=float((qlo+qhi)/2)
    def approximate(v):
        val=0.
        for z in field_coeffs(v):val=val*midpoint+float(z)
        return val
    A=np.array([[approximate(v) for v in row] for row in rows]);b=np.array([approximate(v) for v in rhs])
    rng=np.random.default_rng(370014)
    trials=[];solution=None;chosen=None
    for trial in range(12):
        objective=rng.normal(size=74) if trial else np.arange(1,75)/74
        result=linprog(objective,A_ub=-A,b_ub=-b,bounds=[(None,None)]*74,method='highs')
        rec={'trial':trial,'status':int(result.status),'message':result.message}
        if not result.success:trials.append(rec);continue
        gap=A@result.x-b;active=np.flatnonzero(np.abs(gap)<1e-7)
        _,rr,piv=qr(A[active].T,pivoting=True,mode='economic')
        rec.update({'numeric_min_gap':float(gap.min()),'active_count':len(active),'rank':int(np.linalg.matrix_rank(A[active]))})
        basis=active[piv[:74]].tolist()
        try:sol=exact_solve([rows[k] for k in basis],[rhs[k] for k in basis],K)
        except ValueError as exc:rec['exact_error']=str(exc);trials.append(rec);continue
        margins=[sum((v*z for v,z in zip(row,sol)),zero)-h for row,h in zip(rows,rhs)]
        bad=[];undecided=[];positive=[];zeros=[]
        for k,m in enumerate(margins):
            if not m:zeros.append(k);continue
            box=evaluate(m,qbox)
            if box.a>0:positive.append(k)
            elif box.b<0:bad.append(k)
            else:undecided.append(k)
        rec.update({'exact_zero_margins':len(zeros),'positive_margins':len(positive),'negative_rows':bad,'undecided_rows':undecided})
        trials.append(rec)
        print('trial',trial,'zero',len(zeros),'positive',len(positive),'negative',len(bad),'undecided',len(undecided),flush=True)
        if not bad and not undecided:solution=sol;chosen=basis;break
    audit={'source_certificate_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'root_evidence_sha256':hashlib.sha256(SYMBOLIC.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'field_polynomial':str(M.as_expr()),'irreducible_over_Q':True,'root_interval':{'lo':str(qlo),'hi':str(qhi)},'trials':trials,'success':solution is not None,'elapsed_seconds':time.time()-start}
    if solution is not None:
        assertions=[]
        for k,m in enumerate(margins):
            z={**labels[k],'margin':serial(m),'exact_zero':not bool(m)}
            if m:z['positive_interval']=evaluate(m,qbox).serial()
            assertions.append(z)
        result={'schema':'algebraic-oriented-unit-squares-v1','count':37,'coordinate_encoding':'coefficients descending in powers of q, reduced modulo 7q^8+44q^6+66q^4-4q^2-1','field_polynomial_coeffs':[7,0,44,0,66,0,-4,0,-1],'root_interval':audit['root_interval'],'L':serial(L),'c':serial(C),'s':serial(Sn),'sqrt2':serial(R),'squares':[{'id':i+1,'cx':serial(solution[2*i]),'cy':serial(solution[2*i+1]),'ux':serial(units[i][0][0]),'uy':serial(units[i][0][1])} for i in range(37)],'basis_rows':chosen,'assertions':assertions,'source':source['source'],'audit':audit}
        output=BASE/'analysis/endpoint37_algebraic_certificate.json';output.write_text(json.dumps(result,indent=2),encoding='utf8');audit['certificate_sha256']=hashlib.sha256(output.read_bytes()).hexdigest()
        print('SUCCESS',output,'seconds',time.time()-start,flush=True)
    (BASE/'analysis/endpoint37_reconstruction.json').write_text(json.dumps(audit,indent=2),encoding='utf8')

if __name__=='__main__':main()
