// Integrable 状态为 [b_0,…,b_(N−1), d_0,…,d_(N−1), x_0]。
function integrableFields(t,state) {
  const u=new Float64Array(N+1), x=new Float64Array(N+1);
  const rho=new Float64Array(N), rhoX=new Float64Array(N);
  const u0=exactX(Xleft,t).u, x0=state[2*N];
  u[0]=u0; x[0]=x0;
  let sumB=0, sumD=0;
  for (let i=0;i<N;i++) {
    const b=state[i], d=state[N+i];
    if (!Number.isFinite(b) || !Number.isFinite(d) || d<=0)
      throw Error("Integrable 出现非有限状态或非正胞元格距。");
    sumB+=b; sumD+=d; u[i+1]=u0+sumB; x[i+1]=x0+sumD;
    rho[i]=a/d; rhoX[i]=(x[i]+x[i+1])/2;
  }
  return {x,u,rhoX,rho};
}
function integrableRHS(t,state) {
  const {u}=integrableFields(t,state), result=new Float64Array(2*N+1);
  for (let i=0;i<N;i++) {
    const b=state[i], d=state[N+i], C=d*d-a*(a-1);
    result[i]=2*d*(u[i+1]+u[i])+(C*C-b*b)/(2*d)-d/2;
    result[N+i]=-b;
  }
  result[2*N]=-u[0]; return result;
}
// Thomas 消元解 u_(i−1)−2u_i+u_(i+1)=Δx²(m_i−2)。
function recoverU(m,ubLeft,ubRight) {
  const count=N-1, c=new Float64Array(count), d=new Float64Array(count);
  for (let j=0;j<count;j++) {
    const diagonal=-2-(j ? c[j-1] : 0);
    let rhs=dx*dx*(m[j+1]-2);
    if (j===0) rhs-=ubLeft;
    if (j===count-1) rhs-=ubRight;
    c[j]=j<count-1 ? 1/diagonal : 0;
    d[j]=(rhs-(j ? d[j-1] : 0))/diagonal;
  }
  const u=new Float64Array(N+1); u[0]=ubLeft; u[N]=ubRight;
  for (let j=count-1;j>=0;j--) u[j+1]=d[j]-(j<count-1 ? c[j]*u[j+2] : 0);
  return u;
}
// FD 只推进内部 [m_1,…,m_(N−1), ρ_1,…,ρ_(N−1)]。
function fdFields(t,state) {
  const l=exactPhysical(left,t), r=exactPhysical(right,t);
  const m=new Float64Array(N+1), rho=new Float64Array(N+1);
  m[0]=l.m; m[N]=r.m; rho[0]=l.rho; rho[N]=r.rho;
  for (let i=1;i<N;i++) {
    m[i]=state[i-1]; rho[i]=state[N-1+i-1];
    if (!Number.isFinite(m[i]) || !Number.isFinite(rho[i]) || rho[i]<=0)
      throw Error("FD 出现非有限状态或非正密度。");
  }
  return {x:fixedX,u:recoverU(m,l.u,r.u),rhoX:fixedX,rho,m};
}
function fdRHS(t,state) {
  const {m,rho,u}=fdFields(t,state), result=new Float64Array(2*(N-1));
  for (let i=1;i<N;i++) {
    const ux=(u[i+1]-u[i-1])/(2*dx);
    const mx=(m[i+1]-m[i-1])/(2*dx), rx=(rho[i+1]-rho[i-1])/(2*dx);
    result[i-1]=u[i]*mx+2*m[i]*ux+rho[i]*rx;
    result[N-1+i-1]=u[i]*rx+rho[i]*ux;
  }
  return result;
}
// 式（29）：每一级都在相应 RHS 内恢复物理场和解析边界。
function rk4Step(rhs,t,state,delta) {
  const add=(z,k,factor)=>Float64Array.from(z,(value,i)=>value+factor*k[i]);
  const k1=rhs(t,state), k2=rhs(t+delta/2,add(state,k1,delta/2));
  const k3=rhs(t+delta/2,add(state,k2,delta/2)), k4=rhs(t+delta,add(state,k3,delta));
  return Float64Array.from(state,(value,i)=>value+delta*(k1[i]+2*k2[i]+2*k3[i]+k4[i])/6);
}
function initialStates() {
  const integrable=new Float64Array(2*N+1), fd=new Float64Array(2*(N-1));
  const u0=Float64Array.from(fixedX,x=>exactPhysical(x,0).u);
  for (let i=0;i<N;i++) {
    integrable[i]=initial[i+1].u-initial[i].u;
    integrable[N+i]=initial[i+1].x-initial[i].x;
  }
  integrable[2*N]=left;
  for (let i=1;i<N;i++) {
    fd[i-1]=(u0[i+1]-2*u0[i]+u0[i-1])/(dx*dx)+2;
    fd[N-1+i-1]=exactPhysical(fixedX[i],0).rho;
  }
  return {integrable,fd};
}
// 有序节点上的逐段线性插值，覆盖检查不以端点外推代替。
function interpolate(xs,values,targets) {
  if (targets[0]<xs[0] || targets[targets.length-1]>xs[xs.length-1])
    throw Error("数值网格未覆盖整个评价区间。");
  const out=new Float64Array(targets.length); let j=0;
  for (let k=0;k<targets.length;k++) {
    while (j<xs.length-2 && xs[j+1]<targets[k]) j++;
    const weight=(targets[k]-xs[j])/(xs[j+1]-xs[j]);
    out[k]=values[j]+weight*(values[j+1]-values[j]);
  }
  return out;
}
emit({type:"text",text:"已定义两种空间格式、Thomas 场恢复、RK4 与线性插值；下一单元现场推进单孤子并计算式（30）的误差。"});
