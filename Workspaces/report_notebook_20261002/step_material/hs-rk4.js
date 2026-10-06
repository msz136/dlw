if (!lab.hs?.ready?.spatial) throw Error("先运行空间格式。");
// 式（29）：每一级重新恢复场值和解析边界。
function rk4Step(rhs,t,state,delta) {
  const add=(z,k,factor)=>Float64Array.from(z,(value,i)=>value+factor*k[i]);
  const k1=rhs(t,state), k2=rhs(t+delta/2,add(state,k1,delta/2));
  const k3=rhs(t+delta/2,add(state,k2,delta/2)), k4=rhs(t+delta,add(state,k3,delta));
  return Float64Array.from(state,(value,i)=>value+delta*(k1[i]+2*k2[i]+2*k3[i]+k4[i])/6);
}
Object.assign(lab.hs,{rk4Step,ready:{prepare:true,config:true,reference:true,spatial:true,rk4:true}});
