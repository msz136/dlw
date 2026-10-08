import importlib.util
import json
from fractions import Fraction as F
from pathlib import Path
import sympy as s

root=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('gram_audit',root/'Workspaces/dlw_semidiscrete/verify_gram_reassessment.py')
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
k,z,mu,nu,e1,e2,ss=s.symbols('k z mu nu e1 e2 ss')
kx=mu+nu-k*k
zx=k*(1-z)-ss*z+e1
e1x=nu*(1-z)-ss*e1+e2
zt=mu*(1-z)-ss*k+ss*ss*z-e2+e1*k
zxx=kx*(1-z)-k*zx-ss*zx+e1x
assert s.expand(zxx+zt+2*ss*zx-2*kx*(1-z))==0
p,q,a,d=s.symbols('p q a d')
chi=(p-a+d)*(q+a+d)/((p-a-d)*(q+a-d))
gamma=-(p-a+d)/(q+a-d)
assert s.factor(gamma*(q+a-d)+p-a+d)==0
assert s.factor(gamma*(q+a+d)+chi*(p-a-d))==0
cases=0
for N in range(1,6):
    for h in (F(1,2),F(1,8)):
        g=mod.Gram(N,8,h)
        for j in (-2,0,3):
            f=g.tau(1,j,g.a-h/2)
            assert mod.bil(f,g.tau(0,j,g.a),g.a-h/2)=={}
            assert mod.bil(f,g.tau(0,j+1,g.a),g.a+h/2)=={}
            assert f==g.tau(1,j+1,g.a+h/2)
            if N<=3:
                assert f==g.matrix_tau(1,j,g.a-h/2)
            cases+=1
result={'scalar_identity':'exact zero','one_soliton_both_equations':'exact zero','N_values':[1,2,3,4,5],'parameter_site_cases':cases,'bilinear_residuals':'all coefficients exactly zero','shift_identity':'pass','determinant_vs_subset_N_le_3':'pass'}
Path(__file__).with_name('validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result))
