const fs=require('fs');
const path=require('path');
const vm=require('vm');
const here=__dirname;
const specs=[
  ['error-config','配置：谱参数、纵向格距与相位点','config.js','参数 A 是默认示例；将 p 改为 4、q 改为 −3 可运行参数 B。'],
  ['error-core','核心算法：解析导数、二阶系数与有限格距残差','core.js','这里的 JavaScript 就是执行的核心算法；可修改表达式后重新计算。'],
  ['error-compare','运行比较：解析上界、格距减半与有符号剖面','compare.js','运行本段先重放前两段当前代码。曲线保留残差的正负号。']
];
const cells=specs.map(([id,title,file,note])=>({id,title,note,code:fs.readFileSync(path.join(here,file),'utf8')}));
fs.writeFileSync(path.join(here,'cells.json'),JSON.stringify(cells,null,2));
function run(overrides={}, coreReplace=null) {
  const output=[];
  let config=cells[0].code;
  for(const [from,to] of Object.entries(overrides)) config=config.replace(from,to);
  const core=coreReplace?cells[1].code.replace(...coreReplace):cells[1].code;
  const ctx=vm.createContext({emit:v=>output.push(v)});
  vm.runInContext(config+'\n'+core+'\n'+cells[2].code,ctx,{timeout:10000});
  return output;
}
const defaultOutputs=run();
const bOutputs=run({'a: 2, p: 1, q: 2':'a: 2, p: 4, q: -3'});
const halfOutputs=run({'h: 1 / 8':'h: 1 / 16'});
const coreEditedOutputs=run({},['hh*hh*K*(W[0]/16-1/4)*W[1]','hh*hh*K*(W[0]/16-1/5)*W[1]']);
const valueRows=o=>o.filter(v=>v.type==='table')[1].rows;
const convergenceRows=o=>o.filter(v=>v.type==='table')[2].rows;
const defaultRows=valueRows(defaultOutputs), bRows=valueRows(bOutputs);
const defaultConvergence=convergenceRows(defaultOutputs), bConvergence=convergenceRows(bOutputs);
function assert(test,message) { if(!test) throw Error(message); }
assert(Math.abs(defaultRows[0][1]-1.686105255989)<1e-4,'A SD1 disagrees with exact-arithmetic source bound.');
assert(Math.abs(defaultRows[1][1]-.933195653503)<1e-4,'A SD2 disagrees with exact-arithmetic source bound.');
assert(Math.abs(defaultRows[2][1]-.259905256283)<1e-4,'A FD1 disagrees with exact-arithmetic source bound.');
assert(Math.abs(defaultRows[3][1]-1.395719770374)<1e-4,'A FD2 disagrees with exact-arithmetic source bound.');
assert(Math.abs(bRows[0][1]-.025560181034)<1e-5,'B SD1 disagrees with exact-arithmetic source bound.');
assert(Math.abs(bRows[1][1]-.021076364155)<1e-5,'B SD2 disagrees with exact-arithmetic source bound.');
assert(Math.abs(bRows[2][1]-.007943649186)<1e-5,'B FD1 disagrees with exact-arithmetic source bound.');
assert(Math.abs(bRows[3][1]-.010575226637)<1e-5,'B FD2 disagrees with exact-arithmetic source bound.');
for(const row of [...defaultConvergence,...bConvergence].filter(r=>r[4]!==null))
  assert(row[4]>1.98 && row[4]<2.02,'Scaled residual coefficient did not converge at order two.');
const halfRows=valueRows(halfOutputs);
assert(Math.abs(halfRows[0][3]/defaultRows[0][3]-.25)<1e-13,'Changing h failed to rescale leading residual.');
assert(Math.abs(convergenceRows(coreEditedOutputs)[0][3]-defaultConvergence[0][3])>1e-3,'Visible core edit failed to affect residual.');
let invalidRejected=false;
try {run({'a: 2, p: 1, q: 2':'a: 2, p: 2, q: 2'});}catch(e){invalidRejected=/正分支/.test(e.message);}
assert(invalidRejected,'Invalid spectral pole was not rejected.');
const report={
  status:'passed', execution:'Node.js VM runs exact cell source joined in one scope; browser Worker integration is root responsibility.',
  checks:['A/B sample maxima agree with existing exact-arithmetic all-waveform enclosures to stated sampling tolerance',
    'A/B finite h scaled residual coefficients converge with observed order 1.98—2.02',
    'changing h changes leading residual by h² scaling',
    'editing the visible finite h flux changes recomputed residuals',
    'spectral pole input is rejected'],
  default_outputs:defaultOutputs.filter(v=>v.type!=='series'),
  parameter_B_outputs:bOutputs.filter(v=>v.type!=='series'),
  source_reference:'Workspaces/dlw_h2_bounds_20260930/REPORT.md',
  scientific_scope:'DLW y-direction equation residuals, analytic x/t derivatives; not 2HS field errors, PDE evolution, sampled proof of supremum, or propagated finite-time error bounds.'
};
fs.writeFileSync(path.join(here,'validation.json'),JSON.stringify(report,null,2));
const referenceSamples=[];
for(const [name,config] of [['A',cells[0].code],['B',cells[0].code.replace('a: 2, p: 1, q: 2','a: 2, p: 4, q: -3')]]) {
  const ctx=vm.createContext({emit:()=>{}});
  vm.runInContext(config+'\n'+cells[1].code,ctx);
  for(const z of [-6,-2,-.5,0,.7,2,6]) for(const hh of [.125,.0625,.03125]) {
    const value=vm.runInContext(`({coefficient:coefficient(${z}),SD:residual(${z},${hh},"SD"),FD:residual(${z},${hh},"FD")})`,ctx);
    referenceSamples.push({name,z,h:hh,...value});
  }
}
fs.writeFileSync(path.join(here,'independent_samples.json'),JSON.stringify(referenceSamples,null,2));
console.log(JSON.stringify({status:report.status,default_coefficients:defaultRows,B_coefficients:bRows,
  default_convergence:defaultConvergence},null,2));
