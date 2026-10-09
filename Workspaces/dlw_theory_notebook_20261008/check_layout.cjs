const fs=require('fs'),path=require('path');
const playwrightPath=process.env.DLW_PLAYWRIGHT_PATH || (process.platform==='win32'?'C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright':'playwright');
const {chromium}=require(playwrightPath);
const {pathToFileURL}=require('url');
(async()=>{
const target=process.argv.includes('--final')?path.resolve(__dirname,'../../report/dlw_theory.html'):path.join(__dirname,'preview.html');
const browser=await chromium.launch({headless:true,executablePath:process.env.DLW_BROWSER_PATH || (process.platform==='win32'?'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe':undefined)});
const checks=[];
for(const width of [1440,390]){
const page=await browser.newPage({viewport:{width,height:1000},javaScriptEnabled:false});
await page.goto(pathToFileURL(target).href);
await page.evaluate(()=>document.fonts.ready);
const data=await page.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,math:document.querySelectorAll('math').length,headings:[...document.querySelectorAll('h2')].map(x=>x.textContent),resources:performance.getEntriesByType('resource').filter(r=>/^https?:/.test(r.name)).length,code:document.querySelectorAll('pre,code,details').length,background:getComputedStyle(document.body).backgroundColor,bodyFont:getComputedStyle(document.body).fontFamily,wideEquations:[...document.querySelectorAll('.eq')].filter(e=>e.scrollWidth>e.clientWidth+2).map(e=>({width:e.scrollWidth,available:e.clientWidth,tex:e.querySelector('annotation').textContent}))}));
if(data.scrollWidth>width+1 || data.math<100 || data.resources || data.code || data.background!=='rgb(255, 255, 255)')throw Error(JSON.stringify(data));
await page.screenshot({path:path.join(__dirname,'theory_top_'+width+'.png')});
await page.getByRole('heading',{name:'6.3　固定谱参数的 Gram 解族',exact:true}).scrollIntoViewIfNeeded();
await page.screenshot({path:path.join(__dirname,'theory_limit_'+width+'.png')});
checks.push(data);await page.close();
}
const printPage=await browser.newPage({viewport:{width:658,height:1000},javaScriptEnabled:false});
await printPage.goto(pathToFileURL(target).href);await printPage.evaluate(()=>document.fonts.ready);await printPage.emulateMedia({media:'print'});
const printing=await printPage.evaluate(()=>({print:true,width:innerWidth,scrollWidth:document.documentElement.scrollWidth,background:getComputedStyle(document.body).backgroundColor,wideEquations:[...document.querySelectorAll('.eq')].filter(e=>e.scrollWidth>e.clientWidth+2).length}));
if(printing.wideEquations || printing.scrollWidth>printing.width)throw Error(JSON.stringify(printing));
checks.push(printing);await printPage.screenshot({path:path.join(__dirname,'theory_print.png')});
await browser.close();fs.writeFileSync(path.join(__dirname,'layout_validation.json'),JSON.stringify(checks,null,2));console.log(JSON.stringify(checks.map(({wideEquations,...x})=>({...x,wideEquations:typeof wideEquations==='number'?wideEquations:wideEquations.length}))));
})();

