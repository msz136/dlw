const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const {pathToFileURL} = require('node:url');
const {chromium} = require('C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const here=__dirname,root=path.resolve(here,'../..');
const out=path.join(here,'preview');fs.mkdirSync(out,{recursive:true});
const results={checks:[],views:[],errors:[],requests:[]};
function pass(name,detail){results.checks.push({name,passed:true,detail});console.log('PASS '+name);}
async function waitJS(page){await page.waitForFunction(()=>!document.querySelector('[data-run-js]').disabled,{timeout:35000});}
async function restore(page){await page.locator('[data-restore-all]').click();}
async function runGroup(page,id){await page.locator(`#${id} [data-run]`).click();await waitJS(page);}
async function inspect(page){return page.evaluate(()=>({
  width:innerWidth,overflow:document.documentElement.scrollWidth>innerWidth+1,
  bodyFont:getComputedStyle(document.body).font,mainPadding:getComputedStyle(document.querySelector('main')).padding,
  mathErrors:[...document.querySelectorAll('.katex-error')].map(e=>e.textContent),
  cellCount:document.querySelectorAll('.code-cell[data-kind]').length,
  mathCount:document.querySelectorAll('.katex').length,images:document.images.length,tables:document.querySelectorAll('main>table').length,
  badAnchors:[...document.querySelectorAll('a[href^="#"]')].map(e=>e.getAttribute('href')).filter(h=>!document.getElementById(h.slice(1))),
  status:document.getElementById('notebook-status')?.textContent || '',
  duplicates:[...new Set([...document.querySelectorAll('[id]')].map(e=>e.id))].filter(id=>document.querySelectorAll('[id]').length && [...document.querySelectorAll('[id]')].filter(e=>e.id===id).length>1)
}));}
(async()=>{
 const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
 const page=await browser.newPage({viewport:{width:1440,height:1000}});
 page.on('pageerror',e=>results.errors.push(String(e)));
 page.on('request',r=>{if(/^https?:/.test(r.url()))results.requests.push(r.url());});
 try{
  await page.goto(pathToFileURL(path.join(root,'Report.html')).href);await page.evaluate(()=>document.fonts.ready);
  const original=await browser.newPage({viewport:{width:1440,height:1000}});await original.goto(pathToFileURL(path.join(here,'before/Report.html')).href);
  const old=await inspect(original),fresh=await inspect(page);
  assert.equal(fresh.bodyFont,old.bodyFont);assert.equal(fresh.mainPadding,old.mainPadding);assert.equal(fresh.images,old.images);assert.equal(fresh.tables,old.tables);
  assert.deepEqual(fresh.mathErrors,[]);assert.deepEqual(fresh.duplicates,[]);assert.deepEqual(fresh.badAnchors,[]);
  pass('original typography, images, tables and formula rendering preserved',fresh);await original.close();
  await runGroup(page,'error-compare');
  const defaultText=await page.locator('#error-compare .cell-output').innerText();
  assert.match(defaultText,/OK/);assert.equal(await page.locator('#error-compare svg').count(),2);
  pass('offline Worker executes the three visible DLW cells',defaultText);
  const config=await page.locator('#error-config textarea').inputValue();
  await page.locator('#error-config textarea').fill(config.replace('h: 1 / 8','h: 1 / 16'));
  assert.equal(await page.locator('#error-compare .cell-output').innerText(),'');
  assert.match(await page.locator('#error-compare .cell-status').innerText(),/待运行/);
  await runGroup(page,'error-compare');assert.notEqual(await page.locator('#error-compare .cell-output').innerText(),defaultText);
  pass('parameter edit changes the numerical result and invalidates downstream output');
  await restore(page);
  const core=await page.locator('#error-core textarea').inputValue();
  await page.locator('#error-core textarea').fill(core.replace('/6, zeta','/7, zeta'));
  assert.notEqual(await page.locator('#error-core textarea').inputValue(),core);
  await runGroup(page,'error-compare');const altered=await page.locator('#error-compare .cell-output').innerText();assert.notEqual(altered,defaultText);assert.match(altered,/OK/);
  pass('editing the displayed core expression changes the computed coefficient');
  await page.locator('[data-reset]').click();assert.match(await page.locator('#error-core textarea').inputValue(),/\/7, zeta/);assert.equal(await page.locator('#error-compare .cell-output').innerText(),'');
  pass('reset clears results and preserves edits');
  await page.locator('#error-core textarea').fill(core.replace('const polys = [[1]];','const polys = [;'));
  await runGroup(page,'error-compare');assert.match(await page.locator('#error-core .cell-output').innerText(),/SyntaxError/);assert.equal(await page.locator('#error-compare .cell-output').innerText(),'');
  pass('syntax error is assigned to the correct cell and stops downstream execution');
  await restore(page);await runGroup(page,'error-compare');assert.equal(await page.locator('#error-compare .cell-output').innerText(),defaultText);
  pass('restoring examples reproduces the default result');
  await page.locator('#error-core textarea').fill('while (true) {}');await page.locator('#error-compare [data-run]').click();await page.waitForTimeout(300);await page.locator('[data-cancel]').click();
  assert.equal(await page.locator('[data-run-js]').isDisabled(),false);assert.match(await page.locator('#error-compare .cell-status').innerText(),/已取消/);
  pass('cancel terminates a nonreturning Worker and keeps the page usable');
  await restore(page);await page.locator('#error-core textarea').fill('while (true) {}');await runGroup(page,'error-compare');assert.match(await page.locator('#error-compare .cell-output').innerText(),/超过 15 秒/);
  pass('timeout terminates a nonreturning Worker');
  await restore(page);await runGroup(page,'error-compare');
  await runGroup(page,'error-compare');assert.equal(await page.locator('#error-compare .cell-output').innerText(),defaultText);assert.equal(await page.locator('#error-compare svg').count(),2);
  pass('repeat execution replaces results without duplicates');
  if(await page.locator('.code-cell[data-group="hs-error"]').count()){
    const last=page.locator('.code-cell[data-group="hs-error"]').last();await last.locator('[data-run]').click();await waitJS(page);
    const hsResult=await last.locator('.cell-output').innerText();assert.match(hsResult,/OK/);pass('2HS visible code reproduces the report parameter point',hsResult);
  }
  for(const width of [1440,390]){
    await page.setViewportSize({width,height:width===390?844:1000});await page.evaluate(()=>document.fonts.ready);
    const info=await inspect(page);assert.equal(info.overflow,false);assert.deepEqual(info.mathErrors,[]);results.views.push(info);
    await page.locator('#nonlinear-uw').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(out,`lean-start-${width}.png`)});
    await page.locator('#lean-qrm').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(out,`lean-end-${width}.png`)});
    await page.locator('#error-compare .cell-output').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(out,`dlw-output-${width}.png`)});
  }
  pass('desktop and narrow screen layouts have no page overflow');
  await page.emulateMedia({media:'print'});
  const print=await page.evaluate(()=>({hidden:getComputedStyle(document.querySelector('.source-editor')).display,source:getComputedStyle(document.querySelector('.print-source')).display,code:document.querySelector('.print-source').textContent}));
  assert.equal(print.hidden,'none');assert.equal(print.source,'block');assert.ok(print.code.length>100);pass('printing uses complete synchronized code',print);
  assert.deepEqual(results.errors,[]);assert.deepEqual(results.requests,[]);pass('offline runtime makes no HTTP requests');
 }finally{fs.writeFileSync(path.join(here,'browser_validation.json'),JSON.stringify(results,null,2));await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
