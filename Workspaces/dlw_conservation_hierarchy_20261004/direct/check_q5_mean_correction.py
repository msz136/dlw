"""Mean correction required by Q5 under the periodic original flow."""
import sympy as s
import json
from pathlib import Path
u=s.symbols('u0:7');w=s.symbols('w0:7');beta=s.symbols('beta')
D=lambda f:s.expand(sum(s.diff(f,u[i])*u[i+1]+s.diff(f,w[i])*w[i+1] for i in range(6)))
e0=u[0]**2*w[0]/2+beta*w[0]**3/3+w[0]*u[1]
B0=u[0]**2/2+beta*w[0]**2+u[1];C=u[0]*w[0]-w[1]
qu0=4*w[0]*u[0]**3-12*u[0]**2*w[1]+8*w[0]*u[2]+8*w[1]*u[1]+16*u[0]*w[2]-8*w[3]+8*beta*u[0]*w[0]**3-8*beta*w[0]**2*w[1]
fe0=-B0*C-w[0]*D(B0)
S=s.expand(qu0+8*fe0+16*D(e0))
print('local S=',S)
assert s.expand(S-16*D(D(u[0]*w[0]))+8*w[3])==0
out={'local_S':str(S),'S_sum_mean':'16 D² Π(Uw) −8 D³ Πw +8 Π(w_x Rw_x)=0',
     'corrected_Q5':'Q5 − (8 h N/c) integral_x (Pi e)^2',
     'condition':'full-flow Q5 conservation remains to be structurally certified separately'}
Path(__file__).with_name('q5_mean_correction.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
