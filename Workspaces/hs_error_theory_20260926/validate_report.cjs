const fs=require('node:fs');
const path=require('node:path');
const {pathToFileURL}=require('node:url');
const {chromium}=require('C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const katex=require('../gsg_project/dlw_report/_assets/package/dist/katex.js');
const out=path.join(__dirname,'preview');fs.mkdirSync(out,{recursive:true});
const source=fs.readFileSync(path.join(__dirname,'_src/index.src.html'),'utf8');
const body=source.split('<main')[1].split('</main>')[0].replace(/<svg[\s\S]*?<\/svg>/g,'');
const formulas=[...body.matchAll(/\$\$([\s\S]*?)\$\$|\$([^$]*?)\$/g)];
const tags=[...body.matchAll(/\\tag\{(\d+)\}/g)].map(m=>m[1]);
if(tags.length!==22 || new Set(tags).size!==22)throw new Error('Expected 22 unique equation numbers');
const errors=[];
for(const [i,m] of formulas.entries()){
 try{katex.renderToString((m[1]??m[2]).replaceAll('&lt;','<').replaceAll('&gt;','>').replaceAll('&amp;','&'),{throwOnError:true,displayMode:m[1]!==undefined,strict:'error'});}
 catch(e){errors.push({i,formula:m[0],error:e.message});}
}
(async()=>{
 const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
 const page=await browser.newPage({viewport:{width:1280,height:1000},deviceScaleFactor:1});
 const browserErrors=[];page.on('pageerror',e=>browserErrors.push(String(e)));
 await page.goto(pathToFileURL(path.join(__dirname,'index.html')).href);
 await page.waitForFunction(()=>document.querySelectorAll('.katex').length>0);
 await page.evaluate(()=>document.fonts.ready);
 const inspect=()=>page.evaluate(()=>({
  rendered:document.querySelectorAll('.katex').length,
  mathErrors:[...document.querySelectorAll('.katex-error')].map(e=>e.textContent),
  overflow:document.documentElement.scrollWidth>innerWidth,
  rawDollarCount:(document.querySelector('main').innerText.match(/\$/g)||[]).length,
  missingAnchors:[...document.querySelectorAll('a[href^="#"]')].filter(a=>!document.getElementById(a.getAttribute('href').slice(1))).map(a=>a.getAttribute('href')),
  equationTags:document.querySelectorAll('.katex-display .katex-html > .katex-tag').length,
  overlappingTags:[...document.querySelectorAll('.katex-display .katex-html > .katex-tag')].filter(t=>[...t.parentElement.querySelectorAll(':scope > .katex-base')].some(b=>b.getBoundingClientRect().right>t.getBoundingClientRect().left-5)).map(t=>t.textContent),
  localLinks:[...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href')).filter(h=>!h.startsWith('#')&&!h.includes('://')),
  tables:document.querySelectorAll('table').length,
  title:document.title
 }));
 const desktop=await inspect();
 await page.screenshot({path:path.join(out,'desktop.png')});
 for(const [id,name] of [['coefficients','coefficients'],['main-table','tables'],['design','design']]){
  await page.locator('#'+id).scrollIntoViewIfNeeded();await page.screenshot({path:path.join(out,name+'.png')});
 }
 await page.setViewportSize({width:390,height:844});await page.goto(pathToFileURL(path.join(__dirname,'index.html')).href);await page.evaluate(()=>document.fonts.ready);
 const mobile=await inspect();await page.screenshot({path:path.join(out,'mobile.png')});
 await page.locator('#main-table').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(out,'mobile-tables.png')});
 await page.locator('details').first().locator('summary').click();
 const detailsOpen=await page.locator('details').first().evaluate(e=>e.open);
 const missingFiles=desktop.localLinks.filter(h=>!fs.existsSync(path.join(__dirname,decodeURI(h.split('#')[0]))));
 const result={formulaCount:formulas.length,errors,browserErrors,desktop,mobile,missingFiles,detailsOpen};
 fs.writeFileSync(path.join(out,'validation.json'),JSON.stringify(result,null,2));
 console.log(JSON.stringify(result,null,2));await browser.close();
 if(errors.length||browserErrors.length||desktop.mathErrors.length||mobile.mathErrors.length||desktop.overflow||mobile.overflow||desktop.rawDollarCount||mobile.rawDollarCount||desktop.missingAnchors.length||missingFiles.length||desktop.rendered!==formulas.length||desktop.overlappingTags.length||mobile.overlappingTags.length||desktop.equationTags!==tags.length||mobile.equationTags!==tags.length||!detailsOpen)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1;});
