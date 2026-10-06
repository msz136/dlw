from pathlib import Path
import sympy as s
h=s.symbols('h',nonzero=True)
for M in range(2,10):
 r=M-1;I=s.eye(M);P0=I-s.ones(M)/M;Z=s.Matrix(M,r,lambda i,j:(1 if i==j else 0)-(1 if i==M-1 else 0));E=I[:r,:]
 Kd=s.Matrix(r,M,lambda j,k:-(1 if j==k else 0)-2*(1 if k>j else 0)+(1 if k==M-1 else 0))
 F=(Z.T/2).row_join(h*Kd/8).col_join(s.zeros(r,M).row_join(h*E/8))
 J=s.zeros(M).row_join(-P0).col_join((-P0).row_join(s.zeros(M)))
 target=s.zeros(r).row_join(-h*s.eye(r)/16).col_join((-h*s.eye(r)/16).row_join(s.zeros(r)))
 assert F*J*F.T==target
 print('M',M,'exact canonical free-field bracket passed',flush=True)
 # q,d reconstruct all b from constraints, using only S != 0
 ds=s.symbols('d:'+str(M));qs=s.symbols('q:'+str(r));B=s.symbols('B');S=sum(ds)
 b_last=B-sum(ds[:-1])-sum(ds[j]*qs[j] for j in range(r))/S
 bs=[b_last+qs[j]+ds[j]+2*sum(ds[j+1:-1])+ds[-1] for j in range(r)]+[b_last]
 for j in range(r):assert s.factor(bs[j]-bs[-1]-ds[j]-2*sum(ds[j+1:])+ds[-1]-qs[j])==0
 assert s.factor(sum(bs[j]*ds[j] for j in range(M))-B*S)==0
print('All inverse field formulas also certified.')
