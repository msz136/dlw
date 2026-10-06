const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {chromium}=require('C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const here=__dirname,result={url:'http://127.0.0.1:8766/Report.html',cases:[],errors:[]};
const resumeUW=process.argv[2]==='--resume-uw'?process.argv[3]:null;
(async()=>{
 const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
 const page=await browser.newPage({viewport:{width:1440,height:1000}});page.on('pageerror',e=>result.errors.push(String(e)));
 try{
  await page.goto(result.url);await page.evaluate(()=>document.fonts.ready);
  assert.match(await page.locator('#runtime-status').innerText(),/4\.34\.0/);
  for(const route of ['uw','qrm']){
    if(route==='uw'&&resumeUW){
      const job=await(await page.request.get(`http://127.0.0.1:8766/api/lean/${resumeUW}`)).json();
      assert.equal(job.route,'uw');assert.equal(job.status,'ok');assert.equal(job.returncode,0);assert.equal(job.runResult.status,'PASSED');
      assert.equal(Object.keys(job.axioms).length,2);for(const axioms of Object.values(job.axioms))assert.deepEqual(new Set(axioms),new Set(['propext','Classical.choice','Quot.sound']));
      result.cases.push({route,jobId:resumeUW,previousUiRun:true,reason:'First browser Run reached OK; audit request URL was corrected without recompiling.',elapsedSeconds:job.elapsedSeconds,resultPath:job.resultPath,sourceHashes:job.sourceHashes,axioms:job.axioms,runResult:job.runResult});
      console.log('PASS persisted result from previous actual Lean UI uw Run');continue;
    }
    let jobId='';const handler=async r=>{if(r.url().endsWith('/api/lean')&&r.request().method()==='POST'){const d=await r.json();jobId=d.jobId || '';}};
    page.on('response',handler);const started=Date.now();console.log(`START Lean UI ${route}`);
    await page.locator(`#lean-${route} [data-run]`).click();await page.waitForFunction(()=>document.querySelector('[data-run-all]').disabled);
    while(await page.locator('[data-run-all]').isDisabled()){
      if(Date.now()-started>600000)throw Error('Lean UI timeout');
      await page.waitForTimeout(15000);console.log(`PROGRESS ${route}: ${await page.locator(`#lean-${route} .cell-status`).innerText()}`);
    }
    page.off('response',handler);const text=await page.locator(`#lean-${route} .cell-output`).innerText();assert.match(text,/OK · Lean 重新编译通过/);assert.ok(jobId);
    const job=await (await page.request.get(`http://127.0.0.1:8766/api/lean/${jobId}`)).json();assert.equal(job.status,'ok');assert.equal(job.returncode,0);assert.equal(job.runResult.status,'PASSED');
    assert.equal(Object.keys(job.axioms).length,2);for(const axioms of Object.values(job.axioms))assert.deepEqual(new Set(axioms),new Set(['propext','Classical.choice','Quot.sound']));
    result.cases.push({route,jobId,text,elapsedSeconds:job.elapsedSeconds,resultPath:job.resultPath,sourceHashes:job.sourceHashes,axioms:job.axioms,runResult:job.runResult});
    await page.locator(`#lean-${route} .cell-output`).scrollIntoViewIfNeeded();await page.screenshot({path:path.join(here,'preview',`lean-${route}-verified.png`)});
    console.log(`PASS Lean UI ${route}: ${job.elapsedSeconds.toFixed(2)} seconds, PASSED, two endpoint axiom checks`);
  }
  assert.deepEqual(result.errors,[]);
 }finally{fs.writeFileSync(path.join(here,'lean_ui_validation.json'),JSON.stringify(result,null,2));await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
