const {chromium}=require('C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const path=require('path'),fs=require('fs');const {pathToFileURL}=require('url');
(async()=>{
const b=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
const p=await b.newPage({viewport:{width:1440,height:1050}});
await p.goto(pathToFileURL(path.join(__dirname,'notebook_prose_preview.html')).href);await p.evaluate(()=>document.fonts.ready);
for(const [section,file] of [['theory-05','S2'],['theory-10','Gram'],['theory-08','expansion']]){
await p.locator('#'+section).scrollIntoViewIfNeeded();
await p.screenshot({path:path.join(__dirname,'notebook_'+file+'.png')});
}
const result=await p.evaluate(()=>({math:document.querySelectorAll('math').length,literalStars:document.querySelector('main').innerText.includes('**'),width:innerWidth,scrollWidth:document.documentElement.scrollWidth}));
if(result.literalStars||result.width<result.scrollWidth)throw Error(JSON.stringify(result));
fs.writeFileSync(path.join(__dirname,'notebook_layout_validation.json'),JSON.stringify(result,null,2));console.log(result);await b.close();
})();
