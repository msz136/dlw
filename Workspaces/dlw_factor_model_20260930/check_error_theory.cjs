const fs=require('node:fs'),path=require('node:path');
const {pathToFileURL}=require('node:url');
const runtime='C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const {chromium}=require(path.join(runtime,'playwright'));
const katex=require('../gsg_project/dlw_report/_assets/package/dist/katex.min.js');
const root=path.resolve(__dirname,'../..');
const reportDirectory=path.join(root,'report');
const manifest=JSON.parse(fs.readFileSync(path.join(__dirname,'html_manifest.json'),'utf8'));
const compilationErrors=[];
manifest.formulas.forEach((entry,index)=>{
 const trim=entry.display?2:1;
 try{katex.renderToString(entry.text.slice(trim,-trim).trim(),{
  displayMode:entry.display,throwOnError:true,strict:'ignore'
 });}catch(e){compilationErrors.push({index,message:String(e)});}
});
(async()=>{
 const browser=await chromium.launch({
  executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
  headless:true
 });
 const page=await browser.newPage({viewport:{width:1440,height:1080}}),errors=[],external=[];
 page.on('pageerror',e=>errors.push(String(e)));
 page.on('request',r=>{if(/^https?:/.test(r.url()))external.push(r.url());});
 await page.goto(pathToFileURL(path.join(reportDirectory,'dlw_error_theory.html')).href);
 await page.waitForFunction(()=>document.documentElement.dataset.mathReady==='true');
 await page.evaluate(()=>document.fonts.ready);
 const inspect=()=>page.evaluate(()=>({
  math:document.querySelectorAll('.katex').length,
  bodyMath:[...document.querySelectorAll('.katex')].filter(x=>!x.closest('nav')).length,
  mathErrors:[...document.querySelectorAll('.katex-error')].map(x=>x.textContent),
  tags:[...document.querySelectorAll('.katex-tag')].map(x=>x.textContent),
  rawDollars:(document.querySelector('main').innerText.match(/\$/g)||[]).length,
  overflow:document.documentElement.scrollWidth>innerWidth,
  displayScroll:[...document.querySelectorAll('.katex-display')].map((x,i)=>({
   equation:i+1,scroll:x.scrollWidth>x.clientWidth+2,
   width:x.scrollWidth,available:x.clientWidth
  })).filter(x=>x.scroll),
  links:[...document.querySelectorAll('a[href]')].map(x=>x.getAttribute('href')),
  badAnchors:[...document.querySelectorAll('a[href^="#"]')].map(x=>x.getAttribute('href')).filter(x=>!document.querySelector(x)),
  sections:document.querySelectorAll('h2').length,
  tables:document.querySelectorAll('table').length,
  references:document.querySelectorAll('.references a').length
 }));
 const desktop=await inspect();
 await page.screenshot({path:path.join(__dirname,'theory_desktop.png')});
 await page.locator('#section-5').scrollIntoViewIfNeeded();
 await page.screenshot({path:path.join(__dirname,'theory_derivation.png')});
 await page.locator('#section-9').scrollIntoViewIfNeeded();
 await page.screenshot({path:path.join(__dirname,'theory_propagation.png')});
 await page.setViewportSize({width:390,height:844});
 await page.locator('#section-5').scrollIntoViewIfNeeded();
 const mobile=await inspect();
 await page.screenshot({path:path.join(__dirname,'theory_mobile.png')});
 const numbersContinuous=JSON.stringify(desktop.tags)===JSON.stringify(
  Array.from({length:manifest.equations},(_,i)=>'('+(i+1)+')'));
 const missingFiles=desktop.links.filter(x=>!x.startsWith('#')&&!/^\w+:/.test(x))
  .filter(x=>!fs.existsSync(path.join(reportDirectory,x.split('#')[0])));
 const result={
  status:'passed',source_sha256:manifest.source_sha256,
  compilationErrors,numbersContinuous,missingFiles,external,errors,desktop,mobile
 };
 if(compilationErrors.length||errors.length||external.length||missingFiles.length||
    !numbersContinuous||desktop.bodyMath!==manifest.math_segments||
    desktop.mathErrors.length||mobile.mathErrors.length||desktop.overflow||mobile.overflow||
    desktop.rawDollars||mobile.rawDollars||desktop.badAnchors.length||desktop.references!==5){
  result.status='failed';process.exitCode=1;
 }
 fs.writeFileSync(path.join(__dirname,'html_validation.json'),JSON.stringify(result,null,2));
 console.log(JSON.stringify({
  status:result.status,formulas:desktop.math,equations:desktop.tags.length,
  sections:desktop.sections,compilationErrors,numbersContinuous,missingFiles,external,errors,
  desktopOverflow:desktop.overflow,mobileOverflow:mobile.overflow,
  desktopScroll:desktop.displayScroll,mobileScrollableEquations:mobile.displayScroll.length,
  rawDollars:desktop.rawDollars,references:desktop.references
 },null,2));
 await browser.close();
})().catch(e=>{console.error(e);process.exitCode=1;});
