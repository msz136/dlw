"""Verify an RHS identity only; no time integration or convergence claim."""
import json
from pathlib import Path
import sympy as s

a,c,r=s.symbols('a c r',positive=True)
def defect(C):
    return ((a/r+(C-a)*r)**2-C**2-c**2*(r*r-1))/2
original=s.simplify(defect(c)-a*c*(1-r*r)-a*a/2*(1/r-r)**2)
C=a+s.sqrt(c*c+a*a)
calibrated=s.simplify(defect(C)-a*a/2*(1/r-r)**2)
assert original==0 and calibrated==0
out={'scope':'same-state RHS algebra only; no evolution, positivity or convergence proof',
     'original_residual':str(original),'calibrated_residual':str(calibrated),
     'C_at_a_0p02_c_1':float(C.subs({a:.02,c:1})), 'passed':True}
Path(__file__).with_name('out').joinpath('parameter_calibration_identity.json').write_text(
    json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,indent=2))
