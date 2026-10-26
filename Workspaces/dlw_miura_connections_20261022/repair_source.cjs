const fs=require('fs'),path=require('path');
const file=path.join(__dirname,'report.source.html');
let s=fs.readFileSync(file,'utf8');
s=s.split('$\\eta_y').join('');
s=s.replace('$eta_y=H$','$\\eta_y=H$');
fs.writeFileSync(file,s);
