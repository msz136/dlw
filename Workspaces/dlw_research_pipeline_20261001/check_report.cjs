const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const runtime = 'C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const {chromium} = require(path.join(runtime, 'playwright'));
const root = path.resolve(__dirname, '../..');
const target = path.join(root, 'report', 'dlw_research_ideas.html');
(async () => {
  const browser = await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
  const page = await browser.newPage();
  const errors = [], remoteRequests = [];
  page.on('pageerror', e => errors.push(String(e)));
  page.on('request', r => {if (/^https?:/.test(r.url())) remoteRequests.push(r.url());});
  const views = [];
  for (const width of [1280, 390]) {
    await page.setViewportSize({width,height:900});
    await page.goto(pathToFileURL(target).href);
    await page.evaluate(() => document.fonts.ready);
    views.push(await page.evaluate(() => ({
      width:innerWidth,
      overflow:document.documentElement.scrollWidth > innerWidth,
      title:document.title,
      language:document.documentElement.lang,
      ideas:[...document.querySelectorAll('section[id]')].map(x => x.id),
      links:[...document.querySelectorAll('a[href]')].map(x => x.getAttribute('href')),
      invalidAnchors:[...document.querySelectorAll('a[href^="#"]')].map(x => x.getAttribute('href')).filter(x => !document.querySelector(x)),
      references:document.querySelectorAll('.references li').length,
      pendingPredictions:[...document.querySelectorAll('section')].filter(x => x.textContent.includes('理论预测。')).length,
      falsifiers:[...document.querySelectorAll('section')].filter(x => x.textContent.includes('证明边界。')).length,
      comparisons:[...document.querySelectorAll('section')].filter(x => x.textContent.includes('比较与自由度。')).length,
      integratedT04:document.querySelector('#T04')?.dataset.status,
      explanationSteps:document.querySelectorAll('#T04 h3').length,
      completedResults:document.querySelectorAll('section[data-status]').length,
      totalSteps:document.querySelectorAll('section h3').length
    })));
    await page.screenshot({path:path.join(__dirname, `report_${width}.png`)});
  }
  await page.setViewportSize({width:1280,height:1000});
  await page.locator('#T04').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(__dirname, 'report_idea_detail.png')});
  const missingFiles = views[0].links.filter(x => !x.startsWith('#') && !/^\w+:/.test(x)).filter(x => !fs.existsSync(path.resolve(path.dirname(target), x.split(/[?#]/)[0])));
  const registry = JSON.parse(fs.readFileSync(path.join(__dirname, 'ideas.json'), 'utf8'));
  const passed = views.every(v => !v.overflow && !v.invalidAnchors.length && v.ideas.length === registry.ideas.length && v.references === registry.sources.length && v.pendingPredictions === registry.ideas.length && v.falsifiers === registry.ideas.length && v.comparisons === registry.ideas.length && v.integratedT04 === 'linear_results_available' && v.explanationSteps === 5 && v.completedResults === 3 && v.totalSteps === 15) && !errors.length && !remoteRequests.length && !missingFiles.length && registry.ideas.every(i => ['registered_theory_question','linear_results_available','parameter_limits_results_available','geometry_results_available'].includes(i.status));
  const result = {status:passed ? 'passed':'failed',views,errors,remoteRequests,missingFiles,newPdeRuns:0};
  fs.writeFileSync(path.join(__dirname, 'html_validation.json'), JSON.stringify(result,null,2));
  console.log(JSON.stringify({status:result.status,views:views.map(({links,...rest})=>rest),errors,remoteRequests,missingFiles}));
  await browser.close();
  if (!passed) process.exitCode=1;
})().catch(e => {console.error(e);process.exitCode=1;});
