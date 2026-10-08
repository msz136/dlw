const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {chromium} = require('C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const files = ['integrability.html','nonlinear-definitions.html'];

(async () => {
  const browser = await chromium.launch({headless:true,
    executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
  const reports = [];
  for (const name of files) {
    const page = await browser.newPage({viewport:{width:1440,height:1080}});
    const errors = [], remote = [], failures = [];
    page.on('pageerror', e => errors.push(String(e)));
    page.on('request', r => {if(/^https?:/.test(r.url())) remote.push(r.url());});
    page.on('requestfailed', r => failures.push(r.url()));
    await page.goto(pathToFileURL(path.join(__dirname,'preview',name)).href);
    await page.waitForFunction(() => document.documentElement.dataset.mathReady === 'true');
    await page.evaluate(() => document.fonts.ready);
    const inspect = () => page.evaluate(() => ({
      math:document.querySelectorAll('.katex').length,
      mathErrors:[...document.querySelectorAll('.katex-error')].map(e=>({text:e.textContent,error:e.title})),
      overflow:document.documentElement.scrollWidth>innerWidth+1,
      rawMath:[...document.querySelectorAll('main p,main td,main li')].filter(e=>/\\[()\[\]]|\$\$/.test(e.innerText)).map(e=>e.innerText.slice(0,80)),
      code:document.querySelectorAll('pre.source').length,
      output:document.querySelectorAll('pre.output').length
    }));
    const desktop = await inspect();
    await page.screenshot({path:path.join(__dirname,`${name}_1440.png`)});
    const target = name==='integrability.html' ? '#jacobian-text' : '#lean-uw';
    await page.locator(target).scrollIntoViewIfNeeded();
    await page.screenshot({path:path.join(__dirname,`${name}_code_1440.png`)});
    await page.setViewportSize({width:390,height:844});
    await page.evaluate(()=>scrollTo(0,0));
    const mobile = await inspect();
    await page.screenshot({path:path.join(__dirname,`${name}_390.png`)});
    await page.setViewportSize({width:1440,height:1080});
    await page.emulateMedia({media:'print'});
    const print = await inspect();
    const success = [desktop,mobile,print].every(v=>!v.overflow&&!v.mathErrors.length&&!v.rawMath.length&&v.math>10)
      && !errors.length && !remote.length && !failures.length;
    reports.push({name,success,desktop,mobile,print,errors,remote,failures});
    console.log(JSON.stringify({name,success,math:desktop.math,code:desktop.code,output:desktop.output}));
    await page.close();
  }
  await browser.close();
  const result = {success:reports.every(r=>r.success),reports,
    scope:'Offline HTML reading preview of the exact notebook markdown, source and saved compiler streams; native Colab/VS Code UI was not automated.'};
  fs.writeFileSync(path.join(__dirname,'browser_validation.json'),JSON.stringify(result,null,2)+'\n');
  if(!result.success) process.exitCode=1;
})();
