const fs=require('fs'), path=require('path'), vm=require('vm');
const here=__dirname;
const specs=[
  ['hs-config','单孤子配置：网格、时间步长与评价点','hs_config.js','默认参数对应原表 1；改变 N 与 a 时留意辅助区间。'],
  ['hs-reference','解析解与坐标反解','hs_reference.js','每一级的解析边界与末端的误差参考都由此计算。'],
  ['hs-core','核心算法：空间格式、Thomas 恢复与 RK4','hs_core.js','式（25）—（29）全部在本单元执行；修改核心表达式会改变现场结果。'],
  ['hs-compare','现场推进并复算单孤子误差','hs_compare.js','运行本段重放前面当前代码，然后现场演化两种方案。']
];
const cells=specs.map(([id,title,file,note])=>({id,title,note,code:fs.readFileSync(path.join(here,file),'utf8')}));
fs.writeFileSync(path.join(here,'hs_cells.json'),JSON.stringify(cells,null,2));
function run(replace=[]) {
  let source=cells.map(c=>c.code).join('\n');
  for(const [from,to] of replace) source=source.replace(from,to);
  const outputs=[],ctx=vm.createContext({emit:v=>outputs.push(v)}),start=performance.now();
  vm.runInContext(source,ctx,{timeout:30000});
  const seconds=(performance.now()-start)/1000;
  const result=vm.runInContext('Object.fromEntries(Object.entries(hsResults).map(([k,r])=>[k,{Eu:r.Eu,Erho:r.Erho,minDx:r.minDx,minRho:r.minRho}]))',ctx);
  return {outputs,ctx,result,seconds};
}
const result=run();
const trajectories=vm.runInContext('Object.fromEntries(Object.entries(liveFields).map(([name,f])=>[name,Object.fromEntries(["x","u","rhoX","rho"].map(k=>[k,Array.from(f[k])]))]))',result.ctx);
fs.writeFileSync(path.join(here,'hs_live_default_fields.json'),JSON.stringify(trajectories));
const changed=run([['N: 1600, a: 0.005','N: 800, a: 0.01']]);
const shortened=run([['dt: 0.003125, T: 0.5','dt: 0.003125, T: 0.25']]);
const edited=run([['2*d*(u[i+1]+u[i])','2.01*d*(u[i+1]+u[i])'],['N: 1600, a: 0.005','N: 800, a: 0.01']]);
if(Math.abs(changed.result.FD.Eu-result.result.FD.Eu)<1e-8) throw Error('Grid edit failed to affect errors.');
if(Math.abs(shortened.result.Integrable.Eu-result.result.Integrable.Eu)<1e-6) throw Error('Time edit failed to affect errors.');
if(Math.abs(edited.result.Integrable.Eu-changed.result.Integrable.Eu)<1e-5) throw Error('Core RHS edit failed to affect errors.');
if(!changed.outputs.some(v=>v.type==='text'&&v.text.includes('不与原报告默认表'))) throw Error('Modified config misclassified as default.');
let invalidRejected=false;
try {run([['dt: 0.003125, T: 0.5','dt: 0.003, T: 0.5']]);} catch(e){invalidRejected=e.message.includes('整数倍');}
if(!invalidRejected) throw Error('Invalid temporal grid not rejected.');
const validation={status:'passed',execution:'Exact visible cell source joined in one JavaScript scope in Node VM.',
  default_seconds:result.seconds,default_result:result.result,
  default_outputs:result.outputs.filter(v=>v.type!=='series'),
  changed_grid:{N:800,a:.01,seconds:changed.seconds,result:changed.result},
  changed_T:{T:.25,result:shortened.result},
  changed_core_expression:{expression:'2→2.01 in Integrable nonlinear RHS; N800/a.01',result:edited.result},
  invalid_temporal_grid_rejected:invalidRejected,
  scope:'Actual one-soliton Integrable/FD RK4 evolution from the continuous initial fields; default only compared with original report; no two-soliton browser recomputation.'};
fs.writeFileSync(path.join(here,'hs_validation.json'),JSON.stringify(validation,null,2));
console.log(JSON.stringify({status:validation.status,default_seconds:result.seconds,default_result:result.result,
  changed_grid:validation.changed_grid},null,2));
