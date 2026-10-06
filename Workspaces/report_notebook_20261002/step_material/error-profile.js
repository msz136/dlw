if (!lab.dlw?.ready?.config) throw Error("先运行谱参数配置。");
const {K,ell,Gamma}=lab.dlw;
// S 形函数的解析导数：s^(n)=s(1-s)*P_n(s)。
// 多项式递推：P_(n+1)=(1-2s)*P_n+s(1-s)*P_n'。
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
// u[n]、v[n] 表示对 z 的 n 阶导数。
function profile(z) {
  const s = sigmoidJet(z), f = sigmoidJet(z + Math.log(Gamma));
  return {
    s, f,
    u: Array.from({length:4}, (_,n) => 2*K*(f[n]-s[n])),
    v: Array.from({length:3}, (_,n) => 2*K*ell*(f[n+1]+s[n+1]))
  };
}
Object.assign(lab.dlw,{sigmoidJet,profile,ready:{prepare:true,config:true,profile:true}});
