"""Exact positive-coefficient certificate for F2 monotonicity on [0,2/5]."""
from pathlib import Path
import hashlib,json
import sympy as S

BASE=Path(__file__).resolve().parents[1]

def main():
    q,a,r,x,y=S.symbols('q a r x y')
    N=lambda z:r*z**4-2*z**4-20*z**3+2*r*z*z-28*z*z+20*z+r+14
    D=lambda z:2*(z-1)*(z+1)*(z*z-2*z-1)
    K=S.cancel((N(q)*D(a)-N(a)*D(q))/(a-q))
    P=S.Poly(S.expand((K/4).subs({q:S.Rational(2,5)*x,a:S.Rational(2,5)*y})),x,y)
    coefficients=[[S.factor(sum(P.coeff_monomial(x**k*y**l)*S.binomial(i,k)/S.binomial(3,k)*S.binomial(j,l)/S.binomial(3,l) for k in range(i+1) for l in range(j+1))) for j in range(4)] for i in range(4)]
    coeff_scaled=[[S.expand(140625*(z-3)) for z in row] for row in coefficients]
    vertices=[S.Rational(7,5),S.Rational(3,2)]
    lower=min(b.subs(r,v) for row in coefficients for b in row for v in vertices)
    assert lower>3
    expansion=sum(coeff_scaled[i][j]*S.binomial(3,i)*S.binomial(3,j)*(5*q)**i*(2-5*q)**(3-i)*(5*a)**j*(2-5*a)**(3-j) for i in range(4) for j in range(4))
    assert S.expand(2250000*(K-12)-expansion)==0
    H=S.factor(N(q)*S.diff(D(q),q)-S.diff(N(q),q)*D(q))
    Hp=S.Poly(S.expand(H.subs(q,S.Rational(2,5)*x)),x)
    hb=[S.factor(sum(Hp.nth(k)*S.binomial(i,k)/S.binomial(6,k) for k in range(i+1))) for i in range(7)]
    assert all(b.subs(r,v)>0 for b in hb for v in vertices)
    record={'scope':'Exact polynomial identities and Bernstein positivity for the conditional F2 support function; no unrestricted packing claim.','script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'source_manifest_sha256':hashlib.sha256((BASE/'references/n37/source_manifest.json').read_bytes()).hexdigest(),'domain':{'q':['0','2/5'],'a':['0','2/5'],'r':['7/5','3/2']},'N':str(N(q)),'D':str(D(q)),'K':str(S.factor(K)),'difference_identity':'N(q)D(a)-N(a)D(q)=(a-q)K(q,a,r)','bernstein_basis':'B_i^3(x)=binomial(3,i)*x^i*(1-x)^(3-i), x=5q/2,y=5a/2; K/4=sum(b_ij*B_i^3(x)*B_j^3(y))','bernstein_K_over_4':[[str(z) for z in row] for row in coefficients],'smallest_coefficient_at_r_vertices':str(lower),'coefficient_lower_bound':3,'K_lower_bound':12,'integer_identity':'2250000*(K-12)=sum(T_ij*binomial(3,i)*binomial(3,j)*(5q)^i*(2-5q)^(3-i)*(5a)^j*(2-5a)^(3-j))','integer_T':[[str(z) for z in row] for row in coeff_scaled],'integer_identity_exact':True,'integer_T_at_r_vertices':[[[str(z.subs(r,v)) for z in row] for row in coeff_scaled] for v in vertices],'minus_derivative_numerator_H':str(H),'derivative_H_bernstein_on_q_interval':[str(z) for z in hb],'all_coefficients_positive':True}
    (BASE/'analysis/n37_bernstein_support.json').write_text(json.dumps(record,indent=2),encoding='utf8')
    print('min b',lower,'identity exact, K >= 12')
    print('T matrix:')
    for row in coeff_scaled:print(row)

if __name__=='__main__':main()
