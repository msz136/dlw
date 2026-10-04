const fs=require('node:fs'),path=require('node:path');
const {pathToFileURL}=require('node:url');
const runtime='C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const {chromium}=require(path.join(runtime,'playwright'));
const root=path.resolve(__dirname,'../..');
const target=path.join(root,'report','dlw_bilinear_nonlinear_lean.html');
(async()=>{
  const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
  const page=await browser.newPage({viewport:{width:1440,height:1080}});
  const errors=[],remote=[];
  page.on('pageerror',e=>errors.push(String(e)));
  page.on('request',r=>{if(/^https?:/.test(r.url()))remote.push(r.url());});
  await page.goto(pathToFileURL(target).href);
  await page.waitForFunction(()=>document.documentElement.dataset.mathReady==='true');
  await page.evaluate(()=>document.fonts.ready);
  const inspect=()=>page.evaluate(()=>({
    math:document.querySelectorAll('.katex').length,
    mathErrors:[...document.querySelectorAll('.katex-error')].map(x=>x.textContent),
    overflow:document.documentElement.scrollWidth>innerWidth,
    anchors:[...document.querySelectorAll('a[href^="#"]')].map(x=>x.getAttribute('href')).filter(x=>!document.getElementById(x.slice(1))),
    links:[...document.querySelectorAll('a[href]')].map(x=>x.getAttribute('href')),
    duplicateIds:[...document.querySelectorAll('[id]')].map(x=>x.id).filter((x,i,a)=>a.indexOf(x)!==i),
    rawMath:/\\[\[\(]/.test(document.querySelector('main').innerText),
    placeholders:/__COMBINED_RUN__|@@|尚待核验/.test(document.body.textContent),
    hasBothTheorems:document.body.textContent.includes('bilinear_to_report7')&&document.body.textContent.includes('bilinear_to_report21_22'),
    overflowElements:[...document.querySelectorAll('p, li, .eq')].filter(x=>x.getBoundingClientRect().right>innerWidth+2).map(x=>({tag:x.tagName,class:x.className,text:x.textContent.slice(0,80)}))
  }));
  const desktop=await inspect();
  await page.screenshot({path:path.join(__dirname,'report_1440.png')});
  await page.locator('#route2').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(__dirname,'report_route2.png')});
  await page.setViewportSize({width:390,height:844});
  await page.evaluate(()=>scrollTo(0,0));
  const mobile=await inspect();
  await page.screenshot({path:path.join(__dirname,'report_390.png')});
  const missingFiles=[...new Set(desktop.links.filter(x=>!x.startsWith('#')&&!/^\w+:/.test(x)))].filter(x=>!fs.existsSync(path.resolve(path.dirname(target),x.split(/[?#]/)[0])));
  const validation={status:'passed',desktop,mobile,errors,remote,missingFiles};
  if(errors.length||remote.length||missingFiles.length||desktop.overflow||mobile.overflow||desktop.mathErrors.length||mobile.mathErrors.length||desktop.anchors.length||desktop.duplicateIds.length||desktop.rawMath||desktop.placeholders||!desktop.hasBothTheorems||desktop.math<10){
    validation.status='failed';process.exitCode=1;
  }
  fs.writeFileSync(path.join(__dirname,'html_validation.json'),JSON.stringify(validation,null,2)+'\n');
  console.log(JSON.stringify({status:validation.status,math:desktop.math,desktopOverflow:desktop.overflow,mobileOverflow:mobile.overflow,errors,remote,missingFiles},null,2));
  await browser.close();
})().catch(e=>{console.error(e);process.exitCode=1;});
