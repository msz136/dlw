const fs=require('node:fs'),path=require('node:path');
const {pathToFileURL}=require('node:url');
const {chromium}=require('C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root=path.resolve(__dirname,'../..'),out=path.join(__dirname,'paper_preview');fs.mkdirSync(out,{recursive:true});
(async()=>{
 const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
 const page=await browser.newPage({viewport:{width:1280,height:1050}}),errors=[];
 page.on('pageerror',e=>errors.push(String(e)));
 await page.goto(pathToFileURL(path.join(root,'index.html')).href);
 await page.waitForFunction(()=>document.querySelectorAll('.katex').length>0);
 await page.evaluate(()=>document.fonts.ready);
 const inspect=()=>page.evaluate(()=>({
  title:document.querySelector('h1').textContent,headings:[...document.querySelectorAll('h2')].map(x=>x.textContent),
  tables:document.querySelectorAll('table').length,math:document.querySelectorAll('.katex').length,
  mathErrors:[...document.querySelectorAll('.katex-error')].map(x=>x.textContent),
  font:getComputedStyle(document.body).fontFamily,background:getComputedStyle(document.querySelector('main')).backgroundColor,
  overflow:document.documentElement.scrollWidth>innerWidth,rawDollars:(document.querySelector('main').innerText.match(/\$/g)||[]).length,
  obsoleteTerms:['修复','旧表','新版','哈希','工程','Darboux','Lean','逆散射','研究更新'].filter(x=>document.querySelector('main').innerText.includes(x)),
  links:[...document.querySelectorAll('a')].map(a=>a.getAttribute('href'))
 }));
 const desktop=await inspect();await page.screenshot({path:path.join(out,'desktop.png')});
 await page.locator('#section-3').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(out,'time.png')});
 await page.setViewportSize({width:390,height:844});await page.evaluate(()=>scrollTo(0,0));
 const mobile=await inspect();await page.screenshot({path:path.join(out,'mobile.png')});
 const missingFiles=desktop.links.filter(h=>!fs.existsSync(path.join(root,h)));
 const result={desktop,mobile,missingFiles,errors};fs.writeFileSync(path.join(out,'validation.json'),JSON.stringify(result,null,2));
 console.log(JSON.stringify(result,null,2));await browser.close();
 if(errors.length||missingFiles.length||desktop.mathErrors.length||desktop.rawDollars||desktop.obsoleteTerms.length||desktop.overflow||mobile.overflow||desktop.tables!==5||desktop.headings.length!==6)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
