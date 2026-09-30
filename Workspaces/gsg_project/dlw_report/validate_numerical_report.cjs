const fs=require('node:fs');
const path=require('node:path');
const {pathToFileURL}=require('node:url');
const {chromium}=require('C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root=path.resolve(__dirname,'../../..');
const out=path.join(__dirname,'_preview_numerical');fs.mkdirSync(out,{recursive:true});
(async()=>{
 const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
 const page=await browser.newPage({viewport:{width:1440,height:1050}});
 const errors=[];page.on('pageerror',e=>errors.push(String(e)));
 await page.goto(pathToFileURL(path.join(root,'numerical_analysis.html')).href);
 await page.waitForFunction(()=>document.querySelectorAll('.katex').length>0);
 await page.evaluate(()=>document.fonts.ready);
 await page.evaluate(async()=>{await Promise.all([...document.images].map(async image=>{image.loading='eager';await image.decode();}));});
 const inspect=()=>page.evaluate(()=>({
  rendered:document.querySelectorAll('.katex').length,
  mathErrors:[...document.querySelectorAll('.katex-error')].map(e=>e.textContent),
  overflow:document.documentElement.scrollWidth>innerWidth,
  rawDollars:(document.querySelector('main').innerText.match(/\$/g)||[]).length,
  missingAnchors:[...document.querySelectorAll('a[href^="#"]')].filter(a=>!document.getElementById(a.hash.slice(1))).map(a=>a.hash),
  chapters:[...document.querySelectorAll('h2')].map(h=>h.textContent),
  tables:document.querySelectorAll('table').length,
  details:[...document.querySelectorAll('details')].map(e=>({title:e.querySelector('summary').textContent,tables:e.querySelectorAll('table').length,figures:e.querySelectorAll('figure').length})),
  links:[...document.querySelectorAll('a[href],img[src]')].map(e=>e.getAttribute('href')||e.getAttribute('src')),
  images:[...document.images].map(e=>({src:e.getAttribute('data-source')||e.getAttribute('src'),embedded:e.src.startsWith('data:'),valid:e.complete&&e.naturalWidth>0}))
 }));
 const desktop=await inspect();
 await page.screenshot({path:path.join(out,'desktop.png')});
 await page.locator('#results').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(out,'results.png')});
 await page.locator('details summary').first().click();
 const opened=await page.locator('details').first().evaluate(e=>e.open);
 await page.setViewportSize({width:390,height:844});
 await page.evaluate(()=>{document.querySelectorAll('details').forEach(e=>e.open=true);window.scrollTo(0,0)});
 const mobile=await inspect();await page.screenshot({path:path.join(out,'mobile.png')});
 await page.locator('#results').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(out,'mobile-results.png')});
 const missingFiles=desktop.links.filter(h=>!h.startsWith('#')&&!h.startsWith('data:')&&!h.includes('://')).filter(h=>!fs.existsSync(path.join(root,decodeURIComponent(h.split('#')[0]))));
 const expected=JSON.parse(fs.readFileSync(path.join(__dirname,'numerical_report_build.json'),'utf8'));
 desktop.links=desktop.links.filter(h=>!h.startsWith('data:'));mobile.links=mobile.links.filter(h=>!h.startsWith('data:'));
 const result={desktop,mobile,errors,opened,missingFiles,expected};
 fs.writeFileSync(path.join(out,'validation.json'),JSON.stringify(result,null,2));
 console.log(JSON.stringify({rendered:desktop.rendered,tables:desktop.tables,details:desktop.details,chapters:desktop.chapters,desktopOverflow:desktop.overflow,mobileOverflow:mobile.overflow,mathErrors:mobile.mathErrors,missingFiles,errors,rawDollars:mobile.rawDollars,images:mobile.images},null,2));
 await browser.close();
 if(errors.length||desktop.mathErrors.length||mobile.mathErrors.length||desktop.overflow||mobile.overflow||mobile.rawDollars||desktop.missingAnchors.length||missingFiles.length||!opened||desktop.chapters.length!==expected.chapters||desktop.rendered!==expected.math_expressions||desktop.details.some(x=>x.tables+x.figures!==1)||mobile.images.some(x=>!x.valid||!x.embedded))process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
