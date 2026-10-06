const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {pathToFileURL}=require('node:url');
const {chromium}=require('C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const here=__dirname,root=path.resolve(here,'../..'),dir=path.join(here,'stepwise_preview');fs.mkdirSync(dir,{recursive:true});
const result={checks:[],views:[],errors:[],httpRequests:[]};
const dlw=['error-prepare','error-config','error-profile','error-coefficient','error-residual','error-main','error-convergence'];
const hs=['hs-prepare','hs-config','hs-reference','hs-spatial','hs-rk4','hs-evolve','hs-error'];
const pass=(name,detail)=>{result.checks.push({name,passed:true,detail});console.log('PASS '+name);};
async function run(page,id){await page.locator(`#${id} [data-run]`).click();await page.waitForFunction(()=>document.querySelector('[data-cancel]').disabled,{timeout:35000});}
const count=(page,id)=>page.locator(`#${id} .cell-status`).getAttribute('data-executions');
async function sequence(page,ids){for(const id of ids){await run(page,id);assert.match(await page.locator(`#${id} .cell-status`).innerText(),/OK/);}}
(async()=>{
 const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
 const page=await browser.newPage({viewport:{width:1440,height:1000}});
 page.on('pageerror',e=>result.errors.push(String(e)));page.on('request',r=>{if(/^https?:/.test(r.url()))result.httpRequests.push(r.url());});
 try{
  await page.goto(pathToFileURL(path.join(root,'Report.html')).href);await page.evaluate(()=>document.fonts.ready);
  assert.equal(await page.locator('[data-run-all],[data-run-js]').count(),0);assert.equal(await page.locator('.code-cell[data-kind="js"]').count(),14);assert.equal(await page.locator('.code-cell[data-kind="lean"]').count(),6);
  pass('only per-cell Run controls; import/start/endpoint and two seven-cell numerical sequences');
  await run(page,dlw.at(-1));assert.match(await page.locator('#error-convergence .cell-output').innerText(),/请先运行/);assert.equal(await page.locator('#error-prepare .cell-output').innerText(),'');
  pass('missing prerequisites are reported without executing any preceding cell');
  await sequence(page,dlw.slice(0,5));
  assert.equal(await count(page,dlw[0]),'1');assert.equal(await page.locator('#error-convergence .cell-output').innerText(),'');assert.equal(await page.locator('.cell-output svg').count(),0);
  pass('preparation and definitions preserve state without producing final calculations');
  await run(page,'error-main');assert.equal(await page.locator('#error-main svg').count(),0);assert.match(await page.locator('#error-main .cell-output').innerText(),/1\.68606/);
  await run(page,'error-convergence');assert.equal(await page.locator('#error-convergence svg').count(),2);
  const defaultDLW=await page.locator('#error-convergence .cell-output').innerText();
  assert.equal(await count(page,dlw[0]),'1');assert.equal(await count(page,'error-config'),'1');
  pass('only the final requested cell draws convergence; preparation and configuration ran once');
  await run(page,'error-convergence');assert.equal(await count(page,'error-convergence'),'2');assert.equal(await count(page,'error-profile'),'1');assert.equal(await page.locator('#error-convergence .cell-output').innerText(),defaultDLW);assert.equal(await page.locator('#error-convergence svg').count(),2);
  pass('repeat execution uses the retained state and replaces only current output');
  const cfg=await page.locator('#error-config textarea').inputValue();await page.locator('#error-config textarea').fill(cfg.replace('h: 1 / 8','h: 1 / 16'));
  assert.equal(await page.locator('#error-convergence .cell-output').innerText(),'');await run(page,'error-convergence');assert.match(await page.locator('#error-convergence .cell-output').innerText(),/设置谱参数/);assert.equal(await count(page,'error-prepare'),'1');
  await sequence(page,dlw.slice(1));assert.notEqual(await page.locator('#error-convergence .cell-output').innerText(),defaultDLW);assert.equal(await count(page,'error-prepare'),'1');
  pass('parameter edits invalidate descendants and require explicit reruns without replaying preparation');
  const coeff=await page.locator('#error-coefficient textarea').inputValue();
  await page.locator('#error-coefficient textarea').fill(coeff.replace('function coefficient(z)', 'function coefficient(]'));
  await run(page,'error-coefficient');assert.match(await page.locator('#error-coefficient .cell-output').innerText(),/SyntaxError/);assert.match(await page.locator('#error-profile .cell-status').innerText(),/OK/);
  await page.locator('#error-coefficient textarea').fill(coeff);await sequence(page,dlw.slice(3));
  pass('a syntax error affects its own cell and can be repaired using existing preceding definitions');
  const normalMain=await page.locator('#error-main .cell-output').innerText();
  await page.locator('#error-coefficient textarea').fill(coeff.replace('/6, zeta','/7, zeta'));assert.notEqual(await page.locator('#error-coefficient textarea').inputValue(),coeff);
  await sequence(page,dlw.slice(3));assert.notEqual(await page.locator('#error-main .cell-output').innerText(),normalMain);
  pass('the current core expression is actually executed');
  await page.locator('[data-reset]').click();assert.match(await page.locator('#error-coefficient textarea').inputValue(),/\/7, zeta/);await run(page,'error-main');assert.match(await page.locator('#error-main .cell-output').innerText(),/准备残差/);
  pass('reset clears the retained environment and keeps edits');
  await page.locator('[data-restore-all]').click();await sequence(page,dlw.slice(0,3));
  await page.locator('#error-coefficient textarea').fill('while (true) {}');await page.locator('#error-coefficient [data-run]').click();await page.waitForTimeout(200);await page.locator('[data-cancel]').click();assert.equal(await page.locator('#error-profile .cell-output').innerText(),'');await run(page,'error-main');assert.match(await page.locator('#error-main .cell-output').innerText(),/准备残差/);
  pass('cancel terminates this kernel and asks the reader to restart its preparation');
  await page.locator('[data-restore-all]').click();await sequence(page,dlw.slice(0,3));await page.locator('#error-coefficient textarea').fill('while (true) {}');await run(page,'error-coefficient');assert.match(await page.locator('#error-coefficient .cell-output').innerText(),/超过 15 秒/);
  pass('timeout terminates a nonreturning cell and clears unavailable retained state');
  await page.locator('[data-restore-all]').click();await sequence(page,dlw);assert.equal(await page.locator('#error-convergence .cell-output').innerText(),defaultDLW);
  await run(page,'hs-error');assert.match(await page.locator('#hs-error .cell-output').innerText(),/准备数值环境/);
  await sequence(page,hs.slice(0,5));assert.equal(await page.locator('#hs-evolve .cell-output').innerText(),'');assert.equal(await page.locator('#hs-error .cell-output').innerText(),'');
  await run(page,'hs-evolve');assert.equal(await page.locator('#hs-error .cell-output').innerText(),'');assert.equal(await page.locator('#hs-evolve svg').count(),0);
  await run(page,'hs-error');const defaultHS=await page.locator('#hs-error .cell-output').innerText();assert.match(defaultHS,/OK/);assert.match(defaultHS,/0\.0100127/);assert.equal(await page.locator('#hs-error svg').count(),2);for(const id of hs)assert.equal(await count(page,id),'1');
  pass('2HS definitions, RK4 evolution, and final error plotting happen in separate requested cells',defaultHS);
  const hsCfg=await page.locator('#hs-config textarea').inputValue();await page.locator('#hs-config textarea').fill(hsCfg.replace('T: 0.5','T: 0.25'));await sequence(page,hs.slice(1));assert.notEqual(await page.locator('#hs-error .cell-output').innerText(),defaultHS);assert.equal(await count(page,'hs-prepare'),'1');
  pass('2HS parameter edits recalculate through explicit cells without rerunning its preparation');
  for(const width of [1440,390]){
    await page.setViewportSize({width,height:width===390?844:1000});
    const view=await page.evaluate(()=>({width:innerWidth,overflow:document.documentElement.scrollWidth>innerWidth+1,mathErrors:[...document.querySelectorAll('.katex-error')].map(e=>e.textContent),font:getComputedStyle(document.body).font}));
    assert.equal(view.overflow,false);assert.deepEqual(view.mathErrors,[]);result.views.push(view);
    await page.locator('#nonlinear-uw').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(dir,`import-${width}.png`)});
    await page.locator('#hs-rk4').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(dir,`hs-rk4-${width}.png`)});
    await page.locator('#error-convergence .cell-output').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(dir,`dlw-output-${width}.png`)});
  }
  await page.emulateMedia({media:'print'});assert.equal(await page.locator('#error-config .source-editor').evaluate(e=>getComputedStyle(e).display),'none');assert.equal(await page.locator('#error-config .print-source').evaluate(e=>getComputedStyle(e).display),'block');
  assert.deepEqual(result.errors,[]);assert.deepEqual(result.httpRequests,[]);pass('narrow screen, formulas, synchronized print source and offline execution');
 }finally{fs.writeFileSync(path.join(here,'stepwise_browser_validation.json'),JSON.stringify(result,null,2));await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
