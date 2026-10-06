if (!lab.dlw?.ready?.profile) throw Error("先运行连续剖面。");
const {profile,zeta}=lab.dlw;
// 数组下标 0、1 对应 DLW 的两条方程。
function coefficient(z) {
  const {s,f} = profile(z);
  const d1=f[1]-s[1], d2=f[2]-s[2], d3=f[3]-s[3];
  // 乘积项：B=(s'')^2+s'*s'''=0.5*((s')^2)''。
  const B = s[2]**2 + s[1]*s[3];
  return {
    FD: [zeta**3*(f[5]+s[5])/6, zeta**3*(f[5]-s[5])/3],
    SD: [zeta**3*((2*s[5]-f[5])/3+B) - zeta**2*s[3],
         zeta**3*((f[5]+2*s[5])/3+B+2*(d2*d2+d1*d3))
         - zeta**2*s[3]]
  };
}
// 覆盖全部实相位 z 的上界。
const Z = Math.abs(zeta);
const bounds = {
  FD: [Z**3/12, Z**3/6],
  SD: [251*Z**3/864 + Z**2/8, 59*Z**3/96 + Z**2/8]
};
Object.assign(lab.dlw,{coefficient,bounds,ready:{prepare:true,config:true,profile:true,coefficient:true}});
