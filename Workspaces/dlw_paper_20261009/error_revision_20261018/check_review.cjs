const fs=require('fs'),path=require('path');
const {chromium}=require('C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const {pathToFileURL}=require('url');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
 const results=[];
 for(const width of [1440,390]){
  const page=await browser.newPage({viewport:{width,height:1050},javaScriptEnabled:false});
  await page.goto(pathToFileURL(path.resolve(process.env.DLW_REVIEW_TARGET||'review/dlw_paper_draft.html')).href);
  await page.evaluate(()=>document.fonts.ready);
  if(process.env.DLW_REVIEW_TARGET)for(const im of await page.locator('figure img').all())await im.scrollIntoViewIfNeeded();
  const data=await page.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,mathErrors:document.querySelectorAll('.katex-error').length,unrenderedSlots:document.body.textContent.includes('MATHSLOT'),displayMath:document.querySelectorAll('.eq').length,articles:document.querySelectorAll('article').length,images:document.images.length,brokenImages:[...document.images].filter(i=>!i.complete||!i.naturalWidth).length}));
  if(data.scrollWidth>width+1||data.mathErrors||data.unrenderedSlots||(process.env.DLW_REVIEW_TARGET&&data.brokenImages))throw Error(JSON.stringify(data));
  for(const id of ['en-eq-201','zh-eq-201','en-eq-203','zh-eq-207','zh-app-a','en-app-f']){
   await page.locator('#'+id).scrollIntoViewIfNeeded();await page.screenshot({path:`review/${id}_${width}.png`});
  }
  results.push(data);await page.close();
 }
 await browser.close();fs.writeFileSync('review/layout.json',JSON.stringify(results,null,2));console.log(JSON.stringify(results));
})();
