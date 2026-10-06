const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const runtime = 'C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const {chromium} = require(path.join(runtime, 'playwright'));
const root = path.resolve(__dirname, '../..');
(async () => {
  const browser = await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', headless:true});
  const page = await browser.newPage();
  const errors = [], remoteRequests = [];
  page.on('pageerror', e => errors.push(String(e)));
  page.on('request', r => {if (/^https?:/.test(r.url())) remoteRequests.push(r.url());});
  const views = [];
  for (const width of [1280, 390]) {
    await page.setViewportSize({width,height:950});
    await page.goto(pathToFileURL(path.join(__dirname, 'report.html')).href);
    await page.evaluate(() => document.fonts.ready);
    views.push(await page.evaluate(() => ({
      width:innerWidth, overflow:document.documentElement.scrollWidth > innerWidth,
      title:document.title, language:document.documentElement.lang,
      displayMath:document.querySelectorAll('.eq .katex').length,
      numbers:[...document.querySelectorAll('.num')].map(x => x.innerText),
      renderErrors:document.querySelectorAll('.katex-error').length,
      equationsScroll: [...document.querySelectorAll('.math')].filter(e => e.scrollWidth > e.clientWidth+1).length,
      rows:document.querySelectorAll('tbody tr').length,
      sections:[...document.querySelectorAll('section[id]')].map(x => x.id),
      links:[...document.querySelectorAll('a[href]')].map(x => x.getAttribute('href')),
      theorem:document.querySelector('#distance').innerText,
      scope:document.querySelector('#evolution').innerText,
      unresolvedPlaceholders: document.documentElement.innerHTML.includes('@@'),
      imagesBroken:[...document.images].some(x=>!x.complete || !x.naturalWidth)
    })));
    await page.screenshot({path:path.join(__dirname, `report_${width}.png`)});
  }
  await page.setViewportSize({width:1280,height:1000});
  await page.locator('#distance').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(__dirname, 'report_theorem.png')});
  await page.locator('#validation').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(__dirname, 'report_validation.png')});
  const missingFiles = views[0].links.filter(x => !x.startsWith('#')).filter(x => !fs.existsSync(path.join(__dirname, x)));
  const passed = views.every(v => !v.overflow && v.displayMath===18 && v.numbers.every((n,i)=>n===`(${i+1})`) && !v.renderErrors && v.rows===4 && v.sections.length===8 && !v.unresolvedPlaceholders && !v.imagesBroken) && !errors.length && !remoteRequests.length && !missingFiles.length;
  const result = {status:passed?'passed':'failed',views,errors,remoteRequests,missingFiles,newPdeRuns:0};
  fs.writeFileSync(path.join(__dirname, 'html_validation.json'),JSON.stringify(result,null,2));
  console.log(JSON.stringify({status:result.status,views:views.map(({links,theorem,scope,...rest})=>rest),errors,remoteRequests,missingFiles}));
  await browser.close();
  if (!passed) process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1;});
