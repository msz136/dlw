import sympy as s
S1,S2,c1,c2,a,h=s.symbols('S1 S2 c1 c2 a h',nonzero=True,real=True)
p1=(S1+c1)/2;q1=(S1-c1)/2;p2=(S2+c2)/2;q2=(S2-c2)/2
A=(p1-p2)*(q1-q2)/((p1+q2)*(p2+q1))
A2=((S1-S2)**2-(c1-c2)**2)/((S1+S2)**2-(c1-c2)**2)
assert s.factor(A-A2)==0
# Chamber c1>c2: scattering Q shifts are -log A/S1,+log A/S2.
b1=-s.log(A)/S1;b2=s.log(A)/S2
assert s.factor(s.diff(b1,c2)/S2-s.diff(b2,c1)/S1)==0
print('PASS pairwise scattering shear is canonical on each fixed-S leaf')
C=[]
for n in [1,2,3]:C.append(s.expand(sum((p**n-(-q)**n)/n for p,q in [(p1,q1),(p2,q2)])))
assert s.expand(C[0]-S1-S2)==0
assert s.expand(C[1]-(S1*c1+S2*c2)/2)==0
assert s.expand(C[2]-(S1**3+S2**3)/12-(S1*c1*c1+S2*c2*c2)/4)==0
minor=s.factor(s.det(s.Matrix([[s.diff(C[n],c) for c in [c1,c2]] for n in [1,2]])))
assert s.factor(minor-S1*S2*(c2-c1)/4)==0
print('PASS C2,C3 independence determinant:',minor)
for name,ss,cc in [('Fig1a',[3],[-1]),('Fig1b',[1],[7]),('Fig3',[1,1],[11,7]),('Fig4',[3,1],[-1,7])]:
 print(name,'S',ss,'velocity',cc,'canonical momenta',[x*y for x,y in zip(ss,cc)],'H',sum(s.Rational(x)*y*y/2 for x,y in zip(ss,cc)))
 if len(ss)==2: print('spectral minor',minor.subs({S1:ss[0],S2:ss[1],c1:cc[0],c2:cc[1]}))
# Identity between physical time H and formal transmission coefficient C3.
print('PASS H=2*C3-sum(S_i^3)/6, and C2=sum(P_i)/2')
print('NOT a certificate of inheritance from the original field Poisson bracket.')
