import sympy as s
S,th,c=s.symbols('S theta c')
f=s.Function('f')(S,th,c);g=s.Function('g')(S,th,c);h=s.Function('h')(S,th,c)
B=lambda u,v:-S*(s.diff(u,th)*s.diff(v,c)-s.diff(u,c)*s.diff(v,th))
canonical=lambda u,v:-(s.diff(u,th)*s.diff(v,c)-s.diff(u,c)*s.diff(v,th))
assert s.expand(canonical(S*f,S*g)-S*B(f,g))==0
assert s.expand(B(f,B(g,h))+B(g,B(h,f))+B(h,B(f,g)))==0
assert s.expand(B(f,c*c/2)+S*c*s.diff(f,th))==0
for k in range(1,13):
 numerator=s.expand((((S+c)/2)**k-((c-S)/2)**k)/k)
 b=s.cancel(numerator/S);assert s.denom(b).is_number
 assert s.expand(b.subs(S,0)-(c/2)**(k-1))==0
print('PASS canonical finite atoms = N-independent moment bracket')
print('PASS arbitrary-function Jacobi identity for mark-space Poisson bracket')
print('PASS common Hamiltonian generates theta_t=-S*c')
print('PASS hierarchy test functions have polynomial zero-strength extension (orders1..12)')
