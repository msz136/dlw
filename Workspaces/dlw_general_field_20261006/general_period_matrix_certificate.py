from pathlib import Path
import sympy as s
B,lam=s.symbols('B lambda')
for M in range(2,7):
 ds=s.symbols('d:'+str(M)); bs0=s.symbols('b:'+str(M-1)); dx=s.symbols('dx:'+str(M-1))
 S=sum(ds);nu=B-S
 # enforce sum b_j d_j = B S by eliminating b_last in this symbolic chart
 bs=list(bs0)+[(B*S-sum(bs0[j]*ds[j] for j in range(M-1)))/ds[-1]]
 dv=s.Matrix(ds);ones=s.ones(M,1);H=s.Matrix(M,M,lambda i,j:(1 if j<i else 0))
 C=s.diag(*[bs[i]-ds[i] for i in range(M)])-2*s.diag(*ds)*H-(nu/S)*dv*ones.T
 Z=s.Matrix(M,M-1,lambda i,j:((1 if i==j else 0)-(1 if i==M-1 else 0)))
 T=(dv/S).row_join(Z)
 K=s.eye(M)[:M-1,:]-s.Matrix(ds[:-1])/S*ones.T
 Ti=ones.T.col_join(K)
 assert all(s.factor(v)==0 for v in Ti*T-s.eye(M))
 ddx=s.Matrix(list(dx)+[-sum(dx)])
 Tx=(ddx/S).row_join(s.zeros(M,M-1))
 P=dv*ones.T/S
 A=Ti*(lam*P+C)*T-Ti*Tx
 assert s.factor(A[0,0]-lam)==0
 assert all(s.factor(v)==0 for v in Ti*P*T-s.diag(1,*([0]*(M-1))))
 q=ones.T*C*Z;r=K*(C*dv-ddx)/S;V=K*C*Z
 expected=s.Matrix([[lam]]).row_join(q).col_join(r.row_join(V))
 assert all(s.factor(v)==0 for v in A-expected)
 print('M',M,'rank-one spectral reduction and zero scalar diagonal certified',flush=True)
# M=2 exact identification with previous f,g,C
p,z,c,e,px,zx=s.symbols('p s c eta px sx',nonzero=True)
d0=e*(1+z/c);d1=e*(1-z/c);bbar=2*B-p*z/c
b0=(bbar+p)/2;b1=(bbar-p)/2
S=2*e;nu=B-S
dv=s.Matrix([d0,d1]);o=s.ones(2,1);Z=s.Matrix([1,-1]);K=s.Matrix([[1,0]])-s.Matrix([d0])/S*o.T
C=s.diag(b0-d0,b1-d1)-2*s.diag(d0,d1)*s.Matrix([[0,0],[1,0]])-(nu/S)*dv*o.T
q=(o.T*C*Z)[0];r=(K*(C*dv-s.Matrix([e*zx/c,-e*zx/c]))/S)[0];V=(K*C*Z)[0]
g=-zx/c+(1-z*z/c**2)*(p/2+e)
assert s.factor(q-(p-2*e))==0
assert s.factor(r-g/2)==0
assert s.factor(V-(B-p*z/c))==0
print('M=2 matches q=2f,r=g/2,V=C exactly')
