"""Symbolic dispersion comparison, exact quadratic error identities, local theorem notes."""
from pathlib import Path
import json
import sympy as s
HERE=Path(__file__).resolve().parent
k,l,h,a,c,kap=s.symbols('k l h a c kap',real=True,nonzero=True)
d=2*s.sin(l*h/2)/h;m=s.cos(l*h/2);q=s.sin(l*h)/h
A=a+c*h*h;r=1+kap*h*h
B=k*h*h*r/4-k*k*m/d
alpha=k*k+B*q
Msd=s.Matrix([[alpha-2*s.I*A*k,s.I*B],[s.I*(4*r*k+q*(k*k+alpha)),-alpha-2*s.I*A*k]])
Mfd=s.Matrix([[-2*s.I*a*k,-s.I*k*k*m/d],[s.I*(k*k*q+4*k),-2*s.I*a*k]])
Dsd=k**4+4*r*k**3*m/d-r*r*k*k*h*h
Dfd=k**4*m*m+4*k**3*m/d
checks={}
def eq(name,x):
    val=s.simplify(s.trigsimp(x));checks[name]=str(val);assert val==0,(name,val)
eq('sd_trace',s.trace(Msd)+4*s.I*A*k)
eq('fd_trace',s.trace(Mfd)+4*s.I*a*k)
eq('sd_discriminant',(s.trace(Msd)/2)**2-Msd.det()-Dsd)
eq('fd_discriminant',(s.trace(Mfd)/2)**2-Mfd.det()-Dfd)
D0=k**4+4*k**3/l
Cfd=-k**4*l*l/4-k**3*l/3
Csd=-k**3*l/3-k*k+4*kap*k**3/l
eq('fd_h2',s.expand(s.series(Dfd,h,0,3).removeO()).coeff(h,2)-Cfd)
eq('sd_h2',s.expand(s.series(Dsd,h,0,3).removeO()).coeff(h,2)-Csd)
b=s.symbols('b',real=True)
factor=(b*b/4-1)*(b*b/4+2*b/3+1)
eq('advantage_factor',(b/3+b*b/4)**2-(b/3+1)**2-factor)
eq('positive_second_factor',b*b/4+2*b/3+1-((b+s.Rational(4,3))**2/4+s.Rational(5,9)))
M0=s.Matrix([[-2*s.I*a*k,-s.I*k*k/l],[s.I*(k*k*l+4*k),-2*s.I*a*k]])
leading_sd=Msd.applyfunc(lambda x:s.expand(s.series(x,h,0,3).removeO()).coeff(h,2))
leading_fd=Mfd.applyfunc(lambda x:s.expand(s.series(x,h,0,3).removeO()).coeff(h,2))
diag=(k*k*l*l+k*l)/4
expected_sd=s.Matrix([[diag-2*s.I*c*k,s.I*(k*k*l/12+k/4)],
                     [s.I*(4*kap*k+k*k*l**3/12+k*l*l/4),-diag-2*s.I*c*k]])
for i in range(2):
    for j in range(2):eq(f'sd_matrix_h2_{i}{j}',leading_sd[i,j]-expected_sd[i,j])
out=dict(checks=checks,M0=str(M0),M2sd=str(leading_sd),M2fd=str(leading_fd),
         fd_discriminant=str(Dfd),sd_discriminant=str(Dsd),fd_h2=str(Cfd),sd_h2=str(Csd),
         inequality_factor=str(factor),original_oscillatory_advantage='-4 < k*l < -2, fixed wave numbers, h -> 0, c=kappa=0',
         limitation='Eigenfrequency leading error only; physical-field propagator includes eigenvector errors. No nonlinear total-error implication.')
(HERE/'symbolic.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(f'{len(checks)} symbolic identities passed')

