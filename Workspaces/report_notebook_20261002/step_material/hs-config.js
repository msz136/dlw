if (!lab.hs?.ready?.prepare) throw Error("先运行准备环境。");
// 式（24）：p=5、q=1.25、c=1，初相位为零。
// a：X 方向格距；dt：时间步长；T：终止时间。
const hsCfg = {
  N: 1600, a: 0.005, Xleft: -4,
  dt: 0.003125, T: 0.5,
  xMin: -1, xMax: 1, evaluationPoints: 32001
};
const {N,a,Xleft,dt,T,xMin,xMax,evaluationPoints} = hsCfg;
if (![a,Xleft,dt,T,xMin,xMax].every(Number.isFinite) ||
    !(a>0 && dt>0 && T>=0 && xMax>xMin))
  throw Error("要求有限实数、a>0、dt>0、T≥0、xMax>xMin。");
if (!Number.isInteger(N) || N<20 || N>6400 ||
    !Number.isInteger(evaluationPoints) || evaluationPoints<101 || evaluationPoints>64001)
  throw Error("N 应在 20—6400；评价点数应在 101—64001，均取整数。");
const steps=Math.round(T/dt);
if (Math.abs(steps*dt-T)>1e-12 || steps>3200)
  throw Error("T 须为 dt 的整数倍，且步数≤3200。");
const Xright=Xleft+N*a;
emit({type:"table",columns:["N","a","辅助区间 X","Δt","T","时间步数","评价点数"],
  rows:[[N,a,`[${Xleft}, ${Xright}]`,dt,T,steps,evaluationPoints]]});
Object.assign(lab.hs,{cfg:hsCfg,...hsCfg,steps,Xright,ready:{prepare:true,config:true}});
