const fs=require('node:fs');
const path=require('node:path');
const {pathToFileURL}=require('node:url');
const {chromium}=require('C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root=path.resolve(__dirname,'../..');
const out=path.join(__dirname,'index_preview');fs.mkdirSync(out,{recursive:true});
(async()=>{
 const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
 const page=await browser.newPage({viewport:{width:1280,height:1000}});
 const errors=[];page.on('pageerror',e=>errors.push(String(e)));
 await page.goto(pathToFileURL(path.join(root,'index.html')).href+'#controlled-results');
 await page.waitForFunction(()=>document.querySelectorAll('.katex').length>0);
 await page.evaluate(()=>document.fonts.ready);
 const inspect=()=>page.evaluate(()=>{
  const section=document.getElementById('controlled-results');
  return {tables:section.querySelectorAll('table').length,headings:[...section.querySelectorAll('h3')].map(e=>e.textContent),
   text:section.innerText,mathErrors:[...document.querySelectorAll('.katex-error')].map(e=>e.textContent),
   sourceLinks:[...section.querySelectorAll('a')].map(a=>a.getAttribute('href')),
   sectionOverflow:section.scrollWidth>section.clientWidth+1,
   missingAnchors:[...document.querySelectorAll('a[href^="#"]')].filter(a=>!document.getElementById(a.hash.slice(1))).map(a=>a.hash)};
 });
 const desktop=await inspect();await page.screenshot({path:path.join(out,'desktop.png')});
 await page.getByRole('heading',{name:'4．对照二：固定图3与均匀网格，只换时间算法',exact:true}).scrollIntoViewIfNeeded();
 await page.screenshot({path:path.join(out,'time_mesh.png')});
 await page.setViewportSize({width:390,height:844});
 await page.locator('#controlled-results').evaluate(e=>e.scrollIntoView());
 const mobile=await inspect();await page.screenshot({path:path.join(out,'mobile.png')});
 await page.locator('#controlled-results details').first().locator('summary').click();
 const expanded=await page.locator('#controlled-results details').first().evaluate(e=>e.open);
 const missingFiles=desktop.sourceLinks.filter(h=>!fs.existsSync(path.join(root,h)));
 const summary={tables:desktop.tables,headings:desktop.headings,desktopOverflow:desktop.sectionOverflow,mobileOverflow:mobile.sectionOverflow,
  mathErrors:desktop.mathErrors,missingAnchors:desktop.missingAnchors,missingFiles,expanded,errors,
  hasUpdatedTimeRatio:desktop.text.includes('11.3'),hasSingleSolitonBoundary:desktop.text.includes('单孤子的SD2尚未做同样对齐')};
 fs.writeFileSync(path.join(out,'page_checks.json'),JSON.stringify(summary,null,2));console.log(JSON.stringify(summary,null,2));
 await browser.close();
 if(summary.tables!==6||summary.desktopOverflow||summary.mobileOverflow||summary.mathErrors.length||summary.missingAnchors.length||missingFiles.length||errors.length||!expanded||!summary.hasUpdatedTimeRatio||!summary.hasSingleSolitonBoundary)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
