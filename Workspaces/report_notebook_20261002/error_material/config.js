// DLW 连续单孤子；A: (a,p,q)=(2,1,2)，B: (2,4,-3)。
// h 是 y 方向格距，z 是无量纲相位。x,t 导数保持解析。
const cfg = {
  a: 2, p: 1, q: 2,
  h: 1 / 8,
  zMin: -10, zMax: 10, points: 1601,
  levels: 3
};
const { a, p, q, h, zMin, zMax, points, levels } = cfg;
if (![a,p,q,h,zMin,zMax].every(Number.isFinite))
  throw Error("参数必须是有限实数。");
if (!(h > 0 && zMax > zMin) || zMax - zMin > 100)
  throw Error("要求 h>0、zMax>zMin，且相位区间宽度≤100。");
if (!Number.isInteger(points) || points < 41 || points > 10001 ||
    !Number.isInteger(levels) || levels < 1 || levels > 6)
  throw Error("points 应在 41—10001；levels 应在 1—6，均取整数。");
if (h / 2 ** (levels - 1) < 1 / 1024)
  throw Error("最细格距须≥1/1024，以限制浮点消减误差。");
const K = p + q, P = p - a, Q = q + a;
if (!(K > 0) || P === 0 || Q === 0 || !(-P / Q > 0))
  throw Error("单孤子正分支要求 p+q>0，(p-a)(q+a)<0。");
const ell = 1 / P + 1 / Q, Gamma = -P / Q;
const Omega = q*q - p*p, zeta = K * ell;
if (![ell,Gamma,Omega,zeta].every(Number.isFinite))
  throw Error("参数过近谱极点，所得系数非有限。");
const zs = Array.from({length: points}, (_,i) =>
  zMin + (zMax - zMin) * i / (points - 1));
emit({type:"table", columns:["K","ℓ","Γ","ζ = Kℓ","h","相位点数"],
  rows:[[K,ell,Gamma,zeta,h,points]]});
