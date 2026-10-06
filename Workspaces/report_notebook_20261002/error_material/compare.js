// 同一相位网格比较：R_h / h² → τ；采样最大值不当作连续上界。
const tau = {SD:[[],[]], FD:[[],[]]};
let continuumDefect=0;
for (const z of zs) {
  const t=coefficient(z), {u,v}=profile(z), b=u[0]+2*a;
  for (const S of ["SD","FD"]) for (let i=0;i<2;i++) tau[S][i].push(t[S][i]);
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
const convergence=[], finest={SD:[[],[]],FD:[[],[]]}, previous={};
for (let level=0;level<levels;level++) {
  const hh=h/2**level;
  for (const S of ["SD","FD"]) {
    const values=[[],[]], errors=[[],[]];
    zs.forEach((z,k) => {
      const r=residual(z,hh,S);
      for (let i=0;i<2;i++) {
        const normalized=r[i]/(hh*hh);
        if (!Number.isFinite(normalized)) throw Error("有限 h 残差非有限，请检查参数。");
        values[i].push(normalized); errors[i].push(normalized-tau[S][i][k]);
      }
    });
    for (let i=0;i<2;i++) {
      const key=`${S}${i}`, err=maxAbs(errors[i]);
      const rate=level && err>0 && previous[key]>0 ? Math.log2(previous[key]/err) : null;
      convergence.push([`${S} · ${i+1}`,hh,maxAbs(values[i]),err,rate]);
      previous[key]=err;
      if (level===levels-1) finest[S][i]=values[i];
    }
  }
}
emit({type:"table",columns:["方程","h","采样 max |R_h / h²|","采样 max |R_h / h² − τ|","减半收敛阶"],rows:convergence});
for (let i=0;i<2;i++) emit({type:"series",title:`DLW 第 ${i+1} 式：主系数与有限格距残差`,
  xLabel:"无量纲相位 z",yLabel:"方程残差 / h²",series:[
    {name:"SD / SDR 主系数 τ",x:zs,y:tau.SD[i]},
    {name:"FD 主系数 τ",x:zs,y:tau.FD[i]},
    {name:`SD 有限 h=${h/2**(levels-1)}`,x:zs,y:finest.SD[i],dash:true},
    {name:`FD 有限 h=${h/2**(levels-1)}`,x:zs,y:finest.FD[i],dash:true}
  ]});
emit({type:"text",text:`OK：连续 DLW 方程核对的相对残差为 ${continuumDefect.toExponential(2)}；采样主系数均位于解析上界内。表中收敛阶验证有限 h 残差的二阶主项，未计算有限时间的总场误差。`});
