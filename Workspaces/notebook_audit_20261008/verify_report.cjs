const fs = require('fs');
const path = require('path');
const {pathToFileURL} = require('url');
const {chromium} = require('C:/Program Files/WindowsApps/OpenAI.CodexPrimaryRuntime.v26-1007-641-0_26.1007.641.0_x64__3k8sg7r9htsxt/dependencies/node/node_modules/playwright');

(async () => {
  const root = path.resolve(__dirname, '../..');
  const report = path.join(root, 'report/notebook_review_20261009.html');
  const executable = 'C:/Users/msz/AppData/Local/ms-playwright/chromium_headless_shell-1208/chrome-headless-shell-win64/chrome-headless-shell.exe';
  const result = {report, executable};
  const browser = await chromium.launch({headless:true,executablePath:executable});
  const page = await browser.newPage({viewport:{width:1280,height:900}});
  const errors = [];
  page.on('pageerror', error => errors.push(String(error)));
  await page.goto(pathToFileURL(report).href);
  await page.screenshot({path:path.join(__dirname,'report_desktop.png'),fullPage:true});
  await page.screenshot({path:path.join(__dirname,'report_desktop_top.png')});
  result.desktop = await page.evaluate(() => ({
    scrollWidth:document.documentElement.scrollWidth,
    clientWidth:document.documentElement.clientWidth,
    h1:document.querySelector('h1').textContent,
    tables:document.querySelectorAll('table').length,
    brokenImages:[...document.images].filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.src)
  }));
  await page.setViewportSize({width:390,height:844});
  await page.screenshot({path:path.join(__dirname,'report_mobile.png'),fullPage:true});
  await page.screenshot({path:path.join(__dirname,'report_mobile_top.png')});
  result.mobile = await page.evaluate(() => ({
    scrollWidth:document.documentElement.scrollWidth,
    clientWidth:document.documentElement.clientWidth,
    overflowingTables:[...document.querySelectorAll('.table-wrap')].filter(x=>x.scrollWidth>x.clientWidth).length
  }));
  await page.emulateMedia({media:'print'});
  result.print = await page.evaluate(() => ({detailsHidden:getComputedStyle(document.querySelector('details')).display==='none'}));
  result.pageErrors = errors;
  const links = [...fs.readFileSync(report,'utf8').matchAll(/(?:href|src)="([^"]+)"/g)].map(m=>m[1]);
  result.missingLocalLinks = links.filter(l=>!l.startsWith('http')).filter(l=>!fs.existsSync(path.resolve(path.dirname(report),l)));
  fs.writeFileSync(path.join(__dirname,'report_validation.json'),JSON.stringify(result,null,2));
  await browser.close();
  console.log(JSON.stringify(result));
  if (result.desktop.scrollWidth>result.desktop.clientWidth || result.mobile.scrollWidth>result.mobile.clientWidth || errors.length || result.desktop.brokenImages.length || result.missingLocalLinks.length) process.exitCode=1;
})().catch(e=>{console.error(String(e));process.exitCode=1});
