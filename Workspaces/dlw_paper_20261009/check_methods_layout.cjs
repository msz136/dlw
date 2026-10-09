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
  const data=await page.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,mathErrors:document.querySelectorAll('.katex-error').length,
   tables:[...document.querySelectorAll('table.comparison')].map(t=>({headers:t.tHead.rows.length,columns:t.tHead.rows[0].cells.length,rows:t.tBodies[0].rows.length,bold:t.querySelectorAll('strong').length,white:[...t.querySelectorAll('td,th')].every(c=>getComputedStyle(c).backgroundColor==='rgb(255, 255, 255)')}))}));
  if(data.scrollWidth>width+1||data.mathErrors||data.tables.length!==3||data.tables.some(t=>t.headers!==1||!t.white||t.bold<t.rows))throw Error(JSON.stringify(data));
  const tables=page.locator('table.comparison');
  for(let i=0;i<3;i++){await tables.nth(i).scrollIntoViewIfNeeded();await page.screenshot({path:path.join(__dirname,`methods_table${i+1}_${width}.png`)});}
  if(width===1440){const h=page.getByRole('heading',{name:'9.1　网格与迭代格式',exact:true});await h.scrollIntoViewIfNeeded();await page.screenshot({path:path.join(__dirname,'methods_iteration_1440.png')});}
  checks.push(data);await page.close();
 }
 await browser.close();fs.writeFileSync(path.join(__dirname,'methods_layout_validation.json'),JSON.stringify(checks,null,2));console.log(JSON.stringify(checks));
})();
