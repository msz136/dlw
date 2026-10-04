const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {pathToFileURL,fileURLToPath}=require('node:url');
const {chromium}=require('C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root=path.resolve(__dirname,'../..');
const revision=path.join(__dirname,'revision_euler_crop');
const output=path.join(__dirname,'euler_preview');fs.mkdirSync(output,{recursive:true});
const manifest=JSON.parse(fs.readFileSync(path.join(revision,'euler_plot_validation.json'),'utf8'));
const hash=data=>crypto.createHash('sha256').update(data).digest('hex');
const expectedHashes=manifest.figures.map(f=>hash(fs.readFileSync(path.join(root,f.png)))).sort();
const metadataValid=manifest.method==='Euler'&&JSON.stringify(manifest.x_interval)==='[-1,1]'&&
 manifest.figures.length===36&&manifest.figures.every(f=>f.method==='Euler'&&f.distribution_axes===1&&f.colorbar_axes===1);
const targets=[{name:'atlas',file:path.join(root,'report','dlw_waveform_fields.html')},{name:'index',file:path.join(root,'index.html')}];

async function inspect(page,name){return page.evaluate(name=>{
 const main=document.querySelector('main')||document.body;
 let scope=[main];
 if(name==='index'){
  scope=[];let node=document.getElementById('section-6');
  if(node){scope.push(node);node=node.nextElementSibling;while(node&&node.tagName!=='H2'){scope.push(node);node=node.nextElementSibling;}}
 }
 const collect=selector=>scope.flatMap(e=>[...(e.matches(selector)?[e]:[]),...e.querySelectorAll(selector)]);
 const figures=collect('figure'),images=collect('img'),details=collect('details');
 const text=scope.map(e=>e.textContent).join('\n');
 const ids=[...document.querySelectorAll('[id]')].map(e=>e.id);
 return {width:innerWidth,title:document.title,overflow:document.documentElement.scrollWidth>innerWidth+1,
  mathCount:document.querySelectorAll('.katex').length,
  mathErrors:[...document.querySelectorAll('.katex-error')].map(e=>e.textContent),
  rawDollars:(main.innerText.match(/\$/g)||[]).length,
  figureCount:figures.length,imageCount:images.length,detailCount:details.length,
  plotHeading:name==='index'?document.getElementById('section-6')?.textContent:document.getElementById('euler-errors')?.textContent,
  scopedText:text,scopeHasRK4:/RK4/.test(text),scopeHasWaveform:/波形|剖面|Waveform|profiles/i.test(text),
  images:images.map(e=>({alt:e.alt,width:e.naturalWidth,height:e.naturalHeight,embedded:e.src.startsWith('data:image/png;'),decoded:e.complete&&e.naturalWidth>0})),
  captions:figures.map(e=>e.querySelector('figcaption')?.innerText||''),
  links:[...document.querySelectorAll('a[href]')].map(e=>e.getAttribute('href')),
  badAnchors:[...document.querySelectorAll('a[href^="#"]')].map(e=>e.getAttribute('href'))
   .filter(h=>h.length>1&&!document.getElementById(decodeURIComponent(h.slice(1)))),
  duplicateIds:[...new Set(ids)].filter(id=>ids.filter(x=>x===id).length>1)
 };
},name);}

(async()=>{
 const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
 const pages=[];
 try{
  for(const target of targets){
   const page=await browser.newPage(),errors=[],requests=[],decodeErrors=[];
   page.on('pageerror',e=>errors.push(String(e)));
   page.on('request',r=>{if(/^https?:/.test(r.url()))requests.push(r.url());});
   const views=[];
   for(const width of [1440,390]){
    await page.setViewportSize({width,height:width===390?844:1080});
    await page.goto(pathToFileURL(target.file).href,{waitUntil:'load'});
    await page.evaluate(()=>document.fonts.ready);
    decodeErrors.push(...await page.evaluate(async()=>{
     const failures=[];await Promise.all([...document.images].map(async i=>{i.loading='eager';try{await i.decode();}catch(e){failures.push({alt:i.alt,error:String(e)});}}));return failures;
    }));
    const view=await inspect(page,target.name);views.push(view);
    await page.screenshot({path:path.join(output,`${target.name}_${width}_top.png`)});
    await page.locator(target.name==='index'?'#section-6':'#euler-errors').scrollIntoViewIfNeeded();
    await page.screenshot({path:path.join(output,`${target.name}_${width}_errors.png`)});
   }
   const actualHashes=await page.evaluate(async()=>{
    return (await Promise.all([...document.images].map(async i=>{
     const raw=atob(i.src.split(',')[1]),bytes=Uint8Array.from(raw,c=>c.charCodeAt(0));
     const buffer=await crypto.subtle.digest('SHA-256',bytes);
     return [...new Uint8Array(buffer)].map(n=>n.toString(16).padStart(2,'0')).join('');
    }))).sort();
   });
   const embeddedImagesMatch=JSON.stringify(actualHashes)===JSON.stringify(expectedHashes);
   const first=page.locator('details').first();const before=await first.evaluate(e=>e.open);
   await first.locator('summary').click();const detailsOperable=await first.evaluate(e=>e.open)!==before;
   await page.evaluate(()=>document.querySelectorAll('details').forEach(e=>{e.open=true;}));
   views.push({...await inspect(page,target.name),expanded:true});
   await page.screenshot({path:path.join(output,`${target.name}_390_expanded.png`)});
   await page.setViewportSize({width:1440,height:1080});
   if(target.name==='atlas')for(const index of [0,13,26]){
    await page.locator('figure').nth(index).screenshot({path:path.join(output,`euler_figure_${index+1}.png`)});
   }
   const missingFiles=views[0].links.filter(h=>!h.startsWith('#')&&!/^[\w+-]+:/.test(h))
    .map(h=>({href:h,file:fileURLToPath(new URL(h.split('#')[0],pathToFileURL(target.file)))}))
    .filter(i=>!fs.existsSync(i.file));
   const issues=[];
   if(!embeddedImagesMatch)issues.push('嵌入图片与新生成的36张PNG不一致');
   if(!detailsOperable)issues.push('折叠控制失效');
   if(errors.length||requests.length||decodeErrors.length||missingFiles.length)issues.push('脚本、网络、图片或本地链接错误');
   for(const view of views){
    if(view.overflow)issues.push(`${view.width}px横向溢出`);
    if(view.mathErrors.length||!view.mathCount||view.rawDollars)issues.push(`${view.width}px数学异常`);
    if(view.badAnchors.length||view.duplicateIds.length)issues.push(`${view.width}px锚点异常`);
    if(view.figureCount!==36||view.imageCount!==36)issues.push(`${view.width}px未显示36张独立图`);
    if(!view.plotHeading?.includes('Euler'))issues.push(`${view.width}px图节未限定Euler`);
    if(view.scopeHasRK4||view.scopeHasWaveform)issues.push(`${view.width}px图节残留RK4/波形/剖面文字`);
    if(view.images.some(i=>!i.decoded||!i.embedded||!i.alt.includes('Euler')||!i.alt.includes('单张绝对误差')))issues.push(`${view.width}px图片内容或标签异常`);
    if(!view.scopedText.includes('平方根映射')||!view.scopedText.includes('窗口')||!view.scopedText.includes('window max'))issues.push(`${view.width}px误差尺度或窗口说明缺失`);
   }
   pages.push({name:target.name,file:target.file,status:issues.length?'failed':'passed',issues,errors,requests,decodeErrors,missingFiles,embeddedImagesMatch,detailsOperable,views});
   await page.close();
  }
 }finally{await browser.close();}
 const result={status:metadataValid&&pages.every(p=>p.status==='passed')?'passed':'failed',metadataValid,
  plotMetadata:{method:manifest.method,xInterval:manifest.x_interval,errorFields:manifest.error_fields,distributionAxes:1,colorbarAxes:1},pages};
 fs.writeFileSync(path.join(__dirname,'euler_html_validation.json'),JSON.stringify(result,null,2));
 console.log(JSON.stringify({status:result.status,metadataValid,pages:pages.map(p=>({name:p.name,status:p.status,issues:p.issues,embeddedImagesMatch:p.embeddedImagesMatch,detailsOperable:p.detailsOperable,
  views:p.views.map(v=>({width:v.width,expanded:!!v.expanded,overflow:v.overflow,figures:v.figureCount,math:v.mathCount,scopeHasRK4:v.scopeHasRK4,scopeHasWaveform:v.scopeHasWaveform})),errors:p.errors,missingFiles:p.missingFiles}))},null,2));
 if(result.status!=='passed')process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1;});
