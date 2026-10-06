const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {chromium}=require('C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const here=__dirname,base='http://127.0.0.1:8766',dir=path.join(here,'raw_output_preview');
fs.mkdirSync(dir,{recursive:true});
const result={checks:[],leanStages:[],views:[],errors:[]};
const pass=(name,detail)=>{result.checks.push({name,passed:true,detail});console.log('PASS '+name);};
const sequences=[['hs-prepare','hs-config','hs-reference','hs-spatial','hs-rk4','hs-evolve','hs-error'],['error-prepare','error-config','error-profile','error-coefficient','error-residual','error-main','error-convergence']];
(async()=>{
 const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
 const page=await browser.newPage({viewport:{width:1440,height:1000}});
 page.on('pageerror',error=>result.errors.push(String(error)));
 try{
  await page.goto(base+'/Report.html');
  assert.equal(await page.locator('.latex-source').count(),0);
  assert.equal(await page.locator('.code-cell details:not(.complete-proof)').count(),0);
  assert.equal(await page.locator('.complete-proof').count(),2);
  for(const proof of await page.locator('.complete-proof').all()){
   assert.equal(await proof.getAttribute('open'),'');assert.equal(await proof.locator('details').count(),0);assert.equal(await proof.locator('pre').count(),1);
   assert.match(await proof.locator('pre').innerText(),/-- .*\.lean/);
  }
  assert.equal(await page.locator('.code-cell > .notebook-note').count(),0);
  const titles=await page.locator('.code-cell > .cell-title').evaluateAll(nodes=>nodes.map(node=>({width:node.getBoundingClientRect().width,clip:getComputedStyle(node).clipPath})));
  assert.ok(titles.every(title=>title.width===1&&title.clip==='inset(50%)'));
  for(const cell of await page.locator('.code-cell[data-kind="lean"]').all())assert.match(await cell.locator(':scope > pre.lean-source').innerText(),/--/);
  pass('only Lean source beside formulas; one expanded proof block per route; explanations moved into comments');
  const expected=JSON.parse(fs.readFileSync(path.join(here,'lean_material/stage_manifest.json'),'utf8'));
  for(const route of ['uw','qrm'])for(const stage of ['import','start','endpoint']){
   const id=stage==='endpoint'?`lean-${route}`:`lean-${route}-${stage}`;
   assert.equal(await page.locator(`#${id} > .lean-source`).textContent(),expected.cases[route][stage].code);
  }
  pass('all six visible Lean cells match their actual reviewed compiler input');
  for(const sequence of sequences){
   for(const id of sequence){
    await page.locator(`#${id} [data-run]`).click();
    await page.waitForFunction(id=>document.querySelector(`#${id} .cell-status`).dataset.executions==='1',id,{timeout:35000});
    assert.equal(await page.locator(`#${id} .cell-status`).innerText(),'');
    assert.doesNotMatch(await page.locator(`#${id} .cell-output`).innerText(),/\bOK\b|本段完成|已定义|环境就绪/);
   }
  }
  for(const id of ['hs-prepare','hs-spatial','hs-rk4','error-prepare','error-profile','error-coefficient','error-residual'])assert.equal(await page.locator(`#${id} .cell-output`).innerText(),'');
  assert.equal(await page.locator('#hs-error svg').count(),2);assert.equal(await page.locator('#error-convergence svg').count(),2);
  assert.match(await page.locator('#hs-error .cell-output').innerText(),/0\.0100127/);
  assert.match(await page.locator('#error-main .cell-output').innerText(),/1\.68606/);
  pass('fourteen numerical cells preserve default results; definitions are silent and real tables/plots remain');
  await page.locator('#error-convergence [data-run]').click();
  await page.waitForFunction(()=>document.querySelector('#error-convergence .cell-status').dataset.executions==='2');
  assert.equal(await page.locator('#error-prepare .cell-status').getAttribute('data-executions'),'1');
  assert.equal(await page.locator('#error-convergence svg').count(),2);
  pass('repeat execution replaces current output without replaying prior cells');
  let sessionId='';
  for(const stage of ['import','start','endpoint']){
   const id=stage==='endpoint'?'lean-uw':`lean-uw-${stage}`;
   const posted=page.waitForResponse(response=>response.url()===base+'/api/lean'&&response.request().method()==='POST');
   console.log('START actual UW '+stage);await page.locator(`#${id} [data-run]`).click();
   const response=await posted,lastJob=await response.json();
   assert.equal(response.status(),202,JSON.stringify(lastJob));
   await page.waitForFunction(()=>document.querySelector('[data-cancel]').disabled,null,{timeout:600000});
   assert.ok(lastJob?.jobId);
   const job=await(await page.request.get(`${base}/api/lean/${lastJob.jobId}`)).json();
   assert.equal(job.status,'ok');assert.equal(job.returncode,0);
   if(stage==='import')sessionId=job.sessionId;else assert.equal(job.sessionId,sessionId);
   const displayed=await page.locator(`#${id} .cell-output`).textContent();
   assert.equal(displayed,job.compilerOutput);
   assert.doesNotMatch(displayed,/^CHECK |^PASSED |^PASSED CELL|^REPORT:/m);
   assert.equal(await page.locator(`#${id} .cell-status`).innerText(),'');
   assert.equal(await page.locator(`#${id} .cell-output details`).count(),0);
   if(stage==='endpoint'){
    assert.match(displayed,/semiPair_implies_report7/);assert.match(displayed,/semiPair_implies_report8/);
    assert.equal(Object.keys(job.axioms).length,2);
    for(const axioms of Object.values(job.axioms))assert.ok(axioms.every(axiom=>['propext','Classical.choice','Quot.sound'].includes(axiom)));
   }
   result.leanStages.push({stage,jobId:job.jobId,sessionId:job.sessionId,elapsedSeconds:job.elapsedSeconds,compilerOutput:job.compilerOutput,cellResult:job.cellResult,axioms:job.axioms});
   pass('actual Lean '+stage+' displays exactly the compiler stdout/stderr', {characters:displayed.length,seconds:job.elapsedSeconds});
  }
  for(const width of [1440,390]){
   await page.setViewportSize({width,height:width===390?844:1000});
   const view=await page.evaluate(()=>({width:innerWidth,overflow:document.documentElement.scrollWidth>innerWidth+1,mathErrors:[...document.querySelectorAll('.katex-error')].map(node=>node.textContent)}));
   assert.equal(view.overflow,false);assert.deepEqual(view.mathErrors,[]);result.views.push(view);
   await page.locator('#lean-uw > .lean-source').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(dir,`lean-endpoint-${width}.png`)});
   await page.locator('#error-main').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(dir,`numeric-${width}.png`)});
  }
  await page.emulateMedia({media:'print'});
  assert.equal(await page.locator('#error-config .print-source').evaluate(node=>getComputedStyle(node).display),'block');
  pass('original formulas, narrow screen and print remain readable');assert.deepEqual(result.errors,[]);
 }catch(error){result.errors.push(String(error));throw error;}
 finally{fs.writeFileSync(path.join(here,'raw_output_validation.json'),JSON.stringify(result,null,2));await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
