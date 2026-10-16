const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {chromium} = require('C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root = path.resolve(__dirname, '../..');
const files = ['非线性化讲稿.html', '2HS数值分析讲稿.html', 'DLW数值分析讲稿.html'];

(async () => {
  const browser = await chromium.launch({headless:true,
    executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
  const results = [];
  for (const [index, filename] of files.entries()) {
    const page = await browser.newPage({viewport:{width:1440,height:1080}});
    const errors = [], remote = [], failed = [];
    page.on('pageerror', e => errors.push(String(e)));
    page.on('request', r => {if (/^https?:/.test(r.url())) remote.push(r.url());});
    page.on('requestfailed', r => failed.push({url:r.url(),reason:r.failure()?.errorText}));
    await page.goto(pathToFileURL(path.join(root,'notebook','讲稿',filename)).href);
    await page.waitForFunction(() => document.documentElement.dataset.mathReady === 'true');
    await page.evaluate(() => document.fonts.ready);
    const inspect = () => page.evaluate(() => ({
      math:document.querySelectorAll('.katex').length,
      mathErrors:[...document.querySelectorAll('.katex-error')].map(x => ({text:x.textContent,error:x.title})),
      overflow:document.documentElement.scrollWidth > innerWidth + 1,
      rawMath:[...document.querySelectorAll('main p,main li,main td')].filter(x => /\\[()\[\]]|\$\$/.test(x.innerText)).map(x => x.innerText.slice(0,120)),
      brokenImages:[...document.querySelectorAll('img')].filter(x => !x.complete || x.naturalWidth === 0).map(x => x.src),
      missingAnchors:[...document.querySelectorAll('a[href^="#"]')].filter(x => !document.getElementById(x.getAttribute('href').slice(1))).map(x => x.getAttribute('href')),
      duplicateIds:[...document.querySelectorAll('[id]')].map(x => x.id).filter((x,i,a) => a.indexOf(x)!==i),
      headingCount:document.querySelectorAll('h2').length,
      horizontalCodeBlocks:[...document.querySelectorAll('pre')].filter(x => x.scrollWidth>x.clientWidth).length,
      h1:document.querySelector('h1').innerText,
      mainFont:getComputedStyle(document.querySelector('main')).fontFamily
    }));
    const desktop = await inspect();
    await page.screenshot({path:path.join(__dirname,`lecture_${index+1}_1440.png`)});
    const sections = page.locator('h2');
    await sections.nth(Math.min(4,await sections.count()-1)).scrollIntoViewIfNeeded();
    await page.screenshot({path:path.join(__dirname,`lecture_${index+1}_code_1440.png`)});
    await page.setViewportSize({width:390,height:844});
    await page.evaluate(() => scrollTo(0,0));
    const mobile = await inspect();
    await page.screenshot({path:path.join(__dirname,`lecture_${index+1}_390.png`)});
    await page.setViewportSize({width:1440,height:1080});
    await page.emulateMedia({media:'print'});
    const print = await inspect();
    const passed = [desktop,mobile,print].every(v => !v.overflow && !v.mathErrors.length && !v.rawMath.length && !v.brokenImages.length && !v.missingAnchors.length && !v.duplicateIds.length && v.math > 10)
      && !errors.length && !remote.length && !failed.length;
    results.push({filename,passed,desktop,mobile,print,errors,remote,failed});
    console.log(JSON.stringify({filename,passed,math:desktop.math,desktopOverflow:desktop.overflow,mobileOverflow:mobile.overflow,mathErrors:desktop.mathErrors}));
    await page.close();
  }
  await browser.close();
  const validation = {success:results.every(r=>r.passed),reports:results,
    inspected:'Real headless Edge: local file rendering, desktop, narrow screen, print, font and image resources'};
  fs.writeFileSync(path.join(__dirname,'browser_validation.json'),JSON.stringify(validation,null,2)+'\n');
  if (!validation.success) process.exitCode = 1;
})();
