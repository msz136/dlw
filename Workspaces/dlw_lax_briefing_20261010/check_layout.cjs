const fs=require('fs'),path=require('path');
const {chromium}=require('C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const {pathToFileURL}=require('url');
(async()=>{
const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
const checks=[];
for(const width of [1440,390]){
const page=await browser.newPage({viewport:{width,height:1000},javaScriptEnabled:false});
await page.goto(pathToFileURL(path.resolve(__dirname,'../../report/dlw_lax_briefing.html')).href);
await page.evaluate(()=>document.fonts.ready);
const data=await page.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,math:document.querySelectorAll('math').length,errors:document.querySelectorAll('.katex-error').length,remote:performance.getEntriesByType('resource').filter(r=>/^https?:/.test(r.name)).length,wideEquations:[...document.querySelectorAll('.eq')].filter(e=>e.scrollWidth>e.clientWidth+2).length}));
if(data.scrollWidth>width+1||data.errors||data.remote||data.math<12)throw Error(JSON.stringify(data));
await page.screenshot({path:path.join(__dirname,`top_${width}.png`)});
await page.locator('#s4').scrollIntoViewIfNeeded();
await page.screenshot({path:path.join(__dirname,`reverse_${width}.png`)});
checks.push(data);await page.close();
}
const page=await browser.newPage({viewport:{width:794,height:1100},javaScriptEnabled:false});
await page.goto(pathToFileURL(path.resolve(__dirname,'../../report/dlw_lax_briefing.html')).href);
await page.emulateMedia({media:'print'});await page.evaluate(()=>document.fonts.ready);
const print=await page.evaluate(()=>({print:true,width:innerWidth,scrollWidth:document.documentElement.scrollWidth,wideEquations:[...document.querySelectorAll('.eq')].filter(e=>e.scrollWidth>e.clientWidth+2).length}));
if(print.scrollWidth>print.width+1||print.wideEquations){
const overflow=await page.evaluate(()=>[...document.querySelectorAll('.katex')].filter(e=>e.getBoundingClientRect().right>innerWidth).map(e=>e.querySelector('annotation')?.textContent));
throw Error(JSON.stringify({...print,overflow}));
}
checks.push(print);await browser.close();
fs.writeFileSync(path.join(__dirname,'layout_validation.json'),JSON.stringify(checks,null,2));console.log(JSON.stringify(checks));
})();
