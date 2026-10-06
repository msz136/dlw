from pathlib import Path
import sympy as s
k,h,c,V,q,lam=s.symbols('k h c V cot_theta_half lambda',real=True)
R=-s.I*h*q/2
beta=h*h/32
A=s.Matrix([[k*k-s.I*V*k,-2*s.I*beta*c*k+k*k*R],[-s.I*c*k,-k*k-s.I*V*k]])
disc=k**4-h*c*q*k**3/2-h*h*c*c*k*k/16
res=s.factor((lam*s.eye(2)-A).det()-((lam+s.I*V*k)**2-disc))
assert res==0
print('Characteristic identity:',res)
print('lambda = -i V k +/- sqrt(',disc,')')
print('For any fixed lattice mode theta != 0: lambda_plus/k^2 -> 1 as |k| -> infinity.')
