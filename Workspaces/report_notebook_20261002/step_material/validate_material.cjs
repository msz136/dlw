const fs = require('fs');
const path = require('path');
const vm = require('vm');
const AsyncFunction = Object.getPrototypeOf(async function(){}).constructor;
const here = __dirname;
const old = path.join(here, '..', 'error_material');
const hs = JSON.parse(fs.readFileSync(path.join(here, 'hs_cells.json'), 'utf8'));
const dlw = JSON.parse(fs.readFileSync(path.join(here, 'cells.json'), 'utf8'));
const checks = [];
const evidenceName = process.argv[2] || 'raw_output_validation.json';
const silentCells = new Set(['hs-prepare','hs-spatial','hs-rk4',
  'error-prepare','error-profile','error-coefficient','error-residual']);
const assert = (test, message) => {if (!test) throw Error(message);};

async function one(cell, lab, output, replace) {
  const code = replace ? replace(cell.code, cell) : cell.code;
  const priorOutputs = output.length;
  await new AsyncFunction('lab', 'emit', code)(lab, value => output.push(value));
  if (silentCells.has(cell.id)) assert(output.length === priorOutputs,
    'A definition-only cell emitted artificial output: ' + cell.id);
}
async function run(cells, replace) {
  const lab = {}, output = [], done = new Set();
  for (const cell of cells) {
    assert(cell.requires.every(id => done.has(id)), 'Bad requires graph ' + cell.id);
    await one(cell, lab, output, replace);
    done.add(cell.id);
  }
  return {lab, output};
}
function original(files) {
  const output = [];
  vm.runInNewContext(files.map(file => fs.readFileSync(path.join(old, file), 'utf8')).join('\n'),
    {emit:value => output.push(value)}, {timeout:20000});
  return JSON.parse(JSON.stringify(output));
}
const tables = values => JSON.parse(JSON.stringify(values.filter(value => value.type === 'table')));
function report(name, details) {checks.push({name, passed:true, details}); console.log('PASS ' + name);}

