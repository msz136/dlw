// Static artifact validation; no browser automation or network access.
const fs=require('node:fs'),path=require('node:path');
const katex=require('../gsg_project/dlw_report/_assets/package/dist/katex.js');
const src=fs.readFileSync(path.join(__dirname,'_src/index.src.html'),'utf8');
const built=fs.readFileSync(path.join(__dirname,'index.html'),'utf8');
const body=src.split('<main')[1].split('</main>')[0];
const formulas=[...body.matchAll(/\$\$([\s\S]*?)\$\$|\$([^$]*?)\$/g)];
const errors=[];
for(const [i,m] of formulas.entries()){
 try{katex.renderToString((m[1]??m[2]).replaceAll('&lt;','<').replaceAll('&gt;','>').replaceAll('&amp;','&'),{throwOnError:true,displayMode:m[1]!==undefined,strict:'error'});}
 catch(e){errors.push({i,formula:m[0],error:e.message});}
}
const links=[...built.matchAll(/href="([^"]+)"/g)].map(m=>m[1]);
const ids=new Set([...built.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]));
const missingFiles=links.filter(h=>!h.startsWith('#')&&!h.includes('://')&&!fs.existsSync(path.resolve(__dirname,decodeURI(h.split('#')[0]))));
const missingAnchors=links.filter(h=>h.startsWith('#')&&!ids.has(h.slice(1)));
const images=[...built.matchAll(/<img [^>]*src="data:image\/png;base64,([^"]+)"[^>]*>/g)];
const invalidImages=images.map((m,i)=>({i,bytes:Buffer.from(m[1],'base64')})).filter(v=>v.bytes.subarray(0,8).toString('hex')!=='89504e470d0a1a0a').map(v=>v.i);
const result={type:'static_validation',formulaCount:formulas.length,errors,missingFiles,missingAnchors,embeddedFigures:images.length,invalidImages,
 remainingPlaceholders:(built.match(/@@\w+@@/g)||[]),browserRenderStatus:'not_verified: in-app Browser security policy rejects file://; no workaround attempted'};
fs.writeFileSync(path.join(__dirname,'out/static_validation.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result,null,2));
if(errors.length||missingFiles.length||missingAnchors.length||invalidImages.length||images.length!==12||result.remainingPlaceholders.length)process.exitCode=1;
