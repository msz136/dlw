import sympy as s
c,S,E=s.symbols('c S E',real=True);a=s.Integer(2);h=s.Rational(1,8);d=h/2;p=(S+c)/2;q=(S-c)/2
gam=-(p-a+d)/(q+a-d);chi=(p-a+d)*(q+a+d)/((p-a-d)*(q+a-d))
u=S*(2*gam*E/(1+gam*E)-E/(1+E)-chi*E/(1+chi*E));w=4*S/h*(chi*E/(1+chi*E)-E/(1+E))
J=s.Matrix([[-S*E*s.diff(z,E),s.diff(z,c)/S] for z in [u,w]])
Mu=s.log(((p-a)**2-d*d)/((q+a)**2-d*d));MW=4/h*s.log(chi)
for name,ss,cv in [('Fig1a',3,-1),('Fig1b',1,7)]:
 sub={S:ss,c:cv,E:s.Rational(1,ss)}
 det=s.factor(J.subs(sub).det());assert det!=0
 # New canonical bracket {Q,Mass}=partial Mass/partial P at fixed S.
 br1=s.factor((s.diff(Mu,c)/S).subs(sub));br2=s.factor((s.diff(MW,c)/S).subs(sub))
 assert br1!=0 and br2!=0
 print(name,'physical immersion det=',det,'{Q,Mu}=',br1,'{Q,MW}=',br2)
print('Thus neither mass is a Casimir of the new moduli tensor at these points.')
print('No direct Poisson restriction or Dirac reduction preserving admissible original mass Casimirs can equal this new tensor.')
print('This does not rule out a different boundary phase space in which those masses are not admissible Casimirs.')
