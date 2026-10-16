from pathlib import Path
import json
import sympy as s

checks={}
mu,lam=s.symbols('mu lam')
J=s.diag(s.Rational(2,3),-s.Rational(1,3),-s.Rational(1,3))
Q=s.Matrix(3,3,s.symbols('q0:9'))
W=s.Matrix(3,3,s.symbols('w0:9'))
comm=lambda A,B:A*B-B*A
A_mu=mu*J+Q; A_lam=lam*J+Q
G=-W/(lam-mu)
G_s=-comm(A_mu,W)/(lam-mu)
checks['dimension_three_cauchy_generator_sign']=s.simplify(G_s-comm(A_lam,G)-comm(J,W))==s.zeros(3)
T=s.Matrix([[1,1,0],[0,1,1],[1,0,1]])
Pp=T*s.diag(1,0,0)*T.inv();Pm=T*s.diag(0,1,0)*T.inv()
P=Pp+Pm;V=(Pp-Pm)/2
checks['cluster_projector']=P*P==P
checks['half_projector_square']=V*V==P/4
t=s.symbols('t')
E=s.eye(3)+2*s.sinh(t/2)*V+4*(s.cosh(t/2)-1)*V*V
checks['exponential_solves_transport']=s.simplify(s.diff(E,t)-V*E)==s.zeros(3)
D=s.simplify(E.subs(t,2*s.pi*s.I))
checks['two_pi_jump']=D==s.eye(3)-2*P
checks['two_pi_jump_invertible']=D*D==s.eye(3)
a,b,c,d,v11,v12,v21,v22=s.symbols('a b c d v11 v12 v21 v22')
M=s.Matrix([[a,b],[c,d]]);K=s.Matrix([[v11,v12],[v21,v22]])
Md=comm(K,M)
checks['norming_plus']=s.expand(Md[0,1]-((v11-v22)*b-v12*(a-d)))==0
checks['norming_minus']=s.expand(Md[1,0]-(-(v11-v22)*c+v21*(a-d)))==0
delta_dot=Md[0,0]-Md[1,1]
checks['corrected_product']=s.expand(Md[0,1]*c+b*Md[1,0]+(a-d)*delta_dot/2)==0
checks['scalar_free_discriminant']=s.simplify((b*c+(a-d)**2/4)/M.det()-((s.trace(M)**2)/(4*M.det())-1))==0
f1,f2,f3,u0,u1,u2=s.symbols('f1 f2 f3 u0 u1 u2',nonzero=True)
aa=s.Matrix([[f1,f2]]);bb=s.Matrix([f2,f3]);HH=s.Matrix([[f1,f2],[f3,f1]])
Us=s.diag(u1,u2);Uf=s.diag(u0,u1,u2);Qf=u0*Us.inv()
block=s.Matrix([[lam,f1,f2],[f2,f1,f2],[f3,f3,f1]])
conj=Uf*block*Uf.inv()
checks['constant_frame_top']=conj[:1,1:]==aa*Qf
checks['constant_frame_slow']=conj[1:,1:]==Qf.inv()*HH*Qf
assert all(checks.values()),checks
result={'checks':checks,'passed':sum(checks.values()),'scope':'Exact matrix identities only. Actual DLW periodic return requires the analytic loop existence, Cauchy gluing and original physical slice proof.'}
Path(__file__).with_name('period_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
