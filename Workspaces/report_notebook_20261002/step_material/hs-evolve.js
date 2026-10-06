if (!lab.hs?.ready?.rk4) throw Error("先运行四阶时间步。");
const {steps,dt,T,initialStates,rk4Step,integrableRHS,fdRHS,integrableFields,fdFields}=lab.hs;
// 时间层：t_n=n*dt，T=steps*dt。
let {integrable,fd}=initialStates();
for (let step=0;step<steps;step++) {
  const t=step*dt;
  integrable=rk4Step(integrableRHS,t,integrable,dt);
  fd=rk4Step(fdRHS,t,fd,dt);
}
const liveFields={Integrable:integrableFields(T,integrable),FD:fdFields(T,fd)};
Object.assign(lab.hs,{integrable,fd,liveFields,ready:{prepare:true,config:true,reference:true,spatial:true,rk4:true,evolve:true}});
emit({type:"table",columns:["方案","已推进步数","当前时间","物理节点数"],
  rows:Object.entries(liveFields).map(([name,f])=>[name,steps,T,f.x.length])});
