const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'../..');
const katex=require(path.join(root,'Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.js'));
let count=0;
const source=fs.readFileSync(path.join(__dirname,'report.src.html'),'utf8');
const body=source.replace(/@@M ([\s\S]*?) @@/g,(_,tex)=>{
  count++;
  return '<div class="equation">'+katex.renderToString(tex,{output:'mathml',displayMode:true,throwOnError:true})+'</div>';
});
if(body.includes('@@'))throw Error('Unrendered math marker');
const style=`body{margin:0;background:#faf9f6;color:#242424;font-family:Georgia,"Noto Serif SC","Microsoft YaHei",serif;line-height:1.9}main{max-width:940px;margin:auto;padding:48px 28px 80px}h1{font-size:34px;line-height:1.4;font-weight:600}h2{font-size:23px;margin-top:38px;font-weight:600}.meta{color:#777;font-size:14px}.abstract{padding:17px 20px;background:#efeee9;font-size:16px}p{margin:15px 0}table{border-collapse:collapse;width:100%;font-size:14px}td,th{padding:10px 12px;text-align:left;border-bottom:1px solid #d8d5cf;vertical-align:top}th{background:#efede7}.equation{overflow-x:auto;padding:13px 0;margin:4px 0}a{color:#365b73;text-underline-offset:3px}math{font-size:1.06em}em{font-style:normal;color:#444}@media(max-width:600px){main{padding:24px 16px 48px}h1{font-size:28px}h2{font-size:21px}.abstract{padding:14px}td,th{padding:8px 6px;font-size:12px}}@media print{body{background:white}main{padding:0;max-width:none}.equation{overflow:visible}h2{break-after:avoid}table,p,.equation{break-inside:avoid}a{color:inherit}}`;
const html='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>半离散 DLW 的 Hamilton 表示</title><style>'+style+'</style></head><body><main>'+body+'</main></body></html>';
fs.writeFileSync(path.join(root,'dlw_hamilton.html'),html,'utf8');
fs.writeFileSync(path.join(__dirname,'build_manifest.json'),JSON.stringify({math_blocks:count,output:'dlw_hamilton.html'},null,2));
console.log(JSON.stringify({math_blocks:count,output:'dlw_hamilton.html'}));
