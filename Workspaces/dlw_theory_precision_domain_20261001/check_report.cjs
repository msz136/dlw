const fs=require('node:fs');
const path=require('node:path');
const {pathToFileURL}=require('node:url');
const runtime='C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const {chromium}=require(path.join(runtime,'playwright'));
const root=path.resolve(__dirname,'../..');
(async()=>{
  const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
  const page=await browser.newPage();
  const errors=[],remote=[];
  page.on('pageerror',e=>errors.push(String(e)));
  page.on('request',r=>{if(/^https?:/.test(r.url()))remote.push(r.url())});
  const views=[];
  for(const width of [1280,390]){
    await page.setViewportSize({width,height:960});
    await page.goto(pathToFileURL(path.join(__dirname,'report.html')).href);
    await page.evaluate(()=>document.fonts.ready);
    views.push(await page.evaluate(()=>({
      width:innerWidth,overflow:document.documentElement.scrollWidth>innerWidth,
      ready:document.documentElement.dataset.mathReady,
      math:document.querySelectorAll('.katex').length,
      mathErrors:[...document.querySelectorAll('.katex-error')].map(e=>e.textContent),
      headings:document.querySelectorAll('h2').length,
      equations:document.querySelectorAll('.katex-tag').length,
      tableRows:[...document.querySelectorAll('table tbody')].map(t=>t.rows.length),
      invalidAnchors:[...document.querySelectorAll('a[href^="#"]')].map(a=>a.getAttribute('href')).filter(h=>!document.querySelector(h)),
      links:[...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href'))
    })));
    await page.screenshot({path:path.join(__dirname,'report_'+width+'.png')});
  }
  await page.setViewportSize({width:1280,height:960});
  await page.locator('#uniform').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(__dirname,'report_uniform.png')});
  const missingFiles=views[0].links.filter(h=>!h.startsWith('#')&&!/^https?:/.test(h)).filter(h=>!fs.existsSync(path.join(__dirname,h)));
  const manifest=JSON.parse(fs.readFileSync(path.join(__dirname,'manifest.json'),'utf8'));
  const passed=views.every(v=>!v.overflow&&v.ready==='true'&&!v.mathErrors.length&&!v.invalidAnchors.length&&v.equations===manifest.equation_count&&v.equations>20&&v.headings===9&&JSON.stringify(v.tableRows)==='[3,4,4,4]')&&!errors.length&&!remote.length&&!missingFiles.length;
  const result={status:passed?'passed':'failed',views,errors,remoteRequests:remote,missingFiles};
  fs.writeFileSync(path.join(__dirname,'html_validation.json'),JSON.stringify(result,null,2));
  console.log(JSON.stringify(result,null,2));
  await browser.close();
  if(!passed)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
