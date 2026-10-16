from pathlib import Path
import json
import sympy as s

checks = {}
k = s.symbols('k', positive=True)
R = s.Matrix([[0, -1/k], [1/k, 0]])
zero = s.zeros(2)
A = (-16/s.sqrt(1+k*k))*zero.row_join(R).col_join(R.row_join(zero))
checks['fourier_skew'] = A.T + A == s.zeros(4)
checks['fourier_singular_values'] = s.simplify(A.T*A - 256/(k*k*(1+k*k))*s.eye(4)) == s.zeros(4)
q,p,c = s.symbols('q p c', positive=True)
P = q*p
Q = c*s.log(q/p)/2
bracket = lambda f,g: s.simplify((s.diff(f,q)*s.diff(g,p)-s.diff(f,p)*s.diff(g,q))/c)
checks['weak_pair_conjugacy'] = bracket(Q,P) == 1
checks['weak_pair_form_pullback'] = s.simplify(s.det(s.Matrix([[s.diff(Q,q),s.diff(Q,p)],[s.diff(P,q),s.diff(P,p)]]))-c) == 0
i1,i2,t1,t2 = s.symbols('i1 i2 t1 t2')
xs=s.Matrix([t1,t2,i1,i2])
ys=s.Matrix([t1,t2-2*i2*t1,i1+i2**2,i2])
J=s.zeros(4)
J[:2,2:]=s.eye(2)
J[2:,:2]=-s.eye(2)
B=ys.jacobian(xs)
checks['coupled_actions_canonical'] = s.simplify(B*J*B.T-J)==s.zeros(4)
n=s.symbols('n', integer=True, positive=True)
# At q_n=p_n=exp(-n^2), for I_n=q_n*p_n/n^2 the row norm is sqrt(2)*exp(-n^2)/n^2.
row=s.sqrt(2)*s.exp(-n*n)/(n*n)
right=n*n*s.exp(n*n)/s.sqrt(2)
checks['finite_section_inverse_lower_bound'] = s.simplify(row*right)==1
L,gamma,omega,Gplus,Gminus=s.symbols('L gamma omega Gplus Gminus', nonzero=True)
gquad=-4*Gplus*Gminus/gamma**2
Aquad=s.simplify(-L*gamma*gquad/(4*omega))
checks['reciprocal_period_quadratic'] = s.simplify(Aquad-L*Gplus*Gminus/(omega*gamma))==0
vp,vm=s.symbols('vp vm')
C=L*omega*gamma
Aphysical=vp*vm/C
checks['period_unit_plus_torque'] = s.simplify(C*s.diff(Aphysical,vm)-vp)==0
checks['period_unit_minus_torque'] = s.simplify(-C*s.diff(Aphysical,vp)+vm)==0
z,eps,a,b=s.symbols('z eps a b', nonzero=True)
# Local crossing: κ=(L/2)*sqrt(gamma^2*z^2+4*eps^2*a*b), with the background sheet sqrt(gamma^2*z^2)=gamma*z.
kappa2=L*a*b/(gamma*z)
weight=(1/omega)+(z*s.Symbol('weight_slope'))
checks['period_residue_crossing'] = s.simplify(s.residue(kappa2*weight,z,0)-L*a*b/(gamma*omega))==0
assert all(checks.values()), checks
out={'checks':checks,'passed':sum(checks.values()),'scope':'Exact algebra only; no DLW flow or infinite spectral inverse certified.'}
Path(__file__).with_name('validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False))
