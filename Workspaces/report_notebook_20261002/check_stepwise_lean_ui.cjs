const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {chromium}=require('C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const here=__dirname,result={route:'qrm',stages:[],checks:[],errors:[]},base='http://127.0.0.1:8766';
const pass=name=>{result.checks.push({name,passed:true});console.log('PASS '+name);};
(async()=>{
 const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
 const page=await browser.newPage({viewport:{width:1440,height:1000}});let posts=0,lastJob=null;
 page.on('pageerror',e=>result.errors.push(String(e)));
 page.on('response',async r=>{if(r.url().endsWith('/api/lean')&&r.request().method()==='POST'){posts++;lastJob=await r.json();}});
 try{
  await page.goto(base+'/Report.html');await page.waitForFunction(()=>document.getElementById('runtime-status').textContent.includes('4.34.0'));
  await page.locator('#lean-qrm [data-run]').click();assert.match(await page.locator('#lean-qrm .cell-output').innerText(),/请先运行.*import/);assert.equal(posts,0);pass('endpoint before import is blocked without starting a compile');
  let sessionId='';
  for(const stage of ['import','start','endpoint']){
    const id=stage==='endpoint'?'lean-qrm':`lean-qrm-${stage}`,started=Date.now();lastJob=null;
    console.log('START QRM '+stage);await page.locator(`#${id} [data-run]`).click();
    await page.waitForFunction(()=>!document.querySelector('[data-cancel]').disabled,{timeout:3000});
    while(!await page.locator('[data-cancel]').isDisabled()){
      if(Date.now()-started>600000)throw Error('stage timed out');await page.waitForTimeout(10000);console.log('PROGRESS '+stage+': '+await page.locator(`#${id} .cell-status`).innerText());
    }
    const text=await page.locator(`#${id} .cell-output`).innerText();assert.match(text,/OK/);assert.ok(lastJob?.jobId);
    const job=await(await page.request.get(`${base}/api/lean/${lastJob.jobId}`)).json();assert.equal(job.status,'ok');assert.equal(job.stage,stage);assert.equal(job.returncode,0);
    if(stage==='import')sessionId=job.sessionId;else assert.equal(job.sessionId,sessionId);
    assert.deepEqual(job.completedStages,['import','start','endpoint'].slice(0,['import','start','endpoint'].indexOf(stage)+1));
    if(stage!=='endpoint')assert.equal(await page.locator('#lean-qrm .cell-output').innerText(),'');
    if(stage==='import')assert.equal(await page.locator('#lean-qrm-start .cell-output').innerText(),'');
    if(stage==='endpoint'){assert.equal(Object.keys(job.axioms).length,2);for(const a of Object.values(job.axioms))assert.ok(a.every(x=>['propext','Classical.choice','Quot.sound'].includes(x)));}
    result.stages.push({stage,jobId:job.jobId,sessionId:job.sessionId,elapsedSeconds:job.elapsedSeconds,completedStages:job.completedStages,text,runResult:job.runResult,cellResult:job.cellResult,axioms:job.axioms,resultPath:job.resultPath,sourceHashes:job.sourceHashes});
    await page.locator(`#${id} .cell-output`).scrollIntoViewIfNeeded();await page.screenshot({path:path.join(here,'stepwise_preview',`lean-qrm-${stage}-verified.png`)});pass('QRM '+stage+' executes only its requested cell');
  }
  assert.equal(posts,3);pass('three clicks produced three stages in one retained proof session');
  await page.locator('[data-reset]').click();await page.locator('#lean-qrm [data-run]').click();assert.match(await page.locator('#lean-qrm .cell-output').innerText(),/请先运行.*import/);assert.equal(posts,3);pass('reset discards prior stage completion and prevents use of an old session');
  assert.deepEqual(result.errors,[]);
 }finally{fs.writeFileSync(path.join(here,'stepwise_lean_ui_validation.json'),JSON.stringify(result,null,2));await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
