const fs=require('node:fs'),path=require('node:path');
const {pathToFileURL}=require('node:url');
const runtime='C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const {chromium}=require(path.join(runtime,'playwright'));
const root=path.resolve(__dirname,'../..');
const inventory=JSON.parse(fs.readFileSync(path.join(__dirname,'inventory.json'),'utf8'));
const expected=inventory.groups.flatMap(g=>g.results.map(r=>r.id));
(async()=>{
  const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
  const page=await browser.newPage({viewport:{width:1440,height:1080}});
  const errors=[],remote=[];
  page.on('pageerror',e=>errors.push(String(e)));
  page.on('request',r=>{if(/^https?:/.test(r.url()))remote.push(r.url());});
  await page.goto(pathToFileURL(path.join(root,'theory_results.html')).href);
  await page.waitForFunction(()=>document.documentElement.dataset.mathReady==='true');
  await page.evaluate(()=>document.fonts.ready);
  const inspect=()=>page.evaluate(()=>({
    math:document.querySelectorAll('.katex').length,
    mathErrors:[...document.querySelectorAll('.katex-error')].map(x=>x.textContent),
    overflow:document.documentElement.scrollWidth>innerWidth,
    results:[...document.querySelectorAll('article')].map(x=>x.id),
    badAnchors:[...document.querySelectorAll('a[href^="#"]')].map(x=>x.getAttribute('href')).filter(x=>!document.getElementById(x.slice(1))),
    links:[...document.querySelectorAll('a[href]')].map(x=>x.getAttribute('href')),
    duplicateIds:[...document.querySelectorAll('[id]')].map(x=>x.id).filter((x,i,a)=>a.indexOf(x)!==i),
    pairs:[...document.querySelectorAll('article')].every(x=>x.querySelectorAll('dt').length===2&&x.querySelectorAll('dd').length===2),
    rawMath:/\\[\[\(]/.test(document.querySelector('main').innerText),
    overflowElements:[...document.querySelectorAll('article *, p, .chain')].filter(x=>x.getBoundingClientRect().right>innerWidth+2).map(x=>({tag:x.tagName,class:x.className,text:x.textContent.slice(0,90)})).slice(0,15)
  }));
  const desktop=await inspect();
  await page.screenshot({path:path.join(__dirname,'report_1440.png')});
  await page.locator('#D09').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(__dirname,'report_theorem.png')});
  await page.setViewportSize({width:390,height:844});
  const mobile=await inspect();
  await page.screenshot({path:path.join(__dirname,'report_390.png')});
  const missingFiles=[...new Set(desktop.links.filter(x=>!x.startsWith('#')&&!/^\w+:/.test(x)))].filter(x=>!fs.existsSync(path.join(root,x)));
  const result={status:'passed',desktop,mobile,errors,remote,missingFiles};
  if(errors.length||remote.length||missingFiles.length||desktop.overflow||mobile.overflow||desktop.mathErrors.length||mobile.mathErrors.length||desktop.badAnchors.length||desktop.duplicateIds.length||!desktop.pairs||desktop.rawMath||JSON.stringify(desktop.results)!==JSON.stringify(expected)){
    result.status='failed';process.exitCode=1;
  }
  fs.writeFileSync(path.join(__dirname,'validation.json'),JSON.stringify(result,null,2)+'\n');
  console.log(JSON.stringify({status:result.status,results:desktop.results.length,math:desktop.math,desktopOverflow:desktop.overflow,mobileOverflow:mobile.overflow,errors,missingFiles,mobileOverflowElements:mobile.overflowElements},null,2));
  await browser.close();
})().catch(e=>{console.error(e);process.exitCode=1;});
