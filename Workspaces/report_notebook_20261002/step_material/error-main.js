if (!lab.dlw?.ready?.residual) throw Error("先运行有限格距残差。");
const {zs,a,K,ell,Omega,h,coefficient,profile,bounds}=lab.dlw;
// tau[S][i]：方案 S 第 i 分量的相位采样值。
const tau = {SD:[[],[]], FD:[[],[]]};
let continuumDefect=0;
for (const z of zs) {
  const t=coefficient(z), {u,v}=profile(z), b=u[0]+2*a;
  for (const S of ["SD","FD"]) for (let i=0;i<2;i++) tau[S][i].push(t[S][i]);
  // 归一化残差：abs(sum(terms))/(1+sum(abs(terms)))。
  const terms1=[ell*Omega*u[2], K*K*v[2], K*ell*(u[1]*u[1]+b*u[2])];
  const terms2=[Omega*v[1], K*K*ell*u[3], K*(u[1]*v[0]+b*v[1]-4*u[1])];
  for (const terms of [terms1,terms2]) continuumDefect=Math.max(continuumDefect,
    Math.abs(terms.reduce((x,y)=>x+y,0))/(1+terms.reduce((x,y)=>x+Math.abs(y),0)));
}
if (continuumDefect > 1e-10) throw Error("连续 DLW 方程核对失败，请检查剖面或谱参数。");
const maxAbs = arr => Math.max(...arr.map(Math.abs));
const coeffRows=[];
for (const S of ["SD","FD"]) for (let i=0;i<2;i++) {
  const sampled=maxAbs(tau[S][i]);
  if (!Number.isFinite(sampled) || sampled > bounds[S][i]*(1+1e-10))
    throw Error(`${S} 第 ${i+1} 式超出解析主系数上界，请检查核心表达式。`);
  coeffRows.push([`${S}${S==="SD" ? " / SDR" : ""} · ${i+1}`,sampled,
    bounds[S][i],h*h*sampled,h*h*bounds[S][i]]);
}
emit({type:"table",columns:["方程","采样 max |τ|","全波形解析上界","采样 h² max |τ|","h² 解析上界"],rows:coeffRows});
Object.assign(lab.dlw,{tau,continuumDefect,maxAbs,coeffRows,ready:{prepare:true,config:true,profile:true,coefficient:true,residual:true,main:true}});
emit({type:"text",text:`continuumDefect = ${continuumDefect}`});
