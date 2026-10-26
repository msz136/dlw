const fs=require('fs');
const k=require('C:/Users/msz/aca/Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.js');
const f=JSON.parse(fs.readFileSync('review/formulas.json','utf8'));
const rendered=f.map(({tex,display},i)=>{try{return (display?'<div class="eq">':'')+k.renderToString(tex,{displayMode:display,throwOnError:true,strict:'error',output:'htmlAndMathml'})+(display?'</div>':'')}catch(e){throw Error('formula '+i+' '+tex+' '+e.message)}});
fs.writeFileSync('review/rendered.json',JSON.stringify(rendered));
