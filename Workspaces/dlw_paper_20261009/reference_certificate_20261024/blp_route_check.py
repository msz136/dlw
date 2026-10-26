"""Exact BLP residual map and conservative original-data positivity bounds."""
from pathlib import Path
import json
import sympy as s
from flint import arb,ctx
x,z,t=s.symbols('x z t')
u=s.Function('u')(x,z,t);v=s.Function('v')(x,z,t)
U=-u/2;P=(v-s.diff(u,z)-4)/4
R1=s.diff(u,z,t)+s.diff(v,x,2)+s.diff(u*s.diff(u,z),x)
R2=s.diff(v,t)+s.diff(u,x,2,z)+s.diff(u*v-4*u,x)
B1=s.diff(U,z,t)-s.diff(U**2-s.diff(U,x),x,z)-2*s.diff(P,x,2)
B2=s.diff(P,t)-s.diff(P,x,2)-2*s.diff(U*P,x)
assert s.simplify(B1+R1/2)==0
assert s.simplify(B2-(R2-R1)/4)==0
assert s.simplify(4*P+4-2*s.diff(U,z)-v)==0
ctx.prec=256
k=arb.pi()/4
G=1+2*arb(-256).exp()/(1-arb(-2048).exp())
sine=arb('.03')*k+arb('.02')
gauss=(arb('.05')*k+arb('.03'))*G
assert G<arb('1.000001') and sine<arb('.07') and gauss<arb('.07')
C=arb('1.4')/(arb(1).exp()*arb('.1'))
lo=arb('3.93')*(-C/100).exp();hi=arb('4.07')*(C/100).exp()
assert lo>arb('3.73') and hi<arb('4.29')
out={'residual_equivalence':True,'inverse_map':True,
     'sine_initial_abs_u_z_plus_abs_v_bound':str(sine),
     'gaussian_initial_abs_u_z_plus_abs_v_bound':str(gauss),
     'conditional_small_ball_p_lower':str(lo),'conditional_small_ball_p_upper':str(hi),
     'literature_fulltext_read':False,
     'original_initial_value_problem_certified':False,'eta_u':None,'eta_v':None}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
