const fs=require('fs'),path=require('path');
const {chromium}=require('C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const {pathToFileURL}=require('url');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
 const checks=[];
 for(const width of [1440,390]){
  const page=await browser.newPage({viewport:{width,height:1050},javaScriptEnabled:false});
  await page.goto(pathToFileURL(path.resolve(__dirname,'../../report/dlw_paper_draft.html')).href);
  await page.evaluate(()=>document.fonts.ready);
  for(const im of await page.locator('figure img').all())await im.scrollIntoViewIfNeeded();
  const data=await page.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,mathErrors:document.querySelectorAll('.katex-error').length,
   headings:[...document.querySelectorAll('h2')].map(h=>h.textContent),
   figures:document.querySelectorAll('figure').length,brokenImages:[...document.querySelectorAll('img')].filter(i=>!i.complete||!i.naturalWidth).length,
   tables:[...document.querySelectorAll('table.comparison')].map(t=>({headers:t.tHead.rows.length,columns:t.tHead.rows[0].cells.length,rows:t.tBodies[0].rows.length,bold:t.querySelectorAll('strong').length,white:[...t.querySelectorAll('td,th')].every(c=>getComputedStyle(c).backgroundColor==='rgb(255, 255, 255)')}))}));
  if(data.scrollWidth>width+1||data.mathErrors||data.figures!==6||data.brokenImages||data.tables.length!==4||data.tables.some(t=>t.headers!==1||!t.white||t.bold<t.rows))throw Error(JSON.stringify(data));
  for(const [slug,name] of [['proof','Gram 行列式解及其双线性恒等式'],['results','固定网格上的方法比较'],['time','时间算法比较'],['mesh','动网格对误差的影响'],['single','单孤子波形与误差分布']]){
   const h=page.getByRole('heading').filter({hasText:name}).first();await h.scrollIntoViewIfNeeded();await page.screenshot({path:path.join(__dirname,`structure_${slug}_${width}.png`)});
  }
  checks.push(data);await page.close();
 }
 await browser.close();fs.writeFileSync(path.join(__dirname,'structure_layout_validation.json'),JSON.stringify(checks,null,2));console.log(JSON.stringify(checks));
})();
