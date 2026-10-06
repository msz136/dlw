const fs=require('fs'),path=require('path'),crypto=require('crypto');
const root=path.resolve(__dirname,'../..');
const katex=require(path.join(root,'Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.js'));
let count=0;
const source=fs.readFileSync(path.join(__dirname,'report.src.html'),'utf8');
const body=source.replace(/@@M ([\s\S]*?) @@/g,(_,tex)=>{
 count++;return '<div class="equation">'+katex.renderToString(tex,{output:'mathml',displayMode:true,throwOnError:true})+'</div>';
});
if(body.includes('@@'))throw Error('Unrendered math marker');
const style=`body{margin:0;background:#faf9f6;color:#242424;font-family:Georgia,"Noto Serif SC","Microsoft YaHei",serif;line-height:1.9}main{max-width:960px;margin:auto;padding:48px 28px 80px}h1{font-size:34px;line-height:1.4;font-weight:600}h2{font-size:23px;margin-top:38px;font-weight:600}.meta,.note{color:#666;font-size:14px}.abstract{padding:17px 20px;background:#efeee9;font-size:16px}p{margin:15px 0}table{border-collapse:collapse;width:100%;font-size:14px}td,th{padding:10px;text-align:left;border-bottom:1px solid #d8d5cf;vertical-align:top}th{background:#efede7}.equation{overflow-x:auto;padding:13px 0;margin:4px 0}a{color:#365b73;text-underline-offset:3px}math{font-size:1.06em}@media(max-width:600px){main{padding:24px 16px 48px}h1{font-size:28px}h2{font-size:21px}.abstract{padding:14px}td,th{padding:8px 5px;font-size:12px}}@media print{body{background:white}main{padding:0;max-width:none}.equation{overflow:visible}h2{break-after:avoid}table,p{break-inside:avoid}a{color:inherit}}`;
const html='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>半离散 DLW 的守恒生成式与对易量</title><style>'+style+'</style></head><body><main>'+body+'</main></body></html>';
const out=path.join(root,'report/dlw_conservation_hierarchy.html');
fs.writeFileSync(out,html,'utf8');
const manifest={math_blocks:count,output:'report/dlw_conservation_hierarchy.html',sha256:crypto.createHash('sha256').update(html).digest('hex')};
fs.writeFileSync(path.join(__dirname,'build_manifest.json'),JSON.stringify(manifest,null,2));
console.log(JSON.stringify(manifest));
