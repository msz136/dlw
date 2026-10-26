const fs = require('fs');
const path = require('path');
const {pathToFileURL} = require('url');
const {chromium} = require('C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async () => {
  const browser = await chromium.launch({headless:true, executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
  const results=[];
  for (const width of [1440,390]) {
    const page=await browser.newPage({viewport:{width,height:1000},deviceScaleFactor:1});
    await page.goto(pathToFileURL(path.resolve(__dirname,'../../../dlw-paper.html')).href);
    await page.evaluate(()=>document.fonts.ready);
    for(const img of await page.locator('[id="section-5.1"] img,[id="section-5.2"] img').all()) await img.scrollIntoViewIfNeeded();
    results.push(await page.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,
      brokenImages:[...document.querySelectorAll('[id="section-5.1"] img,[id="section-5.2"] img')].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.src),
      tables:[...document.querySelectorAll('[id="section-5.1"] table,[id="section-5.2"] table')].map(t=>{const r=t.getBoundingClientRect();return {id:t.id,width:r.width,left:r.left,right:r.right,scrollWidth:t.scrollWidth,parentWidth:t.parentElement.clientWidth}}),
      figures:[...document.querySelectorAll('[id="section-5.1"] figure,[id="section-5.2"] figure')].map(f=>({id:f.id,width:f.clientWidth,source:f.querySelector('img').getAttribute('src'),naturalWidth:f.querySelector('img').naturalWidth})),
      emptySections:['section-5.3','section-5.4','section-5.5'].filter(id=>document.getElementById(id).innerText.trim().split('\n').length===1)})));
    for(const id of ['table-parameters','table-initial','table-final','figure-13']) {
      await page.locator('#'+id).scrollIntoViewIfNeeded();
      await page.locator('#'+id).screenshot({path:path.join(__dirname,id+'_'+width+'.png')});
    }
    await page.close();
  }
  await browser.close();
  fs.writeFileSync(path.join(__dirname,'layout_checks.json'),JSON.stringify(results,null,2));
  console.log(JSON.stringify(results.map(x=>({width:x.width,scrollWidth:x.scrollWidth,brokenImages:x.brokenImages,tables:x.tables,emptySections:x.emptySections})),null,2));
})().catch(e=>{console.error(e);process.exitCode=1});

