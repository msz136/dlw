const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {chromium} = require('C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
  const browser = await chromium.launch({headless: true, executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
  const context = await browser.newContext({offline: true, javaScriptEnabled: false});
  const page = await context.newPage();
  const failures = [];
  page.on('requestfailed', r => failures.push({url: r.url(), reason: r.failure()?.errorText}));
  await page.setViewportSize({width: 1440, height: 1080});
  await page.goto(pathToFileURL(path.resolve(__dirname, '../../report/dlw_direct_tau.html')).href);
  await page.evaluate(()=>document.fonts.ready);
  async function inspect() {
    return page.evaluate(()=>({
      title: document.querySelector('h1').innerText,
      math: document.querySelectorAll('.katex').length,
      errors: document.querySelectorAll('.katex-error').length,
      tables: document.querySelectorAll('table').length,
      overflow: document.documentElement.scrollWidth > innerWidth+1,
      images: [...document.images].map(x=>({loaded: x.complete && x.naturalWidth > 0, width: x.naturalWidth})),
      scripts: document.querySelectorAll('script').length
    }));
  }
  const desktop = await inspect();
  await page.screenshot({path: path.join(__dirname, 'report_1440.png'), fullPage: true});
  await page.setViewportSize({width: 390, height: 844});
  const mobile = await inspect();
  await page.screenshot({path: path.join(__dirname, 'report_390.png'), fullPage: true});
  const success = [desktop, mobile].every(x=>x.math>35 && !x.errors && !x.overflow && x.tables===2 && !x.scripts && x.images.every(y=>y.loaded)) && !failures.length;
  const result = {success, offline: true, desktop, mobile, failures};
  fs.writeFileSync(path.join(__dirname, 'browser_validation.json'), JSON.stringify(result, null, 2)+'\n');
  console.log(JSON.stringify(result));
  await browser.close();
  if (!success) process.exitCode = 1;
})();
