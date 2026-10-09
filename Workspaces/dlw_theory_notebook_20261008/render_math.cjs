const fs=require('fs'),path=require('path');
const katex=require(process.env.DLW_KATEX_PATH || path.resolve(__dirname,'../gsg_project/dlw_report/_assets/package/dist/katex.js'));
const formulas=JSON.parse(fs.readFileSync(path.join(__dirname,'formulas.json'),'utf8'));
const result=formulas.map(({tex,display},i)=>{
try{return (display?'<span class="eq">':'')+katex.renderToString(tex,{output:'htmlAndMathml',displayMode:display,throwOnError:true})+(display?'</span>':'');}
catch(e){throw Error('Formula '+i+': '+tex+'\n'+e.message);}
});
fs.writeFileSync(path.join(__dirname,'rendered_math.json'),JSON.stringify(result));
