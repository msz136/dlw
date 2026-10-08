const fs=require('fs'),path=require('path');
const k=require(path.resolve(__dirname,'../gsg_project/dlw_report/_assets/package/dist/katex.js'));
const m=JSON.parse(fs.readFileSync(path.join(__dirname,'notebook_math.json'),'utf8'));
fs.writeFileSync(path.join(__dirname,'notebook_math_rendered.json'),JSON.stringify(m.map(({tex,display})=>(display?'<div class="eq">':'')+k.renderToString(tex,{displayMode:display,throwOnError:true})+(display?'</div>':''))));
