const fs=require('node:fs');
const path=require('node:path');
const {pathToFileURL}=require('node:url');
const {chromium}=require('C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root=path.resolve(__dirname,'../..');
(async()=>{
 const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
 const page=await browser.newPage();const errors=[],requests=[];
 page.on('pageerror',e=>errors.push(String(e)));page.on('request',r=>{if(/^https?:/.test(r.url()))requests.push(r.url())});
 const views=[];
 for(const width of [1280,390]){
  await page.setViewportSize({width,height:950});
  await page.goto(pathToFileURL(path.join(__dirname,'report.html')).href);
  await page.evaluate(()=>document.fonts.ready);
  views.push(await page.evaluate(()=>({width:innerWidth,title:document.title,language:document.documentElement.lang,overflow:document.documentElement.scrollWidth>innerWidth,mathCount:document.querySelectorAll('.katex').length,displayCount:document.querySelectorAll('.katex-display').length,mathErrors:[...document.querySelectorAll('.katex-error')].map(n=>n.innerText),sections:document.querySelectorAll('h2[id]').length,links:[...document.querySelectorAll('a[href]')].map(n=>n.getAttribute('href')),badAnchors:[...document.querySelectorAll('a[href^="#"]')].filter(n=>!document.querySelector(n.getAttribute('href'))).map(n=>n.getAttribute('href')),unrendered:document.querySelector('main').innerText.includes('$$')})));
  await page.screenshot({path:path.join(__dirname,`report_${width}.png`)});
 }
 await page.setViewportSize({width:1280,height:950});await page.locator('#section-5').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(__dirname,'report_physical.png')});
 const missingFiles=views[0].links.filter(s=>!s.startsWith('#')&&!/^https?:/.test(s)).filter(s=>!fs.existsSync(path.join(__dirname,s)));
 const manifest=JSON.parse(fs.readFileSync(path.join(__dirname,'manifest.json'),'utf8'));
 const passed=views.every(v=>!v.overflow&&!v.mathErrors.length&&!v.badAnchors.length&&!v.unrendered&&v.sections===manifest.section_count&&v.mathCount===manifest.math_count&&v.displayCount===manifest.equation_count)&&!errors.length&&!requests.length&&!missingFiles.length;
 const result={status:passed?'passed':'failed',views,errors,remoteRequests:requests,missingFiles,newPdeRuns:0};
 fs.writeFileSync(path.join(__dirname,'html_validation.json'),JSON.stringify(result,null,2));
 console.log(JSON.stringify({...result,views:views.map(({links,...v})=>v)}));await browser.close();if(!passed)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
