"""Exact algebra for two theory seeds; no PDE or empirical error tables."""
from pathlib import Path
import hashlib
import json
import sympy as s

HERE = Path(__file__).resolve().parent
P, Q, G, A, C, m, d, alpha, beta, e, k = s.symbols('P Q G A C m d alpha beta e k', nonzero=True)
checks = []

def zero(name, expression):
    residual = s.factor(s.cancel(expression))
    assert residual == 0, (name, residual)
    checks.append({'name': name, 'exact_residual': str(residual)})

L = 1/P + 1/Q
X = 1/P - 1/Q
B = (P**-2 - 1/(P*Q) + Q**-2) / 12
zero('normalized_phase_cubic', (P**-3 + Q**-3) / (12*L) - B)
zero('normalized_alpha_direction', (P**-2-Q**-2)/L-X)
cg = (G**2+G+1) / (12*(G+1)**2)
zero('fixed_Gamma_curvature', B.subs(P, -G*Q) - cg * X.subs(P, -G*Q)**2)
poly = C*A**2 + alpha*A + beta
zero('minimax_lower_bound_second_difference', poly.subs(A,m-d)-2*poly.subs(A,m)+poly.subs(A,m+d)-2*C*d**2)
candidate = poly.subs({alpha:-2*C*m, beta:C*m**2-C*d**2/2})
zero('minimax_attaining_polynomial', candidate - C*((A-m)**2-d**2/2))
zero('minimax_left_endpoint', candidate.subs(A,m-d)-C*d**2/2)
zero('minimax_midpoint', candidate.subs(A,m)+C*d**2/2)
zero('minimax_right_endpoint', candidate.subs(A,m+d)-C*d**2/2)

# Actual fourth-order centered derivative: coefficients for shifts -2,-1,+1,+2.
weights = [(-2,1),(-1,-8),(1,8),(2,-1)]
def q(parity):
    return (1+e*parity)/(1+e)
def r(parity):
    return 1/q(parity)
for parity in [1,-1]:
    dq = sum(w*q(parity*(s.Integer(-1)**shift)) for shift,w in weights)/(12*k)
    dr = sum(w*r(parity*(s.Integer(-1)**shift)) for shift,w in weights)/(12*k)
    zero(f'Nyquist_DQ_parity_{parity}', dq)
    zero(f'Nyquist_DR_parity_{parity}', dr)
    zero(f'physical_u_parity_{parity}', 2*dq/q(parity))
    zero(f'physical_W_parity_{parity}', 4*(1-q(parity)*r(parity)))
zero('gauge_Q0', q(1)-1)
zero('nongauge_difference', q(-1)-1+2*e/(1+e))

result = {
    'status':'passed', 'checks':checks, 'count':len(checks), 'new_pde_runs':0,
    'meaning':'两个理论种子的精确代数核对，不是完整研究命题或物理误差界的证明。',
    'T01_proof':[
        'C>0，d=(A_+−A_-)/2>0。若区间内|r|≤E，端点/中点二阶差分2Cd²≤4E，故E≥Cd²/2。',
        'alpha=−2Cm，beta=Cm²−Cd²/2时r=C[(A−m)²−d²/2]在区间内恰有sup|r|=Cd²/2。',
        '因此无约束常数的最佳一致剩余为C(A_+−A_-)²/8；受限可行集上它是下界，最优点可行时取等号。仅针对固定Gamma、同一可达半轴及远离极点的区间。',
    ],
    'T02_proof':[
        '偶数周期网格允许ζ_i=(−1)^i，±1及±2移位成对相等，所以D同时消去Q和R。',
        '|epsilon|<1保证Q,R为正，Q0=1；epsilon非零时Q的奇偶值不同，不能由常数规范消去。',
        'y各层取同一状态时delta_0 u=0，故v=W=0；取势m=0还给出静止族。',
        '仅证明该周期类上的非单射；不证明当前边界非单射、不同预像具有不同物理速度或隐藏方向不稳定。',
    ],
    'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
(HERE/'theory_seed_checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':result['status'],'count':len(checks),'new_pde_runs':0},ensure_ascii=False))