(async () => {
  assert(hs.length === 7 && dlw.length === 7, 'Expected the original 14 cells');
  for (const cell of [...hs,...dlw]) {
    assert(cell.code.includes('//'), 'Missing explanatory code comment: ' + cell.id);
    assert(cell.code === fs.readFileSync(path.join(here,cell.id+'.js'),'utf8').replace(/\r\n/g,'\n'),
      'JSON and standalone visible source diverged: ' + cell.id);
  }
  report('All 14 cells retain comments and identical JSON/JavaScript source', null);
  for (const cells of [hs, dlw]) {
    let rejected = false;
    try {await one(cells[cells.length-1], {}, []);} catch (error) {rejected=/先运行/.test(error.message);}
    assert(rejected, 'Missing setup must not execute a calculation');
  }
  report('Missing prior cells are rejected with no implicit replay', null);

  const partial = {lab:{}, output:[]};
  for (const cell of hs.slice(0,5)) await one(cell, partial.lab, partial.output);
  assert(!partial.lab.hs.liveFields && !partial.lab.hs.hsResults, 'Preparation unexpectedly evolved fields');
  assert(!partial.output.some(value => value.type === 'series'), 'Preparation emitted an error figure');
  let beforeEvolutionRejected = false;
  try {await one(hs[6], partial.lab, partial.output);} catch (error) {beforeEvolutionRejected=/实际演化/.test(error.message);}
  assert(beforeEvolutionRejected, 'Error calculation must require actual evolution');
  const rk4Saved = partial.lab.hs.rk4Step;
  partial.lab.hs.calls = 0;
  partial.lab.hs.rk4Step = (...arguments) => {partial.lab.hs.calls++; return rk4Saved(...arguments);};
  await one(hs[5], partial.lab, partial.output);
  assert(partial.lab.hs.calls === 2*partial.lab.hs.steps, 'Evolution must use the already-run RK4 definition');
  assert(!partial.output.some(value => value.type === 'series'), 'Evolution must not automatically run the later figure cell');
  await one(hs[6], partial.lab, partial.output);
  assert(partial.output.filter(value => value.type === 'series').length === 2, 'Expected 2HS error plots after the error cell');
  const originalHs = original(['hs_config.js','hs_reference.js','hs_core.js','hs_compare.js']);
  const currentHs = tables(partial.output).filter(value => value.columns[1] !== '已推进步数');
  assert(JSON.stringify(currentHs) === JSON.stringify(tables(originalHs)), 'Default 2HS result tables changed');
  report('Only evolution advances states; original 2HS tables and figures reproduced', {
    rk4Calls:partial.lab.hs.calls,
    errors:Object.fromEntries(Object.entries(partial.lab.hs.hsResults).map(([name,r])=>[name,{Eu:r.Eu,Erho:r.Erho}])),
    figures:2
  });

  const changedTime = await run(hs, (code,cell)=>cell.id==='hs-config' ? code.replace('T: 0.5','T: 0.25') : code);
  assert(changedTime.lab.hs.steps === 80, 'Edited time config was not used');
  assert(Math.abs(changedTime.lab.hs.hsResults.Integrable.Eu-partial.lab.hs.hsResults.Integrable.Eu)>1e-4,
    'Edited time config did not change actual error');
  report('Visible 2HS parameter edit changes actual evolution and error', {
    T:changedTime.lab.hs.T, steps:changedTime.lab.hs.steps, Eu:changedTime.lab.hs.hsResults.Integrable.Eu
  });

  const changedRk4 = await run(hs, (code,cell)=>cell.id==='hs-rk4' ?
    code.replace('value+delta*(k1[i]+2*k2[i]+2*k3[i]+k4[i])/6',
      'value+0.999*delta*(k1[i]+2*k2[i]+2*k3[i]+k4[i])/6') :
    cell.id==='hs-config' ? code.replace('T: 0.5','T: 0.25') : code);
  assert(Math.abs(changedRk4.lab.hs.hsResults.FD.Eu-changedTime.lab.hs.hsResults.FD.Eu)>1e-7,
    'Visible RK4 core edit was ignored');
  report('Visible RK4 core edit changes recomputed error', {EuFD:changedRk4.lab.hs.hsResults.FD.Eu});

  const defaultDlw = await run(dlw);
  assert(!partial.output.some(value => value.type === 'text'), '2HS added a prose completion message');
  const measuredText = defaultDlw.output.filter(value => value.type === 'text');
  assert(measuredText.length === 1 && /^continuumDefect = [0-9.e+-]+$/.test(measuredText[0].text),
    'DLW text output must be the measured residual only');
  report('Definition cells emit nothing; final output retains only numerical evidence', {
    silentCells:[...silentCells], measuredText:measuredText[0].text
  });
  const originalDlw = original(['config.js','core.js','compare.js']);
  assert(JSON.stringify(tables(defaultDlw.output)) === JSON.stringify(tables(originalDlw)), 'Default DLW tables changed');
  report('Original DLW coefficient and convergence tables reproduced', {
    coefficients:defaultDlw.lab.dlw.coeffRows, convergenceRows:defaultDlw.lab.dlw.convergence.length
  });
  const b = await run(dlw, (code,cell)=>cell.id==='error-config' ? code.replace('a: 2, p: 1, q: 2','a: 2, p: 4, q: -3') : code);
  assert(Math.abs(defaultDlw.lab.dlw.coeffRows[0][1]-b.lab.dlw.coeffRows[0][1])>1, 'Spectral parameter edit was ignored');
  for (const row of b.lab.dlw.convergence.filter(row=>row[4]!==null)) assert(row[4]>1.98 && row[4]<2.02, 'B convergence changed');
  const coreChanged = await run(dlw, (code,cell)=>cell.id==='error-residual' ?
    code.replace('hh*hh*K*(W[0]/16-1/4)*W[1]', 'hh*hh*K*(W[0]/16-1/5)*W[1]') : code);
  assert(Math.abs(defaultDlw.lab.dlw.convergence[0][3]-coreChanged.lab.dlw.convergence[0][3])>1e-3,
    'Edited finite-h residual was ignored');
  report('Visible DLW parameter and finite-h core edits change computed results', {
    bCoefficient:b.lab.dlw.coeffRows[0][1], editedResidualDifference:coreChanged.lab.dlw.convergence[0][3]
  });

  await one(hs[1], partial.lab, []);
  assert(!partial.lab.hs.ready.evolve && !partial.lab.hs.ready.error, 'Rerun config did not invalidate later readiness');
  let staleRejected = false;
  try {await one(hs[6], partial.lab, []);} catch (error) {staleRejected=/先运行/.test(error.message);}
  assert(staleRejected, 'Stale old fields allowed an error figure after upstream rerun');
  report('Upstream rerun clears downstream readiness; old error data cannot be used', null);

  const withFailure = [...hs];
  const reached = [];
  const failureLab = {};
  try {
    for (const cell of withFailure) {
      reached.push(cell.id);
      await one(cell, failureLab, [], (code,item)=>item.id==='hs-reference' ? 'const broken = ;' : code);
    }
    throw Error('Expected syntax error');
  } catch (error) {assert(error instanceof SyntaxError, 'Wrong syntax-error behavior');}
  assert(reached.length===3 && !failureLab.hs.ready.spatial, 'Sequence continued after syntax error');
  await one(hs[2], failureLab, []);
  assert(failureLab.hs.ready.reference, 'Repair failed to restore reference definition');
  report('Real syntax error stops the sequence and corrected cell can run again', {reached});

  const result = {status:'passed', execution:"Persistent explicit lab object; each AsyncFunction receives only the current visible cell source.", checks};
  fs.writeFileSync(path.join(here,evidenceName), JSON.stringify(result,null,2)+'\n');
  console.log('ALL PASSED');
})().catch(error=>{console.error(error.stack); process.exit(1);});
