const fs = require('fs');
const path = require('path');
const {pathToFileURL} = require('url');
const {chromium} = require('C:/Program Files/WindowsApps/OpenAI.CodexPrimaryRuntime.v26-1007-641-0_26.1007.641.0_x64__3k8sg7r9htsxt/dependencies/node/node_modules/playwright');
(async () => {
  const report = path.resolve(__dirname, '../../report/mch_ldg_2608_28077_reading.html');
  const browser = await chromium.launch({headless:true,executablePath:'C:/Users/msz/AppData/Local/ms-playwright/chromium_headless_shell-1208/chrome-headless-shell-win64/chrome-headless-shell.exe'});
  const page = await browser.newPage({viewport:{width:1280,height:900},javaScriptEnabled:false});
  const errors = [];
  page.on('pageerror', e=>errors.push(String(e)));
  await page.goto(pathToFileURL(report).href);
  await page.screenshot({path:path.join(__dirname, 'guide_desktop_top.png')});
  const inspect = () => page.evaluate(() => ({
    width:document.documentElement.clientWidth,scrollWidth:document.documentElement.scrollWidth,
    equations:document.querySelectorAll('.katex').length,
    missingImages:[...document.images].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.alt),
    errorNodes:document.querySelectorAll('.katex-error').length,
  }));
  const result = {desktop:await inspect()};
  await page.locator('#flux').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(__dirname,'guide_flux.png')});
  await page.locator('#error').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(__dirname,'guide_error.png')});
  const figureDetail = page.locator('details').filter({has:page.locator('figure')});
  await figureDetail.locator('summary').click();
  await page.locator('figure').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(__dirname, 'guide_figure.png')});
  result.figureOpens = await figureDetail.getAttribute('open') !== null;
  await page.setViewportSize({width:390,height:844});
  await page.evaluate(()=>window.scrollTo(0,0));
  await page.screenshot({path:path.join(__dirname,'guide_mobile_top.png')});
  result.mobile = await inspect();
  await page.locator('#flux').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(__dirname,'guide_mobile_flux.png')});
  const links = await page.locator('a').evaluateAll(nodes=>nodes.map(a=>a.getAttribute('href')));
  result.missingLocalLinks = links.filter(h=>!h.startsWith('http')&&!h.startsWith('#')).filter(h=>!fs.existsSync(path.resolve(path.dirname(report), h.split('#')[0])));
  result.missingAnchors = await page.locator('a[href^="#"]').evaluateAll(nodes=>nodes.map(a=>a.getAttribute('href').slice(1)).filter(id=>!document.getElementById(id)));
  result.pageErrors = errors;
  fs.writeFileSync(path.join(__dirname,'layout_validation.json'),JSON.stringify(result,null,2));
  await browser.close();
  console.log(JSON.stringify(result));
  if(result.desktop.scrollWidth>result.desktop.width||result.mobile.scrollWidth>result.mobile.width||result.desktop.errorNodes||result.desktop.missingImages.length||result.missingLocalLinks.length||result.missingAnchors.length||errors.length||!result.figureOpens)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
