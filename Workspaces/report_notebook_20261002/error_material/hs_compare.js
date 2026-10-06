// 两种方案均由连续初值出发，实际运行至 T；不读取已保存轨道。
let {integrable,fd}=initialStates();
for (let step=0;step<steps;step++) {
  const t=step*dt;
  integrable=rk4Step(integrableRHS,t,integrable,dt);
  fd=rk4Step(fdRHS,t,fd,dt);
}
const liveFields={Integrable:integrableFields(T,integrable),FD:fdFields(T,fd)};
const xx=Float64Array.from({length:evaluationPoints},(_,i)=>
  xMin+(xMax-xMin)*i/(evaluationPoints-1));
const reference=Array.from(xx,x=>exactPhysical(x,T));
const hsResults={}, resultRows=[];
for (const [name,f] of Object.entries(liveFields)) {
  const u=interpolate(f.x,f.u,xx), rho=interpolate(f.rhoX,f.rho,xx);
  const eu=Float64Array.from(u,(v,i)=>Math.abs(v-reference[i].u));
  const er=Float64Array.from(rho,(v,i)=>Math.abs(v-reference[i].rho));
  let Eu=0, Erho=0, minDx=Infinity, minRho=Infinity;
  for (let i=0;i<evaluationPoints;i++) {Eu=Math.max(Eu,eu[i]);Erho=Math.max(Erho,er[i]);}
  for (let i=1;i<f.x.length;i++) minDx=Math.min(minDx,f.x[i]-f.x[i-1]);
  for (const r of f.rho) minRho=Math.min(minRho,r);
  hsResults[name]={Eu,Erho,eu,er,u,rho,minDx,minRho};
  resultRows.push([name,Eu,Erho,minDx,minRho]);
}
emit({type:"table",columns:["现场运行的方案","E_u(T)","E_ρ(T)","终点最小格距","终点最小密度"],rows:resultRows});
// 图中每个点为一个物理小区间的误差最大值，保留全网格最大误差。
const bins=100, centers=Array.from({length:bins},(_,i)=>xMin+(i+0.5)*(xMax-xMin)/bins);
for (const [key,label] of [["eu","u"],["er","ρ"]]) {
  const series=[];
  for (const name of ["Integrable","FD"]) {
    const envelope=new Array(bins).fill(0), values=hsResults[name][key];
    for (let k=0;k<evaluationPoints;k++) {
      const bin=Math.min(bins-1,Math.floor((xx[k]-xMin)/(xMax-xMin)*bins));
      envelope[bin]=Math.max(envelope[bin],values[k]);
    }
    series.push({name,x:centers,y:envelope.map(v=>Math.log10(Math.max(v,1e-16)))});
  }
  emit({type:"series",title:`单孤子 ${label} 的分段最大绝对误差`,
    xLabel:"物理坐标 x",yLabel:`log10(max |${label}_h − ${label}|)`,series});
}
// 原表仅作为同配置的回归核对；不参与演化、不替代现场误差。
const isReportDefault=N===1600 && a===0.005 && Xleft===-4 && dt===0.003125 &&
  T===0.5 && xMin===-1 && xMax===1 && evaluationPoints===32001;
if (isReportDefault) {
  const saved={Integrable:[0.010012749796509766,0.0011496748742060303],
    FD:[9.399310918062342e-7,3.046420677166317e-6]};
  let discrepancy=0;
  const auditRows=[];
  for (const name of ["Integrable","FD"]) {
    const r=hsResults[name], target=saved[name];
    const du=Math.abs(r.Eu-target[0]), dr=Math.abs(r.Erho-target[1]);
    discrepancy=Math.max(discrepancy,du,dr);
    auditRows.push([name,target[0],target[1],du,dr]);
  }
  emit({type:"table",columns:["方案","原表 E_u","原表 E_ρ","现场 E_u 与原表之差","现场 E_ρ 与原表之差"],rows:auditRows});
  if (discrepancy>1e-8) throw Error("默认配置与原报告误差不吻合，请检查已编辑的核心代码。");
  emit({type:"text",text:`OK：现场完成 ${steps} 步 RK4；默认配置与原报告四项误差的最大绝对差为 ${discrepancy.toExponential(2)}。`});
} else {
  emit({type:"text",text:`OK：现场完成 ${steps} 步 RK4，得到当前配置下的误差；配置已改变，因此不与原报告默认表作回归核对。`});
}
