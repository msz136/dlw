const fs=require('fs'),path=require('path');
const {chromium}=require('C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const {pathToFileURL}=require('url');
(async()=>{
 const out=path.join(__dirname,'discussion_revision_20261020','visual');
 fs.mkdirSync(out,{recursive:true});
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
 const checks=[];
 for(const width of [1440,390]){
  const page=await browser.newPage({viewport:{width,height:1000},javaScriptEnabled:false});
  await page.goto(pathToFileURL(path.resolve(__dirname,'../../report/dlw_paper_draft.html')).href);
  await page.evaluate(()=>{document.querySelectorAll('img').forEach(i=>i.loading='eager');});
  await page.evaluate(()=>Promise.all([...document.images].map(i=>i.decode().catch(()=>{}))));
  await page.evaluate(()=>document.fonts.ready);
  const result=await page.evaluate(()=>({
   width:innerWidth,scrollWidth:document.documentElement.scrollWidth,
   brokenImages:[...document.images].filter(i=>!i.complete||!i.naturalWidth).length,
   mathErrors:document.querySelectorAll('.katex-error').length,
   pairs:document.querySelectorAll('.profile-pair').length,
   tables:[...document.querySelectorAll('article')].map(a=>[...a.querySelectorAll('table')].map(t=>t.tBodies[0]?.rows.length)),
   placeholder:/\[Insert|MATHSLOT/.test(document.body.textContent),
   newEnding:document.body.textContent.includes('In particular, the spatial error coefficients can help identify'),
  }));
  if(result.scrollWidth>width+1||result.brokenImages||result.mathErrors||result.pairs!==16||result.placeholder||result.newEnding)throw Error(JSON.stringify(result));
  const pairs=page.locator('#english .profile-pair');
  for(const i of [0,1,2,3,4,5,6,7]){
   if(width===390 && i!==0 && i!==7)continue;
   await pairs.nth(i).screenshot({path:path.join(out,`pair_${i}_${width}.png`)});
  }
  for(const id of ['en-spatial-results','en-conclusion','zh-conclusion']){
   await page.locator('#'+id).scrollIntoViewIfNeeded();
   await page.screenshot({path:path.join(out,id+'_'+width+'.png')});
  }
  checks.push(result);await page.close();
 }
 await browser.close();
 fs.writeFileSync(path.join(out,'layout.json'),JSON.stringify(checks,null,2));console.log(JSON.stringify(checks));
})().catch(e=>{console.error(e);process.exit(1)});
