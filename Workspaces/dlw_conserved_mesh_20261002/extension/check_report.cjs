const fs=require('node:fs'),path=require('node:path');
const {pathToFileURL,fileURLToPath}=require('node:url');
const {chromium}=require('C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
 const root=path.resolve(__dirname,'../../..');
 const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
 const page=await browser.newPage();const errors=[],remote=[],views=[];
 page.on('pageerror',e=>errors.push(String(e)));page.on('request',r=>{if(/^https?:/.test(r.url()))remote.push(r.url())});
 for(const width of [1280,390]){
  await page.setViewportSize({width,height:900});await page.goto(pathToFileURL(path.join(root,'report','dlw_conserved_mesh.html')).href);
  await page.evaluate(()=>document.fonts.ready);
  views.push(await page.evaluate(()=>({width:innerWidth,expanded:false,overflow:document.documentElement.scrollWidth>innerWidth,title:document.title,images:document.images.length,broken:[...document.images].filter(x=>!x.complete||!x.naturalWidth).length,tables:document.querySelectorAll('table').length,links:[...document.querySelectorAll('a[href]')].map(x=>x.href)})));
  await page.screenshot({path:path.join(__dirname,`report_${width}.png`)});
  await page.evaluate(()=>document.querySelectorAll('details').forEach(x=>x.open=true));
  views.push(await page.evaluate(()=>({width:innerWidth,expanded:true,overflow:document.documentElement.scrollWidth>innerWidth,broken:[...document.images].filter(x=>!x.complete||!x.naturalWidth).length})));
 }
 await page.setViewportSize({width:1280,height:950});await page.evaluate(()=>document.querySelectorAll('details').forEach(x=>x.open=false));
 await page.locator('h2').filter({hasText:'精确解与数值解的实际差值'}).scrollIntoViewIfNeeded();await page.screenshot({path:path.join(__dirname,'report_results.png')});
 await page.locator('h2').filter({hasText:'还有什么密度值得继续'}).scrollIntoViewIfNeeded();await page.screenshot({path:path.join(__dirname,'report_next_density.png')});
 const missing=views[0].links.filter(x=>!fs.existsSync(fileURLToPath(x)));
 await page.goto(pathToFileURL(path.join(root,'Workspaces/dlw_conserved_mesh_20261002/short_time_report.html')).href);
 const shortLinks=await page.evaluate(()=>[...document.querySelectorAll('a[href]')].map(x=>x.href));
 const missingShort=shortLinks.filter(x=>x.startsWith('file:')&&!fs.existsSync(fileURLToPath(x)));
 const passed=!errors.length&&!remote.length&&!missing.length&&!missingShort.length&&views.every(v=>!v.overflow&&!v.broken)&&views[0].images===6&&views[0].tables>=16;
 const result={status:passed?'passed':'failed',views,errors,remote,missing,missingShort};fs.writeFileSync(path.join(__dirname,'html_validation.json'),JSON.stringify(result,null,2));
 console.log(JSON.stringify({status:result.status,views:views.map(({links,...v})=>v),errors,remote,missing,missingShort}));await browser.close();if(!passed)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
