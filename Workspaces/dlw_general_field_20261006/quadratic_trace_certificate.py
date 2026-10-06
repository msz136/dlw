import sympy as s
z,e,k,B,d=s.symbols('z e k B d',real=True)
F=lambda z:z+d*d/(z-B)
A=lambda K,z:d*s.Rational(1,2)*(1/(z+s.I*K-B)-1/(z-B))
L20=-s.Rational(1,4)*(1/(z+s.I*k-B)+1/(z-s.I*k-B))
def res(expr):
 return s.expand(s.series(expr.subs(z,1/e),e,0,2).removeO()).coeff(e,1)
for n in [1,3,5]:
 # normalized trace 1/n. Divide total integral by pi to compare polynomial symbols.
 expr=F(z)**(n-1)*L20
 if n>1:
  for j in range(n-1):
   for K in [k,-k]:expr+=s.Rational(1,2)*A(K,z-s.I*K)*F(z-s.I*K)**j*A(-K,z)*F(z)**(n-2-j)
 ans=s.simplify(2*res(expr))
 print(n,s.factor(ans),flush=True)
 assert s.Poly(ans,k).degree()==n-1
 assert s.expand(ans).coeff(k,n-1)==(-1)**((n+1)//2)
 if n==3:assert s.expand(ans-(k*k-B*B-2*d*d))==0
 if n==5:assert s.expand(ans-(-k**4+(6*B*B+6*d*d)*k*k-(B**4+12*B*B*d*d+6*d**4)))==0
print('Symbolic quadratic certificates passed.')
