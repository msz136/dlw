const fs=require('fs'),path=require('path');
const {chromium}=require('C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const {pathToFileURL}=require('url');
const root=path.resolve(__dirname,'../..');
const target=path.join(root,'report/dlw_conservation_hierarchy.html');
(async()=>{
 const source=fs.readFileSync(path.join(__dirname,'report.src.html'),'utf8');
 if(/[\x00-\x08\x0b\x0c\x0e-\x1f]/.test(source))throw Error('Invalid source control character');
 if(/(?<!\\)\b(?:qquad|frac)\b/.test(source))throw Error('Unescaped TeX command');
 const html=fs.readFileSync(target,'utf8');
 if(html.includes('@@')||html.includes('katex-error'))throw Error('Unrendered equation');
 const links=[...html.matchAll(/href="([^"#]+)"/g)].map(m=>m[1]);
 for(const href of links){if(!fs.existsSync(path.resolve(path.dirname(target),href)))throw Error('Broken link '+href);}
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
 const results=[];
 for(const width of [1440,390]){
  const page=await browser.newPage({viewport:{width,height:1000}});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(pathToFileURL(target).href);await page.waitForLoadState('load');
  const data=await page.evaluate(()=>({math:document.querySelectorAll('math').length,equations:document.querySelectorAll('.equation').length,bodyWidth:document.documentElement.scrollWidth,viewport:innerWidth,title:document.title,externalResources:performance.getEntriesByType('resource').filter(e=>/^https?:/.test(e.name)).length}));
  if(data.bodyWidth>width+1||errors.length||data.math!==26||data.externalResources)throw Error(JSON.stringify({width,data,errors}));
  await page.screenshot({path:path.join(__dirname,'report_top_'+width+'.png')});
  await page.getByRole('heading',{name:'3　逆单值化算子给出无穷生成式'}).scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(__dirname,'report_generator_'+width+'.png')});
  await page.getByRole('heading',{name:'7　原文三组解的精确基准'}).scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(__dirname,'report_benchmarks_'+width+'.png')});
  results.push({width,...data,errors});await page.close();
 }
 await browser.close();fs.writeFileSync(path.join(__dirname,'html_validation.json'),JSON.stringify({passed:true,links,viewports:results},null,2));
 console.log(JSON.stringify({passed:true,viewports:results}));
})().catch(e=>{console.error(e);process.exitCode=1;});
