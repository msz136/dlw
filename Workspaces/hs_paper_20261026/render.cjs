const fs=require('fs');const path=require('path');
const root=__dirname;const ws=path.resolve(root,'../..');
const katex=require(path.join(ws,'Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.js'));
let s=fs.readFileSync(path.join(root,'unrendered.html'),'utf8');let count=0;
s=s.replace(/\\\[([\s\S]*?)\\\]|\\\(([\s\S]*?)\\\)/g,(_,display,inline)=>{count++;const tex=(display??inline).replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&amp;/g,'&');return katex.renderToString(tex,{displayMode:display!==undefined,throwOnError:true});});
const out=path.join(ws,'2HS paper.html');if(fs.existsSync(out)){fs.copyFileSync(out,path.join(root,'before_'+Date.now()+'.html'));}
fs.writeFileSync(out,s);console.log(JSON.stringify({formulas:count,output:out}));
