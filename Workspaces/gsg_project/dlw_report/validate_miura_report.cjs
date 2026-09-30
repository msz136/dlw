const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {chromium} = require('C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root = path.resolve(__dirname, '../../..');
const output = path.join(__dirname, '_preview_miura');
fs.mkdirSync(output, {recursive:true});
const katex = require('./_assets/package/dist/katex.js');
const source = fs.readFileSync(path.join(__dirname,'_src/miura_dlw.src.html'),'utf8');
// SVG exporters include TeX tick labels inside non-rendered comments.
const body = source.split('<main')[1].split('</main>')[0].replace(/<!--[\s\S]*?-->/g,'');
const formulas = [...body.matchAll(/\$\$([\s\S]*?)\$\$|\$([^$]*?)\$/g)];
const expectedTags = [...body.matchAll(/\\tag\{(\d+)\}/g)].map(m=>m[1]);
if(expectedTags.length!==70 || new Set(expectedTags).size!==70) throw new Error('Expected 70 unique equation numbers');
const errors = [];
for (const [i,m] of formulas.entries()) {
  try { katex.renderToString((m[1] ?? m[2]).replaceAll('&lt;','<').replaceAll('&gt;','>').replaceAll('&amp;','&'), {throwOnError:true,displayMode:m[1]!==undefined,strict:'error'}); }
  catch(e) { errors.push({index:i,formula:m[0],error:e.message}); }
}
(async()=>{
  const browser = await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
  const page = await browser.newPage({viewport:{width:1280,height:1000},deviceScaleFactor:1});
  const browserErrors=[];
  page.on('pageerror',e=>browserErrors.push(String(e)));
  await page.goto(pathToFileURL(path.join(root,'miura_dlw.html')).href);
  await page.waitForFunction(()=>document.querySelectorAll('.katex').length>0);
  await page.evaluate(()=>document.fonts.ready);
  const inspect=()=>page.evaluate(()=>({
    rendered:document.querySelectorAll('.katex').length,
    display:document.querySelectorAll('.katex-display').length,
    mathErrors:[...document.querySelectorAll('.katex-error')].map(e=>e.textContent),
    overflow:document.documentElement.scrollWidth>innerWidth,
    rawDollarCount:(document.querySelector('main').innerText.match(/\$/g)||[]).length,
    missingAnchors:[...document.querySelectorAll('a[href^="#"]')].filter(a=>!document.getElementById(a.getAttribute('href').slice(1))).map(a=>a.getAttribute('href')),
    narrowFormulaScrollers:[...document.querySelectorAll('.mathblock')].filter(e=>e.scrollWidth>e.clientWidth+1).length,
    equationTags:document.querySelectorAll('.katex-display .katex-html > .katex-tag').length,
    overlappingTags:[...document.querySelectorAll('.katex-display .katex-html > .katex-tag')].filter(t=>[...t.parentElement.querySelectorAll(':scope > .katex-base')].some(b=>b.getBoundingClientRect().right>t.getBoundingClientRect().left-5)).map(t=>t.textContent),
    forbiddenText:['验收','校验通过','检查通过'].filter(t=>document.querySelector('main').innerText.includes(t)),
    localLinks:[...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href')).filter(h=>!h.startsWith('#')&&!h.includes('://'))
  }));
  const desktop=await inspect();
  await page.screenshot({path:path.join(output,'desktop.png')});
  await page.locator('#dlw-eliminate').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(output,'derivation.png')});
  await page.locator('#choices-presentation').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(output,'physical-equations.png')});
  await page.locator('#model-error').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(output,'model-error.png')});
  await page.locator('#parameter-optimization').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(output,'parameter-optimization.png')});
  await page.setViewportSize({width:390,height:844});
  await page.goto(pathToFileURL(path.join(root,'miura_dlw.html')).href);
  await page.evaluate(()=>document.fonts.ready);
  const mobile=await inspect();
  await page.screenshot({path:path.join(output,'mobile.png')});
  await page.locator('#dlw-physical').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(output,'mobile-equations.png')});
  await page.locator('#choices-presentation').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(output,'mobile-physical-equations.png')});
  const missingFiles=desktop.localLinks.filter(h=>!fs.existsSync(path.join(root,decodeURI(h.split('#')[0]))));
  const result={formulaCount:formulas.length,errors,browserErrors,desktop,mobile,missingFiles};
  fs.writeFileSync(path.join(output,'result.json'),JSON.stringify(result,null,2));
  console.log(JSON.stringify(result,null,2));
  await browser.close();
  if(errors.length||browserErrors.length||desktop.mathErrors.length||mobile.mathErrors.length||desktop.overflow||mobile.overflow||desktop.rawDollarCount||mobile.rawDollarCount||desktop.missingAnchors.length||missingFiles.length||desktop.forbiddenText.length||desktop.rendered!==formulas.length||desktop.overlappingTags.length||mobile.overlappingTags.length||desktop.equationTags!==expectedTags.length||mobile.equationTags!==expectedTags.length)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1;});
