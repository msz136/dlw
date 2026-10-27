"""Independent off-shell identities supporting the finite-Darboux audit."""
from pathlib import Path
import json
import sympy as s
x,z=s.symbols('x z',real=True)
Q=s.Function('Q')(x,z);P=s.Function('P')(x,z)
psi=s.Function('psi')(x,z)
def L(f,q=Q,p=P):return s.diff(f,x,z)+q*s.diff(f,z)+p*f
qplus=Q+s.diff(P,x)/P
pplus=P+s.diff(qplus,z)
forward=L(s.diff(psi,z)/P,qplus,pplus)-s.diff(L(psi)/P,z)
K=P-s.diff(Q,z)
qminus=Q-s.diff(K,x)/K
inverse=L(s.diff(psi,x)+Q*psi,qminus,K)-s.diff(L(psi),x)-qminus*L(psi)
checks={'forward_Laplace_off_shell':s.cancel(s.together(forward))==0,
        'inverse_Laplace_off_shell':s.cancel(s.together(inverse))==0}
bn=s.Function('b')(x,z)
top=s.diff(bn,x)+Q*bn
relation=s.diff(top,z)
checks['pure_z_low_coefficient']=s.simplify(L(bn)-relation-K*bn)==0
assert all(checks.values())
result={'checks':checks,'all_passed':True,
        'meaning':'Independent exact identities; construction-class obstruction only.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
