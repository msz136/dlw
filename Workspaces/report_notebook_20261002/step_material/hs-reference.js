if (!lab.hs?.ready?.config) throw Error("先运行网格与时间配置。");
const {N,a,Xleft,xMin,xMax}=lab.hs;
// 式（24）：X 到 x 的映射，m=u_xx+2。
function exactX(X,t) {
  const z=Math.tanh((3.75*X-0.6*t)/2), S=1-z*z;
  const zx=1.875*S, zxx=-2*zx*1.875*z;
  const J=1+0.3*zx, Jx=0.3*zxx;
  const u=0.09*S, uX=-0.18*z*zx;
  const uXX=-0.18*(zx*zx+z*zxx);
  // 链式法则：d/dx=(1/J)d/dX，其中 J=dx/dX。
  const uxx=(uXX*J-uX*Jx)/(J*J*J);
  return {x:X-0.5+0.3*z,u,rho:1/J,m:uxx+2,X};
}
// dx/dX>0；反解区间为 [x+0.2,x+0.8]。
function exactPhysical(x,t) {
  let lo=x+0.2, hi=x+0.8;
  for (let k=0;k<60;k++) {
    const mid=(lo+hi)/2;
    if (exactX(mid,t).x<x) lo=mid; else hi=mid;
  }
  const value=exactX((lo+hi)/2,t);
  if (Math.abs(value.x-x)>2e-12)
    throw Error("物理坐标反解未达到容差。");
  return value;
}
// 固定网格与初始动网格共用物理端点。
const initial=Array.from({length:N+1},(_,i)=>exactX(Xleft+i*a,0));
const left=initial[0].x, right=initial[N].x, dx=(right-left)/N;
const fixedX=Float64Array.from({length:N+1},(_,i)=>left+i*dx);
if (xMin<=left || xMax>=right)
  throw Error("评价区间必须位于初始物理端点内部。");
emit({type:"table",columns:["初始物理左端","初始物理右端","FD 的 Δx","峰值 u","谷值 ρ"],
  rows:[[left,right,dx,0.09,0.64]]});
Object.assign(lab.hs,{exactX,exactPhysical,initial,left,right,dx,fixedX,ready:{prepare:true,config:true,reference:true}});
