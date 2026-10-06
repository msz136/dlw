from pathlib import Path
import sympy as s
h=s.symbols('h',positive=True)
for M in range(2,9):
 I=s.eye(M);Pi=s.ones(M)/M;P=I-Pi
 R=s.Matrix(M,M,lambda i,j:h*(s.sign(i-j)/2-s.Rational(i-j,M)))
 shift=s.zeros(M)
 for i in range(M):shift[i,(i-1)%M]=1
 dm=(I-shift)/h;avg=(I+shift)/2
 assert R+R.T==s.zeros(M)
 assert R*Pi==s.zeros(M)
 assert dm*R==avg*P
 Z=s.zeros(M)
 principal=(-I).row_join(-R).col_join(Z.row_join(I))
 T=I.row_join(R/2).col_join(Z.row_join(I))
 Ti=I.row_join(-R/2).col_join(Z.row_join(I))
 diag=(-I).row_join(Z).col_join(Z.row_join(I))
 assert T*principal*Ti==diag
 print('M=',M,' exact skew, inverse difference and forward/backward diagonalization passed')
 # D commutes with finite lattice matrices; suppress common -D factor.
 J=P.row_join(Z) # unused preliminary object
 J=Z.row_join(P).col_join(P.row_join(Z))
 assert T*J*T.T==J
print('The forward/backward shear also preserves the reduced Poisson tensor.')
