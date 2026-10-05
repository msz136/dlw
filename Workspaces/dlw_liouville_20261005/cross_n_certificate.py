import sympy as s
S,T,c,b,a,h,z=s.symbols('S T c b a h z', real=True)
r=c-2*a
gamma=-(S+r+h)/(S-r-h)
chi=((S+h)**2-r*r)/((S-h)**2-r*r)
A=((S-T)**2-(c-b)**2)/((S+T)**2-(c-b)**2)
assert s.factor(gamma.subs(S,0)-1)==0
assert s.factor(chi.subs(S,0)-1)==0
assert s.factor(A.subs(T,0)-1)==0
print('PASS zero-strength gamma=chi=A_interaction=1 away from stated poles')
for k in range(1,13):
 C=s.expand((((S+c)/2)**k-((c-S)/2)**k)/k)
 assert C.subs(S,0)==0
 assert s.rem(C,S,S)==0
print('PASS C1..C12 polynomial divisibility by S; general argument: odd in S')
assert (S*c*c/2).subs(S,0)==0
p=(S+c)/2;q=(S-c)/2
assert s.factor(((z+q)/(z-p)).subs(S,0)-1)==0
print('PASS H vanishes and rational transmission factor becomes identity')
# Explicit subset tau recurrence at N=3, with the third mode inactive.
E=s.symbols('E1:4');g=s.symbols('g1:4');ch=s.symbols('ch1:4')
A12,A13,A23=s.symbols('A12 A13 A23')
def tau(weights):
 t=[weights[i]*E[i] for i in range(3)]
 return 1+sum(t)+A12*t[0]*t[1]+A13*t[0]*t[2]+A23*t[1]*t[2]+A12*A13*A23*t[0]*t[1]*t[2]
for name,w in [('G',[1,1,1]),('F',g),('Gnext',ch)]:
 res=s.expand(tau(w).subs({g[2]:1,ch[2]:1,A13:1,A23:1})-(1+E[2])*(1+w[0]*E[0]+w[1]*E[1]+A12*w[0]*w[1]*E[0]*E[1]))
 assert res==0
print('PASS all three tau polynomials acquire the same x,j-independent factor')
# Poisson-algebra boundary test: a compatible observable is F0 + S*f1.
th,cc,q0,p0=s.symbols('theta c Q0 P0');F0=s.Function('F0')(q0,p0);G0=s.Function('G0')(q0,p0)
f=s.Function('f')(S,th,cc,q0,p0);g1=s.Function('g')(S,th,cc,q0,p0)
F=F0+S*f;G=G0+S*g1
PB=lambda x,y:s.diff(x,q0)*s.diff(y,p0)-s.diff(x,p0)*s.diff(y,q0)-s.diff(x,th)*s.diff(y,cc)+s.diff(x,cc)*s.diff(y,th)
assert s.simplify(PB(F,G).subs(S,0)-PB(F0,G0))==0
print('PASS arbitrary smooth zero-strength-compatible observable brackets restrict correctly')
# Obstruction for amplitude deletion with fixed S>0.
print('Amplitude deletion: delta C1=S; hence C1 cannot descend continuously to a ghost-free lower stratum for fixed nonzero S.')
