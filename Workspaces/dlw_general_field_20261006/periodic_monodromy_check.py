import sympy as s
x=s.symbols('x');B,d=s.symbols('B d',nonzero=True);b=s.Function('b')(x)
lo=-7

def mul(A,C,low=lo):
 out={}
 for i,f in A.items():
  for j,g in C.items():
   for k in range(max(0,i+j-low)+1):
    p=i+j-k
    if p<low:continue
    c=s.binomial(i,k)
    if c==0:continue
    out[p]=out.get(p,0)+c*f*s.diff(g,x,k)
 return {i:s.expand(v) for i,v in out.items() if v!=0}
def add(A,C):
 out=A.copy()
 for i,f in C.items():out[i]=s.expand(out.get(i,0)+f)
 return out

def invfirst(w):
 out={-1:s.Integer(1)}
 for n in range(2,-lo+1):out[-n]=s.expand(w*out[-n+1]-s.diff(out[-n+1],x))
 return out
p0=B+b-d;m0=B+b+d;p1=B-b-d;m1=B-b+d
M=mul(mul(mul(invfirst(p1),{1:1,0:-m1}),invfirst(p0)),{1:1,0:-m0})
T=add(M,{0:-1})
L=add({1:1,0:-B+2*d},mul({0:-(b-d)},mul(invfirst(B),{0:b+d})))
prod=mul(T,L)
for n in range(0,-5,-1):
 residual=s.simplify(prod.get(n,0)-(-4*d if n==0 else 0))
 print(n,residual)
 assert residual==0
print('Two-site monodromy inverse identity checked through D^-4.')
print('M1=',s.simplify(M[-1]));print('M2=',s.simplify(M[-2]))
# First residue on this constrained slice.
print('res of L shifted to leading D=',s.factor(L[-1]))
