const fs=require('fs'),path=require('path');
const katex=require(path.resolve(__dirname,'../gsg_project/dlw_report/_assets/package/dist/katex.js'));
const formulas=JSON.parse(fs.readFileSync(path.join(__dirname,'formulas.json'),'utf8'));
const rendered=formulas.map(({tex,display})=>(display?'<div class="eq">':'')+katex.renderToString(tex,{displayMode:display,throwOnError:true,strict:'error',output:'htmlAndMathml'})+(display?'</div>':''));
fs.writeFileSync(path.join(__dirname,'rendered.json'),JSON.stringify(rendered));
