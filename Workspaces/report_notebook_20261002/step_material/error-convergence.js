if (!lab.dlw?.ready?.main) throw Error("先运行主系数计算。");
const {h,levels,zs,tau,residual,maxAbs,continuumDefect}=lab.dlw;
// 余量：R_h/h²−tau=O(h²)。
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
      // 观测阶数=log2(2h 档误差/h 档误差)。
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
Object.assign(lab.dlw,{convergence,finest,ready:{prepare:true,config:true,profile:true,coefficient:true,residual:true,main:true,convergence:true}});
