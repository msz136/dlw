const fs=require('fs'),path=require('path');
const {pathToFileURL}=require('url');
const {chromium}=require('C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
 const checks=[];
 try {
  for(const width of [1440,390]) {
   const page=await browser.newPage({viewport:{width,height:1000}});
   await page.goto(pathToFileURL(path.resolve(__dirname,'../../../report/dlw_figtable_audit_20261025.html')).href);
   await page.evaluate(()=>document.fonts.ready);
   checks.push(await page.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,headings:[...document.querySelectorAll('h2')].map(x=>x.textContent)})));
   if(width===1440) await page.screenshot({path:path.join(__dirname,'report_summary_1440.png')});
   await page.close();
  }
 } finally {await browser.close();}
 fs.writeFileSync(path.join(__dirname,'report_checks.json'),JSON.stringify(checks,null,2));
 if(checks.some(x=>x.scrollWidth>x.width))throw Error('Report overflows');
 console.log(JSON.stringify(checks));
})().catch(e=>{console.error(e);process.exitCode=1});
