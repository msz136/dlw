import sympy as s
U=s.symbols('U0:7');g=s.symbols('g0:7');fields=[U,g]
nextjet={v[k]:v[k+1] for v in fields for k in range(6)}
def D(f):return s.expand(sum(s.diff(f,v)*n for v,n in nextjet.items() if v in f.free_symbols))
def DD(f,n):
 for _ in range(n):f=D(f)
 return f
def mul(A,B):
 out={}
 for i,a in A.items():
  for j,b in B.items():
   for k in range(max(0,i+j+5)+1):
    n=i+j-k
    if n<-5:continue
    out[n]=out.get(n,0)+s.binomial(i,k)*a*DD(b,k)
 return {n:s.expand(v) for n,v in out.items()}
cs=[None,-g[0]];b=(U[0]-g[0])/2
for n in range(1,5):cs.append(s.expand(b*cs[-1]-D(cs[-1])))
A={-n:cs[n] for n in range(1,6)};power={0:s.Integer(1)};k5=0
for n in range(1,6):
 power=mul(power,A);k5+=s.Rational((-1)**(n+1),n)*power.get(-5,0)
k5=s.expand(k5)
local=-U[0]**4*g[0]/16-s.Rational(3,4)*U[0]**2*g[0]*U[1]+g[0]*U[1]**2/4+U[0]*U[1]*g[1]-U[1]*g[2]/2-U[0]**2*g[0]**3/8-g[0]**5/80-g[0]**3*U[1]/12+g[0]*g[1]**2/4
rem=s.expand(k5-local-g[0]*g[1]**2/6)
for vs in fields:
 ev=sum(((-1)**n)*DD(s.diff(rem,v),n) for n,v in enumerate(vs))
 assert s.expand(ev)==0
print('Single-site log coefficient k5 matches -h q5_local/64 + g gx^2/6 modulo Dx.')
# The fourth-order single-site coefficient has no extra local correction.
power={0:s.Integer(1)};k4=0
for n in range(1,5):
 power=mul(power,A);k4+=s.Rational((-1)**(n+1),n)*power.get(-4,0)
local4=-U[0]**3*g[0]/8-U[0]*g[0]**3/8-s.Rational(3,4)*U[0]*g[0]*U[1]+U[1]*g[1]/2
for vs in fields:
 ev=sum(((-1)**n)*DD(s.diff(s.expand(k4-local4),v),n) for n,v in enumerate(vs))
 assert s.expand(ev)==0
print('Single-site k4 matches -3h q4_local/32 modulo Dx.')

# General nested BCH identity, checked as ordinary polynomial identity; a sum-index proof is recorded.
for N in range(1,8):
 gs=s.symbols('g:'+str(N));fs=s.symbols('f:'+str(N));R=s.Matrix(N,N,lambda i,j:s.sign(i-j)/2);Rf=R*s.Matrix(fs)
 nested=0
 for i in range(N):
  for j in range(i):
   nested+=s.Rational(1,3)*((gs[i]+gs[j])*fs[i]*fs[j]-gs[j]*fs[i]**2-gs[i]*fs[j]**2)
   for k in range(j):nested+=s.Rational(2,3)*(2*gs[j]*fs[i]*fs[k]-gs[k]*fs[i]*fs[j]-gs[i]*fs[j]*fs[k])
 expected=-2*sum(gs[i]*Rf[i]**2 for i in range(N))+sum(gs)*sum(fs)**2/6-sum(gs[i]*fs[i]**2 for i in range(N))/6
 assert s.expand(nested-expected)==0
print('Nested BCH cubic identity checked N=1..7; general proof by coefficient classes.')
