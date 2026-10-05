"""Dimension-free determinant calculation for smooth multi-pair seeds.
U=S^-1; c=f^T U r; alpha=f^T U g; b=f_x^T U r;
d=f_x^T U g; e=f^T U g_x; z=f_xx^T U r.
r_x=g+delta*r. All identities hold for arbitrary matrix size.
"""
import sympy as s
a,delta,c,alpha,b,d,e,z=s.symbols('a delta c alpha b d e z')
alpha_x=d+e-alpha**2
c_x=b+alpha+(delta-alpha)*c
b_x=z+d+delta*b-d*c
c_xx=b_x+alpha_x+(delta-alpha)*c_x-alpha_x*c
c_t=-z+(alpha-2*a)*b+e+(delta-2*a)*alpha+(delta**2-2*a*delta+2*a*alpha-e)*c
res=s.expand(-c_xx-c_t+2*(1-c)*alpha_x-2*(a-delta)*c_x)
assert res==0
print('PASS: dimension-free B_(a-delta)(det(S-r f^T),det S)=0')
print('Second pair follows using S_next, f_next and delta -> -delta:')
print('S_next-r f_next^T = S-r f^T, r_x=g_next-delta*r.')
print('Algebra requires invertible S; the regular domain guarantees it.')
