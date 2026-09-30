const fs=require('node:fs'),path=require('node:path');
const {pathToFileURL}=require('node:url');
const {chromium}=require('C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root=path.resolve(__dirname,'../..');
(async()=>{
 const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
 const page=await browser.newPage({viewport:{width:1280,height:1050}}),errors=[];
 page.on('pageerror',e=>errors.push(String(e)));
 await page.goto(pathToFileURL(path.join(root,'index.html')).href);
 await page.waitForFunction(()=>document.querySelectorAll('.katex').length>0);
 await page.evaluate(()=>document.fonts.ready);
 const inspect=()=>page.evaluate(()=>({
  headings:[...document.querySelectorAll('h2')].map(x=>x.textContent),
  methods:[...document.querySelectorAll('h3')].map(x=>x.textContent),
  tables:document.querySelectorAll('table').length,math:document.querySelectorAll('.katex').length,
  mathErrors:[...document.querySelectorAll('.katex-error')].map(x=>x.textContent),
  equationNumbers:[...document.querySelectorAll('.katex-tag')].map(x=>x.textContent),
  overflow:document.documentElement.scrollWidth>innerWidth,
  equationScroll:[...document.querySelectorAll('.katex-display')].map((x,i)=>({number:i+1,scroll:x.scrollWidth>x.clientWidth+1})),
  rawDollars:(document.querySelector('main').innerText.match(/\$/g)||[]).length,
  codeBlocks:document.querySelectorAll('pre').length,
  tableText:[...document.querySelectorAll('table')].map(x=>x.innerText),
  newSectionText:[...document.querySelectorAll('main>*')].slice(0).filter(x=>x.previousElementSibling?.id==='section-2').map(x=>x.innerText)
 }));
 const desktop=await inspect();
 await page.locator('#section-2').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(__dirname,'recurrences_desktop.png')});
 await page.locator('h3').filter({hasText:'2.2'}).scrollIntoViewIfNeeded();await page.screenshot({path:path.join(__dirname,'sd2_desktop.png')});
 await page.setViewportSize({width:390,height:844});
 await page.locator('#section-2').scrollIntoViewIfNeeded();const mobile=await inspect();await page.screenshot({path:path.join(__dirname,'recurrences_mobile.png')});
 await page.goto(pathToFileURL(path.join(__dirname,'before/index.html')).href);
 await page.waitForFunction(()=>document.querySelectorAll('.katex').length>0);
 const beforeTableText=await page.evaluate(()=>[...document.querySelectorAll('table')].map(x=>x.innerText));
 const tablesUnchanged=JSON.stringify(beforeTableText)===JSON.stringify(desktop.tableText);
 const expected=Array.from({length:16},(_,i)=>`(${i+1})`);
 const numbersContinuous=JSON.stringify(desktop.equationNumbers)===JSON.stringify(expected);
 const result={desktop,mobile,tablesUnchanged,numbersContinuous,errors};
 fs.writeFileSync(path.join(__dirname,'validation.json'),JSON.stringify(result,null,2));
 console.log(JSON.stringify({math:desktop.math,tables:desktop.tables,headings:desktop.headings,methods:desktop.methods,
  equationNumbers:desktop.equationNumbers,numbersContinuous,tablesUnchanged,desktopOverflow:desktop.overflow,
  mobileOverflow:mobile.overflow,desktopEquationScroll:desktop.equationScroll.filter(x=>x.scroll),mathErrors:desktop.mathErrors,errors},null,2));
 await browser.close();
 if(errors.length||desktop.mathErrors.length||mobile.mathErrors.length||desktop.overflow||mobile.overflow||desktop.rawDollars||desktop.codeBlocks||!numbersContinuous||!tablesUnchanged)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
