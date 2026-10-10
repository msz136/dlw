const fs=require('fs'),path=require('path');
const {chromium}=require('C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const {pathToFileURL}=require('url');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
 const checks=[];
 for(const width of [1440,390]){
  const page=await browser.newPage({viewport:{width,height:1000},javaScriptEnabled:false});
  await page.goto(pathToFileURL(path.resolve(__dirname,'../../report/dlw_paper_draft.html')).href);
  await page.evaluate(()=>document.fonts.ready);
  for(const img of await page.locator('figure img').all())await img.scrollIntoViewIfNeeded();
  const data=await page.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,
   mathErrors:document.querySelectorAll('.katex-error').length,figures:document.querySelectorAll('figure').length,
   brokenImages:[...document.images].filter(i=>!i.complete||!i.naturalWidth).length,
   tables:[...document.querySelectorAll('table.comparison')].map(t=>({rows:t.tBodies[0].rows.length,bold:t.querySelectorAll('strong').length}))}));
  if(data.scrollWidth>width+1||data.mathErrors||data.brokenImages||data.figures!==20||data.tables.length!==6||data.tables.some((t,i)=>t.rows!==[4,4,4][i%3]))throw Error(JSON.stringify(data));
  for(const section of ['zh-spatial-results','zh-time-results','zh-mesh-results']){ await page.locator('#'+section).scrollIntoViewIfNeeded(); await page.screenshot({path:path.join(__dirname,'four_case_final_revision', section+'_'+width+'.png')}); }
  checks.push(data);await page.close();
 }
 await browser.close();fs.writeFileSync(path.join(__dirname,'four_case_final_revision/layout.json'),JSON.stringify(checks,null,2));console.log(JSON.stringify(checks));
})();
