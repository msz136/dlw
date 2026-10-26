const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'../..');
const katex=require(path.join(root,'Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.js'));
let source=fs.readFileSync(path.join(__dirname,'report.source.html'),'utf8');
let count=0;
source=source.replace(/\$\$([\s\S]*?)\$\$|\$([^\n$]+)\$/g,(_,display,inline)=>{
 count++;
 let out=katex.renderToString(display??inline,{displayMode:display!==undefined,throwOnError:true,strict:'error',output:'htmlAndMathml'});
 return display!==undefined?'<div class="eq">'+out+'</div>':out;
});
fs.writeFileSync(path.join(root,'report/dlw_miura_connections_20261022.html'),source);
console.log(`Rendered ${count} formulas with strict KaTeX validation.`);
