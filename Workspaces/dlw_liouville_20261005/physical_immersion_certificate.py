import sympy as s
h=s.Rational(1,8);a=s.Integer(2);d=h/2
E1,E2,c1,c2=s.symbols('E1 E2 c1 c2');EE=[E1,E2];cc=[c1,c2]
for name,SS,cv in [('Fig3',[1,1],[11,7]),('Fig4',[3,1],[-1,7])]:
 S=list(map(s.Integer,SS));p=[(S[i]+cc[i])/2 for i in range(2)];q=[(S[i]-cc[i])/2 for i in range(2)]
 gam=[-(p[i]-a+d)/(q[i]+a-d) for i in range(2)]
 chi=[(p[i]-a+d)*(q[i]+a+d)/((p[i]-a-d)*(q[i]+a-d)) for i in range(2)]
 A=(p[0]-p[1])*(q[0]-q[1])/((p[0]+q[1])*(p[1]+q[0]))
 def tau(w):return 1+w[0]*E1+w[1]*E2+A*w[0]*w[1]*E1*E2
 G=tau([1,1]);F=tau(gam);GN=tau(chi)
 D=lambda z:sum(S[i]*EE[i]*s.diff(z,EE[i]) for i in range(2))
 u=2*D(F)/F-D(G)/G-D(GN)/GN;W=4/h*(D(GN)/GN-D(G)/G)
 subsC=dict(zip(cc,cv));rows=[]
 for j in [0,1]:
  subs={**subsC,**{EE[i]:chi[i].subs(subsC)**j/S[i] for i in range(2)}}
  for z in [u,W]:
   row=[s.factor((-S[i]*EE[i]*s.diff(z,EE[i])).subs(subs)) for i in range(2)]
   row += [s.factor(((s.diff(z,cc[i])+sum(j*EE[k]*s.diff(chi[k],cc[i])/chi[k]*s.diff(z,EE[k]) for k in range(2)))/S[i]).subs(subs)) for i in range(2)]
   rows.append(row)
 J=s.Matrix(rows);det=s.factor(J.det());assert det!=0
 print(name,'rank=',J.rank(),'det=',det,'decimal=',s.N(det,12),flush=True)
print('PASS exact local physical immersion at both paper two-soliton examples, coordinates(Q1,Q2,P1,P2) with fixed S, theta=-log S, x=t=0 and j=0,1.')
