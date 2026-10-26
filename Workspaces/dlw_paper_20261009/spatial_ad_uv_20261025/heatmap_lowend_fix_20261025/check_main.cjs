const fs=require('fs'),path=require('path');
const {pathToFileURL}=require('url');
const {chromium}=require('C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
 try {
  const page=await browser.newPage({viewport:{width:1440,height:1000}});
  await page.goto(pathToFileURL(path.resolve(__dirname,'../../../../dlw-paper.html')).href);
  await page.evaluate(()=>document.fonts.ready);
  const checks=[];
  for(const n of [9,13,17,21]){
   const fig=page.locator('#figure-'+n);
   await fig.scrollIntoViewIfNeeded();
   await fig.locator('img').evaluate(i=>i.decode());
   checks.push(await fig.evaluate(f=>({id:f.id,image:f.querySelector('img').getAttribute('src'),width:f.clientWidth,naturalWidth:f.querySelector('img').naturalWidth,caption:f.querySelector('figcaption').innerText})));
   await fig.screenshot({path:path.join(__dirname,'main_figure_'+n+'.png')});
  }
  fs.writeFileSync(path.join(__dirname,'browser_check.json'),JSON.stringify(checks,null,2));
  console.log(JSON.stringify(checks.map(c=>({id:c.id,image:c.image,naturalWidth:c.naturalWidth}))));
 } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
