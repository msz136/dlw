const fs=require('node:fs'),path=require('node:path');
const {pathToFileURL}=require('node:url');
const {chromium}=require('C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const katex=require('../gsg_project/dlw_report/_assets/package/dist/katex.js');
const out=path.join(__dirname,'preview_dynamic_mesh');fs.mkdirSync(out,{recursive:true});
const source=fs.readFileSync(path.join(__dirname,'_src/dynamic_mesh.src.html'),'utf8');
const body=source.split('<main')[1].split('</main>')[0].replace(/<svg[\s\S]*?<\/svg>/g,'');
const formulas=[...body.matchAll(/\$\$([\s\S]*?)\$\$|\$([^$]*?)\$/g)];
const errors=[];
for(const [i,m] of formulas.entries()){
 try{katex.renderToString((m[1]??m[2]).replaceAll('&lt;','<').replaceAll('&gt;','>').replaceAll('&amp;','&'),{throwOnError:true,displayMode:m[1]!==undefined,strict:'error'});}
 catch(e){errors.push({i,formula:m[0],error:e.message});}
}
(async()=>{
 const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
 const page=await browser.newPage({viewport:{width:1440,height:1100},deviceScaleFactor:1});
 const browserErrors=[];page.on('pageerror',e=>browserErrors.push(String(e)));
 await page.goto(pathToFileURL(path.join(__dirname,'DYNAMIC_MESH_REPORT.html')).href);await page.evaluate(()=>document.fonts.ready);
 const inspect=()=>page.evaluate(()=>({
  rendered:document.querySelectorAll('.katex').length,
  mathErrors:[...document.querySelectorAll('.katex-error')].map(e=>e.textContent),
  overflow:document.documentElement.scrollWidth>innerWidth,
  rawDollarCount:(document.querySelector('main').innerText.match(/\$/g)||[]).length,
  missingAnchors:[...document.querySelectorAll('a[href^="#"]')].filter(a=>!document.getElementById(a.getAttribute('href').slice(1))).map(a=>a.getAttribute('href')),
  localLinks:[...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href')).filter(h=>!h.startsWith('#')&&!h.includes('://')),
  tables:document.querySelectorAll('table').length,
  fullTableRowCounts:[...document.querySelectorAll('#euler table,#rk4 table')].map(t=>t.querySelectorAll('tbody tr').length),
  fullTableColumnCounts:[...document.querySelectorAll('#euler table,#rk4 table')].map(t=>t.querySelectorAll('thead th').length)
 }));
 const desktop=await inspect();await page.screenshot({path:path.join(out,'desktop.png')});
 await page.locator('#euler .table-wrap').first().scrollIntoViewIfNeeded();await page.screenshot({path:path.join(out,'table-desktop.png')});
 await page.locator('#mesh figure').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(out,'mesh-desktop.png')});
 await page.setViewportSize({width:390,height:844});await page.goto(pathToFileURL(path.join(__dirname,'DYNAMIC_MESH_REPORT.html')).href);await page.evaluate(()=>document.fonts.ready);
 const mobile=await inspect();await page.screenshot({path:path.join(out,'mobile.png')});
 await page.locator('#euler .table-wrap').first().scrollIntoViewIfNeeded();await page.screenshot({path:path.join(out,'table-mobile.png')});
 await page.locator('summary').click();const detailsOpen=await page.locator('details').evaluate(e=>e.open);
 const missingFiles=desktop.localLinks.filter(h=>!fs.existsSync(path.join(__dirname,decodeURI(h.split('#')[0]))));
 const result={formulaCount:formulas.length,errors,browserErrors,desktop,mobile,missingFiles,detailsOpen};
 fs.writeFileSync(path.join(out,'validation.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result,null,2));
 await browser.close();
 if(errors.length||browserErrors.length||desktop.mathErrors.length||mobile.mathErrors.length||desktop.overflow||mobile.overflow||desktop.rawDollarCount||mobile.rawDollarCount||desktop.missingAnchors.length||missingFiles.length||desktop.rendered!==formulas.length||!detailsOpen||desktop.fullTableRowCounts.some(n=>n!==13)||desktop.fullTableColumnCounts.some(n=>n!==7)||desktop.fullTableRowCounts.length!==8)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1;});
