const fs=require('fs'),path=require('path');
const {chromium}=require('C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const {pathToFileURL}=require('url');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
 const results=[];
 for(const width of [1440,390]){
  const page=await browser.newPage({viewport:{width,height:1000},javaScriptEnabled:false});
  await page.goto(pathToFileURL(path.resolve(__dirname,'../../report/dlw_draft_audit_20261010.html')).href);
  await page.evaluate(()=>document.fonts.ready);
  const result=await page.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,math:document.querySelectorAll('math').length,errors:document.querySelectorAll('.katex-error').length,sections:document.querySelectorAll('h2').length,rawMath:/\\(?:alpha|rho|tau|omega|frac|partial)\b/.test(document.body.innerText)}));
  if(result.scrollWidth>width+1||result.errors||result.rawMath)throw Error(JSON.stringify(result));
  await page.screenshot({path:path.join(__dirname,'page_'+width+'.png')});
  await page.locator('#s7').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(__dirname,'dispersion_'+width+'.png')});
  results.push(result);await page.close();
 }
 await browser.close();fs.writeFileSync(path.join(__dirname,'layout_validation.json'),JSON.stringify(results,null,2));console.log(JSON.stringify(results));
})().catch(e=>{console.error(e);process.exit(1)});
