// sigmoid 的解析导数：s^(n)=s(1-s) P_n(s)。
// P_(n+1)=(1-2s)P_n+s(1-s)P_n'；不做数值微分。
const polys = [[1]];
for (let n=1; n<5; n++) {
  const c = polys[n-1];
  polys.push(Array.from({length:c.length+1}, (_,k) =>
    (k+1) * ((c[k] || 0) - (c[k-1] || 0))));
}
function sigmoidJet(z) {
  const e = Math.exp(-Math.abs(z));
  const s = z >= 0 ? 1/(1+e) : e/(1+e);
  const theta = e / (1+e)**2;
  return [s, ...polys.map(c => {
    let value = 0;
    for (let k=c.length-1; k>=0; k--) value = value*s + c[k];
    return theta * value;
  })];
}
function profile(z) {
  const s = sigmoidJet(z), f = sigmoidJet(z + Math.log(Gamma));
  return {
    s, f,
    u: Array.from({length:4}, (_,n) => 2*K*(f[n]-s[n])),
    v: Array.from({length:3}, (_,n) => 2*K*ell*(f[n+1]+s[n+1]))
  };
}
// 两分量二阶主系数，编号对应 DLW 两条物理场方程。
function coefficient(z) {
  const {s,f} = profile(z);
  const d1=f[1]-s[1], d2=f[2]-s[2], d3=f[3]-s[3];
  const B = s[2]**2 + s[1]*s[3];
  return {
    FD: [zeta**3*(f[5]+s[5])/6, zeta**3*(f[5]-s[5])/3],
    SD: [zeta**3*((2*s[5]-f[5])/3+B) - zeta**2*s[3],
         zeta**3*((f[5]+2*s[5])/3+B+2*(d2*d2+d1*d3))
         - zeta**2*s[3]]
  };
}
// 全波形解析上界；不依赖 points 或所选相位区间。
const Z = Math.abs(zeta);
const bounds = {
  FD: [Z**3/12, Z**3/6],
  SD: [251*Z**3/864 + Z**2/8, 59*Z**3/96 + Z**2/8]
};
// 连续解代入有限 h 的 SD/FD 方程；第一式在交错中点求值。
function residual(z, hh, scheme) {
  const cache = new Map();
  function node(j) {
    if (cache.has(j)) return cache.get(j);
    const c=profile(z+ell*hh*j), plus=profile(z+ell*hh*(j+1));
    const minus=profile(z+ell*hh*(j-1));
    const D=c.v.map((_,n) => (plus.u[n]-minus.u[n])/(2*hh));
    const W=c.v.map((v,n) => v-D[n]);
    const Ax=K*(c.u[0]+2*a)*c.u[1];
    const Hx=Ax + (scheme==="SD" ? hh*hh*K*(W[0]/16-1/4)*W[1] : 0);
    const out={...c,D,W,Ax,Hx}; cache.set(j,out); return out;
  }
  const plus=node(1/2), minus=node(-1/2), c=node(0);
  let r1=Omega*(plus.u[1]-minus.u[1])/hh+(plus.Hx-minus.Hx)/hh;
  r1 += K*K*(scheme==="SD"
    ? (plus.u[2]-minus.u[2])/hh+(plus.W[2]+minus.W[2])/2
    : (plus.v[2]+minus.v[2])/2);
  let r2=Omega*c.v[1];
  if (scheme==="SD") {
    const pp=node(1), mm=node(-1);
    r2 += (pp.Hx-mm.Hx)/(2*hh)
      + K*(c.u[1]*c.W[0]+(c.u[0]+2*a)*c.W[1]-4*c.u[1])
      + K*K*(c.D[2]+(pp.W[2]-2*c.W[2]+mm.W[2])/4);
  } else {
    r2 += K*(c.u[1]*c.v[0]+(c.u[0]+2*a)*c.v[1]-4*c.u[1])
      + K*K*c.D[2];
  }
  return [r1,r2];
}
emit({type:"text",text:"已定义解析单孤子、二阶主系数、统一上界及有限 h 方程残差。SDR 的理想半离散残差与 SD 相同。"});
