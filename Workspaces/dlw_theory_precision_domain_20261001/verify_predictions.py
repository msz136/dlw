"""Small, frozen modal checks. Does not import or execute any PDE solver."""
from pathlib import Path
import hashlib
import json
import mpmath as mp

HERE = Path(__file__).resolve().parent
mp.mp.dps = 420
T = mp.mpf(1)/8
registry = HERE / "PREDICTIONS.json"

def gamma(n):
    return mp.sqrt(n**4 + 4*n**3)

def symbol(n, k):
    return (8*mp.sin(n*k)-mp.sin(2*n*k))/(6*k)

def propagator(n):
    B = mp.matrix([[0, n*n], [n*n+4*n, 0]])
    g = gamma(n)
    if not g:
        return mp.eye(2)+T*B
    return mp.cosh(T*g)*mp.eye(2)+mp.sinh(T*g)/g*B

def norm(A):
    if A.cols == 1:
        return mp.sqrt(sum(abs(x)**2 for x in A))
    F = sum(abs(x)**2 for x in A)
    det2 = abs(mp.det(A))**2
    return mp.sqrt((F+mp.sqrt(max(mp.mpf(0),F*F-4*det2)))/2)

def number(x):
    return mp.nstr(x, 18)

checks = []
for n0 in [10,20,40,80]:
    n = mp.mpf(n0)
    k = n**-2
    g = gamma(n)
    gd = gamma(symbol(n,k))
    delta_E = n**-4
    delta_R = n**-3
    e = mp.log1p(delta_E*g)/delta_E
    z = delta_R*g
    q = 1+z+z*z/2+z**3/6+z**4/24
    r = mp.log(q)/delta_R
    checks.append({"n":n0, "space_ratio":number((g-gd)/(k**4*n**6)),
                   "Euler_ratio":number((g-e)/(delta_E*n**4)),
                   "RK4_ratio":number((g-r)/(delta_R**4*n**10)),
                   "gamma_minus_center":number(g-(n+1)**2)})

# Uniform operator indication in centered Gaussian r=1/4 to L2.
# The Fourier projection tail is bounded analytically in the proof.
gaussian = []
previous = None
for N in [64,128,256,512]:
    k = 2*mp.pi/N
    largest = mp.mpf(0)
    witness = None
    for n0 in range(-N//2+1, N//2):
        n = mp.mpf(n0)
        A = mp.exp(-(n+1)**2/4)*(propagator(symbol(n,k))-propagator(n))
        value = norm(A)
        if value > largest:
            largest, witness = value, n0
    gaussian.append({"N":N,"k":number(k),"operator_error":number(largest),
                     "error_over_k4":number(largest/k**4),"maximizing_mode":witness,
                     "refinement_ratio":number(previous/largest) if previous else None})
    previous = largest

bandwidth = []
for c in [4,8]:
    for m in [32,64,128,256]:
        k = 2*mp.pi/mp.power(2,m)
        L = mp.log(1/k)
        K = int(mp.floor(c*mp.sqrt(L)))
        n = mp.mpf(K)
        g = gamma(n)
        v = mp.matrix([1,g/n**2])
        v /= norm(v)
        error = norm((propagator(symbol(n,k))-propagator(n))*v)
        predicted = T*g+4*mp.log(k)+6*mp.log(n)+mp.log(T/15)
        bandwidth.append({"c":c,"log2_N":m,"K":K,"log_error":number(mp.log(error)),
                          "leading_log_prediction":number(predicted),
                          "log_difference":number(mp.log(error)-predicted),
                          "relative_error":number(error/mp.exp(T*g))})

# Algebraic maximum and exact Nyquist check; no optimization scan.
theta = mp.acos(1-mp.sqrt(6)/2)
f = (8*mp.sin(theta)-mp.sin(2*theta))/6
maximum_error = f*f-(mp.mpf(1)/4+2*mp.sqrt(6)/3)
nyquist_error = symbol(mp.pi,mp.mpf(1))

passed = (abs(maximum_error)<mp.mpf('1e-390') and abs(nyquist_error)<mp.mpf('1e-390')
          and all(float(row['space_ratio'])>1/15 for row in checks)
          and abs(float(checks[-1]['space_ratio'])-1/15)<.002
          and abs(float(checks[-1]['Euler_ratio'])-.5)<.025
          and abs(float(checks[-1]['RK4_ratio'])-1/120)<.002
          and float(gaussian[-1]['refinement_ratio'])>15.8
          and all(float(bandwidth[i+1]['log_error'])<float(bandwidth[i]['log_error']) for i in range(3))
          and all(float(bandwidth[i+1]['log_error'])>float(bandwidth[i]['log_error']) for i in range(4,7)))

result={"status":"passed" if passed else "failed", "precision_digits":mp.mp.dps,
        "prediction_sha256":hashlib.sha256(registry.read_bytes()).hexdigest(),
        "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "new_PDE_runs":0,"asymptotic_constants":checks,"gaussian_operator":gaussian,
        "bandwidth_witnesses":bandwidth,"symbol_maximum":{"theta":number(theta),"f_squared":number(f*f),
        "identity_residual":number(maximum_error),"Nyquist_residual":number(nyquist_error)},
        "interpretation":"Direct matrix/multiplier checks of frozen predictions; proofs are independent of these finite evaluations."}
(HERE/"verification.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(result,ensure_ascii=False,indent=2))
if not passed:
    raise SystemExit(1)
